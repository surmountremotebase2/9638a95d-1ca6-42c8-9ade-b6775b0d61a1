from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import LeveredDCF, EarningsSurprises, EarningsCalendar, AnalystEstimates
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]

        # Build data sources for each ticker
        self.data_list = []
        for ticker in self.tickers:
            self.data_list.extend([
                LeveredDCF(ticker),
                EarningsSurprises(ticker),
                EarningsCalendar(ticker),
                AnalystEstimates(ticker)
            ])

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
        allocation = {}

        for ticker in self.tickers:
            # Levered DCF
            levered_dcf = data.get(("levered_dcf", ticker))
            if levered_dcf:
                log(f"{ticker} LeveredDCF: {levered_dcf[-1]}")

            # Earnings Surprises
            earnings_surprises = data.get(("earnings_surprises", ticker))
            if earnings_surprises:
                log(f"{ticker} EarningsSurprises: {earnings_surprises[-1]}")

            # Earnings Calendar
            earnings_calendar = data.get(("earnings_calendar", ticker))
            if earnings_calendar:
                log(f"{ticker} EarningsCalendar: {earnings_calendar[-1]}")

            # Analyst Estimates
            analyst_estimates = data.get(("analyst_estimates", ticker))
            if analyst_estimates:
                log(f"{ticker} AnalystEstimates: {analyst_estimates[0]}")

            allocation[ticker] = 1 / len(self.tickers)

        return TargetAllocation(allocation)
