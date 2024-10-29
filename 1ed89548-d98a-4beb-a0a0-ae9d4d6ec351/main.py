from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from statistics import stdev
from surmount.technical_indicators import SMA

class TradingStrategy(Strategy):

    @property
    def assets(self):
        # Define the assets we will be trading
        return ["KO", "PEP", "SPY", "TQQQ"]

    @property
    def interval(self):
        # Set the trading interval to daily
        return "1day"
    def run(self, data):
        # Ensure we have enough data to calculate the ratio
        if len(data["ohlcv"]) < 4:
            return TargetAllocation({})
        
        # Extract the latest closing prices for KO and PEP
        ko_price = data["ohlcv"][-1]["KO"]["close"]
        pep_price = data["ohlcv"][-1]["PEP"]["close"]

        # Calculate the price ratio of KO to PEP over the available data
        ratio = [data["ohlcv"][i]["KO"]["close"] / data["ohlcv"][i]["PEP"]["close"] for i in range(len(data["ohlcv"]))]
        mean = sum(ratio) / len(ratio)
        dev = stdev(ratio)

        # Default allocations
        ko_stake = 0
        pep_stake = 0
        spy_stake = 0.8
        tqqq_stake = 0.2

        # Adjust allocations based on the ratio deviation from the mean
        if ratio[-1] > mean + dev / 1.2:
            ko_stake = 0
            pep_stake = 0.85
            spy_stake = 0.1
            tqqq_stake = 0.05
        elif ratio[-1] < mean - dev / 1.2:
            ko_stake = 0.85
            pep_stake = 0
            spy_stake = 0.1
            tqqq_stake = 0.05

        # Calculate moving averages for SPY
        ma = SMA("SPY", data["ohlcv"], 20)
        if ma:
            ma = ma[-1]
        else:
            return TargetAllocation({})

        ma2 = SMA("SPY", data["ohlcv"], 32)
        if ma2:
            ma2 = ma2[-1]
        else:
            return TargetAllocation({})

        # Further adjust allocations based on the moving averages
        if ma < 0.99 * ma2:
            ko_stake /= 3
            pep_stake /= 3
            spy_stake = 0.3
            tqqq_stake = 0.1
            if ma < 0.98 * ma2:
                spy_stake = 0.2
                tqqq_stake = 0.3

        # Return the target allocation
        return TargetAllocation({"KO": ko_stake, "PEP": pep_stake, "SPY": spy_stake, "TQQQ": tqqq_stake})