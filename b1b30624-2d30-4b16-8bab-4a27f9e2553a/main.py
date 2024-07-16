from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, MACD, RSI
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
        return "1day"

    def run(self, data):
        return {'FAZ': 1}

from datetime import datetime

start = datetime.strptime("2024-06-08", '%Y-%m-%d')
end = datetime.strptime("2024-07-08", '%Y-%m-%d')
a = backtest(TradingStrategy(), start, end, 10000)

print(a['stats'])