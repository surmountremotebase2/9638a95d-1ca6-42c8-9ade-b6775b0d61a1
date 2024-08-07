from surmount.base_class import Strategy
from surmount.logging import log
from surmount.data import Asset 

class TradingStrategy(Strategy):
    def __init__(self):
        self._assets = ['SPY']

    @property
    def assets(self):
        return self._assets

    @property 
    def interval(self):
        return "1hour"

    def run(self, data):
        return {'AAPL': 0.5, 'GME': 0.5}