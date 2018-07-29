#!/usr/bin/env python

import pandas as pd
import math
import datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression, Lars, BayesianRidge
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import boto3
from io import BytesIO
import os
import base64


class ML:
    def __init__(self, currency='Bitcoin', algorithm=LinearRegression):
        client = boto3.client('s3',
                              aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        obj = client.get_object(Bucket=os.environ['S3_BUCKET_NAME'], Key='{}.txt'.format(currency))
        df = pd.read_csv(BytesIO(obj['Body'].read()))
        df['HL_PCT'] = (df['HIGH'] - df['LOW']) / df['LOW']
        df['PCT_CHANGE'] = (df['CLOSE'] - df['OPEN']) / df['OPEN']
        df = df[['CLOSE', 'HL_PCT', 'PCT_CHANGE', 'VOL']]
        forecast_col = 'CLOSE'
        df.fillna(-99999, inplace=True)
        df = df.replace('-', -99999)

        max_forecast = int(math.ceil(0.1 * len(df)))
        if forecast_out > max_forecast:
            print("Tone it down! We should only extrapolate 10\%!")
            forecast_out = max_forecast
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

        accuracy = clf.score(X_test, y_test)

        forecast_set = clf.predict(X_lately)
        print(forecast_set, accuracy, forecast_out)

        df['Forecast'] = np.nan
        last_date = df.iloc[-1].name
        print (last_date)
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + one_day

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            next_unix += one_day
            df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]


        style.use('ggplot')
        self.draw(df)

    def draw(self, df):
        df['CLOSE'].plot()
        df['Forecast'].plot()
        plt.legend(loc=4)
        plt.xlabel('Date')
        plt.ylabel('Price')

        fig = BytesIO()
        plt.tight_layout()
        plt.savefig('plot.png')
        plt.savefig(fig, format='png')
        fig.seek(0)
        fig_png = base64.b64encode(fig.getvalue())

        return fig

if __name__=='__main__':
    ml = ML(algorithm=BayesianRidge)