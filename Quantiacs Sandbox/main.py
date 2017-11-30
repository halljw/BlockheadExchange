#!/usr/bin/env python

from flask import Flask, render_template, request
from wtforms import Form
from Analyzer import *
from os import listdir

app = Flask(__name__, template_folder=".", static_folder="css")

# The main view of CryptoGuru Analyzer
@app.route('/', methods = ['GET', 'POST'])
def index():
  cca = Crypto_Currency_Analyzer()
  # Available currency data
  available_currencies = [currency[:-4] for currency in listdir('Data')]

  # If user has pushed "Graph"
  if request.method == 'POST':
    select = request.form.getlist('currency')
    cca.data_frame(currencies=select)
    result = cca.plot_data_frame()
  else:
    result = None

  return render_template('index.html', result=result, currencies=available_currencies)


if __name__=='__main__':
  app.run()
