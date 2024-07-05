from surmount.base_class import Strategy, TargetAllocation
from surmount.data import BankPrimeLoanRate, CivilianUnemployment
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker we are interested in.
        self.ticker = "AAPL"
        # Add the data sources we need to the data_list.
        self.data_list = [BankPrimeLoanRate(), CivilianUnemployment()]

    @property
    def interval(self):
        # Economic data does not change throughout the day so '1day' is sufficient.
        return "1day"

    @property
import pandas as pd
from datetime import datetime
from surmount.data import BankPrimeLoanRate, CivilianUnemployment, Asset, ExecutiveComp, FinancialStatement, InstitutionalOwnership, InsiderTrading, Ratios, SocialSentiment, Dividend
from surmount.logging import log
from surmount.base_class import Strategy, TargetAllocation

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        self.data_list = [BankPrimeLoanRate(), CivilianUnemployment()]
    
    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"
    
    @property
def assets(self):
        # Specify the assets that this strategy is interested in.
        return [self.ticker]

    @property
    def data(self):
        # Return the data required for this strategy.
        return self.data_list

    def run(self, data):
        # Initialize allocation to 0; no action by default.
        allocation_dict = {self.ticker: 0}

        # Extract the most recent data for interest rates and unemployment.
        latest_prime_rate = data[("bank_prime_loan_rate",)][-1]['value']
        latest_unemployment_rate = data[("civilian_unemployment",)][-1]['value']

        # Decision making based on economic indicators.
        # Buy logic: Lower interest rates and decreasing unemployment might signal a strong economy, positive for stocks.
        if latest_prime_rate < 5.0 and latest_unemployment_rate < 5.0:
            allocation_dict[self.ticker] = 1  # Full allocation to buy
            log("Buy AAPL: prime rate and unemployment signal positive economic conditions.")

        # Sell logic: Higher interest rates and increasing unemployment might signal a weakening economy, negative for stocks.
        elif latest_prime_rate > 5.0 and latest_unemployment_rate > 5.0:
            allocation_dict[self.ticker] = -1  # Full allocation to sell
            log("Sell AAPL: prime rate and unemployment signal negative economic conditions.")

        # Return the decided allocation.
        return TargetAllocation(allocation_dict)