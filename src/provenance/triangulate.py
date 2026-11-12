"""T2: cross-source triangulation. Standard library only.

Two sources reporting the same quantity should move together. They are in different
currencies and fiscal bases, so levels are not compared and no exchange rate is used:
the year-on-year proportional change (v[y] / v[y-1] - 1) is unit-free. A year-pair is
clean when the two changes differ by at most `tolerance`; score = clean / comparable.

mode="level" compares the values directly and is ONLY meaningful for dimensionless
inputs (e.g. from ratio_series); on currency amounts it would compare incomparable units.
Level mode exists because change mode is blind to a constant-ratio disagreement.
tolerance defaults per mode: 0.15 (change), 0.05 (level).

No counterpart (b is None), a counterpart from the same source (not independent), or no
comparable year-pair all return testable=False, score=None. Never a clean score.
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult

TOLERANCE = 0.15          # change mode: proportional-change gap
LEVEL_TOLERANCE = 0.05    # level mode: 5 percentage points, set a priori (see sweep test)


def _changes(s: IndicatorSeries) -> dict[int, float]:
    """Proportional change into each year whose own and previous-year values are present
    (previous year consecutive and non-zero)."""
    by_year = dict(zip(s.years, s.values))
    out = {}
    for y, v in by_year.items():
        prev = by_year.get(y - 1)
        if v is not None and prev is not None and prev != 0:
            out[y] = v / prev - 1.0
    return out


def _levels(s: IndicatorSeries) -> dict[int, float]:
    return {y: v for y, v in zip(s.years, s.values) if v is not None}


def ratio_series(numerator: IndicatorSeries, denominator: IndicatorSeries, *,
                 key: str, label: str) -> IndicatorSeries:
    """Dimensionless series (num - den) / num per year; None where either side is absent
    or num is zero. Both inputs must share the same years (as series from one loader do)."""
    if numerator.years != denominator.years:
        raise ValueError("ratio_series needs identical years on both inputs")
    vals = [(n - d) / n if n not in (None, 0) and d is not None else None
            for n, d in zip(numerator.values, denominator.values)]
    return IndicatorSeries(key, label, list(numerator.years), vals, numerator.source)


def triangulate_score(a: IndicatorSeries, b: IndicatorSeries | None, *,
                      mode: str = "change", tolerance: float | None = None) -> TestResult:
    if mode not in ("change", "level"):
        raise ValueError(f"mode must be 'change' or 'level', not {mode!r}")
    if tolerance is None:
        tolerance = TOLERANCE if mode == "change" else LEVEL_TOLERANCE
    if b is None:
        return TestResult(None, False, {"reason": "no counterpart", "changes": {}, "agree": []})
    if a.source == b.source:
        return TestResult(None, False, {"reason": "same source, not independent",
                                        "changes": {}, "agree": []})
    ca, cb = (_changes(a), _changes(b)) if mode == "change" else (_levels(a), _levels(b))
    years = sorted(set(ca) & set(cb))
    changes = {y: (ca[y], cb[y]) for y in years}
    agree = [y for y in years if abs(ca[y] - cb[y]) <= tolerance]
    detail = {"changes": changes, "agree": agree}
    if not years:
        return TestResult(None, False, {**detail, "reason": "no comparable year-pair"})
    return TestResult(len(agree) / len(years), True, detail)
