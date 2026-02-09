from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA

class BasicSMACrossoverStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]
        self.interval = "1day"
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return []

    def run(self, data):
        # Retrieve OHLCV data for SPY
        ohlcv_data = data["ohlcv"]
        # Ensure there's enough data to calculate our indicators
        if len(ohlcv_data) < 50:
            # Not enough data; no allocation
            return TargetAllocation({"SPY": 0})
        
        # Calculate the 20-day and 50-day SMAs for SPY
        sma_short = SMA("SPY", ohlcv_data, 20)[-1]
        sma_long = SMA("SPY", ohlcv_data, 50)[-1]

        # Initialize allocation dict
        allocation_dict = {"SPY": 0}

        # Generate signal based on the rule: buy signal when short-term SMA crosses above long-term SMA
        if sma_short > sma_long:
            # Allocate 100% to SPY as we have a buy signal
            allocation_dict["SPY"] = 1
        elif sma_short < sma_long:
            # No position, or consider shorting if your framework allows it
            allocation_dict["SPY"] = 0
        
        # Return the target allocation
        return TargetAllocation(allocation_dict)