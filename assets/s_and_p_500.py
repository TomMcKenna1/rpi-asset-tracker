from base import Asset
import yfinance as yf

class S_And_P_500(Asset):

    def __init__(self):
        self.name = "S&P 500"
        self.price = self.get_latest_price()
        self.yf_ticker = yf.Ticker("^GSPC")

    def get_latest_price(self):
        latest_data = self.yf_ticker.history()
        return latest_data['Close'].iloc[-1]