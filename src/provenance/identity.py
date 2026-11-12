"""T1: internal identity. Standard library only.

Scores two things per year:
  identity     - do the components reconcile with the reported total (within +-10%)?
  completeness - is a total reported while every mapped component is absent?
                 Such a year fails regardless of the arithmetic (0 == 0 reconciles,
                 but "not yet reported" is not "spent nothing").
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult

TOLERANCE = 0.10
_EPS = 1e-9


def _implied(s: IndicatorSeries, i: int) -> float | None:
    """Implied total for year index i, or None if it cannot be formed."""
    if s.identity == "product":
        unit, vol = s.components.get("unit_cost"), s.components.get("volume")
        if unit is None or vol is None or unit[i] is None or vol[i] is None:
            return None
        return unit[i] * vol[i]
    if s.identity == "sum":
        return sum(c[i] for c in s.components.values() if c[i] is not None)
    return None


def _bounds(s: IndicatorSeries, i: int) -> tuple[float, float]:
    """Admissible implied/reported ratio for year index i: flat [0.90, 1.10], widened for
    a product whose integer unit cost c carries rounding error.

    c_true is in [c - 0.5, c + 0.5) and ratio = c / c_true, so the ratio lies in
    (c / (c + 0.5), c / (c - 0.5)]: asymmetric (c = 1 gives (0.667, 2.0]).
    Sum identities keep the flat band; their parts are large and rounding is negligible.
    """
    lo, hi = 1.0 - TOLERANCE, 1.0 + TOLERANCE
    if s.identity == "product":
        unit = s.components.get("unit_cost")
        c = unit[i] if unit else None
        if c is not None and c > 0 and float(c).is_integer():
            lo, hi = min(lo, c / (c + 0.5)), max(hi, c / (c - 0.5))
    return lo, hi


def identity_score(s: IndicatorSeries) -> TestResult:
    if s.identity not in ("product", "sum") or not s.components:
        return TestResult(None, False, {"identity": {}, "incomplete": []})

    ratios: dict[int, float] = {}
    incomplete: list[int] = []
    for i, year in enumerate(s.years):
        reported = s.values[i]
        if reported is None:
            continue  # nothing reported: untestable on both criteria
        if all(c[i] is None for c in s.components.values()):
            incomplete.append(year)
        implied = _implied(s, i)
        if reported != 0 and implied is not None:
            ratios[year] = implied / reported

    detail = {"identity": ratios, "incomplete": incomplete}
    # A year is testable if it has a ratio or failed completeness; a year with neither
    # (e.g. zero total with components present) tells us nothing and is excluded.
    testable = sorted(set(ratios) | set(incomplete))
    if not testable:
        return TestResult(None, False, detail)
    bad = set(incomplete)
    index = {y: i for i, y in enumerate(s.years)}
    clean = [y for y in testable
             if y not in bad
             and _bounds(s, index[y])[0] - _EPS <= ratios[y] <= _bounds(s, index[y])[1] + _EPS]
    return TestResult(len(clean) / len(testable), True, detail)
