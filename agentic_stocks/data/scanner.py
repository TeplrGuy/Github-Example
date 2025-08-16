from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

import pandas as pd
import requests

from agentic_stocks.data.universe import DEFAULT_UNIVERSE


class MarketScanner:
	def __init__(self) -> None:
		pass

	def scan(
		self,
		source: str = "sp500",
		limit: Optional[int] = None,
		min_price: float = 1.0,
		min_avg_volume: int = 200_000,
	) -> List[str]:
		try:
			if source == "sp500":
				syms = self._scan_sp500()
			elif source == "nasdaq100":
				syms = self._scan_nasdaq100()
			elif source == "all_us":
				syms = self._scan_all_us()
			else:
				syms = DEFAULT_UNIVERSE.copy()
			syms = self._normalize_symbols(syms)
			syms = list(dict.fromkeys(syms))
			if limit:
				syms = syms[: int(limit)]
			return syms
		except Exception:
			return DEFAULT_UNIVERSE.copy()

	def _scan_sp500(self) -> List[str]:
		url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
		dfs = pd.read_html(url)
		for df in dfs:
			cols = {c.lower(): c for c in df.columns}
			if "symbol" in cols:
				return [str(x).strip() for x in df[cols["symbol"]].tolist() if x]
		return DEFAULT_UNIVERSE.copy()

	def _scan_nasdaq100(self) -> List[str]:
		url = "https://en.wikipedia.org/wiki/NASDAQ-100"
		dfs = pd.read_html(url)
		for df in dfs:
			lower_cols = [str(c).lower() for c in df.columns]
			if any("ticker" in c or "symbol" in c for c in lower_cols):
				col_candidates = [c for c in df.columns if str(c).lower() in ("ticker", "symbol")]
				col = col_candidates[0]
				return [str(x).strip() for x in df[col].tolist() if x]
		return DEFAULT_UNIVERSE.copy()

	def _scan_all_us(self) -> List[str]:
		url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"
		r = requests.get(url, timeout=10)
		r.raise_for_status()
		content = r.text
		df = pd.read_csv(pd.compat.StringIO(content), sep="|")
		df = df[df["Test Issue"] == "N"]
		df = df[df["ETF"] == "N"]
		df = df[df["NASDAQ Symbol"].notna()]
		syms = df["NASDAQ Symbol"].astype(str).tolist()
		return syms

	def _normalize_symbols(self, symbols: Iterable[str]) -> List[str]:
		result: List[str] = []
		for s in symbols:
			ss = s.strip().upper()
			ss = ss.replace(".", "-")
			if ss and all(c.isalnum() or c == "-" for c in ss):
				result.append(ss)
		return result