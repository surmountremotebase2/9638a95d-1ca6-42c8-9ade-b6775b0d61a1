from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker for SPY
        self.ticker = "SPY"
        # No additional data lists are needed for this strategy
        self.data_list = []

    @property
    def interval(self):
        # Use daily data for finding all-time lows
        return "1day"

    @property
    def assets(self):
        # Operate only on the SPY ETF
        return [self.ticker]

    @property
    def data(self):
        # No additional data other than price is required
        return self.data_list

    def run(self, data):
        # Accessing the historical close prices of SPY
        closes = [day["SPY"]["close"] for day in data["ohlcv"]]
        
        # Check if there are any closing prices available
        if len(closes) == 0:
            log("No data available for SPY.")
            return TargetAllocation({})  # Return an empty allocation if no data is available

        # Determine the current close price and the all-time low up to now
        current_close = closes[-1]
        all_time_low = min(closes)

        # Buy SPY if the current close is at an all-time low
        # Otherwise, do not hold SPY
        if current_close <= all_time_low:
            log(f"SPY is at its all-time low of {current_close}. Buying.")
            allocation = 1.0  # Invest 100% of the portfolio in SPY
        else:
            log("SPY is not at its all-time low. Not buying.")
            allocation = 0.0  # Hold no SPY

        # Return the target allocation
        return TargetAllocation({self.ticker: allocation})