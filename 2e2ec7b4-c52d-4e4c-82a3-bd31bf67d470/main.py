from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Strategy applies to gcusd
        return ["AAPL","AMZN"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]

        return TargetAllocation({"AAPL": 0.5,"AMZN":0.5})