from __future__ import annotations

from typing import Dict, List


class ReasoningEngine:
	def __init__(self) -> None:
		pass

	def explain(self, symbol: str, components: Dict[str, float]) -> List[str]:
		reasons: List[str] = []
		if components.get("momentum", 0) > 0:
			reasons.append("Positive momentum vs peers")
		if components.get("trend", 0) > 0:
			reasons.append("Price above medium-term trend")
		if components.get("rsi_alignment", 0) > 0:
			reasons.append("RSI near neutral implying room to run")
		if components.get("risk_adj_momo", 0) > 0:
			reasons.append("Momentum adjusted for volatility is favorable")
		if components.get("fundamentals", 0) > 0:
			reasons.append("Fundamental quality positive")
		if components.get("sentiment", 0) > 0:
			reasons.append("Sentiment supportive")
		if components.get("options_flow", 0) > 0:
			reasons.append("Options flow bullish")
		if components.get("institution", 0) > 0:
			reasons.append("Institutional accumulation")
		if components.get("insider", 0) > 0:
			reasons.append("Insider alignment")
		return reasons or ["Mixed signals"]