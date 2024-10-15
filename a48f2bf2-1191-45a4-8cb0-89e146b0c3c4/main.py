from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Strategy applies to MSFT
        return ["MSFT"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]
        
        #for i in range(len(data)):
        #    data[i]["MSFT"]["open"] = data[i]["MSFT"]["close"]
        
      
        if len(data) < 12:
            # There isn't enough data to calculate Bollinger Bands
            # log("Not enough data to calculate Bollinger Bands")
            return TargetAllocation({})

        MSFT_stake = holdings.get("MSFT", 0)
        MSFT_bbands = BB("MSFT", data, 12, 1.5)
        current_price = data[-1]["MSFT"]['close']  # Current price of MSFT

        # log(f" {current_price}  {MSFT_bbands['lower'][-1]}   {MSFT_bbands['mid'][-1]}")

        # Buying condition: the price falls below the lower Bollinger Band
        if MSFT_stake ==0 and current_price < MSFT_bbands['lower'][-1]:
            # log(f"Buying MSFT - price below lower Bollinger Band. Current price: {current_price}")
            MSFT_stake = 1  # Buy MSFT
        # Selling condition: the price moves above the middle Bollinger Band
        if MSFT_stake >0 and current_price > MSFT_bbands['mid'][-1]:
            # log(f"Closing MSFT - price above middle Bollinger Band. Current price: {current_price}")
            MSFT_stake = 0  # Exit position in MSFT

        return TargetAllocation({"MSFT": MSFT_stake})