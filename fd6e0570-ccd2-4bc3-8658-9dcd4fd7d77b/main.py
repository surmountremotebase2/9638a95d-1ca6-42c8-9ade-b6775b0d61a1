from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log


class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ['KO', 'PEP']
        self.data_list = []

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
        data = data["ohlcv"]
        resultant = {}

        first_value_0 = RSI(data=data, ticker="KO")
        second_value_0 = RSI(data=data, ticker="PEP")
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

        first_value_0 = RSI(data=data, length = 21, ticker="SPY")
        second_value_0 = RSI(data=data, length = 21, ticker="MSFT")
        if first_value_0 and second_value_0:
            condition_0 = (first_value_0[-1] > second_value_0[-1])
        else:
            condition_0 = False
        condition = condition_0

        if condition:
            allocation = {"SPY": 0.5}
        else:
            allocation = {"MSFT": 0.5}
        resultant = {**resultant, **allocation}

        return TargetAllocation(allocation)