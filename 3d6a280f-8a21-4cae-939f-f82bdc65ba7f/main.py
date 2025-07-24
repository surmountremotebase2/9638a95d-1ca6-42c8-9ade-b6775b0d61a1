from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from .holdings_tracker import get_holdings, possible_tickers
import datetime

class TradingStrategy(Strategy):
    first_run = True
    last_valid_date = "2022-02-18"

    @property
    def assets(self):
        return possible_tickers
    
    @property
    def interval(self):
      return "1day"

    def run(self, data):
        if self.first_run:
            holdings = get_holdings("2022-07-31")
            self.first_run = False
        else:
            try:
                date = data["ohlcv"][-1]["TSLA"]["date"][0:10]
                self.last_valid_date = date
                holdings = get_holdings(date)
            except IndexError:
                new_date = datetime.datetime.strptime(self.last_valid_date, "%Y-%m-%d")
                new_date = new_date + datetime.timedelta(days=1)
                new_date = datetime.datetime.strftime(new_date, "%Y-%m-%d")
                self.last_valid_date = new_date
                holdings = get_holdings(self.last_valid_date)
        
        if holdings:
            return TargetAllocation(holdings)
        else:
            return None