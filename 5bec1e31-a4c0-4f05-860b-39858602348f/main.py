
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import BankPrimeLoanRate
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Defining our asset of interest
        self.ticker = "SPY"
        # Define the data sources we need: Bank Prime Loan Rate and historical data for our asset
        self.data_list = [BankPrimeLoanRate()]

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

        # Check if we have both RSI and bank loan rate data to proceed
        if "ohlcv" in data and ("bank_prime_loan_rate") in data:
            # Calculate RSI for the asset
            rsi_values = RSI(self.ticker, data['ohlcv'], length=14)  # Using a common RSI lookback period of 14 days

            # Check if the latest RSI value is greater than 5 and we also have the bank loan rate available
            if rsi_values and rsi_values[-1] > 5 and len(data[("bank_prime_loan_rate")]) > 0:
                # Log the decision
                log(f"Buying {self.ticker} - RSI is greater than 5 and bank prime loan rate is available.")
                # Allocate 100% of the portfolio to the specified ticker
                allocation_dict[self.ticker] = 1
            else:
                # Log the decision
                log(f"Not buying {self.ticker} - RSI not greater than 5 or bank prime loan rate data not available.")

        return TargetAllocation(allocation_dict)
