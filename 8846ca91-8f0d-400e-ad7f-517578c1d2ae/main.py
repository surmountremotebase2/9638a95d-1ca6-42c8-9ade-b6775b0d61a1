from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import CryptoAltRanking
from surmount.logging import log

class SimpleCryptoStrategy(Strategy):
    def __init__(self):
        # Add CryptoAltRanking as a data source
        self.data_list = [CryptoAltRanking()]
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
        # Get crypto alt ranking data
        crypto_rankings = data[("crypto_alt_ranking",)]
        
        if not crypto_rankings:
            return TargetAllocation({})
        
        # Get the latest ranking
        latest = crypto_rankings[-1]
        rankings = latest.get("alt_ranking", {})
        
        if not rankings:
            return TargetAllocation({})
        
        # Get top 5 cryptocurrencies by ranking (lower is better)
        top_coins = sorted(rankings.items(), key=lambda x: x[1])[:5]
        
        # Update tickers for backtesting
        self.tickers = [coin for coin, _ in top_coins]
        
        # Equal weight allocation
        allocation = {}
        weight = 1.0 / len(self.tickers)
        for coin in self.tickers:
            allocation[coin] = weight
        
        log(f"Trading: {self.tickers}")
        return TargetAllocation(allocation)

