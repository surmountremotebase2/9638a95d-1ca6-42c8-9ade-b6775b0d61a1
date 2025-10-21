from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import TimMoore
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.data_list = [TimMoore()]
        self.tickers = []

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list
        

    def run(self, data):
        tim_moore_holdings = data[("tim_moore",)]      
        log(f"Trading: {tim_moore_holdings}")
        log(f"allocation:{tim_moore_holdings[-1]['allocations']}")
        return TargetAllocation(tim_moore_holdings[-1]['allocations'])