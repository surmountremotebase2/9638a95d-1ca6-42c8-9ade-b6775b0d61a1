from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker for which the strategy will be applied
        self.ticker = "SPY"
        # Initialize any other necessary variables or data lists here

    @property
    def assets(self):
        # Return a list of assets this strategy will handle
        return [self.ticker]

    @property
    def interval(self):
        # Define the time interval for the strategy, such as "1day" for daily strategy execution
        return "1day"
    
    def run(self, data):
        # Implement the strategy's logic to be executed by the trading system
        allocation_dict = {}
        # Calculate the RSI for the designated asset
        rsi_list = RSI(self.ticker, data["ohlcv"], length=14)  # RSI with a period of 14 days is commonly used
        
        if not rsi_list or len(rsi_list) == 0:
            # In case there's an issue with fetching the RSI data, log the occurrence and do not allocate any funds
            log("No RSI data available for {}".format(self.ticker))
            allocation_dict[self.ticker] = 0
        else:
            current_rsi = rsi_list[-1]  # Get the most recent RSI value
            if current_rsi > 60:
                # If the RSI is above 60, allocate a full position to SPY
                log("Current RSI ({}) is above 60, buying {}".format(current_rsi, self.ticker))
                allocation_dict[self.ticker] = 1  # Allocate 100% of the portfolio to SPY
            else:
                # If the RSI is not above 60, do not allocate any funds to SPY
                log("Current RSI ({}) is not above 60, not buying {}".format(current_rsi, self.ticker))
                allocation_dict[self.ticker] = 0

        # Return the target allocation. Note that the total allocation must be between 0 and 1 inclusive.
        return TargetAllocation(allocation_dict)