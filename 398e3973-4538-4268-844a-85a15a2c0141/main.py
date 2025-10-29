from typing import Tuple, List, Dict
import numpy as np
from datetime import datetime

from surmount.base_class import Strategy, TargetAllocation, backtest


def kalman_level_trend(prices: np.ndarray, q_level: float = 1e-4, q_trend: float = 1e-5, r: float = 1e-2) -> Tuple[np.ndarray, np.ndarray]:
    """Compute Kalman level and trend for a 1D price array.

    Uses a simple local linear trend model with state [level, trend].
    """
    if prices is None or len(prices) == 0:
        return np.array([]), np.array([])

    n = len(prices)
    level = np.zeros(n)
    trend = np.zeros(n)

    P = np.eye(2) * 0.1
    x = np.array([prices[0], 0.0])
    Q = np.array([[q_level, 0.0], [0.0, q_trend]])
    R = r
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])

    for t in range(n):
        x = F @ x
        P = F @ P @ F.T + Q

        z = prices[t]
        y = z - (H @ x)
        S = H @ P @ H.T + R
        K = (P @ H.T) / S

        x = x + (K.flatten() * y)
        P = (np.eye(2) - K @ H) @ P

        level[t] = x[0]
        trend[t] = x[1]

    return level, trend


class TradingStrategy(Strategy):
    def __init__(self, trailing_stop_pct: float = 0.05,
                 q_level: float = 1e-4, q_trend: float = 1e-5, r: float = 1e-2):
        self._assets = ["ETH-USD", "BTC-USD"]
        self.trailing_stop_pct = float(trailing_stop_pct)
        self.q_level = float(q_level)
        self.q_trend = float(q_trend)
        self.r = float(r)

        # Persistent state across run() calls
        self.in_trade: bool = False
        self.entry_price: float = 0.0
        self.high_price: float = 0.0

    @property
    def interval(self) -> str:
        return "1day"

    @property
    def assets(self) -> List[str]:
        return self._assets

    def _extract_closes(self, data: List[Dict[str, Dict[str, float]]], ticker: str) -> np.ndarray:
        closes: List[float] = []
        for row in data:
            ohlcv = row.get(ticker)
            if not ohlcv:
                continue
            closes.append(float(ohlcv["close"]))
        return np.asarray(closes, dtype=float)

    def run(self, data) -> TargetAllocation:
        # Expect data["ohlcv"] to be a list of bars; we compute signals on the last bar
        ohlcv = data.get("ohlcv", [])
        if not ohlcv:
            return TargetAllocation({})

        ticker = self._assets[0]
        prices = self._extract_closes(ohlcv, self._assets[1])
        if prices.size < 3:
            return TargetAllocation({})

        level, trend = kalman_level_trend(prices, self.q_level, self.q_trend, self.r)
        last_price = prices[-1]
        last_level = level[-1]
        last_trend = trend[-1]

        base_long_signal = (last_trend > 0.0) and (last_price > last_level)

        # Update trailing stop state machine
        allocation: Dict[str, float] = {}
        if not self.in_trade:
            if base_long_signal:
                self.in_trade = True
                self.entry_price = float(last_price)
                self.high_price = float(last_price)
                allocation[ticker] = 1.0
            else:
                allocation[ticker] = 0.0
        else:
            self.high_price = float(max(self.high_price, last_price))
            stop_level = self.high_price * (1.0 - self.trailing_stop_pct)
            if last_price < stop_level:
                # Exit trade
                self.in_trade = False
                self.entry_price = 0.0
                self.high_price = 0.0
                allocation[ticker] = 0.0
            else:
                allocation[ticker] = 1.0

        return TargetAllocation(allocation)
