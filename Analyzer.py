#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime, re, os

class Crypto_Currency_Analyzer:

  def __init__(self):
    self.features = ["Open", "High", "Low", "Close", "Volume", "Market_Cap"]
    self.available_currencies = [c[:-4] for c in os.listdir('Data/Crypto_Currencies')]
    self.df = self.data_frame()

  def data_frame(self, feature=None, currencies=None, start_date=None, end_date=None):
    """
    Returns and sets a dataframe for the selected feature and currencies.
      Features:
        - Open (default)
        - High
        - Low
        - Close
        - Volume
        - Market_cap
      Shows data for previous year as default.
    """
    # Desired features; if non listed, opening price as default
    if not feature:
      feature = "Open"

    # Desired currencies; if none listed, top three as default
    if not currencies:
      currencies = ["Bitcoin", "Ethereum", "Ripple"]

    # Desired dates; if none listed, past year as default
    if not start_date:
      start_date = self.date(1)
    if not end_date:
      end_date = self.date()

    if not self.allowable_inputs(feature, currencies, start_date, end_date):
      return

    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index = dates)

    # Join using date as index
    # Rename feature to currency name
    for c in currencies:
      df = df.join(pd.read_csv("Data/Crypto_Currencies/"+c+".csv", index_col="Date",
                               parse_dates=True, usecols=["Date", feature],
                               na_values=["nan"]))
      df = df.rename(columns={feature: c})

    self.df = df
    return df.dropna()

  def allowable_inputs(self, feature, currencies, start_date, end_date):
    if feature not in self.features:
      print("Feature '%s' is not a recorded feature in the data." % feature)
      return False
    if type(currencies) is not list:
      print("Currencies '%s' should be entered as type [list]." % currencies)
      return False
    for currency in currencies:
      if currency not in self.available_currencies:
        print("Currency '%s' is not available." % currency)
        return False
    if not self.check_date_format(start_date):
      print("Please use date format 'yyyy-mm-dd'")
      return False
    if not self.check_date_format(end_date):
      print("Please use date format 'yyyy-mm-dd'")
      return False
    return True

  def date(self, year_offset=0):
    """
    Return formatted string containing today's date
    """
    date = datetime.datetime.now()
    return str(date.year - year_offset) + "-" + str(date.month) + "-" + str(date.day)

  def check_date_format(self, date):
    date_reg = re.compile('([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])')
    if date_reg.search(date):
      return True
    else:
      return False

  def fill_incomplete(self, df):
    """
    """
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)
    return df

  def normalize(self, df):
    """
    Normalize stock prices using first row of dataframe.
    """
    return df / df.ix[0,:]

  def daily_returns(self, df=pd.DataFrame()):
    if df.empty:
      df = self.df
    return (df / df.shift(1)) - 1

  def plot_rolling_mean(self, df=pd.DataFrame(), currency=None, window=20, bollinger_bands=True):
    if df.empty:
      df = self.df
    if not currency:
      print("Select currency to plot")
      return
    if not currency in df:
      print("Currency %s not in data frame." % currency)
      return
    rm = pd.DataFrame(pd.rolling_mean(df[currency], window=window))

    if bollinger_bands:
      std = pd.DataFrame(pd.rolling_std(df[currency], window=window))
      upper_band = pd.DataFrame(rm + std * 2)
      lower_band = pd.DataFrame(rm - std * 2)

      rm = rm.rename(columns={currency: 'Rolling mean'})
      upper_band = upper_band.rename(columns={currency: 'Upper band'})
      lower_band = lower_band.rename(columns={currency: 'Lower band'})
      rm = rm.join(upper_band).join(lower_band)

    title = currency + " rolling mean"
    self.plot_data_frame(df=rm, title=title)
    

  def plot_data_frame(self, df=pd.DataFrame(), title="Cryptocurrency values"):
    """
    Plot the given data frame.
    """
    if df.empty:
      df = self.df
    p = df.plot(title=title, fontsize=12)
    p.set_xlabel("Date")
    p.set_ylabel("Value")
    p.legend(loc='upper left')
    plt.show()


  def daily_returns_histogram(self, df=pd.DataFrame(), currency=None):
    """
    """
    if df.empty:
      df = self.df
    if not currency:
      print("Select currency to display")
      return
    if not currency in df:
      print("Currency %s not in data frame." % currency)
      return
    dr = self.daily_returns(df[currency])
    mean = dr.mean()
    std = dr.std()
    hist = dr.hist(bins = 20)
    plt.axvline(mean, color='w', linestyle='dashed', linewidth=2)
    plt.axvline(std, color='r', linestyle='dashed', linewidth=2)
    plt.axvline(-std, color='r', linestyle='dashed', linewidth=2)
    plt.title(currency + " daily returns")
    hist.set_xlabel('Returns')
    hist.set_ylabel('Frequency')
    plt.show()

  def daily_returns_relation(self, c1=None, c2=None, df=pd.DataFrame()):
    """
    """
    if df.empty:
      df = self.df
    if not c1 or not c2:
      print("Select two currencies to compare")
      return
    for currency in [c1, c2]:
      if not currency in df:
        print("Currency %s not in data frame." % currency)
        return
    dr = self.daily_returns(df).dropna()
    dr.plot(kind='scatter', x=c1, y=c2)
    beta, alpha = np.polyfit(dr[c1], dr[c2], 1)
    print("%s alpha: %f \n%s beta: %f" % (c2, alpha, c2, beta))
    plt.plot(dr[c1], beta*dr[c1] + alpha, '-', color='r')
    plt.title("%s performance with respect to %s" % (c2, c1))
    plt.show()


if __name__=='__main__':
  cca = Crypto_Currency_Analyzer()
  df = cca.data_frame()
  cca.plot_data_frame(df)
  
