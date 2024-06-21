from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.technical_indicators import SMA, Slope
from surmount.data import TP
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        self.interval = "1day"
        self.assets = ["AAPL"]
        self.data_AAPL = {
            "average_target_price": TP("AAPL"),
            "sma_10": SMA("AAPL",list(self.data_AAPL.values()), length=10),
            "slope_3": Slope("AAPL",list(self.data_AAPL.values()), length=3)
        }
    
    @property
    def interval(self):
        return self._interval
    
    @interval.setter
    def interval(self, value):
        self._interval = value
    
    @property
    def assets(self):
        return self._assets
    
    @assets.setter
    def assets(self, value):
        self._assets = value
    
    @property
    def data(self):
        return list(self.data_AAPL.values())

    def run(self, data):
        # Fetch the latest values for indicators
        average_target_price = self.data_AAPL["average_target_price"][-1]
        sma_10 = self.data_AAPL["sma_10"][-1]
        slope_3 = self.data_AAPL["slope_3"][-1]
        
        if average_target_price is None or sma_10 is None or slope_3 is None:
            return None  # Skip if any data is missing
        
        # First condition: average_target_price < sma_10
        condition_1 = average_target_price < sma_10

        # Second condition: slope_3 < 0
        condition_2 = slope_3 < 0

        # Combined condition with AND operator
        if condition_1 and condition_2:
            # if_action: allocate 100% to AAPL
            return TargetAllocation({"AAPL": 1.0})
        else:
            # else_action: allocate 10% to AAPL
            return TargetAllocation({"AAPL": 0.1})

# Backtesting the strategy
start = datetime.strptime("2020-11-16", '%Y-%m-%d')
end = datetime.strptime("2022-11-16", '%Y-%m-%d')
initial_cash = 1000

backtest_results = backtest(TradingStrategy(), start, end, initial_cash)

print(backtest_results['stats'])
