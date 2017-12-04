#!/usr/bin/env python

from flask import Flask, render_template, request
from wtforms import Form
from Analyzer import *
from os import listdir
import datetime

app = Flask(__name__, template_folder="../templates", static_folder="../css")
#app = Flask(__name__, static_folder="css")

# The main view of CryptoGuru Invemestment Analyzer
@app.route('/', methods = ['GET', 'POST'])
def landing():
  return render_template('landing.html')


# The main view of CryptoGuru Invemestment Analyzer
@app.route('/investment', methods = ['GET', 'POST'])
def investment():
  cca = Crypto_Currency_Analyzer()

  ################################################################
  # Feed today's date into HTML as max year/month for date sliders
  ################################################################
  # Get current date
  date = datetime.datetime.now()
  cur_date = '%04d-%02d-%02d' % (date.year, date.month, date.day)


  # Get currencies
  select = request.form.getlist('currency')

  # Normalize checkbox
  norm = request.form.get('normalize')

  # Normalize checkbox
  rolling_mean = request.form.get('rollingMean')

  # If user has pushed "Graph"
  if request.method == 'POST' and select:

    # Get start year/month from sliders
    start_date = request.form.get('startDate')

    # Generate results
    cca.data_frame(currencies=select, start_date=start_date)
    if norm:
      cca.normalize()

    if rolling_mean:
      result = cca.plot_rolling_mean(currency='Bitcoin')
    else:
      result = cca.plot_data_frame()
  else:
    result = None

  return render_template('investment.html', result=result, currencies=cca.available_currencies, cur_date=cur_date)


if __name__=='__main__':
  app.run()
