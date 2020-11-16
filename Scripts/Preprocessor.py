# Imports

import pandas as pd

# Dataset Imports

fundamentals_url = 'https://raw.githubusercontent.com/alexhg128/StocksClassifier/master/Dataset/fundamentals.csv'
prices_url = 'https://raw.githubusercontent.com/alexhg128/StocksClassifier/master/Dataset/prices-split-adjusted.csv'
securities_url = 'https://raw.githubusercontent.com/alexhg128/StocksClassifier/master/Dataset/securities.csv'

fundamentals = pd.read_csv(fundamentals_url)
prices = pd.read_csv(prices_url)
securities = pd.read_csv(securities_url)

prices['date'] = pd.to_datetime(prices['date'])
fundamentals['Period Ending'] = pd.to_datetime(fundamentals['Period Ending'])

prices_per_symbol = []
fundamentals_per_symbol = []

for i, s in securities.iterrows():
  prices_per_symbol.append(prices.loc[prices['symbol'] == s['Ticker symbol']])
  fundamentals_per_symbol.append(fundamentals.loc[fundamentals['Ticker Symbol'] == s['Ticker symbol']])

year = pd.Timedelta(365, 'days')
months_1 = pd.Timedelta(30, 'days')
months_3 = pd.Timedelta(91, 'days')
months_6 = pd.Timedelta(182, 'days')
days_5 = pd.Timedelta(5, 'days')

days_50 = pd.Timedelta(50, 'days')
days_200 = pd.Timedelta(200, 'days')
days_300 = pd.Timedelta(300, 'days')

for i in range(len(prices_per_symbol)):
  min_price_date = prices_per_symbol[i]['date'].min()
  max_price_date = prices_per_symbol[i]['date'].max()
  min_fun_date = fundamentals_per_symbol[i]['Period Ending'].min()
  max_fun_date = fundamentals_per_symbol[i]['Period Ending'].max()

  min_date = max(min_price_date, min_fun_date) + year
  max_date = min(max_price_date, max_fun_date) - year

  filter = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= min_date) & (prices_per_symbol[i]['date'] < max_date)]

  for k, p in filter.iterrows():
    try:
      eps = fundamentals_per_symbol[i].loc[(fundamentals_per_symbol[i]['Period Ending'] >= p['date']) & (fundamentals_per_symbol[i]['Period Ending'] >= p['date'] - days_5)].iloc[0]['Earnings Per Share']
      prices.loc[k, 'eps'] = eps
      pe = p['close'] / eps
      prices.loc[k, 'pe'] = pe

      price_1 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - months_1)) & (prices_per_symbol[i]['date'] >= (p['date'] - months_1 + days_5))].iloc[0]['close']
      price_3 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - months_3)) & (prices_per_symbol[i]['date'] >= (p['date'] - months_3 + days_5))].iloc[0]['close']
      price_6 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - months_6)) & (prices_per_symbol[i]['date'] >= (p['date'] - months_6 + days_5))].iloc[0]['close']
      price_12 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - year)) & (prices_per_symbol[i]['date'] >= (p['date'] - year + days_5))].iloc[0]['close']

      yield_1 = p['close'] / price_1 * 100
      yield_3 = p['close'] / price_3 * 100
      yield_6 = p['close'] / price_6 * 100
      yield_12 = p['close'] / price_12 * 100

      prices.loc[k, 'yield1'] = yield_1 - 100
      prices.loc[k, 'yield3'] = yield_3 - 100
      prices.loc[k, 'yield6'] =  yield_6 - 100
      prices.loc[k, 'yield12'] = yield_12 - 100

      last_50 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - days_50)) & (prices_per_symbol[i]['date'] <= p['date'])]['close'].mean()
      last_200 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - days_200)) & (prices_per_symbol[i]['date'] <= p['date'])]['close'].mean()
      last_300 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= (p['date'] - days_300)) & (prices_per_symbol[i]['date'] <= p['date'])]['close'].mean()

      prices.loc[k, 'ma50'] = last_50
      prices.loc[k, 'ma200'] = last_200
      prices.loc[k, 'ma300'] =  last_300

      next_3 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= p['date']) & (prices_per_symbol[i]['date'] <= (p['date'] + months_3))]
      next_6 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= p['date']) & (prices_per_symbol[i]['date'] <= (p['date'] + months_6))]
      next_12 = prices_per_symbol[i].loc[(prices_per_symbol[i]['date'] >= p['date']) & (prices_per_symbol[i]['date'] <= (p['date'] + year))]

      prices.loc[k, 'hi91'] = next_3['high'].max()
      prices.loc[k, 'hi182'] = next_6['high'].max()
      prices.loc[k, 'hi365'] = next_12['high'].max()

      prices.loc[k, 'lo91'] = next_3['low'].min()
      prices.loc[k, 'lo182'] = next_6['low'].min()
      prices.loc[k, 'lo365'] = next_12['low'].min()
    except:
      pass

final_prices = prices[prices['eps'].notna()]

from google.colab import files
final_prices.to_csv('processed_prices.csv') 
files.download('processed_prices.csv')