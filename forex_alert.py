import config as hidden
import requests
import numpy as np
from twilio.rest import Client
import datetime

HEADERS = {'Authorization': 'bearer {}'.format(hidden.OANDA_AUTH)}
BASE_PAIRS = f'https://api-fxpractice.oanda.com/v3/instruments/'
forex_activate = ['good:']
forex_bad = ['bad:']

#binary doesn't like long decimal numbers
forex_list = {
    'EUR_USD': [10950, 10831],
    'GBP_USD': [12200, 12401],

}

jpy_list = {
    'GBP_JPY': [13191, 13192]
}

def get_closing_date():
    """get the closing date in ISO format."""
    return (datetime.datetime.now() - datetime.timedelta(1)).isoformat()

USD_JPY = f'{BASE_PAIRS}USD_JPY/candles?granular=D&from={get_closing_date()}'
EUR_USD = f'{BASE_PAIRS}EUR_USD/candles?granular=D&from={get_closing_date()}'

def get_price_range(url):
    """Get the range of prices into a list."""
    r = requests.get(url=url, headers=HEADERS)
    ro = r.json()
    high = int(round(float(ro['candles'][0]['mid']['h']), 4) * 10000)
    low = int(round(float(ro['candles'][0]['mid']['l']), 4) * 10000)
    return range(low , high)
    #decimal doesn't like long decimal, so I multiplied it out.

def price_alert(forex_pair):
    """Find the right price level."""
    for pair in forex_pair:
        url = F'{BASE_PAIRS}{pair}/candles?granularity=D&from={get_closing_date()}'
        forex_range = get_price_range(url)
        if forex_list[pair][0] in forex_range:
            print('true')
            forex_activate.append(pair)
        if forex_list[pair][1] in forex_range:
            print('true')
            forex_bad.append(pair)


def get_jpy_price_range(url):
    """Get the range of prices into a list."""
    new_list = []
    r = requests.get(url=url, headers=HEADERS)
    ro = r.json()
    high = int(round(float(ro['candles'][0]['mid']['h']), 2) * 100)
    low = int(round(float(ro['candles'][0]['mid']['l']), 2) * 100)
    return range(low, high)

def jpy_price_alert(forex_pair):
    """Find the right price level."""
    for pair in forex_pair:
        url = F'{BASE_PAIRS}{pair}/candles?granularity=D&from={get_closing_date()}'
        forex_range = get_jpy_price_range(url)
        if jpy_list[pair][0] in forex_range:
            print('true')
            forex_activate.append(pair)
        if jpy_list[pair][1] in forex_range:
            print('true')
            forex_bad.append(pair)

def check_lists():
    """check lists if they are empty then send a text"""
    if len(forex_activate) > 1:
        good_body = build_body(forex_activate)
        send_text(good_body)
    if len(forex_bad) > 1:
        bad_body = build_body(forex_bad)
        send_text(bad_body)

def build_body(forexlist):
    """build message to be sent through twilio."""
    return ' '.join(forexlist)

def send_text(body):
    """send a message through twilio"""
    client = Client(hidden.Twilio_ID, hidden.Twilio_Token)

    message = client.messages \
        .create(
        body=body,
        from_=hidden.My_Twilio_number,
        to=hidden.my_number
            )
    print(message.sid)

price_alert(forex_list)
jpy_price_alert(jpy_list)
check_lists()

print(forex_activate)
print(forex_bad)


# if __name__ == "__main__":
#      price_alert(forex_list)
#      check_lists()    
#      pass