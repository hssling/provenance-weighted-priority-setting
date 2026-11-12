"""T4: declared-break alignment. Standard library only.

A step that exceeds `bound` (same rule as T3, including its symmetric step size and stable-reference precondition) is a BREAK. A break is DECLARED when
s.notes has a non-empty entry for the year the step arrives in, else SILENT.

Anti-goal: the instrument must reward disclosure. A declared break scores strictly
higher than an identical silent one, so a programme that footnotes a definitional or
accounting change is never ranked below one that changed silently. A silent break
scores 0 (as in T3); a declared break earns DECLARED_CREDIT; a within-bound step 1.
score = sum(credit) / comparable steps. No comparable step -> testable=False.
"""
from __future__ import annotations

from .series import IndicatorSeries, TestResult
from .implausibility import STABLE_BOUND_MAX, reference_unstable
from .triangulate import _changes, _steps

# Credit for a declared break, strictly between 0 and 1 by construction: > 0 because
# disclosure must beat silence (the anti-goal); < 1 because a declared break is still a
# discontinuity a user must adjust for, so it must not look as clean as a continuous
# series. 0.5 is the midpoint of that interval, a convention with no empirical basis.
# Only the open-interval property is relied on: the declared-vs-silent ordering holds
# for every value in (0, 1); the exact value shifts scores, not that ordering.
DECLARED_CREDIT = 0.5


def declared_score(s: IndicatorSeries, *, bound: float,
                   max_bound: float | None = STABLE_BOUND_MAX) -> TestResult:
    changes = _changes(s)
    if reference_unstable(bound, max_bound):
        return TestResult(None, False, {"reason": f"reference not stable: bound {bound:.3f} >= {max_bound}",
                                        "changes": {}, "declared": [], "silent": [], "bound": bound})
    if not changes:
        return TestResult(None, False, {"reason": "no comparable adjacent period",
                                        "changes": {}, "declared": [], "silent": [],
                                        "bound": bound})
    breaks = [y for y, c in sorted(_steps(s).items()) if c > bound]
    declared = [y for y in breaks if s.notes.get(y)]
    silent = [y for y in breaks if not s.notes.get(y)]
    total = (len(changes) - len(breaks)) + DECLARED_CREDIT * len(declared)
    detail = {"changes": dict(sorted(changes.items())), "declared": declared,
              "silent": silent, "bound": bound}
    return TestResult(total / len(changes), True, detail)
