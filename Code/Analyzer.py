#!/usr/bin/env python

"""
The CryptoGuru Investment Analyzer
"""

from Input import *
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

from io import BytesIO
import base64
import boto3

class Crypto_Currency_Analyzer:

  def __init__(self):
    self.features = ["OPEN", "HIGH", "LOW", "CLOSE", "VOL"]
    self.available_currencies = [c[:-4] for c in os.listdir('Data')]

  def data_frame(self, feature="OPEN", currencies=None, start_date=None, end_date=None):
    """
    Returns and sets a dataframe for the selected feature and currencies.
      Features:
        - OPEN (default)
        - HIGH
        - LOW
        - CLOSE
        - VOL
      Shows data for previous year as default.
    """
    # Desired dates; if none listed, past year as default
    if not start_date:
      start_date = date(1)
    if not end_date:
      end_date = date()

    # Check all inputs allowable
    allowable_inputs(self, feature, currencies, start_date, end_date)

    # Construct DataFrame
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index = dates)

    # Join columns using 'DATE' as index
    # Rename feature to currency name
    for c in currencies:
      df = df.join(pd.read_csv("Data/"+c+".txt", index_col="DATE",
                               parse_dates=True, usecols=["DATE", feature],
                               na_values=["nan"]))
      df = df.rename(columns={feature: c})
    df = self.fill_incomplete(df)
    self.df = df.dropna()
    return df.dropna()

  def fill_incomplete(self, df):
    """
    Fills empty values in Dataframe df with 'NaN'
    """
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)
    return df

  def normalize(self):
    """
    Normalize stock prices using first row of dataframe.
    """
    self.df = self.df / self.df.ix[0,:]
    return self.df / self.df.ix[0,:]

  def plot_rolling_mean(self, currency=None, window=20, bollinger_bands=True):
    """
    Returns file data of a plot of the rolling mean of the selected currency
    Uses default window size of 20 for calculating mean
    Includes bollinger bands (showing standard deviation of average) by default
      Deactivate bands with bollinger_bands = False
    """
    if not currency:
      print("[-] Select currency to plot")
      return
    if not currency in self.df:
      print("[-] Currency %s not in data frame." % currency)
      return
    rm = pd.DataFrame(pd.rolling_mean(self.df[currency], window=window))

    if bollinger_bands:
      std = pd.DataFrame(pd.rolling_std(self.df[currency], window=window))
      upper_band = pd.DataFrame(rm + std * 2)
      lower_band = pd.DataFrame(rm - std * 2)

      rm = rm.rename(columns={currency: 'Rolling mean'})
      upper_band = upper_band.rename(columns={currency: 'Upper band'})
      lower_band = lower_band.rename(columns={currency: 'Lower band'})
      rm = rm.join(upper_band).join(lower_band)

    title = currency + " rolling mean"
    return self.plot_data_frame(df=rm, title=title)


  def plot_data_frame(self, df="NONE", title="Cryptocurrency values", show=False):
    """
    Generates plot of the given data frame or current df attribute of self.
      - [show] Does not show plot by default. In order to show, show=True
    """
    if type(df)==str:
      df = self.df
    p = df.plot(title=title, fontsize=12)
    p.set_xlabel("Date")
    p.set_ylabel("Value")
    p.legend(loc='upper left')
    if show:
      plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png


if __name__=='__main__':
  cca = Crypto_Currency_Analyzer()
  cca.data_frame(currencies=["Bitcoin"])
  cca.plot_data_frame(show=True)
