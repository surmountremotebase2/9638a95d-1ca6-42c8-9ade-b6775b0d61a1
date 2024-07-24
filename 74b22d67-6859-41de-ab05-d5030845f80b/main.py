from surmount.base_class import Strategy, TargetAllocation
from surmount.data import GoldPrice

class TradingStrategy(Strategy):
    def __init__(self):
        # Use AAPL as the asset for trading
        self.ticker = "AAPL"
        # Include GoldPrice in the data list for accessing gold price data
        self.data_list = [GoldPrice()]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Default to no change in allocation
        allocation_dict = {self.ticker: 0.5}  # Start with a neutral (50%) allocation

        gold_prices = data[("gold_price",)]  # Access gold price data

        if len(gold_prices) > 1:
            # Compare the latest two day's closing prices
            latest_price = gold_prices[-1]['value']
            previous_price = gold_prices[-2]['value']

            price_change_percent = ((latest
            _price - previous_price) / previous_price) * 100

            # Define strategy to adjust AAPL allocation
            if price_change_percent > 1:
                # Gold price increased significantly, potentially reduce AAPL position
                allocation_dict[self.ticker] = 0.3  # Reduce AAPL allocation
            elif price_change_percent < -1:
                # Gold price decreased significantly, potential to increase AAPL position
                allocation_dict[self.ticker] = 0.7  # Increase AAPL allocation

        return TargetAllocation(allocation_dict)