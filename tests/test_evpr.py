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
from provenance.evpr import evpr, evpr_detail, evpr_prior_sensitivity, round_to_se, PRIORS


def evpr_floor(*a, **k):
    """the original (Uniform[P, 1]) prior, which the closed-form tests were written for"""
    return evpr(*a, prior="floor", **k)
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
    v = evpr_floor(counts, contested, CLEAN, draws=2000)
    assert set(v) == set(SERIES)            # non-vacuous: an empty dict must not pass
    assert all(x == 0.0 for x in v.values())


def test_the_most_doubtful_series_has_the_highest_audit_value(counts, contested):
    v = evpr_floor(counts, contested, {**CLEAN, "RR_new_pct": 0.2}, draws=2000)
    assert set(v) == set(SERIES)
    assert max(v, key=v.get) == "RR_new_pct"
    assert v["RR_new_pct"] > 0.0
    assert all(v[s] == 0.0 for s in SERIES if s != "RR_new_pct")


def test_evpr_is_deterministic_under_a_fixed_seed(counts, contested):
    P = {**CLEAN, "RR_new_pct": 0.2, "MDR_TSR_pct": 0.6}
    a = evpr_floor(counts, contested, P, draws=2000, seed=7)
    assert a == evpr_floor(counts, contested, P, draws=2000, seed=7)
    assert a["RR_new_pct"] > 0.0
    assert a != evpr_floor(counts, contested, P, draws=2000, seed=8)   # the seed is actually used


# ---- correctness against a closed form ----------------------------------------------------

def test_matches_the_closed_form_for_a_two_contender_decision(counts, contested):
    # q ~ U[a, 1]; B = RR's top cell, m = the best clean rival. Regret of planning from the rival
    # is E[(qB - m)+] = B (1 - t)^2 / (2 (1 - a)), t = m / B, when a < t < 1.
    top = _tops(counts, contested)
    B, m = top["RR_new_pct"], max(v for s, v in top.items() if s != "RR_new_pct")
    a, t = 0.2, m / B
    assert a < t < 1 and ((1 + a) / 2) * B < m   # the rival is the baseline choice, and can be overtaken
    exact = B * (1 - t) ** 2 / (2 * (1 - a))
    got = evpr_floor(counts, contested, {**CLEAN, "RR_new_pct": a}, draws=20000)["RR_new_pct"]
    assert got == pytest.approx(exact, rel=0.02)


def test_unassessable_series_gets_the_widest_prior_not_a_free_pass(counts, contested):
    # None => q ~ U[0, 1] (a = 0): maximal ignorance, never "clean"
    top = _tops(counts, contested)
    B, m = top["RR_new_pct"], max(v for s, v in top.items() if s != "RR_new_pct")
    t = m / B
    assert 0.5 * B < m                          # baseline = rival, so the closed form applies
    exact = B * (1 - t) ** 2 / 2
    got = evpr_floor(counts, contested, {**CLEAN, "RR_new_pct": None}, draws=20000)["RR_new_pct"]
    assert got == pytest.approx(exact, rel=0.02)


def test_doubt_alone_is_not_value_a_dominated_series_is_worth_nothing(counts, contested):
    # MDR_TSR_pct is very doubtful but its best cell (~2.1) is below the clean XDR cell (~2.96)
    # even at provenance 1.0, so resolving it can never change the decision.
    top = _tops(counts, contested)
    assert top["MDR_TSR_pct"] < top["XDR_TSR_pct"]
    v = evpr_floor(counts, contested, {**CLEAN, "MDR_TSR_pct": 0.05}, draws=2000)
    assert set(v) == set(SERIES) and v["MDR_TSR_pct"] == 0.0


def test_evpr_is_never_negative(counts, contested):
    P = {"RR_new_pct": 0.1, "RRMDR_notif_100k": 0.3, "preXDR_fqr_pct": 0.5, "MDR_TSR_pct": 0.7,
         "XDR_TSR_pct": 0.4}
    v = evpr_floor(counts, contested, P, draws=2000)
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
    v = evpr(counts, real_traj, P, prior="floor", draws=2000)
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
        evpr_floor(counts, contested, {s: 1.0 for s in SERIES if s != "RR_new_pct"}, draws=10)


@pytest.mark.parametrize("draws", [0, -5, 2.5, True])
def test_bad_draw_counts_raise(counts, contested, draws):
    with pytest.raises(ValueError, match="draws"):
        evpr_floor(counts, contested, CLEAN, draws=draws)


def test_does_not_disturb_the_global_rng(counts, contested):
    import random
    random.seed(123)
    expected = random.random()
    random.seed(123)
    evpr_floor(counts, contested, {**CLEAN, "RR_new_pct": 0.2}, draws=200)
    assert random.random() == expected


# ---- Ruling FF: Beta prior (default) and prior sensitivity --------------------------------

OBS = {s: 4 for s in SERIES}


def test_beta_prior_prices_the_clean_looking_series_that_is_really_bad(counts, contested):
    # a clean composite resting on only 4 observations is NOT certain under Beta; the floor prior
    # (which never lets an audit find a problem) gives this series zero, the Beta gives it value.
    floor = evpr(counts, contested, CLEAN, prior="floor", draws=4000)["RR_new_pct"]
    beta = evpr(counts, contested, CLEAN, observations=OBS, draws=4000)["RR_new_pct"]
    assert floor == 0.0 and beta > 0.0


def test_beta_uncertainty_shrinks_with_the_evidence_count(counts, contested):
    P = {**CLEAN, "RR_new_pct": 0.9}
    few = evpr(counts, contested, P, observations={**OBS, "RR_new_pct": 2}, draws=20000)["RR_new_pct"]
    many = evpr(counts, contested, P, observations={**OBS, "RR_new_pct": 60}, draws=20000)["RR_new_pct"]
    assert few > many


def test_beta_matches_a_direct_numeric_integral(counts, contested):
    # regret of planning from the rival = E[(qB - m)+], q ~ Beta(P n + 1, (1-P) n + 1)
    top = _tops(counts, contested)
    # the clean rivals rest on OBS=4 observations, so under Beta they are themselves uncertain:
    # their expected utility is top * Beta(5, 1) mean = top * 5/6
    B, m = top["RR_new_pct"], max(v for s, v in top.items() if s != "RR_new_pct") * 5 / 6
    a, b = 0.6 * 5 + 1, 0.4 * 5 + 1
    n, exact = 100000, 0.0
    const = math.gamma(a + b) / (math.gamma(a) * math.gamma(b))
    for i in range(n):
        x = (i + 0.5) / n
        exact += max(x * B - m, 0.0) * const * x ** (a - 1) * (1 - x) ** (b - 1) / n
    assert a / (a + b) * B < m          # baseline is the rival, so the formula applies
    got = evpr(counts, contested, {**CLEAN, "RR_new_pct": 0.6}, observations={**OBS, "RR_new_pct": 5},
               draws=40000)["RR_new_pct"]
    assert exact > 0 and got == pytest.approx(exact, rel=0.05)


def test_none_under_beta_is_uniform_without_needing_an_observation_count(counts, contested):
    P = {s: None for s in SERIES}      # every series unassessable: Beta(1,1) everywhere
    a = evpr(counts, contested, P, observations=OBS, draws=3000, seed=1)
    b = evpr(counts, contested, P, prior="uniform", draws=3000, seed=1)
    assert a == b and a["RR_new_pct"] > 0.0


def test_beta_requires_an_observation_count(counts, contested):
    with pytest.raises(ValueError, match="observation"):
        evpr(counts, contested, CLEAN, draws=10)


def test_unknown_prior_raises(counts, contested):
    with pytest.raises(ValueError, match="prior"):
        evpr(counts, contested, CLEAN, prior="flat", draws=10)


def test_beta_is_deterministic_and_seeded(counts, contested):
    P = {**CLEAN, "RR_new_pct": 0.5}
    a = evpr(counts, contested, P, observations=OBS, draws=1000, seed=3)
    assert a == evpr(counts, contested, P, observations=OBS, draws=1000, seed=3)
    assert a != evpr(counts, contested, P, observations=OBS, draws=1000, seed=4)


@pytest.mark.parametrize("P", [CLEAN, {s: 0.3 for s in SERIES}, {s: None for s in SERIES}])
def test_real_data_is_exactly_zero_under_all_three_priors(counts, real_traj, P):
    sens = evpr_prior_sensitivity(counts, real_traj, P, observations=OBS, draws=1000)
    assert set(sens) == set(PRIORS)
    for pr, v in sens.items():
        assert set(v) == set(SERIES) and all(x == (0.0, 0.0) for x in v.values()), pr


def test_sensitivity_shows_the_priors_disagreeing_on_a_contested_grid(counts, contested):
    sens = evpr_prior_sensitivity(counts, contested, {**CLEAN, "RR_new_pct": 0.5}, observations=OBS, draws=4000)
    vals = {pr: sens[pr]["RR_new_pct"][0] for pr in PRIORS}
    assert len(set(vals.values())) == 3 and all(v > 0 for v in vals.values())


# ---- review fixes: standard errors, rounding, m = 0 ----------------------------------------

def test_standard_error_is_zero_when_the_decision_never_changes_and_positive_otherwise(counts, contested, real_traj):
    z = evpr_detail(counts, real_traj, {s: 0.3 for s in SERIES}, observations=OBS, draws=500)
    assert set(z) == set(SERIES) and all(v == (0.0, 0.0) for v in z.values())
    d = evpr_detail(counts, contested, {**CLEAN, "RR_new_pct": 0.5}, observations=OBS, draws=2000)
    v, se = d["RR_new_pct"]
    assert v > 0 and 0 < se < v


def test_reported_standard_error_matches_the_spread_across_seeds(counts, contested):
    P = {**CLEAN, "RR_new_pct": 0.5}
    runs = [evpr_detail(counts, contested, P, observations=OBS, draws=2000, seed=k)["RR_new_pct"]
            for k in range(25)]
    vals = [v for v, _ in runs]
    mean = sum(vals) / len(vals)
    sd = (sum((x - mean) ** 2 for x in vals) / (len(vals) - 1)) ** 0.5
    se = sum(e for _, e in runs) / len(runs)
    assert 0.6 * sd < se < 1.6 * sd


def test_evpr_returns_the_same_values_as_evpr_detail(counts, contested):
    P = {**CLEAN, "RR_new_pct": 0.5}
    d = evpr_detail(counts, contested, P, observations=OBS, draws=500, seed=2)
    assert evpr(counts, contested, P, observations=OBS, draws=500, seed=2) == {k: v for k, (v, _) in d.items()}


def test_round_to_se_keeps_only_the_digits_the_draws_support():
    assert round_to_se(0.109436, 0.0029) == 0.109
    assert round_to_se(0.0390123, 0.0015) == 0.039
    assert round_to_se(0.0007123, 0.00014) == 0.0007
    assert round_to_se(0.0, 0.0) == 0.0 and round_to_se(1.23456789, 0.0) == 1.23456789


def test_an_assessable_series_with_zero_observations_gets_the_uniform_prior(counts, contested):
    # P is not None but m = 0: Beta(1, 1), a different branch from P is None, must also be Uniform[0, 1]
    P = {s: 0.7 for s in SERIES}
    beta0 = evpr(counts, contested, P, observations={s: 0 for s in SERIES}, draws=3000, seed=5)
    uniform = evpr(counts, contested, P, prior="uniform", draws=3000, seed=5)
    assert beta0 == uniform and beta0["RR_new_pct"] > 0.0
