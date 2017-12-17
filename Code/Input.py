#!/usr/bin/env python

# Checks allowable inputs for Analyzer.py
"""
"""

from Analyzer import *
import datetime


def date(year_offset=0):
  """
  Return formatted string containing today's date
  """
  date = datetime.datetime.now()
  date_str = '%04d-%02d-%02d' % (date.year - year_offset, date.month, date.day)
  return date_str

def check_date_format(date):
  """
  Ensures that a string containing a date is formatted as yyyy-mm-dd

  >>> check_date_format("2015-11-10")
  True
  >>> check_date_format("11-10-2015")
  False
  >>> check_date_format("2015-11-1")
  False
  >>> check_date_format("2015/11/10")
  False
  """

  import re
  date_reg = re.compile('([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])')
  if date_reg.search(date):
    return True
  else:
    return False


def allowable_inputs(cca, feature, currencies, start_date, end_date):
  """
  Checks that a set of inputs is viable for the Cryto_Currency_Analyzer class
   - 'feature' must be contained in cca's list of features
   - 'currencies' must be type [list] and contained cca's list of available data
   -  dates must be correctly formatted strings of form yyyy-mm-dd

  >>> cca = Crypto_Currency_Analyzer()
  >>> allowable_inputs(cca, "OPEN", ["Bitcoin"], "2017-11-20", "2017-11-20")
  >>> allowable_inputs(cca, "open", ["Bitcoin"], "2017-11-20", "2017-11-20")
  Traceback (most recent call last):
    ...
  ValueError: Feature 'open' is not a recorded feature in the data.
  >>> allowable_inputs(cca, "OPEN", "Bitcoin", "2017-11-20", "2017-11-20")
  Traceback (most recent call last):
    ...
  ValueError: Currencies 'Bitcoin' should be entered as type [list].
  >>> allowable_inputs(cca, "OPEN", ["Bitcoin"], "2017/11/20", "2017-11-20")
  Traceback (most recent call last):
    ...
  ValueError: start_date '2017/11/20' poorly formated. Use date format 'yyyy-mm-dd'
  >>> allowable_inputs(cca, "OPEN", ["Bitcoin"], "2017-11-20", "2017/11/20")
  Traceback (most recent call last):
    ...
  ValueError: end_date '2017/11/20' poorly formated. Use date format 'yyyy-mm-dd'
  """

  if feature not in cca.features:
    raise ValueError("Feature '%s' is not a recorded feature in the data." % feature)
  if type(currencies) is not list:
    raise ValueError("Currencies '%s' should be entered as type [list]." % currencies)
  for currency in currencies:
    if currency not in cca.available_currencies:
      raise ValueError("Currency '%s' is not available." % currency)
  if not check_date_format(start_date):
    raise ValueError("start_date '%s' poorly formated. Use date format 'yyyy-mm-dd'" % start_date)
  if not check_date_format(end_date):
    raise ValueError("end_date '%s' poorly formated. Use date format 'yyyy-mm-dd'" % end_date)

if __name__=='__main__':
  import doctest
  doctest.testmod()
