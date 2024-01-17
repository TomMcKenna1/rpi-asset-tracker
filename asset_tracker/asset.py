import yfinance as yf
from pandas import DataFrame


class Asset:
    """
    Wrapper class to yfinance Ticker
    """

    def __init__(self, symbol):
        self.yf_ticker = yf.Ticker(symbol)
        self._name = symbol
        self.refresh()

    @property
    def name(self) -> str:
        return self._name

    @property
    def history(self) -> DataFrame:
        return self._history

    @property
    def price(self) -> int:
        return self.history["Close"].iloc[-1]

    @property
    def change(self) -> int:
        prev_close = self._history["Close"].iloc[-2]
        return ((self.price - prev_close) / prev_close) * 100

    def refresh(self):
        self._history = self.yf_ticker.history()
