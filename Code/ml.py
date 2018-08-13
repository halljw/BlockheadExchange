#!/usr/bin/env python

import pandas as pd
import math
import datetime
import numpy as np
from sklearn import preprocessing, cross_validation
from sklearn.linear_model import LinearRegression, Lars, BayesianRidge
import matplotlib.pyplot as plt2
from matplotlib import style
import pickle
import boto3
from io import BytesIO
import os
import base64
import time


class ML:
    def __init__(self, forecast_out=30, currency='Bitcoin', algorithm=LinearRegression):
        client = boto3.client('s3',
                              aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        if algorithm == LinearRegression:
            self.alg_name = "LinReg"
        elif algorithm == Lars:
            self.alg_name = "Lars"
        elif algorithm == BayesianRidge:
            self.alg_name = "BayesRidge"
        obj = client.get_object(Bucket="blockhead-ex-02", Key='{}.txt'.format(currency))
        df = pd.read_csv(BytesIO(obj['Body'].read()))
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)
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
        self.forecasted_dates = forecast_out

        X = np.array(df.drop(['label'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]

        df.dropna(inplace=True)

        y = np.array(df['label'])

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.2)

        clf = algorithm()
        clf.fit(X_train, y_train)

        self.accuracy = clf.score(X_test, y_test)

        forecast_set = clf.predict(X_lately)
        print(forecast_set, forecast_out)

        df['Forecast'] = np.nan
        last_date = df.iloc[-1].name
        last_unix = time.mktime(last_date.timetuple())
        one_day = 86400
        next_unix = last_unix + one_day

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            next_unix += one_day
            df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]


        style.use('ggplot')
        self.df=df

    def draw(self):
        df = self.df

        chart = df[['CLOSE', 'Forecast']].plot()
        chart.legend(loc=4)
        chart.grid(axis='y', color="black")
        chart.set_xlabel('Date', fontname='Trebuchet MS', fontsize=20, color="black")
        chart.tick_params(axis='x', colors='black')
        chart.set_ylabel('Price', fontname='Trebuchet MS', fontsize=20, color="black")
        chart.tick_params(axis='y', colors='black')
        chart.legend(fancybox=True)
        chart.set_facecolor('#40f123')

        chart.set_title("{}, Projecting {} Days".format(self.alg_name, self.forecasted_dates), fontname='Trebuchet MS', fontsize=22, color="black")

        fig = BytesIO()
        plt2.tight_layout()
        plt2.savefig(fig, format='png', transparent=True)
        fig.seek(0)
        fig_png = base64.b64encode(fig.getvalue())

        return (fig_png, self.accuracy)

if __name__=='__main__':
    ml = ML(algorithm=BayesianRidge)