from surmount.base_class import Strategy, TargetAllocation
from surmount.data import FiveYearBreakevenInflationRate
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]
        self.data_list = [FiveYearBreakevenInflationRate()]
    
    @property
    def interval(self):
        return "1day"
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return self.data_list
    
    def run(self, data):
        allocation_dict = {ticker: 0.5 for ticker in self.tickers}
        
        log(str(data.keys()))
        inflation_data = data[("5year_breakeven_inflation_rate",)]
        if not inflation_data:
            log("No inflation data available")
            return TargetAllocation(allocation_dict)
        
        latest_inflation_rate = inflation_data[-1]["value"]
        log(f"Latest 5-year breakeven inflation rate: {latest_inflation_rate}")
        
        high_inflation_threshold = 2.0
        low_inflation_threshold = 1.5

        if latest_inflation_rate > high_inflation_threshold:
            allocation_dict["SPY"] = 0.7
            allocation_dict["QQQ"] = 0.3
            log("High inflation: Allocating more to SPY")
        elif latest_inflation_rate < low_inflation_threshold:
            allocation_dict["SPY"] = 0.3
            allocation_dict["QQQ"] = 0.7
            log("Low inflation: Allocating more to QQQ")
        
        return TargetAllocation(allocation_dict)
