from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]

    @property
    def interval(self):
        # Depending on your data provider and strategy preference,
        # this interval could be "1day" for daily checks.
        return "1day"

    @property
    def assets(self):
        return self.tickers

    # We don't need any additional data apart from the price history,
    # so we leave the data list empty.
    @property
    def data(self):
        return []

    def run(self, data):
        # Fetch SPY historical data from the provided