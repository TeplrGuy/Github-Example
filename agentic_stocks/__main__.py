import argparse
from typing import List

from agentic_stocks.agents.recommender_agent import AgenticRecommender


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Agentic Stocks Recommender")
	subparsers = parser.add_subparsers(dest="command")

	rec = subparsers.add_parser("recommend", help="Generate stock recommendations")
	rec.add_argument("--symbols", nargs="*", default=[], help="Optional list of symbols")
	rec.add_argument("--limit", type=int, default=10, help="Max results")
	rec.add_argument("--horizon-days", type=int, default=5, help="Evaluation horizon in days")
	rec.add_argument("--scan-source", choices=["sp500", "nasdaq100", "all_us"], default="sp500", help="Market scan source when symbols not provided")
	rec.add_argument("--scan-limit", type=int, default=200, help="Maximum symbols to scan when symbols not provided")

	api = subparsers.add_parser("api", help="Run FastAPI server")
	api.add_argument("--host", default="0.0.0.0")
	api.add_argument("--port", type=int, default=8080)

	return parser.parse_args()


def main() -> None:
	args = parse_args()
	if args.command == "api":
		import uvicorn
		uvicorn.run("agentic_stocks.api.server:app", host=args.host, port=args.port, reload=False)
		return

	agent = AgenticRecommender()
	if args.command == "recommend":
		symbols: List[str] = [s.upper() for s in args.symbols]
		result = agent.recommend(
			symbols=symbols or None,
			limit=args.limit,
			horizon_days=args.horizon_days,
			scan_source=args.scan_source,
			scan_limit=args.scan_limit,
		)
		for idx, r in enumerate(result["recommendations"], start=1):
			print(f"{idx:>2d}. {r['symbol']:<6} score={r['blended_score']:.3f} reasons={r['reasons']}")
		return

	print("No command provided. Use 'recommend' or 'api'.")


if __name__ == "__main__":
	main()