from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.count = 0

    @property
    def assets(self):
        return ["SHOP"]

    @property
    def interval(self):
        return "5min"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]
        
        if self.count % 2 == 0:
            target_allocation = 1
        else:
            target_allocation = 0
        
    
        return TargetAllocation({"AAPL": gcusd_stake})