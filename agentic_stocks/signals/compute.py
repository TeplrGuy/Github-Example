from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


class SignalComputer:
	def compute_signals(self, features: Dict[str, pd.DataFrame], horizon_days: int = 5) -> Dict[str, Dict[str, float]]:
		signals: Dict[str, Dict[str, float]] = {}
		for symbol, df in features.items():
			latest = df.iloc[-1]
			momentum = float(df["close"].pct_change(horizon_days).iloc[-1])
			trend = float((latest["sma_20"] - latest["sma_50"]) / (latest["sma_50"] + 1e-9))
			rsi = float(1 - abs(latest["rsi_14"] - 50) / 50)
			volatility = float(df["return_1d"].std() * np.sqrt(252))
			risk_adjusted_momo = momentum / (volatility + 1e-9)

			fundamentals = 0.0
			sentiment = 0.0
			options_flow = 0.0
			institution = 0.0
			insider = 0.0

			signals[symbol] = {
				"momentum": momentum,
				"trend": trend,
				"rsi_alignment": rsi,
				"risk_adj_momo": risk_adjusted_momo,
				"fundamentals": fundamentals,
				"sentiment": sentiment,
				"options_flow": options_flow,
				"institution": institution,
				"insider": insider,
			}
		return signals