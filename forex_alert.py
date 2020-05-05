##
##       still a work in process
##

import config as hidden
import watchlist as wl
import requests, json
import numpy as np
from datetime import datetime

forex_list = ['EURUSD', 'GBPJPY']

BASE_URL = 'https://api-fxpractice.oanda.com'
ACCOUNT_URL = '{}/v3/accounts/{}'.format(BASE_URL, hidden.OANDA_ID)
HEADERS = {'Authorization': 'bearer {}'.format(hidden.OANDA_AUTH)}
INSTRUMENT_URL = '{}/v3/instruments/{}/candles'.format(BASE_URL,forex_list[0])
PRICING_URL = '{}/instruments/{}/pricing'.format(ACCOUNT_URL, forex_list[0])
activate_forex = []


def get_date():
    """get the current date in ISO format."""
    return datetime.now().strftime('%Y-%m-%d')

def get_price_range(strticker, isodate):
    """Get the range of prices into a list."""
    ts = avt.TimeSeries(key=hidden.alpha_api)
    data, meta = ts.get_daily(strticker)
    high = data[isodate]['2. high']
    low = data[isodate]['3. low']
    return np.arange(float(low), (float(high), .0001))

def price_alert(strticker):
    """Find the right price level."""
    date = get_date()
    for ticker, price in strticker.items():
        price_range = get_price_range(ticker, date)
        if price in price_range:
            activate_forex.append(ticker)
        else:
            None

r = requests.get(url=PRICING_URL, headers=HEADERS)
print(r.status_code)
ro = json.loads(r.content)
print(ro)