from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


def generate_synthetic_features(seed: int = 42, periods: int = 60) -> pd.DataFrame:
	rng = np.random.default_rng(seed)
	steps = rng.normal(loc=0.001, scale=0.02, size=periods).astype(float)
	price = 100 * np.exp(np.cumsum(steps))
	volume = rng.integers(low=1_000_000, high=5_000_000, size=periods)
	index = pd.date_range(end=pd.Timestamp.utcnow().normalize(), periods=periods, freq="B")
	df = pd.DataFrame({
		"open": price * (1 + rng.normal(0, 0.002, size=periods)),
		"high": price * (1 + rng.normal(0.002, 0.004, size=periods)),
		"low": price * (1 - rng.normal(0.002, 0.004, size=periods)),
		"close": price,
		"volume": volume,
	}, index=index)
	df["return_1d"] = df["close"].pct_change()
	df["return_5d"] = df["close"].pct_change(5)
	df["sma_20"] = df["close"].rolling(20).mean()
	df["sma_50"] = df["close"].rolling(50).mean()
	df["rsi_14"] = _compute_rsi(df["close"], 14)
	return df.dropna().tail(60)


def _compute_rsi(series: pd.Series, length: int) -> pd.Series:
	delta = series.diff()
	gain = (delta.where(delta > 0, 0)).rolling(length).mean()
	loss = (-delta.where(delta < 0, 0)).rolling(length).mean()
	rs = gain / (loss.replace(0, 1e-9))
	return 100 - (100 / (1 + rs))