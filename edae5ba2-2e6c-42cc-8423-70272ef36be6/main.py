from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import LobbyTop10
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.data_list = [LobbyTop10()]
        self.tickers = []

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
        lobby_top10_holdings = data[("lobby_top10",)]
        allocations = {"AAPL": 1}
        if lobby_top10_holdings:
            alloc_dict = lobby_top10_holdings[-1]['allocations']
            log(f"Trading: {lobby_top10_holdings[-1]['allocations']}")
            allocations = alloc_dict
        log(f"allocations:{allocations}")
        return TargetAllocation(allocations)
