from surmount.base_class import Strategy, TargetAllocation
from surmount.data import EffectiveFederalFundsRate, CivilianUnemployment

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        # Adding the interest rate and unemployment data to the data list.
        self.data_list = [EffectiveFederalFundsRate(), CivilianUnemployment()]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize the allocation for AAPL to zero.
        allocation_dict = {"AAPL": 0}

        # Extract the latest values for interest rates and unemployment.
        interest_rate_data = data[("effective_federal_funds_rate",)]
        unemployment_data = data[("civilian_unemployment",)]

        if interest_rate_data and unemployment_data:
            # Get the most recent data points.
            latest_interest_rate = interest_rate_data[-1]['value']
            latest_unemployment = unemployment_data[-1]['value']

            # Decision logic: Increase AAPL allocation if interest rates rise or unemployment falls.
            if latest_interest_rate > interest_rate_data[-2]['value'] or latest_unemployment < unemployment_data[-2]['value']:
                allocation_dict["AAPL"] = 1  # Buy or maintain position in AAPL.
            else:
                allocation_dict["AAPL"] = 0.5  # Sell or reduce position in AAPL, indicating caution.

        return TargetAllocation(allocation_dict)