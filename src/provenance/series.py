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

_LINES = ("lab", "staff", "fld", "prog", "sld", "mdrmgt", "tpt", "tbhiv", "patsup", "orsrvy", "oth")
_SOURCES = ("domestic", "gf", "usaid", "grnt")


def _sum_of(prefix: str) -> tuple[str, dict[str, str]]:
    cols = [f"{prefix}_{x}" for x in _LINES]
    return "sum", {c: c for c in cols}


# series key -> (identity, {component name: source column}).
# "product": the series equals unit_cost * volume. "sum": it equals the sum of its parts.
# A synthetic key (not a CSV column) is declared in _SYNTHETIC as key -> underlying column.
BUDGET_IDENTITIES = {
    "budget_tpt": ("product", {"unit_cost": "budget_cpp_tpt", "volume": "tx_tpt"}),
    "budget_tot": _sum_of("budget"),
    "cf_tot": _sum_of("cf"),
}
EXP_IDENTITIES = {
    "exp_tot": _sum_of("exp"),
    "rcvd_tot": _sum_of("rcvd"),
    "rcvd_tot_by_source": ("sum", {f"rcvd_tot_{x}": f"rcvd_tot_{x}" for x in _SOURCES}),
}
_SYNTHETIC = {"rcvd_tot_by_source": "rcvd_tot"}


@dataclass
class IndicatorSeries:
    key: str
    label: str
    years: list[int]
    values: list[float | None]
    source: str
    notes: dict[int, str] = field(default_factory=dict)
    components: dict[str, list[float | None]] = field(default_factory=dict)
    identity: str | None = None  # "product" | "sum" | None; appended last, keep it last


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


def _load(path: Path, iso3: str, identities: dict[str, tuple[str, dict[str, str]]],
          source: str) -> dict[str, IndicatorSeries]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        columns = [c for c in (reader.fieldnames or []) if c not in _ID_COLUMNS]
        rows = sorted((r for r in reader if r["iso3"] == iso3),
                      key=lambda r: int(r["year"]))
    # Fail loudly on a mistyped/missing mapped column, even for a country with no rows.
    for key, (_, parts) in identities.items():
        needed = list(parts.values()) + [_SYNTHETIC.get(key, key)]
        for col in needed:
            if col not in columns:
                raise ValueError(f"{path}: identity for series {key!r} needs column {col!r}, which is missing")
    if not rows:
        return {}
    years = [int(r["year"]) for r in rows]
    cols = {c: [_parse(r[c]) for r in rows] for c in columns}
    out = {}
    for key in list(columns) + list(_SYNTHETIC):
        if key in _SYNTHETIC and key not in identities:
            continue
        identity, parts = identities.get(key, (None, {}))
        comp = {name: list(cols[src]) for name, src in parts.items()}
        values = cols[_SYNTHETIC.get(key, key)]
        out[key] = IndicatorSeries(key, key, list(years), list(values), source, {}, comp, identity)
    return out


def load_who_budget(path: Path, iso3: str) -> dict[str, IndicatorSeries]:
    return _load(Path(path), iso3, BUDGET_IDENTITIES, "WHO TB budget")


def load_who_expenditure(path: Path, iso3: str) -> dict[str, IndicatorSeries]:
    return _load(Path(path), iso3, EXP_IDENTITIES, "WHO TB expenditure and utilisation")
