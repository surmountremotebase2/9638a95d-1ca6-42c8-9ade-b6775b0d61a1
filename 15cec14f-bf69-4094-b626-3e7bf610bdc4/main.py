from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log


class TradingStrategy(Strategy):
    """
    This trading strategy trades AAPL every minute based on the moving average trend.
    It calculates the 5-minute SMA; if the latest price is above the SMA it holds a
    full position in AAPL, and if the latest price is below the SMA it exits to cash.
    """

    # Single source of truth for the traded ticker.
    TICKER = "AAPL"

    @property
    def assets(self):
        # Defines the asset(s) this strategy is interested in.
        return [self.TICKER]

    @property
    def interval(self):
        # Sets the data interval to 1 minute for high-frequency trading.
        return "1"

    def run(self, data):
        # Main logic of the trading strategy executed every minute.

        # Fetch the latest 6 minutes of data to calculate the 5-minute SMA.
        recent_data = data["ohlcv"][-6:]

        # Check if we have enough data points.
        if len(recent_data) < 6:
            # Not enough history yet - hold the current position rather than liquidating.
            log("Not enough data for SMA calculation")
            return None

        # Calculate the SMA over the 5 minutes preceding the current one.
        recent_closes = [i[self.TICKER]["close"] for i in recent_data]
        sma = sum(recent_closes[:-1]) / 5

        # Get the latest closing price.
        latest_close = recent_closes[-1]

        # Determine action based on SMA and the latest close.
        if latest_close > sma:
            # Above the SMA: hold a full position.
            log(f"Buying {self.TICKER}")
            return TargetAllocation({self.TICKER: 1})

        if latest_close < sma:
            # Below the SMA: exit to cash. Allocations are portfolio weights in [0, 1] -
            # there is no short side, so "sell" means a 0% allocation.
            log(f"Selling {self.TICKER}")
            return TargetAllocation({self.TICKER: 0})

        # Exactly at the SMA - hold whatever we currently have.
        log("No action")
        return None