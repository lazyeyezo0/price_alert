
# =============================================================================
# python==3.7.4
# alpha_vantage==2.2.0
# 
# =============================================================================

import config as hidden
import watchlist as wl
from datetime import datetime
import alpha_vantage.timeseries as avt
import smtplib, ssl
import os

activate_stock = []
bad_stock = []

def get_today():
    """get the current date in ISO format."""
    return datetime.now().strftime('%Y-%m-%d')


def get_stock_data(strticker):
    """request to get the data for stocks"""
    ts = avt.TimeSeries(key=hidden.alpha_api)
    data, meta = ts.get_daily(strticker)
    return data

def get_price_range(strticker, isodate):
    """Get the range of prices into a list."""
    data = get_stock_data(strticker)
    high = data[isodate]['2. high']
    low = data[isodate]['3. low']
    return range(int(float(low)), int(float(high)), 1)

def price_alert(strticker):
    """Find the right price level."""
    date = get_today()
    x = []
    for ticker, price in strticker.items():
        price_range = get_price_range(ticker, date)
        if price in price_range:
            x.append(ticker)
    return x
        

def check_list(activate_stock):
    """checks lists then activate email func if not empty"""
    if len(activate_stock) > 0:
        email_notification(activate_stock)


def write_message(activate_stock):
    """write a message to be sent out to email."""
    message = ['\n\ncheck', 'out','these:\n\n'] + activate_stock + ['\n\nhappy', 'trading!']
    return ' '.join(message)


def email_notification(activate_stock):
    """sends myself a email of a good price on stock"""
    port = 465
    sender_email = hidden.email
    receiver_email = hidden.email
    message = write_message(activate_stock)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(receiver_email,hidden.email_password)
        server.sendmail(sender_email, receiver_email,message)

if __name__ == '__main__':
    price_alert(wl.stock)
    check_list(activate_stock)
