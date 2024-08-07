from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import TenYearBreakevenInflationRate

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        self.data_list = [TenYearBreakevenInflationRate()]

    @property
    def interval(self):
        # Data frequency. Using '1day' as inflation data does not update more frequently.
        return "1day"

    @property
    def assets(self):
        # The assets this strategy is interested in.
        return self.tickers

    @property
    def data(self):
        # The economic data the strategy uses to make decisions.
        return self.data_list

    def run(self, data):
        allocation_dict = {"AAPL": 0}  # Default to 0 allocation to AAPL.

        # Accessing ten-year breakeven inflation rate data.
        inflation_data_key = ("10year_breakeven_inflation_rate",)
        if inflation_data_key in data and len(data[inflation_data_key]) > 1:
            # Compare the latest two records to check if inflation expectation is rising.
            last_inflation_rate = data[inflation_data_key][-1]["value"]
            prev_inflation_rate = data[inflation_data_key][-2]["value"]

            # If inflation is expected to rise, allocate more to AAPL. The logic below is simplistic and
            # meant for demonstration. It scales the allocation based on the rate change, with a max of 0.9 allocation.
            if last_inflation_rate > prev_inflation_rate:
                rate_difference = last_inflation_rate - prev_inflation_rate
                # This simplistic scaling is arbitrary and can be replaced with a more sophisticated logic based on backtesting.
                new_allocation = min(0.9, rate_difference * 10)
                allocation_dict["AAPL"] = new_allocation

        return TargetAllocation(allocation_dict)