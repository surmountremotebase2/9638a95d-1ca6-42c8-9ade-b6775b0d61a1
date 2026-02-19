from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.logging import log
from surmount.data import NDWFirstTrustFocusFive, NDWFirstTrustFocusFiveTrades
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = []
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
        for i in self.data_list:
            if tuple(i)[0] == "ndw_ftrust5":
                ndw_data = data.get(tuple(i))
                log(f"NDW FTrust5 data: {ndw_data}")
                if ndw_data and len(ndw_data) > 0:
                    allocations = ndw_data[-1].get("allocations", {})
                    total = sum(allocations.values())
                    if total > 0:
                        return TargetAllocation({k: v / total for k, v in allocations.items()})
            elif tuple(i)[0] == "ndw_ftrust5":
                trades_data = data.get(tuple(i))
                log(f"NDW FTrust5 Trades data: {trades_data}")
        return None
