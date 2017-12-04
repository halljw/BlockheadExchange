#!/usr/bin/env python

"""
The CryptoGuru Investment Analyzer
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime, re, os

from io import BytesIO
import base64

class Crypto_Currency_Analyzer:

  def __init__(self):
    self.features = ["Open", "High", "Low", "Close", "Volume", "Market_Cap"]
    self.available_currencies = [c[:-4] for c in os.listdir('../Data')]

  def data_frame(self, feature="Open", currencies=None, start_date=None, end_date=None):
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
    if not currencies:
      raise ValueError("[-] Crypto_Currency_Analyzer.data_frame(currencies=[currencies])")

    # Desired dates; if none listed, past year as default
    if not start_date:
      start_date = self.date(1)
    if not end_date:
      end_date = self.date()

    # Check all inputs allowable
    self.allowable_inputs(feature, currencies, start_date, end_date)

    # Construct DataFrame
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index = dates)

    # Join using date as index
    # Rename feature to currency name
    for c in currencies:
      df = df.join(pd.read_csv("../Data/"+c+".txt", index_col="DATE",
                               parse_dates=True, usecols=["DATE", feature],
                               na_values=["nan"]))
      df = df.rename(columns={feature: c})
    self.df = df.dropna()
    return df.dropna()

  def allowable_inputs(self, feature, currencies, start_date, end_date):
    if feature not in self.features:
      raise ValueError("Feature '%s' is not a recorded feature in the data." % feature)
    if type(currencies) is not list:
      raise ValueError("Currencies '%s' should be entered as type [list]." % currencies)
    for currency in currencies:
      if currency not in self.available_currencies:
        raise ValueError("Currency '%s' is not available." % currency)
    if not self.check_date_format(start_date):
      raise ValueError("start_date '%s' poorly formated\nPlease use date format 'yyyy-mm-dd'" % start_date)
    if not self.check_date_format(end_date):
      raise ValueError("end_date '%s' poorly formated\nPlease use date format 'yyyy-mm-dd'" % end_date)

  def date(self, year_offset=0):
    """
    Return formatted string containing today's date
    """
    date = datetime.datetime.now()
    date_str = '%04d-%02d-%02d' % (date.year - year_offset, date.month, date.day)
    return date_str

  def check_date_format(self, date):
    date_reg = re.compile('([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])')
    if date_reg.search(date):
      return True
    else:
      return False

  def fill_incomplete(self, df):
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)
    return df

  def normalize(self):
    """
    Normalize stock prices using first row of dataframe.
    """
    self.df = self.df / self.df.ix[0,:]
    return self.df / self.df.ix[0,:]

  def daily_returns(self, df):
    return (df / df.shift(1)) - 1

  def cumulative_returns(self, df):
    return df / df.ix[0,:] - 1

  def plot_rolling_mean(self, currency=None, window=20, bollinger_bands=True):
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
    p = rm.plot(title=title, fontsize=12)
    p.set_xlabel("Date")
    p.set_ylabel("Value")
    p.legend(loc='upper left')
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png
    

  def plot_data_frame(self, title="Cryptocurrency values", show=False):
    """
    Plot the given data frame.
    """
    p = self.df.plot(title=title, fontsize=12)
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
  cca.data_frame(currencies=["Bitcoin"])
  cca.plot_data_frame(show=True)
  cca.normalize()
  #cca.plot_rolling_mean(currency="Bitcoin")
  #cca.plot_rolling_mean(currency="Ethereum")
  #cca.daily_returns_histogram(currency="Bitcoin")

  #cca.daily_returns_relation(c1="Bitcoin", c2="Ethereum")

  #df = cca.sharpe_ratio()
  #cca.plot_data_frame(df)
 


"""
Next task, optimize a portfolio for a year of data,
optimize based on sharpe ratio month by month

provide a function to minimize
provide an initial guess for x
call the optimizer

And fix the crawler

""" 
