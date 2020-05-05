"""
python==3.7.4
alpaca_trade_api==0.46
alpha_vantage==2.2.0
request==2.23.0
"""

import config as hidden
import watchlist as wl
from datetime import datetime
import alpha_vantage.timeseries as avt
import smtplib, ssl

activate_stock = []

def get_date():
    """get the current date in ISO format."""
    return datetime.now().strftime('%Y-%m-%d')

def get_price_range(strticker, isodate):
    """Get the range of prices into a list."""
    ts = avt.TimeSeries(key=hidden.alpha_api)
    data, meta = ts.get_daily(strticker)
    high = data[isodate]['2. high']
    low = data[isodate]['3. low']
    return range(int(float(low)), int(float(high)), 1)

def price_alert(strticker):
    """Find the right price level."""
    date = get_date()
    for ticker, price in strticker.items():
        price_range = get_price_range(ticker, date)
        if price in price_range:
            activate_stock.append(ticker)
        else:
            None

def check_list(activate_stock):
    if len(activate_stock) > 0:
        email_notification(activate_stock)
    else:
        None

def email_notification(activate_stock):
    port = 465
    sender_email = hidden.email
    receiver_email = hidden.email
    message = 'subject: check out these stocks\n\n' + activate_stock + '\n\nhappy trading'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(hidden.email,hidden.email_password)
        server.sendmail(sender_email, receiver_email,message)

price_alert(wl.stock)
check_list(activate_stock)