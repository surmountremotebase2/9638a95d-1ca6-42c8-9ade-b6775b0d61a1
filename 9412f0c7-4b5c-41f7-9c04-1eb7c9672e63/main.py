from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, BB
from surmount.data import Asset, SocialSentiment, InsiderTrading, Volume
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "RKLB"
        self.data_list = [
            SocialSentiment(self.ticker),
            InsiderTrading(self.ticker)
        ]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        sentiment_data = data[("social_sentiment", self.ticker)]
        insider_data = data[("insider_trading", self.ticker)]
        ohlcv_data = data["ohlcv"]

        # Initialize allocation to 0, indicating no investment initially
        allocation = 0

        # Strategy Logic
        # 1. Check if the latest market sentiment is positive (>0.9) which indicates high confidence
        # 2. Check for any recent insider sales which might indicate a lack of confidence by insiders
        if sentiment_data and sentiment_data[-1]["twitterSentiment"] > 0.9:
            has_recent_insider_sales = any(
                trade for trade in insider_data if trade["transactionType"].lower() == "sale"
            )
            if not has_recent_insider_sales:
                # Calculate minor dip using RSI & Bollinger Bands
                if len(ohlcv_data) > 14:  # Ensure there's enough data for RSI calculation
                    rsi = RSI(self.ticker, ohlcv_data, length=14)
                    bb = BB(self.ticker, ohlcv_data, length=20, std=2)
                    current_price = ohlcv_data[-1][self.ticker]['close']
                    if rsi and bb:
                        # Criteria for a 'Buy' signal: RSI below 30 (oversold) and price near lower Bollinger Band
                        if rsi[-1] < 30 and current_price <= bb["lower"][-1]:
                            allocation = 1  # Maximal investment in RKLB due to high confidence in its rise

        # Log reasoning
        log(f"Investment decision for {self.ticker}: {'Invest Full' if allocation else 'Hold/Do not Invest'}")

        return TargetAllocation({self.ticker: allocation})