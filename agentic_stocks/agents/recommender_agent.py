from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pandas as pd

from agentic_stocks.data.universe import load_universe
from agentic_stocks.features.loader import FeatureLoader
from agentic_stocks.signals.compute import SignalComputer
from agentic_stocks.models.blender import SignalBlender
from agentic_stocks.utils.reasoning import ReasoningEngine
from agentic_stocks.agents.learning_agent import LearningAgent


@dataclass
class Recommendation:
	symbol: str
	blended_score: float
	reasons: List[str]


class AgenticRecommender:
	def __init__(self) -> None:
		self.feature_loader = FeatureLoader()
		self.signal_computer = SignalComputer()
		self.blender = SignalBlender()
		self.reasoner = ReasoningEngine()
		self.learning_agent = LearningAgent(self.blender)

	def recommend(
		self,
		symbols: Optional[List[str]] = None,
		limit: int = 10,
		horizon_days: int = 5,
	) -> Dict[str, object]:
		universe: List[str] = symbols or load_universe()
		features: Dict[str, pd.DataFrame] = self.feature_loader.load_features(universe)
		signals: Dict[str, Dict[str, float]] = self.signal_computer.compute_signals(features, horizon_days=horizon_days)
		blended: List[Tuple[str, float, Dict[str, float]]] = self.blender.blend(signals)

		recommendations: List[Recommendation] = []
		for symbol, score, components in blended[:limit]:
			reasons = self.reasoner.explain(symbol, components)
			recommendations.append(Recommendation(symbol=symbol, blended_score=score, reasons=reasons))

		# Agentic behavior: record recs for future learning and attempt weight updates
		self.learning_agent.record_recommendations([r.symbol for r in recommendations])
		self.learning_agent.learn_from_market(signals)

		return {
			"recommendations": [r.__dict__ for r in recommendations],
			"universe_size": len(universe),
			"weights": self.blender.learned_weights,
		}