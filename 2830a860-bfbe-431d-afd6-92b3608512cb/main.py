from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers you're interested in
        self.tickers = ["MSFT"]
        # Initialize a list to hold OHLCV data for the tickers
        self.data_list = [OHLCV(i) for i in self.tickers]

    @property
    def interval(self):
        # Set the data interval, e.g., "1day" for daily data
        return "1day"

    @property
    def assets(self):
        # Return the list of tickers this strategy will operate on
        return self.tickers

    @property
    def data(self):
        # Return the data needed for this strategy
        return self.data_list

    def run(self, data):
        # Initialize an allocation dictionary with 0 allocation for the defined tickers
        allocation_dict = {i: 0 for i in self.tickers}

        # For each ticker in the strategy
        for ticker in self.tickers:
            # Check if we have OHLCV data available for this ticker
            if ticker in data["ohlcv"]:
                # Extract the closing price of the most recent data point
                close_price = data["ohlcv"][-1][ticker]["close"]
                # If the closing price is above $10, set allocation for this ticker to 1 (100%)
                if close_price > 10:
                    allocation_dict[ticker] = 1
                    
        # Return the target allocation based on the above logic
        return TargetAllocation(allocation_dict)