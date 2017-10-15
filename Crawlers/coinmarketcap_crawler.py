#!/usr/bin/env python

import sys, requests, urllib, json, csv
import os
from bs4 import BeautifulSoup as bs


class Currency:

    def __init__(self, name):
        self.name = name
        self.url = "https://coinmarketcap.com/currencies/"+name+"/historical-data/?start=20000101&end=20171013"
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.market_caps = []

    def format_dates(self):
        """
        Convert dates to format YYYY-MM-DD
        """
        MONTHS = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        new_dates = []
        for date in self.dates:
            m = MONTHS[date.split()[0]]
            d = self.remove_commas(date.split()[1])
            y = date.split()[2]
            new_dates.append(y+"-"+m+"-"+d)
        self.dates = new_dates

    def remove_commas(self, entry):
        return ''.join([char for char in entry if char != ","])

    def cleanse_commas(self):
        self.opens = [self.remove_commas(o) for o in self.opens]
        self.highs = [self.remove_commas(h) for h in self.highs]
        self.lows = [self.remove_commas(l) for l in self.lows]
        self.closes = [self.remove_commas(c) for c in self.closes]
        self.volumes = [self.remove_commas(v) for v in self.volumes]
        self.market_caps = [self.remove_commas(m) for m in self.market_caps]

    def write_csv(self):
        header = ["Date", "Open", "High", "Low", "Close", "Volume", "Market_cap"]
        path = os.path.abspath('..'+os.sep+'Data/Crypto_Currencies'+os.sep+self.name+'.csv')
        f = open(path, 'w')
        writer = csv.writer(f)
        writer.writerow(header)
        for d, o, h, l, c, v, m in zip(self.dates, self.opens, self.highs, self.lows, self.closes, self.volumes, self.market_caps):
            row = [d, o, h, l, c, v, m]
            writer.writerow(row)
        f.close()


class Coin_Market_Cap_Spider:
    """
    """

    def __init__(self):
        self.url = "https://coinmarketcap.com"
        self.html = requests.get(self.url).text
        self.soup = bs(self.html, "html.parser")
        self.currencies = []

    def crawl_main_page(self):
        """
        """

        # a tag contains currencies
        #  class="currency-name-display"
        # href link to further details
        for line in self.soup.findAll('a', class_="currency-name-display"):
            #print line
            #print line.text
            #print "\n"
            self.currencies.append(Currency(line.text))

        for currency in self.currencies:
            try:
                self.crawl_currency(currency)
                currency.format_dates()
                currency.cleanse_commas()
                currency.write_csv()
                print("[+] Crawled: " + currency.name)
            except:
                print("[-] failed to crawl: " + currency.name)

    def crawl_currency(self, currency):
        """
        """
        html = requests.get(currency.url).text
        soup = bs(html, "html.parser")

        history = [line.text.split('\n\n') for line in soup.findAll('tbody')]
        history = history[0]
        for day in history:
            if day:
                lines = day.split("\n")
                lines = [line for line in lines if line]
                currency.dates.append(lines[0])
                currency.opens.append(lines[1])
                currency.highs.append(lines[2])
                currency.lows.append(lines[3])
                currency.closes.append(lines[4])
                currency.volumes.append(lines[5])
                currency.market_caps.append(lines[6])


if __name__=='__main__':
    cmcs = Coin_Market_Cap_Spider()
    cmcs.crawl_main_page()
