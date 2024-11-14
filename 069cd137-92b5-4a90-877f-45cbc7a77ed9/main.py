from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.ticker = "AAPL"
        self.window = 5  # The lookback window for moving averages

    @property
    def assets(self):
        return [self.ticker]
        
    @property
    def interval(self):
        return "1day"

    def run(self, data):
        if len(data["ohlcv"]) < self.window:  
            return TargetAllocation({})  

        closes = [item[self.ticker]["close"] for item in data["ohlcv"]][-self.window:]  
        volumes = [item[self.ticker]["volume"] for item in data["ohlcv"]][-self.window:] 

        close_sma = SMA(self.ticker, data["ohlcv"], self.window)  
        volume_sma = SMA(self.ticker, data["ohlcv"], self.window)  

        if not close_sma or not volume_sma: 
            return TargetAllocation({})

        roc_close = (closes[-1] - closes[-2]) / closes[-2]
        roc_volume = (volumes[-1] - volumes[-2]) / volumes[-2]

        allocation = 0
        if roc_close > 0 and roc_volume > 0:  
            log(f"Buying {self.ticker}")
            allocation = 1  

        return TargetAllocation({self.ticker: allocation})