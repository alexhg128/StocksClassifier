# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19M8EKPVrJMxlrwngVLN0A1MiWA41hKdB
"""

# Imports

import pandas as pd
import sys

# Import dataset

url = 'https://raw.githubusercontent.com/alexhg128/StocksClassifier/master/Dataset/processed_prices.csv'
prices = pd.read_csv(url)

sym_url = 'https://raw.githubusercontent.com/alexhg128/StocksClassifier/master/Dataset/securities.csv'
securities = pd.read_csv(sym_url)

def printProgress(c, t):
  sys.stdout.write('\r[')
  x = int(c / t * 100)
  for y in range(x):
    sys.stdout.write('=')
  for y in range(100 - x):
    sys.stdout.write(' ')
  sys.stdout.write('] ' + str(current) + '/' + str(total))

acceptable_gains = [ 0.05, 0.10, 0.15, 0.20 ]

pr = pd.DataFrame([], columns=[
    'date', 'symbol', 'open', 'close', 'low', 'high', 'volume', 'eps', 'pe',
    'yield1', 'yield3', 'yield6', 'yield12', 'ma50', 'ma200', 'ma300', 'rec',
    'term', 'gain', 'symid'
])

total = prices.shape[0]
current = 0

for k, p in prices.iterrows():
  id = securities.index[securities['Ticker symbol'] == p['symbol']].tolist()[0]
  for g in acceptable_gains:
    # ST = 3
    choiceST = 0
    if (p['hi91'] / p['close']) - g > 1:
      choiceST = 1

    # MT = 6
    choiceMT = 0
    if (p['hi182'] / p['close']) - g > 1:
      choiceMT = 1

    # LT = 12
    choiceLT = 0
    if (p['hi365'] / p['close']) - g > 1:
      choiceLT = 1

    ST = pd.Series([
                      p['date'], p['symbol'], p['open'], p['close'], p['low'],
                      p['high'], p['volume'], p['eps'], p['pe'], p['yield1'],
                      p['yield3'], p['yield6'], p['yield12'], p['ma50'], 
                      p['ma200'], p['ma300'], choiceST, 3, g, id
                  ],
                  index=[
                      'date', 'symbol', 'open', 'close', 'low', 'high', 'volume', 'eps', 'pe',
                      'yield1', 'yield3', 'yield6', 'yield12', 'ma50', 'ma200', 'ma300', 'rec',
                      'term', 'gain', 'symid'
                  ])
    MT = pd.Series([
                      p['date'], p['symbol'], p['open'], p['close'], p['low'],
                      p['high'], p['volume'], p['eps'], p['pe'], p['yield1'],
                      p['yield3'], p['yield6'], p['yield12'], p['ma50'], 
                      p['ma200'], p['ma300'], choiceMT, 6, g, id
                  ],
                  index=[
                      'date', 'symbol', 'open', 'close', 'low', 'high',
                      'volume', 'eps', 'pe', 'yield1', 'yield3', 'yield6',
                      'yield12', 'ma50', 'ma200', 'ma300', 'rec', 'term', 'gain', 'symid'
                  ])
    LT = pd.Series([
                      p['date'], p['symbol'], p['open'], p['close'], p['low'],
                      p['high'], p['volume'], p['eps'], p['pe'], p['yield1'],
                      p['yield3'], p['yield6'], p['yield12'], p['ma50'], 
                      p['ma200'], p['ma300'], choiceLT, 12, g, id
                  ],
                  index=[
                      'date', 'symbol', 'open', 'close', 'low', 'high',
                      'volume', 'eps', 'pe', 'yield1', 'yield3', 'yield6',
                      'yield12', 'ma50', 'ma200', 'ma300', 'rec', 'term', 'gain', 'symid'
                  ])
    pr = pr.append(ST, ignore_index=True)
    pr = pr.append(MT, ignore_index=True)
    pr = pr.append(LT, ignore_index=True)
  current += 1
  printProgress(current, total)

from google.colab import files
pr.to_csv('train_set.csv') 
files.download('train_set.csv')