from surmount.base_class import Strategy, TargetAllocation

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers (assets) the strategy will concern itself with
        self.tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]

    @property
    def assets(self):
        # Return the list of tickers this strategy is concerned with
        return self.tickers

    @property
    def interval(self):
        # Define how frequently the strategy should be run; '1day' means once per day
        return "1day"

    def run(self, data):
        # This method is called to determine the allocation across the defined assets
        # A neutral 'do nothing' strategy means allocating 0 for each asset
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        # Return the allocation dict wrapped in a TargetAllocation object
        return TargetAllocation(allocation_dict)