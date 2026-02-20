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
        key = tuple(self.data_list[0])
        ndw_data = data.get(key)
        log(str(ndw_data))
        if ndw_data and len(ndw_data) > 0:
            allocations = ndw_data[-1].get("allocations", {})
            total = sum(allocations.values())
            log(str(allocations.values()))

            if total > 0:
                normalized = {k: v / total for k, v in allocations.items()}
                self.tickers = list(normalized.keys())
                return TargetAllocation(normalized)

        return None