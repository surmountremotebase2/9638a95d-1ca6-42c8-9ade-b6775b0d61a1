from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import NDWPowerSevenTrades
from surmount.logging import log


class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]

        # Build data sources for each ticker
        self.data_list = [NDWPowerSevenTrades()]

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

        ndw_power7_trades = data.get(("ndw_power7_trades"))
        log(f"ndw_power7_trades: {ndw_power7_trades}")


        return TargetAllocation(allocation)
