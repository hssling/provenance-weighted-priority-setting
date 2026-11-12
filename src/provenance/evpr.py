"""EVPR: the expected value of provenance resolution. Standard library only.

Sampling uncertainty cannot be bought down after the fact (a past year cannot be re-collected).
Provenance uncertainty can: someone can go and read the accounts. EVPR asks what resolving one
series' provenance to certainty would be worth BEFORE planning from it. It is the standard
(partial) EVPI construction applied to provenance instead of effect size.

THE DECISION. The action is "which intervention-target cell to plan around"; the utility of an
action is that cell's provenance-adjusted BOPAS under the TRUE provenance. EVPR_s is the expected
regret of the best decision you can make today (maximise expected utility, series s unresolved)
relative to deciding after learning series s's true provenance:
    EVPR_s = E_{q_s}[ max_a E_{q_-s} U(a, q) ] - max_a E_q U(a, q).
Expected rank change and the identity of the top cell were considered and rejected as the decision
variable: neither has a utility scale, so neither yields an expected GAIN, only a probability of
change, which cannot be compared across series or priced against an audit. The probability that the
top cell changes is a different (and worse) quantity: a change among near-tied cells is worth
almost nothing, a change among distant ones a great deal. Units here are BOPAS points.

THE PRIOR (an assumption, not a finding). A series' true provenance q_s is drawn independently
from Uniform[P_s, 1], where P_s is its composite score: the composite is read as a floor, audit can
reveal the series was better than the tests suggest (a failed test can be a real policy change
rather than corruption) but the tests are not assumed to overstate quality. A series that passes
everything (P_s = 1) is therefore certain and worth nothing to audit, and a series with no testable
result (None) gets the widest prior, Uniform[0, 1]. A flat Uniform[0, 1] for every series was
rejected because it ignores the composite entirely: a clean series would then be as worth auditing
as a failed one. The floor reading is the single most consequential modelling choice here; the
direction it excludes (a clean-looking series that is in fact bad) is not priced.

ZEROS ARE EXPECTED ON THE REAL DATA. Provenance scales a series' cells uniformly, so it can only
reorder cells ACROSS series. On the real TB data all 11 positive cells belong to one series, so the
decision can never change and every EVPR is exactly 0.0. That is the correct answer, not a bug.

HOW IT IS COMPUTED. propagate() recomputes the grid in ~25 ms, so 10,000 draws x 5 series through
it would take ~20 minutes. Instead propagate() is called ONCE (validating the inputs and returning
the published scores at provenance 1.0), and each series' scores are scaled by q. That is exact
because BOPAS is linear in T and provenance multiplies T only; it differs from a full recompute only
by the published 3-decimal rounding (<= 0.001: one rounding in each score; asserted in tests). Because cells of one series
scale together, only its best cell matters; the other series enter through their expected value
(utility is linear in each independent q, so E_{q_-s} U is U at the prior means). Draws are
stratified (one per 1/draws slice of the prior's quantile range), which makes the estimate far less
noisy than plain Monte Carlo at the same draw count. The gain is computed as the mean per-draw REGRET
of the baseline decision, so a series that can never change the decision gets exactly 0.0, not
floating-point dust.
"""
from __future__ import annotations

import math
import random

from provenance.propagate import propagate

# Default number of draws per series. Not a tuned value: with stratified sampling the error of a
# mean is ~1/draws^1.5 of the spread, so 10,000 gives ~4 significant digits for any series whose
# decision can change, and the whole call takes about a second.
DEFAULT_DRAWS = 10_000


def evpr(node_counts, traj_rows, provenance: dict[str, float | None], *,
         draws: int = DEFAULT_DRAWS, seed: int = 0, **bopas_kwargs) -> dict[str, float]:
    """series key -> expected gain (BOPAS points) from resolving that series' provenance.

    `provenance` is series -> composite score in [0, 1], or None if unassessable; every series in
    `traj_rows` must appear (propagate raises otherwise). Deterministic for a given `seed`, which
    is applied per series so that adding a series does not change another's estimate. The global
    random state is never touched.
    """
    if isinstance(draws, bool) or not isinstance(draws, int) or draws < 1:
        raise ValueError(f"draws must be a positive integer, got {draws!r}")
    rows = propagate(node_counts, traj_rows, provenance, **bopas_kwargs)   # validates inputs

    series = list(dict.fromkeys(t["series"] for t in traj_rows))
    top = {s: 0.0 for s in series}                      # best published score of each series
    for r in rows:
        top[r["series"]] = max(top[r["series"]], r["BOPAS"])
    floor = {s: 0.0 if provenance[s] is None else float(provenance[s]) for s in series}
    expected = {s: top[s] * (1.0 + floor[s]) / 2.0 for s in series}   # best cell's mean utility

    out = {}
    for s in series:
        rival = max((expected[o] for o in series if o != s), default=0.0)
        rng = random.Random(f"evpr:{seed}:{s}")
        lo = floor[s]
        q = [lo + (1.0 - lo) * ((i + rng.random()) / draws) for i in range(draws)]
        own = top[s] * (math.fsum(q) / draws)           # mean utility of planning from s
        plan_from_s = own >= rival                      # the best decision available today
        regret = 0.0
        for qi in q:
            u_s = top[s] * qi
            best = u_s if u_s > rival else rival
            regret += best - (u_s if plan_from_s else rival)
        out[s] = regret / draws
    return out
