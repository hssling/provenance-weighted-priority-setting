"""T3: adjacent-period implausibility. Standard library only.

Is a year-on-year proportional change larger than the underlying process could plausibly
produce? A step is a violation when |v[y] / v[y-1] - 1| > bound. score = within-bound
steps / comparable steps. A step is comparable only for consecutive years with both values
present and a non-zero base (same rule as T2); a series with no comparable step (e.g. a
single point) returns testable=False, score=None, never a clean score and never an error.

The bound is DERIVED, not chosen: derive_bound() takes a high percentile of the absolute
year-on-year changes of a reference set believed stable. It must not be tuned against the
cases we already know about; which series form the reference set is reported with the result.
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult
from .triangulate import _changes

# Default percentile of the reference changes taken as the bound. The 95th is the
# conventional upper-tail cut: it tolerates the ordinary noise of series believed stable
# while keeping a bound that a stable process rarely exceeds (about 1 step in 20). It is a
# convention, not tuned: its effect on the known cases is reported, not optimised.
DEFAULT_PERCENTILE = 0.95


def implausibility_score(s: IndicatorSeries, *, bound: float) -> TestResult:
    changes = _changes(s)
    if not changes:
        return TestResult(None, False, {"reason": "no comparable adjacent period",
                                        "changes": {}, "exceed": [], "bound": bound})
    exceed = [y for y, c in sorted(changes.items()) if abs(c) > bound]
    detail = {"changes": dict(sorted(changes.items())), "exceed": exceed, "bound": bound}
    return TestResult(1.0 - len(exceed) / len(changes), True, detail)


def derive_bound(reference: list[IndicatorSeries], *,
                 percentile: float = DEFAULT_PERCENTILE) -> float:
    """The `percentile` (linear interpolation) of |year-on-year change| pooled over reference."""
    if not 0.0 < percentile < 1.0:
        raise ValueError(f"percentile must be in (0, 1), not {percentile!r}")
    pooled = sorted(abs(c) for s in reference for c in _changes(s).values())
    if not pooled:
        raise ValueError("reference series contain no comparable adjacent periods")
    pos = percentile * (len(pooled) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(pooled) - 1)
    return pooled[lo] + (pooled[hi] - pooled[lo]) * (pos - lo)
