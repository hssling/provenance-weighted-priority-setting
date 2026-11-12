"""Composite provenance score over a series' test results. Standard library only.

Untestable results are excluded from the combination, never counted as 1.0: a test that could
not run is not evidence of cleanliness. If nothing is testable the composite is None (the series
is *unassessable*), which is distinct from 0.0 (testable and wholly failed) and from 1.0 (clean).

The existence test (T5) is deliberately not an input: it scores interventions, not series.
"""
from __future__ import annotations

import math
from statistics import fmean

from provenance.series import TestResult

# Default is geometric so one catastrophic test cannot be averaged away by several clean ones
# (the additive-scoring failure mode). Author's call, open to being overturned with reasons.
DEFAULT_RULE = "geometric"

# Rules reported by composite_sensitivity by default: the default plus a lenient (arithmetic)
# and a strictest (minimum) bound, so the reader sees how much the conclusion hinges on the rule.
DEFAULT_SENSITIVITY_RULES = ("geometric", "arithmetic", "minimum")


def _geometric(scores: list[float]) -> float:
    # math.prod ** (1/n) rather than exp(mean(log)): an exact 0.0 score yields 0.0 directly,
    # with no log(0) domain error. The collapse is intended: a 0.0 means every testable year
    # failed that test, which is exactly the catastrophic case the geometric rule must not dilute.
    # min() guards a last-ulp overshoot above 1.0 (TestResult scores are bounded to [0, 1]).
    return min(1.0, math.prod(scores) ** (1.0 / len(scores)))


_RULES = {
    "geometric": _geometric,
    "arithmetic": fmean,
    "minimum": min,
}


def composite(results: list[TestResult], *, rule: str = DEFAULT_RULE) -> float | None:
    """Combine testable scores under `rule`; None when no result is testable."""
    if rule not in _RULES:
        raise ValueError(f"unknown rule {rule!r}; expected one of {sorted(_RULES)}")
    scores = [r.score for r in results if r.testable]
    if not scores:
        return None
    return float(_RULES[rule](scores))


def composite_sensitivity(results: list[TestResult],
                          rules: tuple[str, ...] = DEFAULT_SENSITIVITY_RULES) -> dict[str, float]:
    """Composite under each rule. Empty dict when the series is unassessable (no number exists)."""
    out = {rule: composite(results, rule=rule) for rule in rules}
    return {k: v for k, v in out.items() if v is not None}
