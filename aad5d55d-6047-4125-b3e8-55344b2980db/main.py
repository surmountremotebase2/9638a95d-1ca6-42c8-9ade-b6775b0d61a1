from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["AAPL"]

    @property
    def interval(self):
        return "5min"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]
        aapl_stake = 0.5
        return TargetAllocation({"AAPL": aapl_stake})