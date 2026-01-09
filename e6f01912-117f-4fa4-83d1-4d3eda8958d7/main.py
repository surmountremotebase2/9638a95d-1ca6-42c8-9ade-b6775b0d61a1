from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import LeveredDCF, EarningsSurprises, EarningsCalendar, AnalystEstimates
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Test all four data sources
        self.tickers = ["AAPL"]
        self.data_list = [
            LeveredDCF("AAPL"),
            EarningsSurprises("AAPL"),
            EarningsCalendar("AAPL"),
            AnalystEstimates("AAPL")
        ]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list


    def run(self, data):
        # Test LeveredDCF
        levered_dcf = data.get(("levered_dcf", "AAPL"))
        if levered_dcf:
            log(f"LeveredDCF data: {levered_dcf[-1] if levered_dcf else 'No data'}")

        # Test EarningsSurprises
        earnings_surprises = data.get(("earnings_surprises", "AAPL"))
        if earnings_surprises:
            log(f"EarningsSurprises data: {earnings_surprises[-1] if earnings_surprises else 'No data'}")

        # Test EarningsCalendar
        earnings_calendar = data.get(("earnings_calendar", "AAPL"))
        if earnings_calendar:
            log(f"EarningsCalendar data: {earnings_calendar[-1] if earnings_calendar else 'No data'}")

        # Test AnalystEstimates
        analyst_estimates = data.get(("analyst_estimates", "AAPL"))
        if analyst_estimates:
            log(f"AnalystEstimates data: {analyst_estimates[-1] if analyst_estimates else 'No data'}")

        return TargetAllocation({"AAPL": 1})

    