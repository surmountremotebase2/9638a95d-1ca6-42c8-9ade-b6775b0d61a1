from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):

   @property
   def assets(self):
      return ["SCHO"]

   @property
   def interval(self):
      return "1hour"

   def run(self, data):
      d = data["ohlcv"]
      qqq_stake = 0
      if len(d)>3 and "13:00" in d[-1]["SCHO"]["date"]:
         v_shape = d[-2]["SCHO"]["close"]<d[-3]["SCHO"]["close"] and d[-1]["SCHO"]["close"]>d[-2]["SCHO"]["close"]
         log(str(v_shape))
         if v_shape:
            qqq_stake = 1

      return TargetAllocation({"SCHO": qqq_stake})
