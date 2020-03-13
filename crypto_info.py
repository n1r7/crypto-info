# IMPORT LIBRARIES

import pandas as pd
import requests
import json
import math


# DETERMINE HOW MANY GET REQUESTS ARE REQUIRED AT 100 PER REQUEST

coinlore = requests.get('https://api.coinlore.com/api/global/')
# print(coinlore)

coinlore_json = coinlore.json()
# print(coinlore_json)

num_coins = pd.DataFrame(coinlore_json)
# num_coins.head()

num_reqs = math.ceil(num_coins['coins_count']/100)
# print(num_reqs)


# CRYPTOCURRENCIES

currencies = pd.DataFrame([])
    
for i in range(num_reqs):
    coin_req = requests.get(f'https://api.coinlore.com/api/tickers/?start={i*100}&limit=100').json()
    df_temp = pd.DataFrame(coin_req['data'])
    currencies = currencies.append(df_temp, ignore_index=True, sort=False)

currencies['type']='currency'
currencies.to_csv(r'crypto_currencies.csv') # Save to CSV


# CRYPTO EXCHANGES

ex_req = requests.get('https://api.coinlore.com/api/exchanges/').json()
exchanges = pd.DataFrame(ex_req)
exchanges['type']='exchange'
exchanges.to_csv(r'crypto_exchanges.csv') # Save to CSV


# EXTRACT NAME

curr_clean = currencies[['type','name','nameid','symbol']]
exch_clean = exchanges[['type','name','country','url']]

crypto_combined = pd.concat([exch_clean, curr_clean], axis=0, ignore_index=True, sort=True)
crypto_combined.to_csv(r'crypto_combined.csv') # Save to CSV
