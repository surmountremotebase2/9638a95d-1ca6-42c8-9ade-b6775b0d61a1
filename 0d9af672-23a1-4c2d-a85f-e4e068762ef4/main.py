from surmount.base_class import Strategy, TargetAllocation
from surmount.data import CryptoAltRanking
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.data_list = [CryptoAltRanking()]  # ensures exchange_name='coinbase'
        self.tickers = []
        self.counter = 0

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
        self.counter += 1
        if self.counter % 30 != 1:
            return TargetAllocation({})

        crypto_rankings = data[("coinbase_crypto_alt_ranking",)]  # or ("kraken_crypto_alt_ranking",)
        if not isinstance(crypto_rankings, list) or len(crypto_rankings) < 5:
            return TargetAllocation({})

        exclude = {"APE", "SUI", "REZ"}
        alt_rank_history = {}

        # Guard against strings or malformed entries
        for day_data in crypto_rankings[-30:]:
            if not isinstance(day_data, dict) or "alt_ranking" not in day_data:
                continue
            for coin, rank in day_data["alt_ranking"].items():
                if coin in exclude:
                    continue
                alt_rank_history.setdefault(coin, []).append(rank)

        average_ranks = []
        for coin, ranks in alt_rank_history.items():
            if len(ranks) == 30:
                average_ranks.append((coin, sum(ranks) / len(ranks)))

        top_n = 5
        top = sorted(average_ranks, key=lambda x: x[1])[:top_n]
        if not top:
            return TargetAllocation({})

        allocation = {}
        self.tickers = []
        for coin, _ in top:
            symbol = coin + "USD"
            allocation[symbol] = 1 / len(top)
            self.tickers.append(symbol)

        return TargetAllocation(allocation)