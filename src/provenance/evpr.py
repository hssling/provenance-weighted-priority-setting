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

THE PRIOR (an assumption, not a finding; Ruling FF). Default: q_s ~ Beta(P_s*m_s + 1, (1-P_s)*m_s + 1),
independent across series, where P_s is the composite and m_s the total testable observations behind
it (sum of CompositeReport.observations). Mean (P_s*m_s+1)/(m_s+2), which shrinks P_s toward 0.5 by an amount that depends on m_s; it is TWO-SIDED (a series that passes its tests
may still be bad: the failure this project has found most often is a test that silently missed a
problem) and its width is set by the evidence count, not a free parameter. It is the same
Beta(k+1, n-k+1) construction the parent project uses for literature support (lower_beta_bound).
A series with no testable result (None, m = 0) gets Beta(1, 1) = Uniform[0, 1]: the uninformative
case falls out of the same formula. Consequence: a clean composite resting on few observations is
NOT certain, so all-clean input does not give zero EVPR except where the decision cannot change.
Two alternatives are available for sensitivity, because the prior is the most contestable choice:
  "uniform": Uniform[0, 1] for every series (ignores the composite entirely).
  "floor":   Uniform[P_s, 1] (the composite is a lower bound; the audit never misses anything, so
             a clean series is certain). Optimistic: it excludes the direction this project has
             most evidence for.
EVPR is not monotone in P_s: a lower composite widens the prior but may not raise the chance of
crossing a rival, so doubt alone is not value. That is a property of the construction, not a bug.

ZEROS ARE EXPECTED ON THE REAL DATA. Provenance scales a series' cells uniformly, so it can only
reorder cells ACROSS series. On the real TB data all 11 positive cells belong to one series, so the
decision can never change and every EVPR is exactly 0.0. That is the correct answer, not a bug.

THE BASELINE IS THE PRIOR-MEAN RANKING, NOT THE PUBLISHED ONE. The "decision today" term max_a E[u]
is a prior-mean quantity: each series' best cell is scored at (P_s*m_s+1)/(m_s+2), not at P_s. At P=1,
m=4 that is 0.833, and series with different m shrink by different amounts, so the cell EVPR treats as
today's best can differ from the one the published BOPAS_adj ranking (scored at P_s) puts first. That is
correct EVPI (the value of information is measured against the best decision under current beliefs,
which are the prior), not an inconsistency, but a reader comparing EVPR with the rank_changes report
must not assume they share a baseline.

PRECISION. Values are Monte Carlo estimates. evpr_detail returns each value with its standard error
(sample sd of the per-draw regret / sqrt(draws); conservative for the stratified floor prior).

HOW IT IS COMPUTED. propagate() recomputes the grid in ~25 ms, so 10,000 draws x 5 series through
it would take ~20 minutes. Instead propagate() is called ONCE (validating the inputs and returning
the published scores at provenance 1.0), and each series' scores are scaled by q. That is exact
because BOPAS is linear in T and provenance multiplies T only; it differs from a full recompute only
by the published 3-decimal rounding (<= 0.001: one rounding in each score; asserted in tests). Because cells of one series
scale together, only its best cell matters; the other series enter through their expected value
(utility is linear in each independent q, so E_{q_-s} U is U at the prior means). Under the "floor" prior draws are
stratified; Beta draws use random.betavariate (plain Monte Carlo). The gain is computed as the mean per-draw REGRET
of the baseline decision, so a series that can never change the decision gets exactly 0.0, not
floating-point dust.
"""
from __future__ import annotations

import math
import random

from provenance.composite import composite_report
from provenance.propagate import propagate

# The three priors reported side by side by evpr_prior_sensitivity (Ruling FF + two bounds).
PRIORS = ("beta", "uniform", "floor")

# Default number of draws per series. Not a tuned value: a round number whose achieved precision is
# MEASURED, not assumed. The Beta path is plain Monte Carlo, so the error falls as 1/sqrt(draws):
# at 10,000 draws a value whose decision can change is good to roughly 3% relative (about two
# significant figures) and a small one (e.g. 0.0007) can be off by ~20% relative. Always read a value
# with its standard error (evpr_detail) and round with round_to_se. The call takes ~0.05-0.2 s.
DEFAULT_DRAWS = 10_000


def observations_from_results(results_by_series) -> dict[str, int]:
    """series -> total testable observations behind its composite (0 if none testable)."""
    return {k: sum(composite_report(r).observations.values()) for k, r in results_by_series.items()}


def round_to_se(value: float, se: float) -> float:
    """Round `value` to the decimal place of the leading digit of its standard error (the precision
    the draws support). se == 0 (the decision never changed) leaves the exact value untouched."""
    if se <= 0.0:
        return value
    return round(value, max(0, -math.floor(math.log10(se))))


def evpr(node_counts, traj_rows, provenance, **kw) -> dict[str, float]:
    """series key -> expected gain (BOPAS points) from resolving that series' provenance.
    A Monte Carlo estimate: use evpr_detail for the standard errors. Arguments as evpr_detail."""
    return {k: v for k, (v, _) in evpr_detail(node_counts, traj_rows, provenance, **kw).items()}


def evpr_detail(node_counts, traj_rows, provenance: dict[str, float | None], *, observations=None,
         prior: str = "beta", draws: int = DEFAULT_DRAWS, seed: int = 0,
                **bopas_kwargs) -> dict[str, tuple[float, float]]:
    """series key -> (expected gain in BOPAS points from resolving that series' provenance,
    Monte Carlo standard error of that gain).

    `provenance` is series -> composite in [0, 1], or None if unassessable; every series in
    `traj_rows` must appear (propagate raises otherwise). `observations` (series -> testable
    observation count m) is required for prior="beta" for every series whose composite is not None
    (see observations_from_results); it is ignored by the other priors. Deterministic per `seed`
    (applied per series); the global random state is never touched.
    """
    if isinstance(draws, bool) or not isinstance(draws, int) or draws < 1:
        raise ValueError(f"draws must be a positive integer, got {draws!r}")
    if prior not in PRIORS:
        raise ValueError(f"unknown prior {prior!r}; expected one of {list(PRIORS)}")
    rows = propagate(node_counts, traj_rows, provenance, **bopas_kwargs)   # validates inputs

    series = list(dict.fromkeys(t["series"] for t in traj_rows))
    top = {s: 0.0 for s in series}                      # best published score of each series
    for r in rows:
        top[r["series"]] = max(top[r["series"]], r["BOPAS"])

    shape, mean = {}, {}                                # Beta (a, b) / floor lo, and the prior mean
    for s in series:
        P = provenance[s]
        if prior == "floor":
            lo = 0.0 if P is None else float(P)          # None: Uniform[0, 1]
            shape[s], mean[s] = lo, (1.0 + lo) / 2.0
        elif prior == "uniform" or P is None:
            shape[s], mean[s] = (1.0, 1.0), 0.5          # Beta(1,1) == Uniform[0,1]
        else:
            m = (observations or {}).get(s)
            if m is None or isinstance(m, bool) or not isinstance(m, int) or m < 0:
                raise ValueError(f"prior='beta' needs a non-negative integer observation count for series "
                                 f"{s!r}, got {m!r}")
            shape[s] = (P * m + 1.0, (1.0 - P) * m + 1.0)
            mean[s] = shape[s][0] / (shape[s][0] + shape[s][1])
    expected = {s: top[s] * mean[s] for s in series}    # best cell's mean utility

    out = {}
    for s in series:
        rival = max((expected[o] for o in series if o != s), default=0.0)
        rng = random.Random(f"evpr:{seed}:{s}")
        if prior == "floor":
            lo = shape[s]       # stratified: one draw per 1/draws slice of Uniform[P, 1]
            q = [lo + (1.0 - lo) * ((i + rng.random()) / draws) for i in range(draws)]
        else:
            a, b = shape[s]
            q = [rng.betavariate(a, b) for _ in range(draws)]
        # best decision today, from the ANALYTIC prior means on both sides (not the draws' sample
        # mean), so a near-tie cannot flip on draw noise
        plan_from_s = expected[s] >= rival
        reg = []
        for qi in q:
            u_s = top[s] * qi
            best = u_s if u_s > rival else rival
            reg.append(best - (u_s if plan_from_s else rival))
        gain = math.fsum(reg) / draws
        var = math.fsum((r - gain) ** 2 for r in reg) / (draws - 1) if draws > 1 else 0.0
        out[s] = (gain, math.sqrt(var / draws))
    return out


def evpr_prior_sensitivity(node_counts, traj_rows, provenance, *, observations=None,
                           **kw) -> dict[str, dict[str, tuple[float, float]]]:
    """EVPR under every prior, side by side: {prior: {series: (evpr, se)}}. The prior is the most
    contestable assumption in the method; report all three, not one."""
    return {pr: evpr_detail(node_counts, traj_rows, provenance, observations=observations, prior=pr, **kw)
            for pr in PRIORS}
