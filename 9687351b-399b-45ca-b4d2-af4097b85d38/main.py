from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Trackers for AAPL and Gold prices.
        self.tickers = ["AAPL", "GOLD"]
        # Assuming GOLD is a placeholder for actual gold price data.
        # This should be replaced with the correct symbol or method of fetching gold prices.
        self.data_list = [Asset("AAPL"), Asset("GOLD")]

    @property
    def interval(self):
        # Daily price check.
        return "1day"

    @property
    def assets(self):
        # Focusing on trading AAPL.
        return ["AAPL"]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Default allocation when there is not enough data.
        allocation_dict = {"AAPL": 0.5}

        try:
            gold_prices = [i["GOLD"]["close"] for i in data["ohlcv"]]
            # Compare the last two closing prices of gold to decide on AAPL allocation.
            if len(gold_prices) >= 2:
                if gold_prices[-1] > gold_prices[-2]:
                    # If gold price increased, allocate more to AAPL (risk-off sentiment).
                    allocation_dict["AAPL"] = 0.7
                else:
                    # If gold price decreased, allocate less to AAPL (risk-on sentiment).
                    allocation_dict["AAPL"] = 0.3
        except KeyError as e:
            log(f"Data missing for analysis: {e}")

        return TargetAllocation(allocation_dict)