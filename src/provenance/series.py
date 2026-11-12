"""Data model and WHO CSV loaders. Standard library only.

Absent values (blank or "NA") load as None; a reported "0" loads as 0.0.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
BUDGET_CSV = DATA_DIR / "TB_budget_2026-11-12.csv"
EXP_CSV = DATA_DIR / "TB_expenditure_utilisation_2026-08-25.csv"
ITR_CSV = DATA_DIR / "india_tb_report_table16_1.csv"

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
# WHO reports budget_cpp_tpt as a whole number, so the unit cost carries +-0.5 of rounding error.
_UNIT_ROUNDING = {"budget_tpt": 0.5}
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
    identity: str | None = None  # "product" | "sum" | None; keep it where it is (positional callers)
    # Half-width of the rounding applied to the product identity's unit_cost, in the unit_cost's own
    # units (0.5: reported to the nearest whole unit). None: no rounding model, flat tolerance only.
    # Declared by whoever knows how the figure was reported (the loader), never inferred from the value.
    unit_rounding: float | None = None


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
        rounding = _UNIT_ROUNDING.get(key)
        out[key] = IndicatorSeries(key, key, list(years), list(values), source, {}, comp, identity,
                                   rounding)
    return out


def load_who_budget(path: Path, iso3: str) -> dict[str, IndicatorSeries]:
    return _load(Path(path), iso3, BUDGET_IDENTITIES, "WHO TB budget")


def load_who_expenditure(path: Path, iso3: str) -> dict[str, IndicatorSeries]:
    return _load(Path(path), iso3, EXP_IDENTITIES, "WHO TB expenditure and utilisation")


_ITR_COLUMNS = (("requested", "itr_requested", "Requested"),
                ("approved", "itr_approved", "Approved"),
                ("released", "itr_released", "Released"),
                ("spent", "itr_spent", "Spent"))
_ITR_NOTES = {
    "approved": {
        2022: "Excludes cash grant released directly by NHM under the RCH Flexible Pool.",
        2023: "Excludes cash grant released directly by NHM under the RCH Flexible Pool.",
    },
    "spent": {
        2023: "As at 15.03.2024; partial year.",
    },
}


def load_india_tb_report(path: Path) -> dict[str, IndicatorSeries]:
    """India TB Report 2024, Table 16.1 (p.174). Rupees crore; fiscal years labelled by start year.

    Blank cells (e.g. released for 2022-23, not printed in the report) load as None.
    """
    path = Path(path)
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = sorted(csv.DictReader(fh), key=lambda r: int(r["year"]))
    years = [int(r["year"]) for r in rows]
    source = "India TB Report 2024, Table 16.1"
    out = {}
    for col, key, label in _ITR_COLUMNS:
        out[key] = IndicatorSeries(
            key=key,
            label=label,
            years=list(years),
            values=[_parse(r[col]) for r in rows],
            source=source,
            notes=dict(_ITR_NOTES.get(col, {})),
        )
    return out


NTEP_TRAJECTORIES_CSV = DATA_DIR.parents[1] / "tb_bopas_repo" / "data" / "ntep_trajectories.csv"

# The source repeats one note on every row of a series. Copying it onto every year would
# make every jump look "declared" and reward silent breaks, so a note is pinned only to a
# year it names as a break ("changed at 2020"). Notes naming no break year are descriptive
# of the whole series and are not turned into per-year declarations.
_BREAK_YEAR = re.compile(r"changed at (\d{4})")


def load_trajectories(path: Path) -> dict[str, IndicatorSeries]:
    """NTEP trajectories CSV (read-only) -> one IndicatorSeries per `series` value."""
    with open(Path(path), newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    grouped: dict[str, list[dict]] = {}
    for r in rows:
        grouped.setdefault(r["series"], []).append(r)
    out = {}
    for key, rs in grouped.items():
        rs.sort(key=lambda r: int(r["year"]))
        notes = {}
        for r in rs:
            m = _BREAK_YEAR.search(r["note"] or "")
            if m:
                notes[int(m.group(1))] = r["note"].strip()
        out[key] = IndicatorSeries(
            key=key, label=rs[0]["label"], years=[int(r["year"]) for r in rs],
            values=[_parse(r["value"]) for r in rs],
            source=f"NTEP trajectories ({rs[0]['who_dataset']})", notes=notes)
    return out
