from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import NDWFirstTrustFocusFive
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]

        # Build data sources for each ticker
        self.data_list = [NDWFirstTrustFocusFive()]

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
        allocation = {}

        ndw_ftrust5 = data.get(("ndw_ftrust5"))
        log(f"ndw_ftrust5: {ndw_ftrust5[-1]}")


        return TargetAllocation(allocation)
