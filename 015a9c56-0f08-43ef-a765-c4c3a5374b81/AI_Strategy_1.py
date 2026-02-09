from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]
        # No additional data needed for this strategy
        self.data_list = []

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        ohlcv = data["ohlcv"]
        allocation_dict = {}

        for ticker in self.tickers:
            # Calculate technical indicators
            rsi = RSI(ticker, ohlcv, 14)
            short_sma = SMA(ticker, ohlcv, 50)  # Short-term SMA
            long_sma = SMA(ticker, ohlcv, 200)  # Long-term SMA

            # Check if the data is sufficient to make decisions
            if rsi and short_sma and long_sma and len(rsi) > 0 and len(short_sma) > 0 and len(long_sma) > 0:
                last_rsi = rsi[-1]
                last_short_sma = short_sma[-1]
                last_long_sma = long_sma[-1]

                # Define buy conditions
                if last_rsi < 30 and last_short_sma > last_long_sma:
                    allocation_dict[ticker] = 0.5  # Allocate half of the portfolio to this asset
                else:
                    allocation_dict[ticker] = 0  # Do not allocate to this asset
            else:
                # Default to no allocation if there is insufficient data
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)

# Example usage (this part is not meant to be executed in this isolated script example)
# strategy = TradingStrategy()
# allocations = strategy.run(data_provided_by_surmount_framework)
# print(allocations)