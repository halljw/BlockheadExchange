#!/usr/bin/env python

import sys, requests, urllib, json, csv, os, datetime, traceback
import pandas as pd
from bs4 import BeautifulSoup as bs
import boto3
from io import BytesIO

class Currency:

    def __init__(self, name):
        self.name = name.replace(' ', '-')
        self.url = "https://coinmarketcap.com/currencies/"+self.name+"/historical-data/?start=20000101&end="+self.todays_date()
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.market_caps = []

    def reverse_lists(self):
        """
        Reverses the order of all lists in the currency
        """
        self.dates.reverse()
        self.opens.reverse()
        self.highs.reverse()
        self.lows.reverse()
        self.closes.reverse()
        self.volumes.reverse()
        self.market_caps.reverse()

    def todays_date(self, formatted=False):
        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day
        if (d == 1):
          m -= 1
          d = 31
        if formatted:
            return "%d-%02d-%02d" % (y, m, d-1)
        return "%d%02d%d" % (y, m, d-1)

    def up_to_date(self):
        """
        Returns true if currency's csv:
          - exists
          - has up to date data (checks for day before today)
        Returns false otherwise
        """
        path = os.path.abspath('Data'+os.sep+self.name+'.txt')
        try:
            f = open(path, 'r')
        except IOError:
            return False
        lines = f.readlines()
        latest_date = lines[-1].split(',')[0]
        f.close()
        todays_date = self.todays_date(formatted=True)
        return todays_date == latest_date
        

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
            new_dates.append(y+m+d)
        self.dates = new_dates

    def remove_commas(self, line):
        return ''.join([char for char in line if char != ","])

    def cleanse_commas(self):
        self.opens = [self.remove_commas(o) for o in self.opens]
        self.highs = [self.remove_commas(h) for h in self.highs]
        self.lows = [self.remove_commas(l) for l in self.lows]
        self.closes = [self.remove_commas(c) for c in self.closes]
        self.volumes = [self.remove_commas(v) for v in self.volumes]
        self.market_caps = [self.remove_commas(m) for m in self.market_caps]

    def make_df(self):
        self.reverse_lists()
        header = ["DATE", "OPEN", "HIGH", "LOW", "CLOSE", "VOL", "P", "R", "RINFO"]
        df = pd.DataFrame(columns=header)
        for d, o, h, l, c, v in zip(self.dates, self.opens, self.highs, self.lows, self.closes, self.volumes):
            row = pd.DataFrame([[d, o, h, l, c, v, 0, 0, 0]], columns=header)
            df = df.append(row)
        return df


class Coin_Market_Cap_Spider:
    """
    Spider for 'coinmarketcap.com'
    Creates a list of Currency objects for each cryptocurrency on the site
    Crawls main page to find all available currencies; crawls each currency page
    """
    CURRENCIES = ['Bitcoin', 'Litecoin', 'Monero', 'Bitcoin-Cash', 'Bitcoin-Gold',
                  'Cardano', 'Dash', 'EOS', 'Ethereum-Classic', 'Ethereum', 'IOTA',
                  'NEM', 'NEO', 'Qtum', 'Ripple', 'Stellar-Lumens']

    def __init__(self):
        self.url = "https://coinmarketcap.com/all/views/all"
        self.html = requests.get(self.url).text
        self.soup = bs(self.html, "html.parser")
        self.currencies = []
        self.failed_to_crawl = []

    def crawl_main_page(self):
        """
        Creates list of currencies found on main page
        Crawls each currency page to create Currency object
        """
        # Creates currency objects from list of desired CURRENCIES
        for currency in self.CURRENCIES:
          self.currencies.append(Currency(currency))

        l = len(self.currencies)
        for i, currency in enumerate(self.currencies):
            if currency.up_to_date():
                print("[+] %d/%d Currency '%s' already up-to-date" % (i+1, l, currency.name))
                continue
            try:
                self.crawl_currency(currency)
                currency.format_dates()
                currency.cleanse_commas()
                df = currency.make_df()
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer)
                content = csv_buffer.getvalue()
                client = boto3.client('s3', 
                    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
                    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
                client.put_object(Bucket=os.environ['S3_BUCKET_NAME'], Key='{}.txt'.format(currency.name), Body=content)
                print("[+] %d/%d Crawled: %s" % (i+1, l, currency.name))
            except:
                print("[-] %d/%d failed to crawl: %s" % (i+1, l, currency.name))
                print(traceback.format_exc())
                self.failed_to_crawl.append(currency.name)

    def crawl_currency(self, currency):
        """
        Crawls specific page for given currency
        """
        html = requests.get(currency.url).text
        soup = bs(html, "html.parser")
        history = [line.text.split('\n\n') for line in soup.findAll('tbody')]

        # Occasionally hyphenated names, drop the second in the url
        if (not history):
            currency.url = currency.url.replace(currency.name, currency.name.split('-')[0])
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

    def log_failures(self):
        """
        Write log file detailing date, currencies which could not be updated
        """
        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day
        date = "%d-%d-%d" % (y, m, d-1)

        f = open('log_failures.csv', 'a')
        writer = csv.writer(f)
        row = [date] + self.failed_to_crawl
        writer.writerow(row)
        f.close()
       

if __name__=='__main__':
    cmcs = Coin_Market_Cap_Spider()
    cmcs.crawl_main_page()
    cmcs.log_failures()
