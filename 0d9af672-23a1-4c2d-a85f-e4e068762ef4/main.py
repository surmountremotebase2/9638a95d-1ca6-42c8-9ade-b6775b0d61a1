from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import CryptoAltRanking
from surmount.logging import log

class TradingStrategy(Strategy):
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
        asset = next(iter(crypto_rankings[-1]['alt_ranking'])) + "USD"   
        log(f"Trading: {asset}")
        return TargetAllocation({asset:1})