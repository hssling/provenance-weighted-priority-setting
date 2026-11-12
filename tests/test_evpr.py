"""Task 10: EVPR, the expected value of provenance resolution.

Two kinds of data are used and the split matters. On the REAL TB data all 11 positive BOPAS cells
belong to one series (RRMDR_notif_100k), so per-series provenance scales every live cell together
and cannot reorder the ranking: EVPR is exactly zero there by construction. Those zeros are asserted
(and asserted non-vacuously: the result must name every series). A SYNTHETIC "contested" grid, in
which one doubtful series has a top cell that could overtake a clean rival, is needed to show that
EVPR is not simply always zero.
"""
import math
from pathlib import Path

import pytest

from provenance import propagate as prop
from provenance.evpr import evpr
from provenance.propagate import propagate

SERIES = ["RR_new_pct", "RRMDR_notif_100k", "preXDR_fqr_pct", "MDR_TSR_pct", "XDR_TSR_pct"]
CLEAN = {s: 1.0 for s in SERIES}


@pytest.fixture(scope="module")
def mod():
    return prop._bopas_module()


@pytest.fixture(scope="module")
def counts(mod):
    return mod.code_corpus(mod._read_corpus(), corrected=True)


@pytest.fixture(scope="module")
def real_traj(mod):
    by_series, _ = mod.load_series()
    return mod.fit_trajectories(by_series)


def _t(series, slope, half=1.0, sign=+1):
    return dict(series=series, label=series + " label", sign=sign, slope_primary=slope,
                primary_lo=slope - half, primary_hi=slope + half, classification_primary="x")


@pytest.fixture(scope="module")
def contested():
    # RR_new_pct has the highest top cell (~3.9) but XDR_TSR_pct is close behind (~2.96): a doubtful
    # RR_new_pct could plausibly fall below, or stay above, the clean rival.
    return [_t("RR_new_pct", 8.0), _t("RRMDR_notif_100k", 2.0), _t("preXDR_fqr_pct", 3.0),
            _t("MDR_TSR_pct", -4.0, sign=-1), _t("XDR_TSR_pct", -5.0, sign=-1)]


def _tops(counts, traj):
    rows = propagate(counts, traj, CLEAN)
    out = {}
    for r in rows:
        out[r["series"]] = max(out.get(r["series"], 0.0), r["BOPAS"])
    return out


# ---- the three requirements from the brief ------------------------------------------------

def test_a_perfectly_clean_series_is_worth_nothing_to_audit(counts, contested):
    v = evpr(counts, contested, CLEAN, draws=2000)
    assert set(v) == set(SERIES)            # non-vacuous: an empty dict must not pass
    assert all(x == 0.0 for x in v.values())


def test_the_most_doubtful_series_has_the_highest_audit_value(counts, contested):
    v = evpr(counts, contested, {**CLEAN, "RR_new_pct": 0.2}, draws=2000)
    assert set(v) == set(SERIES)
    assert max(v, key=v.get) == "RR_new_pct"
    assert v["RR_new_pct"] > 0.0
    assert all(v[s] == 0.0 for s in SERIES if s != "RR_new_pct")


def test_evpr_is_deterministic_under_a_fixed_seed(counts, contested):
    P = {**CLEAN, "RR_new_pct": 0.2, "MDR_TSR_pct": 0.6}
    a = evpr(counts, contested, P, draws=2000, seed=7)
    assert a == evpr(counts, contested, P, draws=2000, seed=7)
    assert a["RR_new_pct"] > 0.0
    assert a != evpr(counts, contested, P, draws=2000, seed=8)   # the seed is actually used


# ---- correctness against a closed form ----------------------------------------------------

def test_matches_the_closed_form_for_a_two_contender_decision(counts, contested):
    # q ~ U[a, 1]; B = RR's top cell, m = the best clean rival. Regret of planning from the rival
    # is E[(qB - m)+] = B (1 - t)^2 / (2 (1 - a)), t = m / B, when a < t < 1.
    top = _tops(counts, contested)
    B, m = top["RR_new_pct"], max(v for s, v in top.items() if s != "RR_new_pct")
    a, t = 0.2, m / B
    assert a < t < 1 and ((1 + a) / 2) * B < m   # the rival is the baseline choice, and can be overtaken
    exact = B * (1 - t) ** 2 / (2 * (1 - a))
    got = evpr(counts, contested, {**CLEAN, "RR_new_pct": a}, draws=20000)["RR_new_pct"]
    assert got == pytest.approx(exact, rel=0.02)


def test_unassessable_series_gets_the_widest_prior_not_a_free_pass(counts, contested):
    # None => q ~ U[0, 1] (a = 0): maximal ignorance, never "clean"
    top = _tops(counts, contested)
    B, m = top["RR_new_pct"], max(v for s, v in top.items() if s != "RR_new_pct")
    t = m / B
    assert 0.5 * B < m                          # baseline = rival, so the closed form applies
    exact = B * (1 - t) ** 2 / 2
    got = evpr(counts, contested, {**CLEAN, "RR_new_pct": None}, draws=20000)["RR_new_pct"]
    assert got == pytest.approx(exact, rel=0.02)


def test_doubt_alone_is_not_value_a_dominated_series_is_worth_nothing(counts, contested):
    # MDR_TSR_pct is very doubtful but its best cell (~2.1) is below the clean XDR cell (~2.96)
    # even at provenance 1.0, so resolving it can never change the decision.
    top = _tops(counts, contested)
    assert top["MDR_TSR_pct"] < top["XDR_TSR_pct"]
    v = evpr(counts, contested, {**CLEAN, "MDR_TSR_pct": 0.05}, draws=2000)
    assert set(v) == set(SERIES) and v["MDR_TSR_pct"] == 0.0


def test_evpr_is_never_negative(counts, contested):
    P = {"RR_new_pct": 0.1, "RRMDR_notif_100k": 0.3, "preXDR_fqr_pct": 0.5, "MDR_TSR_pct": 0.7,
         "XDR_TSR_pct": 0.4}
    v = evpr(counts, contested, P, draws=2000)
    assert set(v) == set(SERIES) and all(x >= 0.0 for x in v.values())


# ---- real TB data: exact zeros, by construction -------------------------------------------

@pytest.mark.parametrize("P", [CLEAN,
                               {s: 0.3 for s in SERIES},
                               {**CLEAN, "RRMDR_notif_100k": 0.01},
                               {s: None for s in SERIES}])
def test_real_data_evpr_is_exactly_zero_because_one_series_holds_every_live_cell(counts, real_traj, P):
    rows = propagate(counts, real_traj, CLEAN)
    live = {r["series"] for r in rows if r["BOPAS"] > 0}
    assert live == {"RRMDR_notif_100k"}         # the premise; if data change, this fails loudly
    v = evpr(counts, real_traj, P, draws=2000)
    assert set(v) == set(SERIES)
    assert all(x == 0.0 for x in v.values())


# ---- the linear fast path is faithful to the full recompute -------------------------------

@pytest.mark.parametrize("series", ["RR_new_pct", "XDR_TSR_pct"])
@pytest.mark.parametrize("q", [0.0, 0.13, 0.5, 0.87, 1.0])
def test_scaling_published_scores_by_q_agrees_with_a_full_propagate(counts, contested, series, q):
    # evpr scales each series' scores by q instead of re-running propagate per draw (24 ms each).
    # That is only valid if the published score really is linear in q up to its 3-dp rounding.
    top = _tops(counts, contested)
    rows = propagate(counts, contested, {**CLEAN, series: q})
    full = max(r["BOPAS_adj"] for r in rows if r["series"] == series)
    assert abs(full - q * top[series]) <= 0.001   # two roundings at 3 dp: the q=1 score (scaled by q) and the adjusted one


# ---- input handling -----------------------------------------------------------------------

def test_missing_series_raises_rather_than_defaulting(counts, contested):
    with pytest.raises(ValueError, match="RR_new_pct"):
        evpr(counts, contested, {s: 1.0 for s in SERIES if s != "RR_new_pct"}, draws=10)


@pytest.mark.parametrize("draws", [0, -5, 2.5, True])
def test_bad_draw_counts_raise(counts, contested, draws):
    with pytest.raises(ValueError, match="draws"):
        evpr(counts, contested, CLEAN, draws=draws)


def test_does_not_disturb_the_global_rng(counts, contested):
    import random
    random.seed(123)
    expected = random.random()
    random.seed(123)
    evpr(counts, contested, {**CLEAN, "RR_new_pct": 0.2}, draws=200)
    assert random.random() == expected
