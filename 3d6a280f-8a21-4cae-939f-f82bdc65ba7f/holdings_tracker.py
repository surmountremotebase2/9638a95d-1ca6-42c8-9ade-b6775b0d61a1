from datetime import datetime

possible_tickers = [
    "AAPL",
    "V",
    "MSFT",
    "UNH",
    "TMUS",
    "CB",
    "GOOG",
    "MOH",
    "JPM",
    "HD",
    "SCHW",
    "TSLA",
    "TMO",
    "MMC",
    "DHR",
    "ACN",
    "DG",
    "AMZN",
    "NVDA",
    "XOM",
    "BRK.B",
    "CRM"
]

holdings = {
    "2022-07-31": {
        "MSFT": .22,
        "AAPL": .19,
        "GOOG": .12,
        "AMZN": .12,
        "TSLA": .075,
        "UNH": .05,
        "NVDA": .05,
        "V": .039,
        "BRK.B": .039,
        "CRM": .039,    
    },
    "2023-01-31": {
        "MSFT": .19,
        "AAPL": .18,
        "GOOG": .09,
        "AMZN": .081,
        "XOM": .055,
        "NVDA": .06,
        "UNH": .05,
        "V": .039,
        "BRK.B": .039,
        "CRM": .039
    }
}

def get_holdings(date):
    return holdings.get(date, None)