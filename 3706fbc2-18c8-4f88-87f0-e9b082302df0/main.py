from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, Slope
from surmount.data import VOLUME

from surmount.logging import log


class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ['TQQQ', 'AAPL']
        self.data_list = [VOLUME('AAPL')]

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        holdings = data["holdings"]
        data_ohlcv = data["ohlcv"]
        log(str(data.keys()))
        resultant = {}

        first_value_0 = RSI(data=data, length=21, ticker="TQQQ")
        second_value_0 = 50
        if first_value_0 and second_value_0:
            condition_0 = (first_value_0[-1] > second_value_0)
        else:
            condition_0 = False
        first_value_1 = Slope(data=data, length=3, ticker="TQQQ")
        second_value_1 = 0
        if first_value_1 and second_value_1:
            condition_1 = (first_value_1[-1] < second_value_1)
        else:
            condition_1 = False
        condition = condition_0 and condition_1

        if condition:
            allocation = {"TQQQ": 1.0}
        else:
            allocation = {"TQQQ": 0.1}
        resultant = {**resultant, **allocation}

        first_value_0 = data[('volume', 'AAPL')][-1]['value']
        second_value_0 = 100000
        if first_value_0 and second_value_0:
            condition_0 = (first_value_0[-1] < second_value_0)
        else:
            condition_0 = False
        condition = condition_0

        if condition:
            allocation = {"AAPL": 0.5, "TQQQ": 0.5}
        else:
            allocation = {}
        resultant = {**resultant, **allocation}

        return TargetAllocation(allocation)