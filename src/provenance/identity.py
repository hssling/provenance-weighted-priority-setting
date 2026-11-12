"""T1: internal identity. Standard library only.

Scores two things per year:
  identity     - do the components reconcile with the reported total (within +-TOLERANCE)?
  completeness - is a total reported while every mapped component is absent?
                 Such a year fails regardless of the arithmetic (0 == 0 reconciles,
                 but "not yet reported" is not "spent nothing").
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult

# +-10% on implied/reported. A CONVENTION, not a derived value: it is wide enough to absorb the
# rounding of reported parts in the sum identities and tight enough that a 3x divergence (budget_tpt
# 2024) is unmistakable. Its effect is swept in tests/test_identity.py rather than defended here:
# every sum identity on India's data has the SAME score at every tolerance from 0.01 to 0.15
# (budget_tot and cf_tot 1.0; exp_tot, rcvd_tot, rcvd_tot_by_source 0.9, the loss being the 2026
# completeness failure, not arithmetic), while the one product identity (budget_tpt) moves from
# 4/6 clean at 0.10 to 2/6 at 0.05 (1/3 from 0.01), so THAT verdict depends on this number.
# Sensitive on budget_tpt, insensitive elsewhere.
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


def _bounds(s: IndicatorSeries, i: int, tolerance: float = TOLERANCE) -> tuple[float, float]:
    """Admissible implied/reported ratio for year index i: flat [1 - tol, 1 + tol], widened for
    a product whose unit cost c was reported rounded to +-h (s.unit_rounding = h).

    c_true is in [c - h, c + h) and ratio = c / c_true, so the ratio lies in
    (c / (c + h), c / (c - h)]: asymmetric (h = 0.5, c = 1 gives (0.667, 2.0]); unbounded above
    when c <= h. The rounding model is DECLARED on the series, not inferred from c being a whole
    number: a unit cost derived as scale / denominator can be integral by accident and carries no
    rounding. Sum identities keep the flat band; their parts are large and rounding is negligible.
    """
    lo, hi = 1.0 - tolerance, 1.0 + tolerance
    h = s.unit_rounding
    if s.identity == "product" and h:
        unit = s.components.get("unit_cost")
        c = unit[i] if unit else None
        if c is not None and c > 0:
            lo = min(lo, c / (c + h))
            hi = max(hi, c / (c - h)) if c > h else float("inf")
    return lo, hi


def identity_score(s: IndicatorSeries, *, tolerance: float = TOLERANCE,
                   independent: bool = True) -> TestResult:
    """`independent=False` declares that the components were built from the same record as the
    total (e.g. value recomputed from the numerator and denominator in the same file). Such a check
    can fail only on a transcription slip, so it is evidence about the file's arithmetic, not about
    provenance: it returns testable=False (ratios still reported in detail), never a clean 1.0."""
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
    bad = set(incomplete)
    index = {y: i for i, y in enumerate(s.years)}
    clean = []
    for y in testable:
        lo, hi = _bounds(s, index[y], tolerance)
        if y not in bad and lo - _EPS <= ratios[y] <= hi + _EPS:
            clean.append(y)
    detail["clean"] = clean          # the years that reconcile and are complete
    if not testable:
        return TestResult(None, False, detail)
    if not independent:
        return TestResult(None, False, {**detail, "reason": "self-derived components: the identity is "
                                        "built from the same record as the total, so it cannot "
                                        "discriminate (a transcription check, not evidence)"})
    return TestResult(len(clean) / len(testable), True, detail)
