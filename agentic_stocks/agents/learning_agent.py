from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

import yfinance as yf

from agentic_stocks.models.blender import SignalBlender
from agentic_stocks.storage.state import StateStore


class LearningAgent:
	def __init__(self, blender: SignalBlender, state_path: str = "storage/state.json") -> None:
		self.blender = blender
		self.state = StateStore(state_path)

	def record_recommendations(self, symbols: List[str]) -> None:
		st = self.state.load()
		today = datetime.utcnow().date()
		for sym in symbols:
			st["pending"].append({
				"symbol": sym,
				"date": today.isoformat(),
			})
		self.state.save(st)

	def evaluate_and_learn(self) -> Dict[str, float]:
		st = self.state.load()
		pending = st.get("pending", [])
		if not pending:
			return {}

		cutoff = datetime.utcnow().date() - timedelta(days=5)
		to_score = [p for p in pending if datetime.fromisoformat(p["date"]).date() <= cutoff]

		realized: Dict[str, float] = {}
		for p in to_score:
			sym = p["symbol"]
			tkr = yf.Ticker(sym)
			df = tkr.history(period="1mo", interval="1d")
			if df.empty:
				continue
			start_idx = df.index.get_loc(min(df.index[-1], df.index[-6]))
			end_idx = df.index.get_loc(df.index[-1])
			start_price = float(df["Close"].iloc[start_idx])
			end_price = float(df["Close"].iloc[end_idx])
			ret = (end_price - start_price) / start_price
			realized[sym] = ret

		# Remove evaluated from pending
		st["pending"] = [p for p in pending if p not in to_score]
		self.state.save(st)
		return realized

	def learn_from_market(self, signals: Dict[str, Dict[str, float]]) -> None:
		realized = self.evaluate_and_learn()
		if not realized:
			return
		self.blender.update_weights_from_outcomes(realized, signals)
		self.state.append_weights_snapshot(self.blender.learned_weights)