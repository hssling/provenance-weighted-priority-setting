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
    n = int(re.search(r"changed rank: (\d+)", SUMMARY.read_text()).group(1))
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
    assert "rounding artefact" in text and "strict order inverted: 0" in text


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
    prov = {s: d1_tb.provenance_from_results(results)[s] for s in BOPAS5}
    rr = d1_tb.rank_report(counts, traj, prov)
    assert (rr["n_cells"], rr["n_live"], rr["n_zero"]) == (60, 11, 49)
    assert rr["live_series"] == ["RRMDR_notif_100k"]
    assert rr["inversions"] == []                    # no pair of cells traded places
    # the one literal rank change is a rounding tie being split: two cells share a published score
    assert [(c.intervention[:4], c.rank_before, c.rank_after) for c in rr["changes"]] == [("Milk", 9, 10)]
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
    assert d1_tb.is_structural_null(rr, None) is False


def test_rank_changes_writer_writes_every_change(tmp_path, inputs, synth):
    counts, _ = inputs
    rr = d1_tb.rank_report(counts, synth, {**{s: 1.0 for s in BOPAS5}, "XDR_TSR_pct": 0.05})
    p = tmp_path / "rc.csv"
    d1_tb.write_rank_changes(p, rr["changes"])
    with open(p, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == len(rr["changes"]) > 0
    assert set(rows[0]) == {"intervention", "target", "rank_before", "rank_after"}


def test_unassessable_series_cells_are_reported_apart_and_not_ranked(inputs, synth):
    counts, _ = inputs
    prov = {s: 1.0 for s in BOPAS5}
    prov["XDR_TSR_pct"] = None
    rr = d1_tb.rank_report(counts, synth, prov)
    assert rr["unassessable_series"] == ["XDR_TSR_pct"] and len(rr["unassessable_cells"]) == 12
    assert not any(c.target == "XDR_TSR_pct" for c in rr["changes"])


# ---- T1-T4 on the NTEP inputs ------------------------------------------------------------------

def test_t1_reconciles_all_42_ntep_rows():
    results, _ = d1_tb.audit_ntep()
    n = ok = 0
    for key in NTEP:
        d = results[key][0].detail["identity"]
        n += len(d)
        ok += sum(1 for v in d.values() if 0.9 <= v <= 1.1)
    assert n == 42 and ok == 42
    assert all(results[k][0].testable and results[k][0].score == 1.0 for k in NTEP)


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
    assert r["n_testable"] == "3" and r["min_observations"] == "7"
    assert "identity=8" in r["observations"] and "implausibility=7" in r["observations"]
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
    assert fin["bound"] == pytest.approx(1.917, abs=5e-4) and fin["n_steps"] == 691
    assert fin["n_countries"] == 215
    tpt = fin["t1"]["budget_tpt"].detail["identity"]
    assert tpt[2024] == pytest.approx(3.3, abs=0.1) or 1 / tpt[2024] == pytest.approx(3.3, abs=0.1)
    assert tpt[2025] == pytest.approx(9.1, abs=0.1) or 1 / tpt[2025] == pytest.approx(9.1, abs=0.1)
    assert fin["t1"]["exp_tot"].detail["incomplete"] == [2026]
    for k in ("budget_tot", "cf_tot"):
        assert fin["t1"][k].score == 1.0
    for k in ("exp_tot", "rcvd_tot", "rcvd_tot_by_source"):      # arithmetic reconciles; 2026 is incomplete
        d = fin["t1"][k].detail
        assert len(d["identity"]) == 9 and all(0.9 <= v <= 1.1 for v in d["identity"].values())
        assert d["incomplete"] == [2026]
    # level-mode T2: WHO's funding gap contradicts the India TB Report in every year (FINDINGS 1.1)
    assert fin["t2"]["funding_gap"].score == 0.0
    cpp = next(r for r in fin["rows"] if r["series"] == "budget_cpp_xdr" and r["test"].startswith("T3"))
    assert cpp["score"] == 1.0


def test_invisibility_csv_matches_findings():
    rows = _csv("d1_invisibility.csv")
    assert len(rows) == 11
    none = {int(r["evidence_rank"]) for r in rows if r["coverage"] == "none"}
    assert none == {2, 4, 5, 7, 8, 10}
    assert {int(r["evidence_rank"]) for r in rows if r["coverage"] == "partial"} == {3, 6, 11}
