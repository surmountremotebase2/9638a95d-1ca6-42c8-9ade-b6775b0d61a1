from surmount.base_class import Strategy, TargetAllocation
from surmount.data import *
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]
        self.data_list = [GDPAllCountries()]
    
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
        log(str(VOLUME('PEP').get_data()[-1]["date"]))

        # Access the GDP data by country
        #log(str(data.keys()))
        gdp_data = data[("gdp_by_country",)]
        
        if not gdp_data:
         #   log("No GDP data available")
            return TargetAllocation(allocation_dict)
        
        # Filter for the latest United States GDP data
        us_gdp_data = [entry for entry in gdp_data if entry["country"] == "United States"]
        if not us_gdp_data:
         #   log("No US GDP data available")
            return TargetAllocation(allocation_dict)
        
        latest_us_gdp = us_gdp_data[-1]["date"]

        log(f"Latest US GDP: {latest_us_gdp}")
        
        # Define the GDP threshold for high and low GDP
        high_gdp_threshold = 20000000000000  # Example threshold
        low_gdp_threshold = 18000000000000   # Example threshold
        
        # Trading logic: Adjust allocation based on GDP
        if latest_us_gdp > high_gdp_threshold:
            # High GDP scenario: More allocation to SPY, less to QQQ
            allocation_dict["SPY"] = 0.7
            allocation_dict["QQQ"] = 0.3
         #   log("High GDP: Allocating more to SPY")
        elif latest_us_gdp < low_gdp_threshold:
            # Low GDP scenario: More allocation to QQQ, less to SPY
            allocation_dict["SPY"] = 0.3
            allocation_dict["QQQ"] = 0.7
          #  log("Low GDP: Allocating more to QQQ")
        
        return TargetAllocation(allocation_dict)
