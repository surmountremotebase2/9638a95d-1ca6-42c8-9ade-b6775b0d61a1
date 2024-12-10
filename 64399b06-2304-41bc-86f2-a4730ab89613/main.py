from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from .get_holdings import get_initial_holdings, get_recent_trades, get_tickers
import datetime
import requests
import pandas as pd

class TradingStrategy(Strategy):
    first_run = True
    curr_holdings = {}
    last_valid_date = "2022-02-18"

    @property
    def assets(self):
        return get_tickers()
    
    @property
    def interval(self):
      return "1day"

    def run(self, data):
        if self.first_run:
            holdings = get_initial_holdings()
            self.curr_holdings = holdings
            self.first_run = False
            return self.curr_holdings
        else:
            try:
                new_date = data["ohlcv"][-1]["TSLA"]["date"]
            except:
                new_date = datetime.datetime.strptime(self.last_valid_date, "%Y-%m-%d")
                new_date = new_date + datetime.timedelta(days=1)
                new_date = datetime.datetime.strftime(new_date, "%Y-%m-%d")
                self.last_valid_date = new_date
                
            holding_changes = get_recent_trades(new_date)
        
            if holding_changes:
                for key, value in holding_changes.items():
                    new_value = self.curr_holdings.get(key, 0.0)
                    new_value += value
                    self.curr_holdings[key] = new_value
                return TargetAllocation(self.curr_holdings)
            else:
                return None