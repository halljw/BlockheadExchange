#!/usr/bin/env python

from flask import Flask, render_template, request

from Code.Analyzer import *
from os import listdir
import datetime

app = Flask(__name__)

#  The main view of CryptoGuru Invemestment Analyzer
@app.route('/', methods = ['GET', 'POST'])
def landing():
  return render_template('landing.html')

# The main view of CryptoGuru Invemestment Analyzer
@app.route('/investment', methods = ['GET', 'POST'])
def investment():
  cca = Crypto_Currency_Analyzer()

  # Get start/end dates
  #  - default, previous 3 months
  start_date = request.form.get('startDate')
  end_date = request.form.get('endDate')
  if not start_date:
    date = datetime.datetime.now()
    end_date = '%04d-%02d-%02d' % (date.year, date.month, date.day)
    start_date = '%04d-%02d-%02d' % (date.year, date.month - 3, date.day)

  # Get currencies
  select = request.form.getlist('currency')

  # Normalize checkbox
  norm = request.form.get('normalize')

  # Rolling mean checkbox
  rolling_mean = request.form.get('rollingMean')
  rm_window = request.form.get('rm_window')
  if not rm_window:
    rm_window = 20

  # If user has pushed "Graph"
  if request.method == 'POST' and select:

    # Get start year/month from sliders
    start_date = request.form.get('startDate')

    # Generate results
    cca.data_frame(currencies=select, start_date=start_date)
    if norm:
      cca.normalize()

    if rolling_mean:
      result = cca.plot_rolling_mean(currency=select[0], window=int(rm_window))
    else:
      result = cca.plot_data_frame()
  else:
    cca.data_frame(currencies=['Bitcoin'], start_date=start_date)
    result = cca.plot_data_frame()

  return render_template('investment.html',
			result=result, 
			currencies=cca.available_currencies, 
			start_date=start_date, 
			end_date=end_date, 
			select=select, 
			norm=norm, 
			rolling_mean=rolling_mean, 
			rm_window=rm_window)

if __name__=='__main__':
  app.run(debug=True)
