# Github-Example
New project 

## Agentic Stocks (experimental)

- Install deps: `pip3 install -r requirements.txt`
- CLI recommend: `python3 -m agentic_stocks recommend --limit 10`
- Run API: `./scripts/dev.sh` then POST to `/recommend` with `{ "symbols": ["AAPL"], "limit": 10 }`

This system learns weights over time by recording recommendations and updating them after a short horizon.


