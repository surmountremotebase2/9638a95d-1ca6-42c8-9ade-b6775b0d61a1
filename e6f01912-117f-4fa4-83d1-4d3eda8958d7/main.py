from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.data import LeveredDCF, EarningsSurprises, EarningsCalendar, AnalystEstimates
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Multiple tickers
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

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
        for ticker in self.tickers:
            # LeveredDCF
            levered_dcf = data.get(("levered_dcf", ticker))
            if levered_dcf:
                log(f"{ticker} LeveredDCF: {levered_dcf[-1]}")

            # EarningsSurprises
            earnings_surprises = data.get(("earnings_surprises", ticker))
            if earnings_surprises:
                log(f"{ticker} EarningsSurprises: {earnings_surprises[-1]}")

            # EarningsCalendar
            earnings_calendar = data.get(("earnings_calendar", ticker))
            if earnings_calendar:
                log(f"{ticker} EarningsCalendar: {earnings_calendar[-1]}")

            # AnalystEstimates
            analyst_estimates = data.get(("analyst_estimates", ticker))
            if analyst_estimates:
                log(f"{ticker} AnalystEstimates: {analyst_estimates[0]}")

        # Equal-weight allocation
        weight = 1 / len(self.tickers)
        return TargetAllocation({ticker: weight for ticker in self.tickers})
