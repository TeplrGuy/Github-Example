from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict


class StateStore:
	def __init__(self, path: str) -> None:
		self.path = path
		os.makedirs(os.path.dirname(self.path), exist_ok=True)
		if not os.path.exists(self.path):
			self._initialize()

	def _initialize(self) -> None:
		init_state = {"pending": [], "history": [], "weights_history": []}
		with open(self.path, "w", encoding="utf-8") as f:
			json.dump(init_state, f)

	def load(self) -> Dict[str, Any]:
		with open(self.path, "r", encoding="utf-8") as f:
			return json.load(f)

	def save(self, state: Dict[str, Any]) -> None:
		backup_path = self.path + ".backup"
		if os.path.exists(self.path):
			try:
				os.replace(self.path, backup_path)
			except Exception:
				pass
		with open(self.path, "w", encoding="utf-8") as f:
			json.dump(state, f)

	def append_weights_snapshot(self, weights: Dict[str, float]) -> None:
		state = self.load()
		state["weights_history"].append({
			"timestamp": datetime.utcnow().isoformat(),
			"weights": weights,
		})
		self.save(state)