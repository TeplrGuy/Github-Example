from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


class SignalBlender:
	def __init__(self) -> None:
		self.learned_weights: Dict[str, float] = {
			"momentum": 0.25,
			"trend": 0.15,
			"rsi_alignment": 0.10,
			"risk_adj_momo": 0.20,
			"fundamentals": 0.15,
			"sentiment": 0.05,
			"options_flow": 0.05,
			"institution": 0.03,
			"insider": 0.02,
		}

	def blend(self, signals: Dict[str, Dict[str, float]]) -> List[Tuple[str, float, Dict[str, float]]]:
		if not signals:
			return []

		# Z-score normalize each signal across the universe
		keys = list(next(iter(signals.values())).keys())
		matrix = {k: [] for k in keys}
		for _, s in signals.items():
			for k in keys:
				matrix[k].append(float(s.get(k, 0.0)))

		stats: Dict[str, Tuple[float, float]] = {}
		for k, arr in matrix.items():
			v = np.array(arr, dtype=float)
			mu = v.mean() if v.size else 0.0
			sigma = v.std() + 1e-9
			stats[k] = (mu, sigma)

		blended: List[Tuple[str, float, Dict[str, float]]] = []
		for symbol, s in signals.items():
			normed: Dict[str, float] = {k: (float(s.get(k, 0.0)) - stats[k][0]) / stats[k][1] for k in keys}
			score = float(sum(self.learned_weights.get(k, 0.0) * normed[k] for k in keys))
			blended.append((symbol, score, normed))

		blended.sort(key=lambda x: x[1], reverse=True)
		return blended

	def update_weights_from_outcomes(self, realized_returns: Dict[str, float], signals: Dict[str, Dict[str, float]], lr: float = 0.01) -> None:
		if not realized_returns:
			return
		keys = list(self.learned_weights.keys())
		for symbol, outcome in realized_returns.items():
			if symbol not in signals:
				continue
			x = np.array([signals[symbol].get(k, 0.0) for k in keys], dtype=float)
			pred = float(sum(self.learned_weights[k] * x[i] for i, k in enumerate(keys)))
			err = outcome - pred
			for i, k in enumerate(keys):
				self.learned_weights[k] += lr * err * x[i]