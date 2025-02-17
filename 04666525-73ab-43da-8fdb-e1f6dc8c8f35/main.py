
from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import GDPAllCountries, CivilianUnemployment, CryptoAltRanking
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        # Add GDP and Unemployment data to the data_list
        self.data_list = [GDPAllCountries(), CivilianUnemployment(), CryptoAltRanking()]

    @property
    def interval(self):
        # Use daily data as economic indicators do not update more frequently
        return "1day"

    @property
    def assets(self):
        # We are only trading AAPL based on economic indicators
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {"AAPL": 0}  # Default to no position
        gdp_data = data[("gdp_by_country",)]
        unemployment_data = data[("civilian_unemployment",)]
        alt_ranking_data = data[("crypto_alt_ranking",)]
        log(f"here: {str(data)}")
        print(f"here: {str(data.keys())}")
        print(f"gdp: {str(len(gdp_data))}")
        print(f"unemployment_data: {str(len(unemployment_data))}")
        print(f"alt_ranking_data: {str(alt_ranking_data)}")


        # Determine the recent trends in GDP and Unemployment Rate
        if len(gdp_data) > 1 and len(unemployment_data) > 1:
            latest_gdp_growth = gdp_data[-1]["value"] - gdp_data[-2]["value"]
            latest_unemployment_change = unemployment_data[-1]["value"] - unemployment_data[-2]["value"]

            # GDP is growing, and stable or decreasing, buy AAPL
            if latest_gdp_growth > 0 and latest_unemployment_change <= 0:
                allocation_dict["AAPL"] = 1  # Full allocation to AAPL
            # If unemployment rises, sell AAPL (or avoid buying)
            elif latest_unemployment_change > 0:
                allocation_dict["AAPL"] = 0  # No position in AAPL
                
            log(f"Latest GDP Growth: {latest_gdp_growth}, Latest Unemployment Change: {latest_unemployment_change}")

        return TargetAllocation(allocation_dict)