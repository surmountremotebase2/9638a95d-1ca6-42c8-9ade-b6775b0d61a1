from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, RSI
from surmount.data import IndustriesPERatio
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        self.data_list = [IndustriesPERatio("S&P 500 Basic Materials")]

    @property
    def interval(self):
        # Daily data provides enough insight for this strategy.
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}

        aapl_macd = MACD("AAPL", data["ohlcv"], 12, 26)
        aapl_rsi = RSI("AAPL", data["ohlcv"], 14)
        pe_ratio_data = data[("industries_pe_ratio", "S&P 500 Basic Materials")]

        if aapl_macd and aapl_rsi and pe_ratio_data:
            current_pe_ratio = pe_ratio_data[-1]["pe"] if pe_ratio_data else None
            macd_signal_cross = aapl_macd["MACD"][-1] > aapl_macd["signal"][-1]
            not_overbought = aapl_rsi[-1] < 70 and aapl_rsi[-1] > 50
            healthy_market_sentiment = current_pe_ratio < 18  # Example threshold

            if macd_signal_cross and not_overbought and healthy_market_sentiment:
                allocation_dict["AAPL"] = 1.0  # Full investment signal
            else:
                allocation_dict["AAPL"] = 0.0  # Exit signal

        return TargetAllocation(allocation_dict)