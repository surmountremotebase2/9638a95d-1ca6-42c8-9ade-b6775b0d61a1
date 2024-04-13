from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["BTC", "ETH", "LTC", "XRP"]  # Example cryptocurrency tickers. Adjust accordingly.

    @property
    def interval(self):
        return "1day"  # Daily timeframe for analysis.

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return []

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            macd_signal = MACD(ticker, data["ohlcv"], 12, 26)
            if macd_signal is not None:
                # Check if MACD line crosses above the signal line, indicating a potential upward momentum.
                if len(macd_signal["MACD"]) > 1 and macd_signal["MACD"][-1] > macd_signal["signal"][-1] and macd_signal["MACD"][-2] < macd_signal["signal"][-2]:
                    allocation_dict[ticker] = 1 / len([t for t in self.tickers if t in allocation_dict]) if ticker not in allocation_dict else allocation_dict[ticker]
                else:
                    allocation_dict[ticker] = 0
            else:
                # If no MACD signal is available, no allocation to this ticker.
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)