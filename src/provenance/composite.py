"""Composite provenance score over a series' test results. Standard library only.

Untestable results are excluded from the combination, never counted as 1.0: a test that could
not run is not evidence of cleanliness. If nothing is testable the composite is None (the series
is *unassessable*), which is distinct from 0.0 (testable and wholly failed) and from 1.0 (clean).

The existence test (T5) is deliberately not an input: it scores interventions, not series.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
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
    """Composite under each rule.

    Returns an EMPTY dict when the series is unassessable (no testable result): no number exists
    under any rule. An empty dict and a dict of zeros mean opposite things -- {} is "could not be
    assessed", {"geometric": 0.0, ...} is "assessed and wholly failed". Check `if not d` first.
    """
    out = {rule: composite(results, rule=rule) for rule in rules}
    return {k: v for k, v in out.items() if v is not None}


_SHAPES = ("identity: keys 'identity'+'incomplete'; triangulation: keys 'changes'+'agree'; "
           "implausibility: keys 'changes'+'exceed'; declared: keys 'changes'+'declared'+'silent'")


def _identify(detail: dict) -> tuple[str, int]:
    """(test name, observations evaluated) from a TestResult.detail.

    The four test modules shape `detail` differently, so each gets its own accessor, recognised by
    a key unique to that module. Derivation of the count:
      identity       (identity.py):       years that were testable = |ratios keys U incomplete years|
      triangulation  (triangulate.py):    len(detail["changes"]) = year-pairs compared (the score's denominator)
      implausibility (implausibility.py): len(detail["changes"]) = adjacent-period steps (denominator)
      declared       (declared.py):       len(detail["changes"]) = adjacent-period steps (denominator)
    An unrecognised shape raises rather than guessing.
    """
    if "identity" in detail:
        return "identity", len(set(detail["identity"]) | set(detail.get("incomplete", ())))
    if "agree" in detail:
        return "triangulation", len(detail["changes"])
    if "exceed" in detail:
        return "implausibility", len(detail["changes"])
    if "declared" in detail and "silent" in detail:
        return "declared", len(detail["changes"])
    raise ValueError(f"unrecognised TestResult.detail shape (keys: {sorted(detail)}); "
                     f"recognised shapes are {_SHAPES}")


@dataclass(frozen=True)
class CompositeReport:
    score: float | None           # same value composite() returns
    n_testable: int               # how many tests could run
    observations: dict[str, int]  # test name -> observations behind its score; testable tests only
    min_observations: int | None  # min(observations.values()); None if none testable
    collapsed_by: list[str]       # names of tests scoring exactly 0.0, in input order


def composite_report(results: list[TestResult], *, rule: str = DEFAULT_RULE) -> CompositeReport:
    """composite() plus the evidential weight behind it.

    Exposes thinness without correcting for it: no minimum-evidence cutoff, no shrinkage. A 0.0
    resting on one observation and a 0.0 resting on twenty have the same score but are reported
    differently.

    Read `observations` beside `collapsed_by` to judge a 0.0. `min_observations` is only a
    summary over ALL testable tests: it may belong to a clean test, not to the one that collapsed.
    """
    score = composite(results, rule=rule)  # validates `rule`
    observations: dict[str, int] = {}
    collapsed: list[str] = []
    for i, r in enumerate(results):
        if not r.testable:
            continue
        try:
            name, n = _identify(r.detail)
        except ValueError as e:
            raise ValueError(f"results[{i}]: {e}") from None
        if name in observations:
            raise ValueError(f"results[{i}]: more than one {name!r} result; observations is keyed by test")
        observations[name] = n
        if r.score == 0.0:
            collapsed.append(name)
    return CompositeReport(score=score, n_testable=len(observations), observations=observations,
                           min_observations=min(observations.values(), default=None),
                           collapsed_by=collapsed)
