
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import Slope, RSI
from surmount.data import VOLUME
from surmount.logging import log


class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ['KO', 'PEP']
        self.data_list = [VOLUME('AAPL')]

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        holdings = data["holdings"]
        data_ohlcv = data["ohlcv"]
        resultant = {}

        first_value_0 = RSI(data=data_ohlcv, length=21, ticker="KO")
        second_value_0 = RSI(data=data_ohlcv, length=21, ticker="PEP")
        if first_value_0 and second_value_0:
            condition_0 = (first_value_0[-1] < second_value_0[-1])
        else:
            condition_0 = False
        condition = condition_0

        if condition:
            allocation = {"KO": 0.25, "PEP": 0.75}
        else:
            allocation = {"PEP": 0.25, "KO": 0.75}
        resultant = {**resultant, **allocation}

        log(f"Allocating {resultant}")

        return TargetAllocation(resultant)
