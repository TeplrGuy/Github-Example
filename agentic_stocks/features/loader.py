from __future__ import annotations

from typing import Dict, List

import pandas as pd
import yfinance as yf

from agentic_stocks.features.offline import generate_synthetic_features


class FeatureLoader:
	def load_features(self, symbols: List[str]) -> Dict[str, pd.DataFrame]:
		data: Dict[str, pd.DataFrame] = {}
		for i, s in enumerate(symbols):
			try:
				tkr = yf.Ticker(s)
				hist = tkr.history(period="6mo", interval="1d")
				if hist.empty:
					raise ValueError("empty history")
				hist = hist.rename(columns=str.lower)
				hist = hist[["open", "high", "low", "close", "volume"]].copy()
				hist["return_1d"] = hist["close"].pct_change()
				hist["return_5d"] = hist["close"].pct_change(5)
				hist["sma_20"] = hist["close"].rolling(20).mean()
				hist["sma_50"] = hist["close"].rolling(50).mean()
				hist["rsi_14"] = self._compute_rsi(hist["close"], 14)
				data[s] = hist.dropna().tail(60)
			except Exception:
				data[s] = generate_synthetic_features(seed=42 + i)
		return data

	def _compute_rsi(self, series: pd.Series, length: int) -> pd.Series:
		delta = series.diff()
		gain = (delta.where(delta > 0, 0)).rolling(length).mean()
		loss = (-delta.where(delta < 0, 0)).rolling(length).mean()
		rs = gain / (loss.replace(0, 1e-9))
		return 100 - (100 / (1 + rs))