from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import (
    TopActiveStocks
)
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize data sources
        self.data_list = [
            TopActiveStocks(),
        ]
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
        allocation_dict = {}
        
        # Get top active stocks
        active_stocks = data[("top_active_stocks",)]    
        tickers = [stock["ticker"] for stock in active_stocks]
        log(str(tickers))
        allocation_dict = {"AAPL":0.5, "NVDA": 0.5}

        return TargetAllocation(allocation_dict)

