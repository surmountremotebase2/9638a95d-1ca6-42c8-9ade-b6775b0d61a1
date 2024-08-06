
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import BankPrimeLoanRate,CboeNasdaqHundredVolatilityIndex
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Defining our asset of interest
        self.ticker = "SPY"
        # Define the data sources we need: Bank Prime Loan Rate and historical data for our asset
        self.data_list = [BankPrimeLoanRate(), CboeNasdaqHundredVolatilityIndex()]

    @property
    def interval(self):
        # Setting our data interval to daily for this strategy
        return "1day"

    @property
    def assets(self):
        # Specifying the assets we're interested in (in this case, just our one ticker)
        return [self.ticker]

    @property
    def data(self):
        # Defining the data required for running this strategy
        return self.data_list

    def run(self, data):
        # Initializing allocation with no investment
        allocation_dict = {self.ticker: 0}
        log(str(data[("cboe_nasdaq_hundred_volatility_index")][-1]))

        return TargetAllocation(allocation_dict)
