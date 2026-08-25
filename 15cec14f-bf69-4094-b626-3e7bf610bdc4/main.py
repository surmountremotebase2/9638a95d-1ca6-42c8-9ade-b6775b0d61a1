from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    This trading strategy aims to buy and sell SPY every minute based on the moving average trend.
    It calculates the 5-minute SMA and if the latest price is above the SMA, it buys SPY,
    and if the latest price is below the SMA, it sells SPY.
    """
    @property
    def assets(self):
        # Defines the asset(s) this strategy is interested in.
        return ["AAPL"]

    @property
    def interval(self):
        # Sets the data interval to 1 minute for high-frequency trading.
        return "1min"

    def run(self, data):
        # Main logic of the trading strategy executed every minute.
        
        # Initialize allocation dictionary with no allocation.
        allocation_dict = {"AAPL": 0}
        
        # Fetch the latest 6 minute data to calculate SMA for 5 minutes.
        recent_data = data["ohlcv"][-6:]  # Ensure we have enough data
        
        # Check if we have enough data points.
        if len(recent_data) >= 6:
            # Calculate the SMA for the last 5 minutes.
            recent_closes = [i["AAPL"]["close"] for i in recent_data]
            sma = sum(recent_closes[:-1]) / 5  # Exclude the current minute for SMA calculation
            
            # Get the latest closing price.
            latest_close = recent_closes[-1]
            
            # # Determine action based on SMA and the latest close.
            # if latest_close > sma:
            #     # If the latest price is above SMA, set allocation to buy.
            #     log("Buying SPY")
            #     allocation_dict["AAPL"] = 1
            # elif latest_close < sma:
            #     # If the latest price is below SMA, set allocation to sell.
            #     log("Selling SPY")
            #     allocation_dict["AAPL"] = -1  # Assuming the platform supports short selling.
            # else:
            #     # No action if latest price is equal to SMA.
            #     log("No action")
            if latest_close > sma:
                # If the latest price is above SMA, hold a full position.
                log("Buying AAPL")
                allocation_dict["AAPL"] = 1
            elif latest_close < sma:
                # If the latest price is below SMA, exit to cash.
                log("Selling AAPL")
                allocation_dict["AAPL"] = 0
            else:
                log("No action")

        else:
            # Log if not enough data is available.
            log("Not enough data for SMA calculation")
        
        # Return the target allocation based on the strategy logic.
        return TargetAllocation(allocation_dict)