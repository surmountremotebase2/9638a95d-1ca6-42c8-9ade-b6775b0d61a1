from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, WestTexasIntermediate

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # List of ticker symbols to be considered for the strategy
        self.data_list = [WestTexasIntermediate()]  # Gold price data is needed for the strategy
    
    @property
    def interval(self):
        # This strategy's logic will be applied on a daily basis.
        return "1day"
    
    @property
    def assets(self):
        # The assets that this strategy will make decisions on.
        return self.tickers
    
    @property
    def data(self):
        # Data used by this strategy, in this case, gold prices.
        return self.data_list

    def run(self, data):
        allocation = {}
        
        # Assuming we have gold price data in data dictionary.
        # Pretending 'WestTexasIntermediate' as a placeholder for gold price data.
        # In real application, replace it with the actual data source for gold prices.
        gold_prices = data.get(("west_texas_intermediate",), [])
        
        if len(gold_prices) < 2:
            # Not enough data to make a decision
            return TargetAllocation({})
        
        today_gold_price = gold_prices[-1]['value']
        yesterday_gold_price = gold_prices[-2]['value']
        
        # Strategy logic based on gold price movement
        if today_gold_price < yesterday_gold_price:
            # If gold price decreased, allocate more to AAPL (risk on)
            allocation["AAPL"] = 1.0  # 100% allocation
        else:
            # If gold price increased, decrease allocation in AAPL (risk off)
            allocation["AAPL"] = 0.0  # 0% allocation
        
        # Return the allocation decision
        return TargetAllocation(allocation)