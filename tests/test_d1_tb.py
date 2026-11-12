"""Task 11: D1, the TB demonstration end to end.

The null result is the honest outcome on this data, so most of these tests exist to make sure a
null cannot be faked by an empty file or an empty dict: counts are checked against independent
reads of the published repository, and the machinery is exercised on a grid where reordering IS
possible.
"""
import csv
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos"))
import d1_tb                                                       # noqa: E402
from d1_tb import OUTPUTS, SUMMARY, main                           # noqa: E402

REPO = ROOT.parent / "tb_bopas_repo"
NTEP = ["RRMDR_notif_100k", "RR_new_pct", "preXDR_fqr_pct", "MDR_TSR_pct", "XDR_TSR_pct", "BDQ_res_pct"]
BOPAS5 = NTEP[:5]
FILES = ("d1_provenance_scores.csv", "d1_rank_changes.csv", "d1_evpr.csv", "d1_invisibility.csv")


def _csv(name):
    with open(OUTPUTS / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture(scope="module", autouse=True)
def ran():
    """Delete the outputs first (outputs/ is gitignored, so they must be GENERATED, never assumed)."""
    for f in (*FILES, "d1_summary.txt", "d1_financing_audit.csv"):
        (OUTPUTS / f).unlink(missing_ok=True)
    before = sorted(p.name for p in (REPO / "outputs").iterdir())
    text = main()
    assert sorted(p.name for p in (REPO / "outputs").iterdir()) == before   # read-only repo untouched
    return text


@pytest.fixture(scope="module")
def inputs():
    return d1_tb.load_bopas_inputs()


# ---- the four tests of the brief --------------------------------------------------------------

def test_d1_runs_end_to_end_and_writes_four_outputs():
    for f in FILES:
        assert (OUTPUTS / f).exists() and (OUTPUTS / f).stat().st_size > 0


def test_demonstration_reports_whether_any_rank_changed():
    out = (OUTPUTS / "d1_rank_changes.csv").read_text()
    assert "rank_before" in out
    n = int(re.search(r"of any kind: (\d+)", SUMMARY.read_text()).group(1))
    assert n == len(_csv("d1_rank_changes.csv"))     # the file and the stated count agree


def test_audits_the_bopas_input_series_not_the_financing_series():
    scores = (OUTPUTS / "d1_provenance_scores.csv").read_text()
    assert "RRMDR_notif_100k" in scores
    assert "budget_tpt" not in scores and "budget_" not in scores
    assert {r["series"] for r in _csv("d1_provenance_scores.csv")} == set(NTEP)
    assert "budget_tpt" in (OUTPUTS / "d1_financing_audit.csv").read_text()   # its own section


def test_null_reordering_is_stated_not_hidden():
    text = SUMMARY.read_text().lower()
    assert "cannot reorder" in text
    assert "by construction" in text and "degenerate" in text and "d2/d3" in text
    assert "[-0.11, +0.30]" in SUMMARY.read_text()          # the published slope CI, in the words
    assert "inversions: 0" in text and "tie splits: 0" in text
    # the null is attributed to BOTH the data and the design (one scalar per series reorders only
    # across series), not to BOPAS alone
    assert "the design" in text and "the data" in text and "only reorder cells across series" in text
    assert "zero instances of reordering anywhere" in text
    assert "t2 is untestable for all six" in text


# ---- the null is checked against independent reads, so an empty result cannot pass ------------

def test_structure_of_the_null_matches_the_published_output_independently():
    with open(REPO / "outputs" / "ijtb_bopas_long.csv", newline="", encoding="utf-8") as fh:
        pub = list(csv.DictReader(fh))
    live = [r for r in pub if float(r["BOPAS"]) > 0]
    assert len(pub) == 60 and len(live) == 11 and {r["series"] for r in live} == {"RRMDR_notif_100k"}
    text = SUMMARY.read_text()
    assert "49 of 60 cells score exactly 0.0" in text and "all 11" in text


def test_summary_slope_ci_equals_the_published_ci(inputs):
    with open(REPO / "outputs" / "ijtb_slopes.csv", newline="", encoding="utf-8") as fh:
        row = next(r for r in csv.DictReader(fh) if r["series"] == "RRMDR_notif_100k")
    t = next(t for t in inputs[1] if t["series"] == "RRMDR_notif_100k")
    assert (t["primary_lo"], t["primary_hi"]) == (float(row["primary_lo"]), float(row["primary_hi"]))
    assert float(row["primary_lo"]) < 0 < float(row["primary_hi"])


def test_zero_rank_changes_and_no_unassessable_cells_on_real_data(inputs):
    counts, traj = inputs
    results, _ = d1_tb.audit_ntep()
    prov = {s: d1_tb.provenance_from_results({k: d1_tb.composite_inputs(v) for k, v in results.items()})[s]
            for s in BOPAS5}
    rr = d1_tb.rank_report(counts, traj, prov)
    assert (rr["n_cells"], rr["n_live"], rr["n_zero"]) == (60, 11, 49)
    assert rr["live_series"] == ["RRMDR_notif_100k"]
    assert rr["inversions"] == []                    # no pair of cells traded places
    # With the symmetric step size RRMDR_notif_100k's composite is 0.786 and the rounding tie that
    # used to split (Milk 9 -> 10 at 0.926) no longer does. The tie itself is still in the published
    # scores: two cells share 0.033, which is what a tie_split would act on.
    assert rr["changes"] == [] and rr["tie_splits"] == []
    pub = {r["intervention"][:4]: r["BOPAS"] for r in rr["rows"] if r["series"] == "RRMDR_notif_100k"}
    assert pub["Milk"] == pub["Nutr"] == 0.033
    assert rr["unassessable_cells"] == [] and rr["unassessable_series"] == []
    # the live series really is down-weighted, so the null is not "nothing was audited"
    assert prov["RRMDR_notif_100k"] < 1.0


def test_stress_test_sweeps_the_whole_provenance_range(inputs):
    counts, traj = inputs
    sweep = d1_tb.stress_test(counts, traj, "RRMDR_notif_100k")
    assert sweep[0][0] == 0.0 and sweep[-1][0] == 1.0 and len(sweep) == 21
    assert all(inv == 0 for _, inv, _ in sweep)          # never a strict inversion
    assert sweep[-1][2] == 0                             # provenance 1.0 changes nothing
    assert sweep[0][2] > 0                               # 0.0 wipes the series: the sweep is not vacuous


# ---- the machinery CAN report change (mutation guards) ----------------------------------------

def _t(series, slope, sign=+1):
    return dict(series=series, label=series, sign=sign, slope_primary=slope,
                primary_lo=slope - 1.0, primary_hi=slope + 1.0, classification_primary="x")


@pytest.fixture(scope="module")
def synth():
    return [_t("RR_new_pct", 1.0), _t("RRMDR_notif_100k", 2.0), _t("preXDR_fqr_pct", 3.0),
            _t("MDR_TSR_pct", -4.0, -1), _t("XDR_TSR_pct", -5.0, -1)]


def test_rank_report_reports_changes_when_series_can_trade_places(inputs, synth):
    counts, _ = inputs
    prov = {s: 1.0 for s in BOPAS5}
    prov["XDR_TSR_pct"] = 0.05
    rr = d1_tb.rank_report(counts, synth, prov)
    assert len(rr["changes"]) > 0 and len(rr["inversions"]) > 0 and len(rr["live_series"]) > 1
    assert all(c.kind == "inversion" for c in rr["inversions"])
    assert d1_tb.is_structural_null(rr, None) is False


def test_rank_changes_writer_writes_every_change(tmp_path, inputs, synth):
    counts, _ = inputs
    rr = d1_tb.rank_report(counts, synth, {**{s: 1.0 for s in BOPAS5}, "XDR_TSR_pct": 0.05})
    p = tmp_path / "rc.csv"
    d1_tb.write_rank_changes(p, rr["changes"])
    with open(p, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == len(rr["changes"]) > 0
    assert set(rows[0]) == {"intervention", "target", "rank_before", "rank_after", "kind"}


def test_unassessable_series_cells_are_reported_apart_and_not_ranked(inputs, synth):
    counts, _ = inputs
    prov = {s: 1.0 for s in BOPAS5}
    prov["XDR_TSR_pct"] = None
    rr = d1_tb.rank_report(counts, synth, prov)
    assert rr["unassessable_series"] == ["XDR_TSR_pct"] and len(rr["unassessable_cells"]) == 12
    assert not any(c.target == "XDR_TSR_pct" for c in rr["changes"])


# ---- T1-T4 on the NTEP inputs ------------------------------------------------------------------

def test_t1_reconciles_all_42_ntep_rows_but_is_untestable_because_it_is_self_derived():
    # I1: value, numerator and denominator come from ONE file, so the identity can fail only on a
    # transcription slip. It is reported as such and kept out of the composite, never scored 1.0.
    results, _ = d1_tb.audit_ntep()
    n = ok = 0
    for key in NTEP:
        d = results[key][0].detail
        n += len(d["identity"])
        ok += len(d["clean"])
    assert n == 42 and ok == 42
    assert all(not results[k][0].testable and results[k][0].score is None for k in NTEP)
    assert all("self-derived" in results[k][0].detail["reason"] for k in NTEP)


def test_t2_is_untestable_for_every_ntep_series_and_one_triangulation_each():
    results, _ = d1_tb.audit_ntep()
    for key in NTEP:
        assert len(results[key]) == 4
        assert results[key][1].testable is False and results[key][1].score is None


def test_t3_bound_is_leave_one_out_not_self_referential():
    _, loo = d1_tb.audit_ntep()
    _, pooled = d1_tb.audit_ntep(pooled_reference=True)
    assert len(set(loo.values())) > 1 and set(pooled.values()) == {next(iter(pooled.values()))}
    assert loo["RRMDR_notif_100k"] != pooled["RRMDR_notif_100k"]


def test_scores_csv_carries_the_evidence_weight_beside_each_composite():
    rows = {r["series"]: r for r in _csv("d1_provenance_scores.csv")}
    r = rows["RRMDR_notif_100k"]
    assert r["n_testable"] == "1" and r["min_observations"] == "7"
    assert r["observations"] == "declared=7"                 # T1 (self-derived) contributes nothing
    assert r["T1_identity"] == "untestable"
    assert r["collapsed_by"] == "" and 0.0 < float(r["composite_geometric"]) < 1.0
    assert rows["BDQ_res_pct"]["in_bopas_grid"] == "False"
    for row in rows.values():
        assert {"n_testable", "observations", "collapsed_by"} <= set(row)


# ---- EVPR --------------------------------------------------------------------------------------

def test_evpr_is_reported_for_every_prior_and_series_with_se():
    rows = _csv("d1_evpr.csv")
    assert len(rows) == 15 and {r["prior"] for r in rows} == {"beta", "uniform", "floor"}
    assert {r["series"] for r in rows} == set(BOPAS5)
    assert all(float(r["evpr"]) == 0.0 and float(r["se"]) == 0.0 for r in rows)
    assert "evpr_rounded" in rows[0]


def test_evpr_is_not_always_zero_when_the_decision_can_change(inputs, synth):
    # guard against a pipeline that returns zeros whatever it is given
    counts, _ = inputs
    results, _ = d1_tb.audit_ntep()
    prov = {s: 0.5 for s in BOPAS5}
    obs = {s: 10 for s in BOPAS5}
    ev = d1_tb.evpr_prior_sensitivity(counts, synth, prov, observations=obs, draws=2000)
    assert any(v > 0 for d in ev.values() for v, _ in d.values())


# ---- the financing section: separate, and consistent with FINDINGS.md --------------------------

def test_financing_audit_reproduces_the_recorded_findings():
    fin = d1_tb.audit_financing()
    assert fin["bound"] == pytest.approx(4.132, abs=5e-4) and fin["n_steps"] == 691
    assert fin["n_countries"] == 215
    tpt = fin["t1"]["budget_tpt"]
    # direction pinned: implied (unit cost x volume) over reported. >1 means the parts exceed the total
    assert tpt.detail["identity"][2023] == pytest.approx(0.90, abs=0.005)
    assert tpt.detail["identity"][2024] == pytest.approx(3.33, abs=0.01)
    assert tpt.detail["identity"][2025] == pytest.approx(9.14, abs=0.01)
    assert tpt.score == pytest.approx(2 / 3, abs=1e-4)
    assert fin["t1"]["exp_tot"].detail["incomplete"] == [2026]
    for k in ("budget_tot", "cf_tot"):
        assert fin["t1"][k].score == 1.0
    for k in ("exp_tot", "rcvd_tot", "rcvd_tot_by_source"):      # arithmetic reconciles; 2026 is incomplete
        d = fin["t1"][k].detail
        assert len(d["identity"]) == 9 and all(0.9 <= v <= 1.1 for v in d["identity"].values())
        assert d["incomplete"] == [2026]
    # level-mode T2: WHO's funding gap contradicts the India TB Report in every year (FINDINGS 1.1)
    assert fin["t2"]["funding_gap"].score == 0.0
    # I3: the cross-country reference is not stable (p95 step ~ 5-fold; ~28% of steps exactly zero),
    # so T3/T4 on budget_cpp_xdr are NOT TESTABLE. They are not reported as a clean 1.0.
    cpp = next(r for r in fin["rows"] if r["series"] == "budget_cpp_xdr" and r["test"].startswith("T3"))
    assert cpp["testable"] is False and cpp["score"] == "" and "not stable" in cpp["note"]
    assert fin["t3"].testable is False and fin["t4"].testable is False
    assert fin["zero_share"] == pytest.approx(0.279, abs=0.001)


def test_invisibility_csv_matches_findings():
    rows = _csv("d1_invisibility.csv")
    assert len(rows) == 11
    none = {int(r["evidence_rank"]) for r in rows if r["coverage"] == "none"}
    assert none == {2, 4, 5, 7, 8, 10}
    assert {int(r["evidence_rank"]) for r in rows if r["coverage"] == "partial"} == {3, 6, 11}


# ---- Ruling GG: T4 subsumes T3 in the composite; both are still reported --------------------------

def test_t3_does_not_enter_the_composite_when_t4_is_testable():
    results, _ = d1_tb.audit_ntep()
    for key in NTEP:
        used = d1_tb.composite_inputs(results[key])
        names = [d1_tb.composite_report([r]).observations for r in used]
        flat = {n for o in names for n in o}
        assert "implausibility" not in flat and "declared" in flat
    rep = {r["series"]: r for r in _csv("d1_provenance_scores.csv")}
    assert "implausibility" not in rep["RRMDR_notif_100k"]["observations"]
    assert rep["RRMDR_notif_100k"]["n_testable"] == "1"


def test_composite_is_t4_alone_because_t1_and_t2_are_untestable():
    results, _ = d1_tb.audit_ntep()
    prov = d1_tb.provenance_from_results({k: d1_tb.composite_inputs(v) for k, v in results.items()})
    for k in NTEP:
        assert prov[k] == pytest.approx(results[k][3].score)
    assert prov["RRMDR_notif_100k"] == pytest.approx(5.5 / 7)     # 5 clean steps + a half-credited declared one


def test_t3_is_used_when_t4_is_untestable():
    from provenance.series import TestResult
    t3 = TestResult(0.5, True, {"changes": {2001: 1.0}, "exceed": [2001]})
    t4 = TestResult(None, False, {})
    t1 = TestResult(1.0, True, {"identity": {2001: 1.0}, "incomplete": []})
    used = d1_tb.composite_inputs([t1, TestResult(None, False, {}), t3, t4])
    assert [r for r in used if r.testable] == [t1, t3]


def test_both_t3_and_t4_scores_are_still_reported_side_by_side():
    r = {x["series"]: x for x in _csv("d1_provenance_scores.csv")}["RRMDR_notif_100k"]
    assert r["T3_implausibility"] != "" and r["T4_declared"] != ""


# ---- C2/C3: the symmetric step size, the known case, and the one positive result ------------------

def test_known_declared_break_is_detected_and_the_disclosure_mechanism_fires_on_real_data():
    # C3. Under the old asymmetric statistic the 2020 step (-25.7%) was invisible at the derived bound
    # (|c| = 0.257 < 0.321), declared[] was empty for all six series and T4 == T3 everywhere, so the
    # disclosure mechanism had never run on real data. The bound is unchanged by the fix (0.3211).
    results, bounds = d1_tb.audit_ntep()
    assert bounds["RRMDR_notif_100k"] == pytest.approx(0.3211, abs=5e-5)
    r = results["RRMDR_notif_100k"]
    assert r[3].detail["declared"] == [2020] and r[3].detail["silent"] == [2018]
    assert r[3].score > r[2].score                                   # T4 credits the disclosure
    assert r[2].score == pytest.approx(5 / 7) and r[3].score == pytest.approx(5.5 / 7)
    for k in NTEP:
        if k != "RRMDR_notif_100k":
            assert results[k][3].detail["declared"] == []
    known = d1_tb.known_cases(results, d1_tb.load_trajectories(d1_tb.NTEP_TRAJECTORIES_CSV))
    assert [(k["series"], k["year"], k["flagged"]) for k in known] == [("RRMDR_notif_100k", 2020, True)]


def test_known_case_miss_is_reported_not_hidden():
    # the generator must be able to say MISSED: a note on a year whose step is within the bound
    from provenance.series import IndicatorSeries
    s = IndicatorSeries("k", "k", [2019, 2020, 2021], [1.0, 1.01, 1.02], "t", {2021: "changed"}, {})
    from provenance.implausibility import implausibility_score
    from provenance.declared import declared_score
    res = {"k": [None, None, implausibility_score(s, bound=0.5), declared_score(s, bound=0.5)]}
    (k,) = d1_tb.known_cases(res, {"k": s})
    assert k["comparable"] and not k["flagged"]


def test_the_positive_result_rr_new_pct_2021_is_flagged_silent_and_persistent():
    # The strongest evidence the instrument works: an undeclared +82.5% level shift on the series the
    # spec names as motivating case 1, found by a bound derived WITHOUT reference to it (leave-one-out).
    results, bounds = d1_tb.audit_ntep()
    s = d1_tb.load_trajectories(d1_tb.NTEP_TRAJECTORIES_CSV)["RR_new_pct"]
    by = dict(zip(s.years, s.values))
    flags = d1_tb.flagged_steps(results, {k: v for k, v in d1_tb.load_trajectories(
        d1_tb.NTEP_TRAJECTORIES_CSV).items()})
    (f,) = [x for x in flags if x["series"] == "RR_new_pct"]
    assert f["year"] == 2021 and not f["declared"] and s.notes == {}
    assert (f["prev"], f["value"]) == (2.5927, 4.732) and f["change"] == pytest.approx(0.825, abs=5e-4)
    assert f["size"] > bounds["RR_new_pct"] and bounds["RR_new_pct"] == pytest.approx(0.3367, abs=5e-5)
    assert min(by[y] for y in (2021, 2022, 2023, 2024)) > by[2020]       # stays above the pre-shift level
    text = SUMMARY.read_text()
    assert "RR_new_pct 2021: 2.5927 -> 4.732 (+82.5%" in text and "SILENT" in text


def test_summary_states_the_stress_interior_count_it_computed():
    # M5: the "19 interior values" was a hardcoded literal; it is now computed from the sweep.
    assert re.search(r"at 12 of the 19 interior values", SUMMARY.read_text())


def test_narrative_never_claims_not_single_axis_when_it_is_single_axis(inputs):
    # I8: with one live series, no inversions and a slope CI that EXCLUDES zero, the old narrative
    # fell through to "the grid is not the single-axis degenerate case". It must not say that.
    counts, traj = inputs
    results, bounds = d1_tb.audit_ntep()
    prov = d1_tb.provenance_from_results({k: d1_tb.composite_inputs(v) for k, v in results.items()})
    rr = d1_tb.rank_report(counts, traj, {s: prov[s] for s in BOPAS5})
    series = d1_tb.load_trajectories(d1_tb.NTEP_TRAJECTORIES_CSV)
    srows, _ = d1_tb.score_rows(results, bounds, BOPAS5)

    def build(live_ci, structural):
        return d1_tb.build_summary(dict(
            rank=rr, score_rows=srows, prov=prov, t1_ok=42, t1_n=42, structural_null=structural,
            live_ci=live_ci, stress_max=0, stress_ties=[], stress_interior=19, evpr={},
            fin=d1_tb.audit_financing(), invis=d1_tb.invisibility_rows(), pooled_note="x",
            flags=d1_tb.flagged_steps(results, series), known=d1_tb.known_cases(results, series)))

    assert d1_tb.is_structural_null(rr, (-0.1, 0.3)) is True
    assert d1_tb.is_structural_null(rr, (0.1, 0.3)) is False             # CI excludes zero
    text = build((0.1, 0.3), False)
    assert "not the single-axis degenerate case" not in text
    assert "single-series case" in text and "does not span zero" in text
    assert "not the single-axis degenerate case" not in build((-0.1, 0.3), True)
    # empty EVPR must not print the zero claim vacuously (M7)
    assert "Every EVPR is exactly 0.0" not in text
