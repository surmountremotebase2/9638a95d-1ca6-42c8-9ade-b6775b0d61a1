from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership, Dividend, InsiderTrading
from datetime import datetime, timedelta

class TradingStrategy(Strategy):

   def __init__(self):
      self.tickers = ["KO", "PEP", "NSRGY", "ADM", "BG", "SYY", "SJM", "K", "MKC", "CPB", "HRL", "CAG", "GIS", "INGR", "AWK", "FIW", "CWT", "YORW", "MSEX", "SJW", "PCT", "SPY", "DHR", "VEOEY"]
      self.weights = [0.065, 0.065 , 0.065 , 0.055, 0.055, 0.045, 0.045, 0.045, 0.045, 0.035, 0.035, 0.035, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.0125, 0.0125, 0.0150, 0.0150, 0.0150, 0.0150]
      self.equal_weighting = False
      self.count = 0

   @property
   def interval(self):
      return "1day"

   @property
   def assets(self):
      return self.tickers

   def run(self, data):
      self.count += 1
      if (self.count%30 == 1):
         if self.equal_weighting: 
            allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
         else:
            allocation_dict = {self.tickers[i]: self.weights[i] for i in range(len(self.tickers))} 
         return TargetAllocation(allocation_dict)
      return None