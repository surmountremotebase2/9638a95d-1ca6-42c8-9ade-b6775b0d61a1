from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from datetime import datetime, time

class TradingStrategy(Strategy):
    """
    Intraday trading strategy for QQQ:
      - Trades TQQQ if QQQ breaks above the day's high (first 45 min),
      - Trades SQQQ if QQQ breaks below the day's low (first 45 min),
      - 1% profit target,
      - Possible flip to the opposite symbol if the original breakout fails,
      - End-of-day exit at 3:59 PM,
      - Max one TQQQ trade and one SQQQ trade per day.
    """

    def __init__(self):
        super().__init__()
        # State variables to track intraday logic
        self.current_day = None
        self.day_high = None
        self.day_low = None
        self.position = None           # "TQQQ", "SQQQ", or None
        self.entry_price = 0.0
        self.traded_tqqq = False       # Have we already traded TQQQ today?
        self.traded_sqqq = False       # Have we already traded SQQQ today?
        self.day_high_low_locked = False  # Once 10:15 passes, lock day_high & day_low

    @property
    def assets(self):
        """
        We need QQQ for the breakout signals, 
        and TQQQ / SQQQ are the ETFs we actually trade.
        """
        return ["QQQ", "TQQQ", "SQQQ"]

    @property
    def interval(self):
        """
        Surmount must support a 1-minute (or at least intraday) interval
        for this strategy to work as intended.
        """
        return "1min"

    def run(self, data):
        # Ensure we have at least one bar of data
        if len(data["ohlcv"]) < 1:
            return TargetAllocation({QQQ:0.5})