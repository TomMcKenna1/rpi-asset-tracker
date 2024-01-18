from typing import Union

import yfinance as yf
from pandas import DataFrame


class Asset:
    """
    Wrapper class to yfinance Ticker.
    """

    def __init__(self, ticker: str, name: Union[str, None] = None):
        self.yf_ticker = yf.Ticker(ticker)
        self._ticker = ticker
        # An asset's name is it's ticker unless specified
        self._name = ticker
        if name != None:
            self._name = name
        self.refresh()

    @property
    def ticker(self) -> str:
        return self._ticker

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

    def refresh(self) -> None:
        self._history = self.yf_ticker.history()
