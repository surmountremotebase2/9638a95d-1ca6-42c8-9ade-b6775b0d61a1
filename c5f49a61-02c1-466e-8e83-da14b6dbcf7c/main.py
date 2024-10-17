from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):

   @property
   def assets(self):
      return ["NOK"]

   @property
   def interval(self):
      return "1min"

   def run(self, data):
      d = data["ohlcv"]
      qqq_stake = 0
      if len(d)>3 and "13:00" in d[-1]["NOK"]["date"]:
         v_shape = d[-2]["NOK"]["close"]<d[-3]["NOK"]["close"] and d[-1]["NOK"]["close"]>d[-2]["NOK"]["close"]
         log(str(v_shape))
         if v_shape:
            qqq_stake = 1
      else:
         log("zero allocation")

      return TargetAllocation({"NOK": qqq_stake})
