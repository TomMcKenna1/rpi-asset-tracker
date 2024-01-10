import yfinance as yf


class Asset:
    def __init__(self, symbol):
        self.yf_ticker = yf.Ticker(symbol)
        self._name = symbol
        self.refresh()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def change(self):
        return self._change

    @change.setter
    def change(self, value):
        self._change = value

    def refresh(self):
        self._history = self.yf_ticker.history()
        self._price = self._history["Close"].iloc[-1]
        prev_close = self._history["Close"].iloc[-2]
        self._change = ((self._price - prev_close) / prev_close) * 100
