from surmount.base_class import Strategy, TargetAllocation

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["SPY"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]
  
        return TargetAllocation({"SPY": -0.5})