# BlockheadExchange

## Authors

[**John Hall**](http://www.halljw.com)  and [**Brian Heath**](http://www.brianheath.info)


## Synopsis
BlockheadExchange is a webapp 



We set out to build a website that would help individuals with technical trading experience in securities and bonds markets explore the world of cryptocurrencies. We recognized that there was an understandable apprehension for most traders when approaching cryptocurrencies, but we believed that with some practical tools, we could show that substantial parallels exist between trading securities and trading crypto. 

The finished project is currently deployed and live. Check out [BlockheadExchange](http://www.blockheadexchange.com)!


## Getting Started

BlockheadExchange is implemented in the Flask python development framework using the Bootstrap front-end framework. See the *requirements.txt* for necessary dependencies for launching the primary webapp. Functionality is dvidied between the site's landing page and investment/analysis page. The landing page contains the mission statement of the project, information on navigation, and live updates on cryptocurrency news and prices. The investment page provides tools for graphing and analyzing historical data on a selection of cryptocurrencies.

The wireframing of the webapp and the main launch point for the deployed flask app are contained in the below files and directories:
* routes.py
* templates/
* static/

The full app is deployed through heroku and the finished project is currently live. 



### Live Tweet Updates

The class Twitter\_Searcher access the twitter API to randomly return information on a recent cryptocurrency tweet. The method get\_tweet() will return a tweet ID and the corresponding user. In order to view a sample output of the Twitter\_Searcher class, execute the following code. By default, the method returns a single result pertaining to search term 'bitcoin'.

```
python Twitter/twitter_searcher.py
```

### Crawling and displaying data

Class Coin\_Market\_Cap\_Spider crawls the site 'coinmarketcap.com' for the latest prices on a selection of cryptocurrencies. In order to manually download data, execute the following command. Resulting data will be written in CSV format to the 'Data' directory.

```
python coinmarketcap_crawler.py
```

The Crypto\_Currency\_Analyzer class constructs a dataframe of one or more currencies against a target feature (opening price, closing, etc…) indexed by trading date. The resulting collected data may be plotted using a standard line graph, as a rolling average with adjustable window average, normalized against a starting date, and analyzed over any arbitrary time period for which data is available. The dataframe is constructed using the Python Pandas library and plotting conducted with the Python Matplotlib library. The analysis code further includes Input.py which includes helper functions to ensure the correct formatting of inputs to the Analyzer code.

To display a sample of data generate by the web crawler, use the Analyzer.py class. By default, the analyzer will plot the previous year of Bitcoin data.

```
python Analyzer.py
```

## Acknowledgements

* Thanks to Swapneel Sheth, without whom this project would not have started
* Special thanks to coinmarketcap.com for publicly providing Cryptocurrency Market data


