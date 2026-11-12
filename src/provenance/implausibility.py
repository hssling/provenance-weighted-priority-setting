"""T3: adjacent-period implausibility. Standard library only.

Is a year-on-year proportional change larger than the underlying process could plausibly
produce? A step is a violation when |v[y] / v[y-1] - 1| > bound. score = within-bound
steps / comparable steps. "Size" is inversion-symmetric (triangulate._steps: fold change - 1,
a monotone function of |log(v/prev)|), so a fall is as flaggable as an equal-fold rise. The
raw |v/prev - 1| is not: it is capped at 1 for any fall, so with a bound >= 1 no fall of any
size could be flagged. A step is comparable only for consecutive years with both values
present and a non-zero base (same rule as T2); a series with no comparable step (e.g. a
single point) returns testable=False, score=None, never a clean score and never an error.

PRECONDITION. The bound is only meaningful if the reference set really is stable. A reference
whose own p95 step is a doubling or halving (bound >= STABLE_BOUND_MAX = 1.0) is not: a bound
that wide would pass a process that doubles and halves at will, and "no violations" would then
be an artefact of the reference, not evidence about the series. When the precondition fails the
score is testable=False, score=None, never 1.0. 1.0 is a convention (a factor of two), not a
fitted value; it is also the point at which the old asymmetric statistic went blind to falls.

The bound is DERIVED, not chosen: derive_bound() takes a high percentile of the absolute
year-on-year changes of a reference set believed stable. It must not be tuned against the
cases we already know about; which series form the reference set is reported with the result.
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult
from .triangulate import _changes, _steps

# Default percentile of the reference changes taken as the bound. The 95th is the
# conventional upper-tail cut: it tolerates the ordinary noise of series believed stable
# while keeping a bound that a stable process rarely exceeds (about 1 step in 20). It is a
# convention, not tuned: its effect on the known cases is reported, not optimised.
DEFAULT_PERCENTILE = 0.95

# Largest derived bound at which the reference set still counts as stable (see PRECONDITION).
STABLE_BOUND_MAX = 1.0


def reference_unstable(bound: float, max_bound: float | None = STABLE_BOUND_MAX) -> bool:
    """True when the derived bound shows the reference set is not stable (bound >= max_bound).
    max_bound=None disables the check (mechanism tests at an explicit bound)."""
    return max_bound is not None and bound >= max_bound


def implausibility_score(s: IndicatorSeries, *, bound: float,
                         max_bound: float | None = STABLE_BOUND_MAX) -> TestResult:
    changes = _changes(s)
    if reference_unstable(bound, max_bound):
        return TestResult(None, False, {"reason": f"reference not stable: bound {bound:.3f} >= {max_bound}",
                                        "changes": {}, "exceed": [], "bound": bound})
    if not changes:
        return TestResult(None, False, {"reason": "no comparable adjacent period",
                                        "changes": {}, "exceed": [], "bound": bound})
    steps = _steps(s)
    exceed = [y for y, c in sorted(steps.items()) if c > bound]
    detail = {"changes": dict(sorted(changes.items())), "steps": dict(sorted(steps.items())),
              "exceed": exceed, "bound": bound}
    return TestResult(1.0 - len(exceed) / len(changes), True, detail)


def derive_bound(reference: list[IndicatorSeries], *,
                 percentile: float = DEFAULT_PERCENTILE) -> float:
    """The `percentile` (linear interpolation) of the symmetric step size (triangulate._steps)
    pooled over reference. A +inf step (to or through zero) is a legitimate pooled value: the
    bound is +inf only if the percentile lands on or between infinities."""
    if not 0.0 < percentile < 1.0:
        raise ValueError(f"percentile must be in (0, 1), not {percentile!r}")
    pooled = sorted(c for s in reference for c in _steps(s).values())
    if not pooled:
        raise ValueError("reference series contain no comparable adjacent periods")
    pos = percentile * (len(pooled) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(pooled) - 1)
    frac = pos - lo
    if frac == 0.0 or pooled[hi] == pooled[lo]:
        return pooled[lo]
    return pooled[lo] + (pooled[hi] - pooled[lo]) * frac
