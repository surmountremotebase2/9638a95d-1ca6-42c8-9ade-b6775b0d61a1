from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import BroadUSDollarIndex

class TradingStrategy(Strategy):
    def __init__(self):
        # We're interested in trading AAPL based on our proxy indicator
        self.tickers = ["AAPL"]
        # Assuming BroadUSDollarIndex as a proxy for silver's economic impact
        self.data_list = [BroadUSDollarIndex()]

    @property
    def interval(self):
        # Daily analysis
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Placeholder for trading logic based on the BroadUSDollarIndex
        # Assuming we have a hypothetical strategy that buys AAPL when
        # the dollar weakens and sells when it strengthens,
        # as a weaker dollar could mean higher silver prices,
        # potentially beneficial for companies that depend on such commodities.

        # Initialize allocation to AAPL as 0
        allocation_dict = {"AAPL": 0}

        # Sample logic to decide on allocation
        dollar_index = data[("broad_us_dollar_index", )][-1]['value']  # Most recent value
        previous_dollar_index = data[("broad_us_dollar_index", )][-2]['value']  # Previous value

        # If the dollar index is decreasing, i.e., dollar is weakening
        if dollar_index < previous_dollar_index:
            # Increase allocation to AAPL, assuming a hypothetical correlation
            allocation_dict["AAPL"] = 0.5  # 50% allocation as an example
        else:
            # Decrease or maintain low allocation to AAPL
            allocation_dict["AAPL"] = 0.1  # 10% allocation as a defensive move

        return TargetAllocation(allocation_dict)