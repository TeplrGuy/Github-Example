from __future__ import annotations

from typing import List

DEFAULT_UNIVERSE: List[str] = [
	"AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK.B", "JPM", "V",
	"JNJ", "WMT", "MA", "XOM", "PG", "HD", "CVX", "ABBV", "BAC", "AVGO",
]


def load_universe() -> List[str]:
	return DEFAULT_UNIVERSE.copy()