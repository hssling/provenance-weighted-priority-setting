"""Data model and WHO CSV loaders. Standard library only.

Absent values (blank or "NA") load as None; a reported "0" loads as 0.0.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
BUDGET_CSV = DATA_DIR / "TB_budget_2026-11-12.csv"
EXP_CSV = DATA_DIR / "TB_expenditure_utilisation_2026-08-25.csv"

_ABSENT = {"", "NA"}
_ID_COLUMNS = {"country", "iso2", "iso3", "iso_numeric", "g_whoregion", "year"}

# series key -> {component name: source column} for identity-testable lines
BUDGET_COMPONENTS = {
    "budget_tpt": {"unit_cost": "budget_cpp_tpt", "volume": "tx_tpt"},
}
EXP_COMPONENTS: dict[str, dict[str, str]] = {}


@dataclass
class IndicatorSeries:
    key: str
    label: str
    years: list[int]
    values: list[float | None]
    source: str
    notes: dict[int, str] = field(default_factory=dict)
    components: dict[str, list[float | None]] = field(default_factory=dict)


@dataclass(frozen=True)
class TestResult:
    score: float | None      # None when not testable. Otherwise in [0.0, 1.0], 1.0 = clean
    testable: bool
    detail: dict             # test-specific evidence, e.g. {year: ratio}

    __test__ = False  # not a pytest test class

    def __post_init__(self):
        if not self.testable:
            if self.score is not None:
                raise ValueError("score must be None when testable is False")
        else:
            if self.score is None:
                raise ValueError("score is required when testable is True")
            if not 0.0 <= self.score <= 1.0:
                raise ValueError(f"score {self.score} outside [0, 1]")


def _parse(raw: str | None) -> float | None:
    if raw is None:
        return None
    raw = raw.strip()
    if raw in _ABSENT:
        return None
    return float(raw)


def _load(path: Path, iso3: str, components: dict[str, dict[str, str]],
          source: str) -> dict[str, IndicatorSeries]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        columns = [c for c in (reader.fieldnames or []) if c not in _ID_COLUMNS]
        rows = sorted((r for r in reader if r["iso3"] == iso3),
                      key=lambda r: int(r["year"]))
    if not rows:
        return {}
    years = [int(r["year"]) for r in rows]
    cols = {c: [_parse(r[c]) for r in rows] for c in columns}
    out = {}
    for c in columns:
        comp = {name: list(cols[src]) for name, src in components.get(c, {}).items() if src in cols}
        out[c] = IndicatorSeries(c, c, list(years), list(cols[c]), source, {}, comp)
    return out


def load_who_budget(path: Path, iso3: str) -> dict[str, IndicatorSeries]:
    return _load(Path(path), iso3, BUDGET_COMPONENTS, "WHO TB budget")


def load_who_expenditure(path: Path, iso3: str) -> dict[str, IndicatorSeries]:
    return _load(Path(path), iso3, EXP_COMPONENTS, "WHO TB expenditure and utilisation")
