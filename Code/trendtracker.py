#make dictionary of text files
#scan each text file for...
#-greatest variance over last seven days against BTC
#-greatest volume change in the last seven days vs previous seven days
#make csv

from Input import *

class Volatility_Analyzer:

	def __init__(self):
		self.features = ["HIGH", "LOW", "VOL"]
		self.available_currencies = [c[:-4] for c in os.listdir('Data')]
		print self.available_currencies;

	def compare_currencies_variance(self)
		return (coin_variance)

	def compare_currencies_volume(self)
		return (coin_volume)

	def output_data_variance(currency)
		df = df.join(pd.read_csv("Data/"+c+".txt", index_col="DATE",
			parse_dates=True, usecols=["DATE", feature],
			na_values=["nan"]))

	def output_data_volume(currency)
		df = df.join(pd.read_csv("Data/"+c+".txt", index_col="DATE",
			parse_dates=True, usecols=["DATE", feature],
			na_values=["nan"]))



if __name__=='__main__':
	va = Volatility_Analyzer()
	va.output_data_variance(va.compare_currencies_variance())
	va.output_data_volume(va.compare_currencies_volume())