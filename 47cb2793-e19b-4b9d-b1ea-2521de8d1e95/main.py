from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from datetime import datetime
import datetime as dt

possible_tickers = [
    "AAPL", "V", "MSFT", "UNH", "TMUS", "CB", "GOOG", "MOH", "JPM", "HD",
    "SCHW", "TSLA", "TMO", "MMC", "DHR", "ACN", "DG", "AMZN", "NVDA",
    "XOM", "BRK.B", "CRM"
]

holdings = {
    "2022-07-31": {
        "MSFT": .22, "AAPL": .19, "GOOG": .12, "AMZN": .12, "TSLA": .075,
        "UNH": .05, "NVDA": .05, "V": .039, "BRK.B": .039, "CRM": .039,
    },
    "2023-01-31": {
        "MSFT": .19, "AAPL": .18, "GOOG": .09, "AMZN": .081, "XOM": .055,
        "NVDA": .06, "UNH": .05, "V": .039, "BRK.B": .039, "CRM": .039
    }
}

def get_holdings(date):
    return holdings.get(date, None)


class TradingStrategy(Strategy):
    first_run = True
    last_valid_date = "2022-02-18"

    @property
    def assets(self):
        return possible_tickers

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        if self.first_run:
            holdings_data = get_holdings("2022-07-31")
            self.first_run = False
        else:
            try:
                date = data["ohlcv"][-1]["TSLA"]["date"][0:10]
                self.last_valid_date = date
                holdings_data = get_holdings(date)
            except IndexError:
                new_date = datetime.strptime(self.last_valid_date, "%Y-%m-%d")
                new_date = new_date + dt.timedelta(days=1)
                new_date = datetime.strftime(new_date, "%Y-%m-%d")
                self.last_valid_date = new_date
                holdings_data = get_holdings(self.last_valid_date)

        if holdings_data:
            return TargetAllocation(holdings_data)
        else:
            return None