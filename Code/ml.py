#!/usr/bin/env python

import pandas as pd
import math
import datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
# from matplotlib import style./
import pickle
import boto3
from io import BytesIO
import os


class ML:
    def __init__(self, currency='Bitcoin', algorithm=LinearRegression):
        client = boto3.client('s3',
                              aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        client.get_object(Bucket=os.environ['S3_BUCKET_NAME'], Key='{}.txt'.format(currency))
        df = pd.read_csv(BytesIO(obj['Body'].read()))
        df['HL_PCT'] = (df['HIGH'] - df['LOW']) / df['LOW']
        df['PCT_CHANGE'] = (df['CLOSE'] - df['OPEN']) / df['OPEN']
        df = df[['CLOSE', 'HL_PCT', 'PCT_CHANGE', 'VOL']]
        forecast_col = 'CLOSE'
        df.fillna(-99999, inplace=True)

        forecast_out = int(math.ceil(0.01 * len(df)))
        df['label'] = df[forecast_col].shift(-forecast_out)

        X = np.array(df.drop(['label'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]

        df.dropna(inplace=True)

        y = np.array(df['label'])

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.2)

        clf = algorithm()
        clf.fit(X_train, y_train)

        # with open('linearregression.pickle', 'wb') as f:
        #     pickle.dump(clf, f)
        #
        # pickle_in = open('linearregression.pickle', 'rb')
        # clf = pickle.load(pickle_in)

        accuracy = clf.score(X_test, y_test)

        forecast_set = clf.predict(X_lately)
        print(forecast_set, accuracy, forecast_out)

        df['Forecast'] = np.nan

        last_date = df.iloc[-1].name
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + one_day

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            next_unix += one_day
            df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]

#
# class Draw:
#     style.use('ggplot')
#     df['Adj. Close'].ppylot()
#     df['Forecast'].plot()
#     plt.legend(loc=4)
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#     plt.show()

if __name__=='__main__':
    ml = ML()