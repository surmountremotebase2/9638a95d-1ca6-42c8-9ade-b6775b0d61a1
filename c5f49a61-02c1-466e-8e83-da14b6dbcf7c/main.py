from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):

   @property
   def assets(self):
      return ["ORCL"]

   @property
   def interval(self):
      return "1hour"

   def run(self, data):
      d = data["ohlcv"]
      qqq_stake = 0
      if len(d)>3 and "13:00" in d[-1]["ORCL"]["date"]:
         v_shape = d[-2]["ORCL"]["close"]<d[-3]["ORCL"]["close"] and d[-1]["ORCL"]["close"]>d[-2]["ORCL"]["close"]
         log(str(v_shape))
         if v_shape:
            qqq_stake = 1

      return TargetAllocation({"ORCL": qqq_stake})
