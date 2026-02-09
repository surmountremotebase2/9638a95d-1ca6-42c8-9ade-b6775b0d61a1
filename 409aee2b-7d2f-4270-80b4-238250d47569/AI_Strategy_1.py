from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA

class MovingAverageCrossoverStrategy(Strategy):
    def __init__(self):
        # Define the assets the strategy will deal with
        self.tickers = ["SPY"]

    @property
    def interval(self):
        # The data interval. For this strategy, daily data is sufficient.
        return "1day"

    @property
    def assets(self):
        # Return the list of ticker symbols
        return self.tickers

    @property
    def data(self):
        # No additional data sources are needed for this basic strategy.
        return []

    def run(self, data):
        # We will need to extract the OHLCV data for the ticker
        ohlcv_data = data["ohlcv"]
        
        # Calculate the short-term and long-term SMAs
        short_term_sma = SMA("SPY", ohlcv_data, 50)  # E.g., 50-day SMA
        long_term_sma = SMA("SPY", ohlcv_data, 200)  # E.g., 200-day SMA

        # Ensure we have enough data points to calculate both SMAs
        if short_term_sma is None or long_term_sma is None or len(short_term_sma) < 1 or len(long_term_sma) < 1:
            # Not enough data, no action
            return TargetAllocation({})
        
        target_allocation = {}

        # Check the latest SMA values to decide on allocation
        if short_term_sma[-1] > long_term_sma[-1]:
            # If the short-term SMA is above the long-term SMA, allocate 100% to SPY
            target_allocation["SPY"] = 1.0
        else:
            # If the short-term SMA is below the long-term SMA, do not allocate to SPY
            target_allocation["SPY"] = 0.0

        return TargetAllocation(target_allocation)

# The strategy class is now defined and can be instantiated and used within the Surmount framework.