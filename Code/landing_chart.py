#!/usr/bin/env python

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.ticker as ticker
from io import BytesIO
import base64

class ChartCreator(object):
	"""docstring for FileWork"""
	def __init__(self):
		x = 12

	def find_largest_swing(self):
		currency_list = ['Bitcoin', 'Litecoin', 'Monero', 'Bitcoin-Cash', 'Bitcoin-Gold',
		'Cardano', 'Dash', 'EOS', 'Ethereum-Classic', 'Ethereum', 'IOTA', 'NEM', 'NEO',
		'Qtum', 'Ripple', 'Stellar-Lumens']
		currency_dict = {}
		for currency in currency_list:
			currency_file = 'Data/' + currency + '.txt'
			with open(currency_file, 'rb') as coin_file:
				coin_array = np.genfromtxt(coin_file, delimiter=',', dtype=None)
				compare_array_string = coin_array[-7::6]
				compare_array = compare_array_string.astype(np.float)
				vol_diff = (compare_array[0][5] - compare_array[1][5]) / ((compare_array[0][5] + compare_array[1][5]) / 2)
				currency_dict[currency_file]=abs(vol_diff)
		largest_vol_swing = 'Data/Bitcoin.txt'
		for currency in currency_dict:
			if currency_dict[currency] >= currency_dict[largest_vol_swing]:
				largest_vol_swing = currency
		largest_vol_swing_str = largest_vol_swing[8:-4]
		return (largest_vol_swing)
		# self.create_chart(largest_vol_swing, largest_vol_swing_str, '../Data/Bitcoin.txt')

	def file_to_name(self, input_currency):
		output = input_currency[5:-4]
		return output

	def txt_to_csv(self, input_file):
		file = open(input_file, "r")

		String = ""
		for line in file:
		    String += line

		file.close()

		file = open('volume.csv', 'w')
		output_string = String[-8100::]
		file.write(output_string)
		file.close()

	def create_chart_ma(self, input_file, coin_name, btc_file):
		#dataset1 setup
		compare_data = pd.read_csv(input_file)
		btc_data = pd.read_csv(btc_file)
		compare_data.rename(columns={'VOL' : 'VOLUME'}, inplace=True)
		compare_data['15 DAY ROLLING MEAN'] = pd.rolling_mean(compare_data['CLOSE'],15)
		top = compare_data.head(0)
		bottom = compare_data.tail(90)
		recent_quarter = pd.concat([top, bottom])
		recent_quarter['DATE'] = pd.to_datetime(recent_quarter['DATE'], format='%Y%m%d')
		recent_quarter.set_index('DATE', inplace=True)

		#chart1 manipulation
		chart = recent_quarter[['CLOSE', '15 DAY ROLLING MEAN']].plot()
		chart.grid(color='k', axis='y', linestyle='dotted')
		chart.set_xlabel('Date', fontname='Trebuchet MS', fontsize=16)
		chart.set_ylabel('Price', fontname='Trebuchet MS', fontsize=16)
		chart.legend(fancybox=True)
		chart.set_facecolor('#90f1a3')
		chart.set_title("%s 90 Day Price Chart" % coin_name, fontname='Trebuchet MS', fontsize=20)

		fig_left = BytesIO()
		plt.tight_layout()
		plt.savefig('plot.png')
		plt.savefig(fig_left, format='png')
		fig_left.seek(0)
		fig_left_png = base64.b64encode(fig_left.getvalue())

		return (fig_left_png)
		
	def create_chart_pv(self, input_file, coin_name, btc_file):
		compare_data = pd.read_csv(input_file)
		btc_data = pd.read_csv(btc_file)
		compare_data.rename(columns={'VOL' : 'VOLUME'}, inplace=True)
		compare_data['15 DAY ROLLING MEAN'] = pd.rolling_mean(compare_data['CLOSE'],15)
		top = compare_data.head(0)
		bottom = compare_data.tail(90)
		recent_quarter = pd.concat([top, bottom])
		recent_quarter['DATE'] = pd.to_datetime(recent_quarter['DATE'], format='%Y%m%d')
		recent_quarter.set_index('DATE', inplace=True)

		#dataset2 setup
		fig = plt.figure()
		ax1 = plt.subplot2grid((2,1), (0,0))
		ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)
		v_top = compare_data.head(0)
		v_bottom = compare_data.tail(14)
		fourteen = pd.concat([v_top, v_bottom])

		#dataset2a setup
		fourteen_top = fourteen.reset_index()
		fourteen_top = fourteen_top.drop('index', 1)
		fourteen_top['DATE'] = pd.to_datetime(fourteen_top['DATE'], format='%Y%m%d')
		fourteen_top['DATE'] = fourteen_top['DATE'].map(mdates.date2num)

		#chart2a setup
		candlestick_ohlc(ax1, fourteen_top.values, colorup='#53c156', colordown='#ff1717', width=.7)
		ax1.set_title("%s 14 Day Chart" % coin_name, fontname='Trebuchet MS', fontsize=20)
		ax1.set_ylabel('Price', fontname='Trebuchet MS', fontsize=16)

		fourteen_bottom = fourteen
		fourteen_bottom['DATE'] = pd.to_datetime(fourteen_bottom['DATE'], format='%Y%m%d')
		fourteen_bottom['DATE'] = fourteen_bottom['DATE'].map(mdates.date2num)
		fourteen_bottom.set_index('DATE', inplace=True)
		fourteen_bottom['VOLUME'] = fourteen_bottom['VOLUME'] / 1000000
		ax2.bar(fourteen_bottom[['VOLUME']].index, fourteen_bottom['VOLUME'])
		ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
		ax2.xaxis_date()
		ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
		ax2.set_ylabel('Volume', fontname='Trebuchet MS', fontsize=16)
		ax2.set_xlabel('Date', fontname='Trebuchet MS', fontsize=16)

		# plt.show()

		fig_right = BytesIO()
		plt.tight_layout()
		plt.savefig('plot.png')
		plt.savefig(fig_right, format='png')
		fig_right.seek(0)
		fig_right_png = base64.b64encode(fig_right.getvalue())

		return (fig_right_png)

if __name__=='__main__':
	cc = ChartCreator()
	currency_file = cc.find_largest_swing()
	currency = cc.file_to_name(currency_file)
	cc.create_chart_ma(currency_file, currency, '../Data/Bitcoin.txt')
	cc.create_chart_pv(currency_file, currency, '../Data/Bitcoin.txt')

