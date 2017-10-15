#!/usr/bin/env python

from Analyzer import Crypto_Currency_Analyzer as c

c = c()
c.df = c.fill_incomplete(c.df)
#c.plot_rolling_mean(currency='Ethereum')
#c.daily_returns_histogram(currency='Ethereum')
c.daily_returns_relation('Bitcoin', 'Ethereum')
