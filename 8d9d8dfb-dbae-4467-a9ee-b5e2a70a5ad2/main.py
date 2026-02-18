from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.logging import log
from surmount.data import (
    NDWFirstTrustFocusFive,
    NDWPowerSeven,
    NDWSectorFour,
    NDWPowerSmall,
    NDWISharesTactical,
    NDWFirstTrustInternational,
    NDWPowrShares,
)
from surmount.data_client import SurmountDataClient
from datetime import datetime


def _get_tickers(model_symbol):
    """Fetch current allocation to determine which tickers the model trades."""
    client = SurmountDataClient()
    allocation = client.get_ndw_model_allocation(model_symbol)
    if isinstance(allocation, list) and len(allocation) > 0:
        return list(allocation[0]["allocations"].keys())
    return []


def _build_target(ndw_data, key, tickers):
    """Extract latest allocation from NDW data and return TargetAllocation."""
    records = ndw_data.get(key)
    if not records or len(records) == 0:
        return None
    latest = records[-1]
    allocations = latest.get("allocations", {})
    valid = {k: v for k, v in allocations.items() if k in tickers}
    total = sum(valid.values())
    if total == 0:
        return None
    return TargetAllocation({k: v / total for k, v in valid.items()})


# ============================================================================
# FTRUST5 — First Trust Focus Five (Bi-weekly rebalance)
# ============================================================================

class NDWFirstTrustFocusFiveStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("FTRUST5")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWFirstTrustFocusFive()]

    def run(self, data):
        return _build_target(data, ("ndw_ftrust5",), self.tickers)


# ============================================================================
# POWER7 — Invesco Sector Seven (Weekly rebalance)
# ============================================================================

class NDWPowerSevenStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("POWER7")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWPowerSeven()]

    def run(self, data):
        return _build_target(data, ("ndw_power7",), self.tickers)


# ============================================================================
# POWER4 — NDW Sector 4 (Monthly rebalance)
# ============================================================================

class NDWSectorFourStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("POWER4")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWSectorFour()]

    def run(self, data):
        return _build_target(data, ("ndw_power4",), self.tickers)


# ============================================================================
# POWERSMALL — Invesco Small Cap Sector (Weekly rebalance)
# ============================================================================

class NDWPowerSmallStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("POWERSMALL")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWPowerSmall()]

    def run(self, data):
        return _build_target(data, ("ndw_powersmall",), self.tickers)


# ============================================================================
# ISHRTACTICAL — iShares Tactical (Weekly rebalance)
# ============================================================================

class NDWISharesTacticalStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("ISHRTACTICAL")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWISharesTactical()]

    def run(self, data):
        return _build_target(data, ("ndw_ishrtactical",), self.tickers)


# ============================================================================
# FTRUSTINTL — First Trust International (Bi-weekly rebalance)
# ============================================================================

class NDWFirstTrustInternationalStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("FTRUSTINTL")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWFirstTrustInternational()]

    def run(self, data):
        return _build_target(data, ("ndw_ftrustintl",), self.tickers)


# ============================================================================
# POWRSHARES — Invesco Commodity (Weekly rebalance)
# ============================================================================

class NDWPowrSharesStrategy(Strategy):
    def __init__(self):
        self.tickers = _get_tickers("POWRSHARES")

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [NDWPowrShares()]

    def run(self, data):
        return _build_target(data, ("ndw_powrshares",), self.tickers)


# ============================================================================
# Run backtests
# ============================================================================

if __name__ == "__main__":
    start = datetime.strptime("2021-11-16", "%Y-%m-%d")
    end = datetime.strptime("2022-11-16", "%Y-%m-%d")
    initial_capital = 10000

    strategies = [
        ("FTRUST5  - First Trust Focus Five",      NDWFirstTrustFocusFiveStrategy),
        ("POWER7   - Invesco Sector Seven",         NDWPowerSevenStrategy),
        ("POWER4   - NDW Sector 4",                 NDWSectorFourStrategy),
        ("POWERSMALL - Invesco Small Cap",          NDWPowerSmallStrategy),
        ("ISHRTACTICAL - iShares Tactical",         NDWISharesTacticalStrategy),
        ("FTRUSTINTL - First Trust International",  NDWFirstTrustInternationalStrategy),
        ("POWRSHARES - Invesco Commodity",          NDWPowrSharesStrategy),
    ]

    for name, StrategyClass in strategies:
        print(f"\n{'='*60}")
        print(f"Running backtest: {name}")
        print(f"{'='*60}")
        try:
            result = backtest(StrategyClass(), start, end, initial_capital)
            print(result["stats"])
        except Exception as e:
            print(f"Error: {e}")
