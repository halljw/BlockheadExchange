#!/usr/bin/env python

from flask import Flask, render_template, request

from Code.Analyzer import *
from Twitter.twitter_searcher import *
from Code.landing_chart import *
from os import listdir
import datetime
import urllib

app = Flask(__name__)

#  The main view of CryptoGuru Invemestment Analyzer
@app.route('/', methods = ['GET', 'POST'])
def landing():
    ts = Twitter_Searcher()
    tweet_id, twitter_user = ts.get_tweet()
    href_output = "https://twitter.com/" + str(twitter_user) + "/status/" + str(tweet_id);

    cc = ChartCreator()
    currency_file = cc.find_largest_swing()
    currency = cc.file_to_name(currency_file)
    chart_left = cc.create_chart_ma(currency_file, currency, 'Data/Bitcoin.txt')
    chart_right = cc.create_chart_pv(currency_file, currency, 'Data/Bitcoin.txt')

    return render_template('landing.html',
      fig_left = chart_left,
      fig_right = chart_right,
      href_hail_mary = href_output, 
      id_output = tweet_id,
      handle_output = twitter_user)



# The main view of CryptoGuru Invemestment Analyzer
@app.route('/investment', methods = ['GET', 'POST'])
def investment():
  cca = Crypto_Currency_Analyzer()

  ###############################
  # Get start/end dates
  #  - default, previous 3 months
  ###############################
  start_date = request.form.get('startDate')
  end_date = request.form.get('endDate')
  if not start_date:
    end_date = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(days=90)
    end_date = '%04d-%02d-%02d' % (end_date.year, end_date.month, end_date.day)
    start_date = '%04d-%02d-%02d' % (start_date.year, start_date.month, start_date.day)

  ###############################
  # Get currencies
  ###############################
  select = request.form.getlist('currency')
  if not select:
    select = ['Bitcoin']
  select = [str(s) for s in select]

  ###############################
  # Get feature
  ###############################
  feature = request.form.get('features')
  if not feature:
    feature = "OPEN"
  feature = str(feature)

  ###############################
  # Normalize checkbox
  ###############################
  norm = request.form.get('normalize')

  ###############################
  # Rolling mean checkbox/slider
  ###############################
  rolling_mean = request.form.get('rollingMean')
  rm_window = request.form.get('rm_window')
  if not rm_window:
    rm_window = 20
  else:
    rm_window = int(rm_window)

  ###############################
  # Generate graph results
  # Default graph:
  # - Bitcoin
  # - Open
  # - Previous 3 months
  ###############################
  cca.data_frame(currencies=select, feature=feature, start_date=start_date)
  if norm:
    cca.normalize()
  if rolling_mean:
    result = cca.plot_rolling_mean(currency=select[0], window=rm_window)
  else:
    result = cca.plot_data_frame()
 
  return render_template('investment.html',
			result=result, 
			currencies=cca.available_currencies, 
			feature=feature,
			start_date=start_date, 
			end_date=end_date, 
			select=select, 
			norm=norm, 
			rolling_mean=rolling_mean, 
			rm_window=rm_window)

if __name__=='__main__':
  app.run(debug=True)
