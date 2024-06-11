from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset ticker we are interested in
        self.ticker = "TSLA"
        # Define short and long windows for moving averages
        self.short_window = 5
        self.long_window = 20

    @property
    def assets(self):
        # List of assets this strategy will handle. Currently only TSLA.
        return [self.ticker]

    @property
    def interval(self):
        # Data fetching interval, using daily data for this strategy.
        return "1day"

    def run(self, data):
        # Initialize allocation to 0
        allocation_dict = {self.ticker: 0}

        # Check if we have enough data to compute both short and long SMAs
        if len(data["ohlcv"]) < self.long_window:
            # Not enough data, skip this run
            return TargetAllocation(allocation_dict)
        
        # Calculate short and long simple moving averages
        short_sma = SMA(self.ticker, data["ohlcv"], self.short_window)
        long_sma = SMA(self.ticker, data["ohlcv"], self.long_window)
        
        # Implement the crossover strategy
        # Buy signal: if short SMA crosses above long SMA
        if short_sma[-1] > long_sma[-1] and short_sma[-2] < long_sma[-2]:
            log(f"BUY signal for {self.ticker}")
            allocation_dict[self.ticker] = 1.0  # Set allocation to 100% of portfolio
        
        # Sell signal: if short SMA crosses below long SMA
        elif short_sma[-1] < long_sma[-1] and short_sma[-2] > long_sma[-2]:
            log(f"SELL signal for {self.ticker}")
            allocation_dict[self.ticker] = 0  # Set allocation to 0% of portfolio
        else:
            # No action required if there's no crossover
            log(f"No action for {self.ticker}")
            # We retain the existing allocation (not changing the position)

        return TargetDisposition(allocation_dict)