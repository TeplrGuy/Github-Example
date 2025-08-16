from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from agentic_stocks.agents.recommender_agent import AgenticRecommender


app = FastAPI(title="Agentic Stocks API", version="0.1.0")
agent = AgenticRecommender()


class RecommendRequest(BaseModel):
	symbols: Optional[List[str]] = None
	limit: int = 10
	horizon_days: int = 5
	scan_source: str = "sp500"
	scan_limit: int = 200


@app.get("/health")
def health() -> dict:
	return {"status": "ok"}


@app.post("/recommend")
def recommend(req: RecommendRequest) -> dict:
	return agent.recommend(
		symbols=req.symbols,
		limit=req.limit,
		horizon_days=req.horizon_days,
		scan_source=req.scan_source,
		scan_limit=req.scan_limit,
	)