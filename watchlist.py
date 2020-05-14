import stock_alert

stock = {
    'TSLA':[345, 900],
    'AAPL':[200, 335],
    'AMZN':[2050, 2500],
    'AMD':[40, 62],
}

activate = stock_alert.price_alert(stock)
stock_alert.check_list(activate)
