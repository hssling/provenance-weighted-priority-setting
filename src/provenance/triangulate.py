"""T2: cross-source triangulation. Standard library only.

Two sources reporting the same quantity should move together. They are in different
currencies and fiscal bases, so levels are not compared and no exchange rate is used:
the year-on-year proportional change (v[y] / v[y-1] - 1) is unit-free. A year-pair is
clean when the two changes differ by at most `tolerance`; score = clean / comparable.

No counterpart (b is None), a counterpart from the same source (not independent), or no
comparable year-pair all return testable=False, score=None. Never a clean score.
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult

TOLERANCE = 0.15


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


def triangulate_score(a: IndicatorSeries, b: IndicatorSeries | None, *,
                      tolerance: float = TOLERANCE) -> TestResult:
    if b is None:
        return TestResult(None, False, {"reason": "no counterpart", "changes": {}, "agree": []})
    if a.source == b.source:
        return TestResult(None, False, {"reason": "same source, not independent",
                                        "changes": {}, "agree": []})
    ca, cb = _changes(a), _changes(b)
    years = sorted(set(ca) & set(cb))
    changes = {y: (ca[y], cb[y]) for y in years}
    agree = [y for y in years if abs(ca[y] - cb[y]) <= tolerance]
    detail = {"changes": changes, "agree": agree}
    if not years:
        return TestResult(None, False, {**detail, "reason": "no comparable year-pair"})
    return TestResult(len(agree) / len(years), True, detail)
