from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.count = 0

    @property
    def assets(self):
        return ["gcusd"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]
        
    
        return TargetAllocation({"gcusd": gcusd_stake})