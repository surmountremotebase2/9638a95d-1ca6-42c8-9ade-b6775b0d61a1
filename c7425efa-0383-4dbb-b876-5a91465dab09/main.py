from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    A trading strategy that aims to buy AAPL when its RSI is below 30,
    indicating that it might be oversold and potentially set for a rebound.
    """
    
    @property
    def assets(self):
        # Define the stock tickers you're interested in – in this case, AAPL
        return ["AAPL"]
    
    @property
    def interval(self):
        # Define the time interval to be 1 day for this strategy
        return "1day"
    
    def run(self, data):
        """
        The core method of the strategy where the trading logic is implemented.
        """
        # Initialize AAPL's stake at 0
        aapl_stake = 0
        
        # Calculate the RSI for AAPL
        rsi = RSI("AAPL", data["ohlcv"], length=14)  # A common period for RSI is 14 days
        
        if rsi:
            log(f"Current AAPL RSI: {rsi[-1]}")  # Log the latest RSI value
            
            # Check if the latest RSI value is below 30
            if rsi[-1] < 30:
                log("AAPL RSI below 30 - buying signal!")
                aapl_stake = 1  # Update AAPL's stake to indicate a buying position
            else:
                log("AAPL does not meet buying criteria.")
        else:
            log("RSI calculation failed.")
        
        # Return the target allocation as per our strategy's decision
        return TargetAllocation({"AAPL": aapl_stake})