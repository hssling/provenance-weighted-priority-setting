"""Task 9: propagation of provenance into BOPAS.

Real-data tests read the published TB-BOPAS repository (read-only). Synthetic trajectories are
used where a test needs several series with positive worsening slopes at once: on the real data
only RRMDR_notif_100k has any positive BOPAS cell, so reordering cannot be exercised there.
"""
import copy
import random
import sys
from pathlib import Path

import pytest

from provenance import propagate as prop
from provenance.propagate import (RankChange, load_compute_bopas, propagate, provenance_from_results,
                                  rank_changes)
from provenance.series import TestResult

REPO = Path(__file__).resolve().parents[2] / "tb_bopas_repo"
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
def synth():
    # all five series worsening and strongly separated, so every series has positive BOPAS cells
    return [_t("RR_new_pct", 1.0), _t("RRMDR_notif_100k", 2.0), _t("preXDR_fqr_pct", 3.0),
            _t("MDR_TSR_pct", -4.0, sign=-1), _t("XDR_TSR_pct", -5.0, sign=-1)]


# ---- Review Focus 4: the identity property -------------------------------------------------

def test_all_clean_provenance_leaves_ranking_bit_identical_real_data(mod, counts, real_traj):
    before, _ = mod.compute_bopas(counts, real_traj)
    after = propagate(counts, real_traj, CLEAN)
    assert [r["BOPAS"] for r in before] == [r["BOPAS_adj"] for r in after]
    assert rank_changes(before, after) == []


def test_all_clean_provenance_leaves_ranking_bit_identical_synthetic(mod, counts, synth):
    before, _ = mod.compute_bopas(counts, synth)
    after = propagate(counts, synth, CLEAN)
    assert [r["BOPAS"] for r in before] == [r["BOPAS_adj"] for r in after]
    assert [r["T"] for r in before] == [r["T_adj"] for r in after]
    assert rank_changes(before, after) == []


def test_identity_holds_for_slopes_that_do_not_round_cleanly(mod, counts):
    awkward = [_t(s, 0.1 * (i + 1) / 3.0, half=0.7) for i, s in enumerate(SERIES)]
    before, _ = mod.compute_bopas(counts, awkward)
    after = propagate(counts, awkward, CLEAN)
    assert [r["BOPAS"] for r in before] == [r["BOPAS_adj"] for r in after]


# ---- where provenance multiplies -----------------------------------------------------------

def test_downweighting_a_series_lowers_only_cells_that_have_something_to_lose(counts, synth):
    after = propagate(counts, synth, {**CLEAN, "RR_new_pct": 0.1})
    hit = [r for r in after if r["series"] == "RR_new_pct"]
    assert any(r["BOPAS"] > 0 for r in hit)
    assert all(r["BOPAS_adj"] < r["BOPAS"] for r in hit if r["BOPAS"] > 0)
    # a cell already at zero (M == 0 or T == 0) has nothing to lose and must stay at zero
    assert all(r["BOPAS_adj"] == 0 for r in hit if r["BOPAS"] == 0)
    assert all(r["BOPAS_adj"] == r["BOPAS"] for r in after if r["series"] != "RR_new_pct")


def test_provenance_scales_T_and_leaves_L_M_C_untouched(mod, counts, synth):
    before, _ = mod.compute_bopas(counts, synth)
    after = propagate(counts, synth, {**CLEAN, "RR_new_pct": 0.5})
    b = {(r["intervention"], r["series"]): r for r in before}
    for r in after:
        o = b[(r["intervention"], r["series"])]
        assert (r["L"], r["M"], r["C"], r["T"]) == (o["L"], o["M"], o["C"], o["T"])
        if r["series"] == "RR_new_pct":
            assert r["T_adj"] == pytest.approx(o["T"] * 0.5, abs=1e-3)
        else:
            assert r["T_adj"] == o["T"]


def test_bopas_adj_is_p_times_bopas_to_rounding(mod, counts, synth):
    before, _ = mod.compute_bopas(counts, synth)
    after = propagate(counts, synth, {**CLEAN, "XDR_TSR_pct": 0.25})
    b = {(r["intervention"], r["series"]): r["BOPAS"] for r in before}
    hit = [r for r in after if r["series"] == "XDR_TSR_pct"]
    assert any(r["BOPAS"] > 0 for r in hit)
    for r in hit:
        assert r["BOPAS_adj"] == pytest.approx(0.25 * b[(r["intervention"], r["series"])], abs=1e-3)


def test_zero_provenance_zeroes_the_series_without_negative_zero(counts, synth):
    after = propagate(counts, synth, {**CLEAN, "RR_new_pct": 0.0})
    cells = [r for r in after if r["series"] == "RR_new_pct"]
    assert all(str(r["BOPAS_adj"]) == "0.0" and str(r["T_adj"]) == "0.0" for r in cells)


def test_a_non_worsening_series_with_zero_provenance_prints_positive_zero(counts):
    flat = [_t(s, -1.0) for s in SERIES]   # improving everywhere: T == 0 already
    after = propagate(counts, flat, {**CLEAN, "RR_new_pct": 0.0})
    assert all(str(r["BOPAS_adj"]) == "0.0" and str(r["T_adj"]) == "0.0" for r in after)


def test_propagate_does_not_mutate_its_inputs(counts, synth):
    snap = copy.deepcopy(synth)
    propagate(counts, synth, {**CLEAN, "RR_new_pct": 0.3})
    assert synth == snap


def test_rows_carry_the_provenance_applied(counts, synth):
    after = propagate(counts, synth, {**CLEAN, "RR_new_pct": 0.3})
    assert {r["provenance"] for r in after if r["series"] == "RR_new_pct"} == {0.3}


# ---- unassessable series -------------------------------------------------------------------

def test_none_provenance_is_not_silently_one(counts, synth):
    after = propagate(counts, synth, {**CLEAN, "RR_new_pct": None})
    cells = [r for r in after if r["series"] == "RR_new_pct"]
    assert {r["provenance"] for r in cells} == {None}          # not 1.0
    assert all(r["unassessable"] is True for r in cells)
    assert all(r["unassessable"] is False for r in after if r["series"] != "RR_new_pct")


def test_none_provenance_leaves_cells_unadjusted_and_is_listed(mod, counts, synth):
    before, _ = mod.compute_bopas(counts, synth)
    after = propagate(counts, synth, {**CLEAN, "RR_new_pct": None, "MDR_TSR_pct": None})
    assert sorted(after.unassessable) == ["MDR_TSR_pct", "RR_new_pct"]
    assert [r["BOPAS"] for r in before] == [r["BOPAS_adj"] for r in after]


def test_all_clean_has_empty_unassessable_list(counts, synth):
    assert propagate(counts, synth, CLEAN).unassessable == []


def test_result_is_a_list_of_dicts(counts, synth):
    after = propagate(counts, synth, CLEAN)
    assert isinstance(after, list) and all(isinstance(r, dict) for r in after)


# ---- input validation ----------------------------------------------------------------------

def test_series_missing_from_provenance_raises_rather_than_defaulting_to_clean(counts, synth):
    partial = {k: v for k, v in CLEAN.items() if k != "RR_new_pct"}
    with pytest.raises(ValueError, match="RR_new_pct"):
        propagate(counts, synth, partial)


@pytest.mark.parametrize("bad", [-0.1, 1.0000001, float("nan"), "0.5"])
def test_provenance_outside_unit_interval_raises(counts, synth, bad):
    with pytest.raises(ValueError, match="RR_new_pct"):
        propagate(counts, synth, {**CLEAN, "RR_new_pct": bad})


# ---- rank_changes --------------------------------------------------------------------------

def test_rank_changes_names_which_interventions_moved(mod, counts, synth):
    before, _ = mod.compute_bopas(counts, synth)
    after = propagate(counts, synth, {**CLEAN, "XDR_TSR_pct": 0.01, "MDR_TSR_pct": 0.01})
    ch = rank_changes(before, after)
    assert ch, "downweighting the two strongest series must reorder something"
    assert all(isinstance(c, RankChange) for c in ch)
    assert all(c.rank_before != c.rank_after for c in ch)
    assert all(c.intervention and c.target for c in ch)


def test_rank_changes_reports_correct_ranks():
    before = [dict(intervention="A", target="t", BOPAS=3.0), dict(intervention="B", target="t", BOPAS=2.0)]
    after = [dict(intervention="A", target="t", BOPAS_adj=1.0), dict(intervention="B", target="t", BOPAS_adj=2.0)]
    assert rank_changes(before, after) == [RankChange("A", "t", 1, 2), RankChange("B", "t", 2, 1)]


def test_tied_scores_share_a_rank_so_input_order_cannot_manufacture_a_change():
    before = [dict(intervention="A", target="t", BOPAS=0.0), dict(intervention="B", target="t", BOPAS=0.0)]
    after = [dict(intervention="B", target="t", BOPAS_adj=0.0), dict(intervention="A", target="t", BOPAS_adj=0.0)]
    assert rank_changes(before, after) == []


def test_rank_changes_pairs_cells_by_identity_not_position():
    before = [dict(intervention="A", target="t", BOPAS=3.0), dict(intervention="B", target="t", BOPAS=2.0)]
    after = [dict(intervention="B", target="t", BOPAS_adj=2.0), dict(intervention="A", target="t", BOPAS_adj=3.0)]
    assert rank_changes(before, after) == []


def test_rank_changes_rejects_mismatched_cell_sets():
    before = [dict(intervention="A", target="t", BOPAS=3.0)]
    after = [dict(intervention="B", target="t", BOPAS_adj=3.0)]
    with pytest.raises(ValueError):
        rank_changes(before, after)


# ---- Ruling Z: exactly one triangulation per series ---------------------------------------

def _tri(score=1.0):
    return TestResult(score, True, {"changes": {2020: (0.1, 0.1)}, "agree": [2020]})


def _ident(score=1.0):
    return TestResult(score, True, {"identity": {2020: 1.0}})


def test_provenance_from_results_combines_one_triangulation_with_other_tests():
    p = provenance_from_results({"s": [_ident(0.5), _tri(0.5)]})
    assert p == {"s": pytest.approx(0.5)}


def test_two_triangulation_results_for_one_series_are_refused():
    # change-mode and level-mode answer the same question; both would double-weight T2
    with pytest.raises(ValueError, match="triangulation"):
        provenance_from_results({"s": [_ident(), _tri(), _tri()]})


def test_series_with_no_testable_result_gets_none_not_one():
    p = provenance_from_results({"s": [TestResult(None, False, {"reason": "x"})]})
    assert p == {"s": None}


# ---- the published repository stays untouched -----------------------------------------------

def test_importing_the_published_module_leaves_no_files_in_the_repository(mod):
    for sub in ("code", "outputs"):
        assert not list((REPO / sub).rglob("__pycache__"))
        assert not list((REPO / sub).rglob("*.pyc"))


def test_loader_returns_the_published_function(mod):
    assert load_compute_bopas() is mod.compute_bopas


# ---- the read-only mitigation itself (regressions here would write into a DOI-published repo) --

@pytest.fixture
def fresh_loader(monkeypatch):
    saved = prop._module
    monkeypatch.setattr(prop, "_module", None)
    yield monkeypatch
    prop._module = saved


def _fake_repo(tmp_path, body, outputs=True):
    code = tmp_path / "code"
    code.mkdir()
    (tmp_path / "outputs").mkdir() if outputs else None
    src = code / "fake.py"
    src.write_text(body, encoding="utf-8")
    return src


def test_loading_the_published_module_does_not_disturb_the_global_rng(fresh_loader):
    random.seed(12345)
    state = random.getstate()
    prop._bopas_module()           # the real script calls random.seed(20260908) at import
    assert random.getstate() == state


def test_failed_import_restores_flags_rng_and_caches_nothing(fresh_loader, tmp_path):
    src = _fake_repo(tmp_path, "import random\nrandom.seed(1)\nraise RuntimeError('boom')\n")
    fresh_loader.setattr(prop, "BOPAS_SOURCE", src)
    fresh_loader.setattr(sys, "dont_write_bytecode", False)   # make restoration observable
    random.seed(999)
    state, flag = random.getstate(), sys.dont_write_bytecode
    with pytest.raises(RuntimeError, match="boom"):
        prop._bopas_module()
    assert sys.dont_write_bytecode == flag
    assert random.getstate() == state
    assert prop._module is None
    assert not list(tmp_path.rglob("__pycache__"))


def test_missing_outputs_dir_is_a_loud_failure_not_a_quiet_mkdir(fresh_loader, tmp_path):
    src = _fake_repo(tmp_path, "x = 1\n", outputs=False)
    fresh_loader.setattr(prop, "BOPAS_SOURCE", src)
    with pytest.raises(RuntimeError, match="outputs"):
        prop._bopas_module()
    assert not (tmp_path / "outputs").exists()
    assert prop._module is None


# ---- rank_changes must not be able to emit meaningless movement -----------------------------

def test_cells_zero_before_and_after_are_never_reported():
    row = lambda i, v: dict(intervention=i, target="t", BOPAS=v, BOPAS_adj=v)
    before = [dict(intervention="A", target="t", BOPAS=2.0), dict(intervention="D", target="t", BOPAS=1.0),
              dict(intervention="B", target="t", BOPAS=0.0), dict(intervention="C", target="t", BOPAS=0.0)]
    after = [dict(intervention="A", target="t", BOPAS_adj=0.0), dict(intervention="D", target="t", BOPAS_adj=1.0),
             dict(intervention="B", target="t", BOPAS_adj=0.0), dict(intervention="C", target="t", BOPAS_adj=0.0)]
    # A (2.0 -> 0.0) and D move; B and C were never in contention though A now ties them at rank 2
    assert rank_changes(before, after) == [RankChange("A", "t", 1, 2), RankChange("D", "t", 2, 1)]


def test_zeroing_the_only_live_series_reports_no_rank_movement_for_dead_cells(counts, real_traj):
    after = propagate(counts, real_traj, {**CLEAN, "RRMDR_notif_100k": 0.0})
    before = [{k: v for k, v in r.items()} for r in after]
    ch = rank_changes(before, after)
    assert len(ch) <= 11            # only the 11 live cells can move; never 59
    live = {(r["intervention"], r["target"]) for r in before if r["BOPAS"] > 0}
    assert {(c.intervention, c.target) for c in ch} <= live


def test_unassessable_cells_are_excluded_from_the_ranking_not_ranked_as_clean(counts, synth, mod):
    before, _ = mod.compute_bopas(counts, synth)
    p = {**CLEAN, "XDR_TSR_pct": None, "RR_new_pct": 0.1, "MDR_TSR_pct": 0.1}
    after = propagate(counts, synth, p)
    ch = rank_changes(before, after)
    assert not any(c.target.startswith("XDR_TSR_pct") for c in ch)
    # ranks are computed among assessable cells only: unassessable cells hold no rank slot
    assessable = [r for r in after if not r["unassessable"]]
    top = max(assessable, key=lambda r: r["BOPAS_adj"])
    top_rank_after = [c.rank_after for c in ch if (c.intervention, c.target) == (top["intervention"], top["target"])]
    assert top_rank_after in ([], [1])


def test_unassessable_series_cells_are_listed_apart_from_the_ranking(counts, synth):
    after = propagate(counts, synth, {**CLEAN, "XDR_TSR_pct": None})
    cells = after.unassessable_cells
    assert {c["series"] for c in cells} == {"XDR_TSR_pct"}
    assert len(cells) == sum(1 for r in after if r["series"] == "XDR_TSR_pct")
    assert all({"intervention", "target", "series"} <= set(c) for c in cells)
    assert propagate(counts, synth, CLEAN).unassessable_cells == []


def test_unassessable_cells_never_appear_in_rank_changes_even_when_they_lead(counts, synth, mod):
    before, _ = mod.compute_bopas(counts, synth)
    after = propagate(counts, synth, {**CLEAN, "XDR_TSR_pct": None, "RRMDR_notif_100k": 0.01})
    xdr_label = "XDR_TSR_pct label"
    assert all(c.target != xdr_label for c in rank_changes(before, after))


# ---- duplicate series ------------------------------------------------------------------------

def test_duplicate_series_in_traj_rows_raises(counts, synth):
    with pytest.raises(ValueError, match="RR_new_pct"):
        propagate(counts, synth + [synth[0]], CLEAN)
