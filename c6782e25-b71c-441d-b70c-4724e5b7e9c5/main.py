from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
from datetime import datetime, timedelta

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["AAPL", "GOOG"]
        self.data_list = []

    @property
    def interval(self):
        return "1hour"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        goog = [i["GOOG"]["close"] for i in data["ohlcv"]]
        aapl = [i["AAPL"]["close"] for i in data["ohlcv"]]
        try:
            if (goog[-1]/goog[-2] < 1 or aapl[-1]/aapl[-2]<1):
                return TargetAllocation({})
            if goog[-1]/goog[-2] > aapl[-1]/aapl[-2]:
                return TargetAllocation({"AAPL": 1})
            else:
                return TargetAllocation({"GOOG": 1})
        except: pass
        return TargetAllocation({})