import unittest
import forex_alert
import requests


class Test_Stock(unittest.TestCase):
    def test_response_status(self):
        response = forex_alert.get_forex_data(forex_alert.EUR_USD)
        self.assertEqual(response["instrument"], "EUR_USD")


if __name__ == "__main__":
    unittest.main()
