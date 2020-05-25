import forex_alert as fa

url_eurusd = f"https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?granular=D&from={fa.get_closing_date()}"
url_usdjpy = f"https://api-fxpractice.oanda.com/v3/instruments/USD_JPY/candles?granular=D&from={fa.get_closing_date()}"


def test_message():
    list_of_strings = ["this", "is", "a", "list"]
    result = fa.build_body(list_of_strings)
    assert result == "this is a list"


def test_oanda_response():
    result = fa.get_forex_data(url_eurusd)
    assert result["instrument"] == "EUR_USD"


def test_get_price_range():
    range_forex = fa.get_price_range(url_eurusd)
    assert range_forex.start > 0
    assert range_forex.step > 0


def test_get_jpy_price_range():
    range_forex = fa.get_jpy_price_range(url_usdjpy)
    assert range_forex.start > 0
    assert range_forex.step > 0


# todo
# def test_price_alert():
# def test_check_lists():
# def test_send_text():
#     body = 'This is a text'
