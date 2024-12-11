from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]
        self.data_list = [Asset(i) for i in self.tickers]  # Assuming Asset class can provide OHLCV data
        
    @property
    def interval(self):
        return "1day"  # Use daily price data
        
    @property
    def assets(self):
        return self.tickers  # Trading strategy focuses on SPY
        
    @property
    def data(self):
        return self.data_list  # Define the data required

    def run(self, data):
        # Assuming 'data' parameter contains a dictionary with OHLCV data for each ticker
        # Key format is expected to be ("ohlcv", ticker)
        log(str(data))
        spy_data = data.get(("ohlcv", "SPY"), [])
        