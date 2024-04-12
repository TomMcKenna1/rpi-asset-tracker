from typing import Union
import time
import random

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
        self._error_message = ""
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
    def error_message(self) -> DataFrame:
        return self._error_message
    
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
        retry_delay = 1  # Initial delay in seconds
        for _ in range(4):
            try:
                self._history = self.yf_ticker.history(raise_errors=True)
                self._error_message = ""
                return
            except Exception as e:
                print(e)
                time.sleep(retry_delay)
                retry_delay *= 2
                retry_delay += random.uniform(0, 1)
        self._error_message = "Error getting ticker data."