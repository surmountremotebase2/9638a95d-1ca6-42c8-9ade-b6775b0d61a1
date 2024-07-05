from surmount.base_class import Strategy, TargetAllocation
from surmount.data import EffectiveFederalFundsRate, CivilianUnemployment

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset(s) to trade
        self.tickers = ["AAPL"]
        # Add necessary data sources: federal funds rate and unemployment rate
        self.data_list = [EffectiveFederalFundsRate(), CivilianUnemployment()]

    @property
    def interval(self):
        # The only intervals allowed for the provided data are 1min, 5min, 1hour, 4hour, 1day
        # Since we're dealing with macroeconomic indicators, a daily frequency is the most appropriate
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {"AAPL": 0}
        
        # Check if we have data for both indicators
        if ("effective_federal_funds_rate",) in data and ("civilian_unemployment",) in data:
            # Latest effective federal funds rate and unemployment data
            latest_fed_rate = data[("effective_federal_funds_rate",)][-1]["value"]
            latest_unemployment = data[("civilian_unemployment",)][-1]["value"]
            
            # Sample logic for buying/selling based on economic indicators
            if latest_fed_rate < 1.0 or latest_unemployment > 5.0:
                # Conditions suggest a buying opportunity (expansionary monetary policy or higher unemployment)
                allocation_dict["AAPL"] = 1
            elif latest_fed_rate > 2.0 or latest_unemployment < 4.0:
                # Conditions suggest selling or reducing holdings (contractionary monetary policy or lower unemployment)
                allocation_dict["AAPL"] = 0
            # Adjust the thresholds above as per the strategy's risk and expectation criteria
        
        return Target///////////////////////////////////////////////////////////////////////////