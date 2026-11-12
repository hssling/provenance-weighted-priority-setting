"""D1: the provenance instrument end to end on India's TB data. Standard library only.

Two audits, kept apart (Ruling AA):

  1. THE BOPAS INPUTS. The six epidemiological series in tb_bopas_repo/data/ntep_trajectories.csv
     are audited with T1-T4, composed, propagated into BOPAS, ranked, and priced with EVPR.
  2. THE FINANCING DATA. WHO budget/expenditure and the India TB Report are audited in their own
     right (T1-T3, T5). Nothing from this section is propagated: the provenance of a budget line
     says nothing about the provenance of a notification rate.

Writes outputs/d1_*.csv and outputs/d1_summary.txt, and prints the summary. The null result
(provenance cannot reorder this BOPAS ranking) is computed, stated in words, and never left to be
inferred from an empty file (Ruling BB).
"""
from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from provenance import propagate as prop                                          # noqa: E402
from provenance.composite import composite_report, composite_sensitivity          # noqa: E402
from provenance.declared import declared_score                                    # noqa: E402
from provenance.evpr import (PRIORS, evpr_prior_sensitivity, observations_from_results,  # noqa: E402
                             round_to_se)
from provenance.existence import (NODE_LABELS, TB_BUDGET_MAPPING, TB_BUDGET_PARTIAL,  # noqa: E402
                                  existence_report)
from provenance.identity import identity_score                                    # noqa: E402
from provenance.implausibility import derive_bound, implausibility_score          # noqa: E402
from provenance.propagate import provenance_from_results, rank_changes            # noqa: E402
from provenance.series import (BUDGET_CSV, EXP_CSV, ITR_CSV, NTEP_TRAJECTORIES_CSV,  # noqa: E402
                               IndicatorSeries, load_india_tb_report, load_trajectories,
                               load_who_budget, load_who_expenditure)
from provenance.triangulate import _changes, ratio_series, triangulate_score      # noqa: E402

OUTPUTS = ROOT / "outputs"
SUMMARY = OUTPUTS / "d1_summary.txt"
SCORES_CSV = OUTPUTS / "d1_provenance_scores.csv"
RANKS_CSV = OUTPUTS / "d1_rank_changes.csv"
EVPR_CSV = OUTPUTS / "d1_evpr.csv"
INVIS_CSV = OUTPUTS / "d1_invisibility.csv"
FIN_CSV = OUTPUTS / "d1_financing_audit.csv"

BOPAS_SEED = 20260908     # the published script's seed; reproduces its published bootstrap CIs
ISO3 = "IND"
PERCENTILE = 0.95         # fixed a priori (see implausibility.DEFAULT_PERCENTILE); sensitivity is reported
DRAWS = 10_000
_SCALE = {"_pct": 100.0, "_100k": 100_000.0}   # value = scale * numerator / denominator
_TESTS = ("identity", "triangulation", "implausibility", "declared")


# ---------------------------------------------------------------- section 1: the BOPAS inputs

def _ntep_rows() -> list[dict]:
    with open(NTEP_TRAJECTORIES_CSV, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _identity_view(series: IndicatorSeries, rows: list[dict]) -> IndicatorSeries:
    """value = scale * numerator / denominator, as a 'product' identity: unit_cost = scale/den,
    volume = numerator. Checks that the file's own value reconciles with its own counts."""
    scale = next((v for suf, v in _SCALE.items() if series.key.endswith(suf)), None)
    if scale is None:
        raise ValueError(f"no scale known for series {series.key!r}")
    by_year = {int(r["year"]): r for r in rows if r["series"] == series.key}
    unit = [scale / float(by_year[y]["denominator"]) for y in series.years]
    vol = [float(by_year[y]["numerator"]) for y in series.years]
    return IndicatorSeries(series.key, series.label, list(series.years), list(series.values),
                           series.source, dict(series.notes), {"unit_cost": unit, "volume": vol},
                           "product")


def composite_inputs(results: list) -> list:
    """The results that enter a series' composite: T1, T2, and ONE of T4 / T3 (Ruling GG).

    T4 (declared-break alignment) is T3 (implausibility) on the SAME steps, with credit for a
    disclosed break: identical to T3 where nothing is declared, more generous where something is.
    Combining both would penalise one implausible step twice and treat the two as independent
    evidence when one strictly contains the other. So when T4 is testable only T4 enters; T3 enters
    only when T4 is untestable. Both scores are still REPORTED (d1_provenance_scores.csv). Do not
    re-add T3 to the composite: its absence is deliberate, not an oversight.
    Order of `results` is (T1 identity, T2 triangulation, T3 implausibility, T4 declared).
    """
    t1, t2, t3, t4 = results
    return [t1, t2, t4 if t4.testable else t3]


def audit_ntep(percentile: float = PERCENTILE, pooled_reference: bool = False):
    """T1-T4 per NTEP series -> (results_by_series, bounds).

    T3/T4 bound: DERIVED from the OTHER epidemiological series in the file (leave-one-out), so no
    series sets its own yardstick. `pooled_reference=True` pools all six (sensitivity only).
    T2: no series has an independent second source anywhere in this repository, so it is run with
    no counterpart and returns untestable. One triangulation result per series (Ruling Z).
    """
    series = load_trajectories(NTEP_TRAJECTORIES_CSV)
    rows = _ntep_rows()
    results, bounds = {}, {}
    for key, s in series.items():
        ref = list(series.values()) if pooled_reference else [o for k, o in series.items() if k != key]
        bound = derive_bound(ref, percentile=percentile)
        bounds[key] = bound
        results[key] = [identity_score(_identity_view(s, rows)),
                        triangulate_score(s, None, mode="level"),
                        implausibility_score(s, bound=bound),
                        declared_score(s, bound=bound)]
    return results, bounds


def load_bopas_inputs(seed: int = BOPAS_SEED):
    """(node_counts, traj_rows) from the published repository. The bootstrap CIs depend on the
    global RNG, so it is seeded as the published script seeds it (and restored): the CIs then
    match the published ijtb_slopes.csv exactly instead of varying from run to run."""
    mod = prop._bopas_module()
    counts = mod.code_corpus(mod._read_corpus(), corrected=True)
    by_series, _ = mod.load_series()
    state = random.getstate()
    random.seed(seed)
    try:
        traj = mod.fit_trajectories(by_series)
    finally:
        random.setstate(state)
    return counts, traj


def rank_report(counts, traj, provenance: dict[str, float | None]) -> dict:
    """Propagate, rank, and describe the structure of the grid. Pure; used by main and the tests."""
    rows = prop.propagate(counts, traj, provenance)
    changes = rank_changes(rows, rows)     # BOPAS (published) vs BOPAS_adj, both carried by each row
    live = [r for r in rows if r["BOPAS"] > 0]
    # rank_changes classifies each change (Ruling HH). An inversion is a real reordering: cells with
    # distinct scores traded places. A tie_split is a tie created or broken by the published
    # 3-decimal rounding, which is monotone and so can never invert an order.
    inversions = [c for c in changes if c.kind == "inversion"]
    tie_splits = [c for c in changes if c.kind == "tie_split"]
    return {
        "rows": rows, "changes": changes, "inversions": inversions,
        "tie_splits": tie_splits, "n_cells": len(rows),
        "n_live": len(live), "n_zero": len(rows) - len(live),
        "live_series": sorted({r["series"] for r in live}),
        "unassessable_series": list(rows.unassessable),
        "unassessable_cells": list(rows.unassessable_cells),
    }


def is_structural_null(rr: dict, live_ci) -> bool:
    """True only when the null is the degenerate kind: every positive cell in ONE series, no pair
    of cells with distinct scores trading places, and that series' slope CI spans zero. Rank
    changes that are only rounding ties do not make the grid reorderable."""
    return (len(rr["live_series"]) == 1 and len(rr["inversions"]) == 0 and live_ci is not None
            and live_ci[0] < 0 < live_ci[1])


def stress_test(counts, traj, live_series: str, grid=None) -> list[tuple[float, int, int]]:
    """Provenance of the live series over a grid -> (value, strict inversions, literal rank changes).
    Evidence that the null is structural rather than an accident of the audited values. Literal
    changes are non-zero at some values (rounding ties; at 0.0 the series is wiped out and all its
    cells tie at zero); strict inversions are zero everywhere."""
    grid = grid or [i / 20 for i in range(21)]
    base = {t["series"]: 1.0 for t in traj}
    out = []
    for p in grid:
        rr = rank_report(counts, traj, {**base, live_series: p})
        out.append((p, len(rr["inversions"]), len(rr["changes"])))
    return out


# ---------------------------------------------------------------- section 2: the financing audit

def _restrict(s: IndicatorSeries, years: list[int]) -> IndicatorSeries:
    by = dict(zip(s.years, s.values))
    return IndicatorSeries(s.key, s.label, list(years), [by.get(y) for y in years], s.source)


def _gap(num, den, years, key, label) -> IndicatorSeries:
    return ratio_series(_restrict(num, years), _restrict(den, years), key=key, label=label)


def _all_countries(key: str) -> list[IndicatorSeries]:
    with open(BUDGET_CSV, newline="", encoding="utf-8-sig") as fh:
        iso = sorted({r["iso3"] for r in csv.DictReader(fh)})
    found = (load_who_budget(BUDGET_CSV, c).get(key) for c in iso)
    return [s for s in found if s is not None]


def audit_financing() -> dict:
    """T1, T3, T4 and level-mode T2 on India's financing data. Reported; never propagated."""
    bud, exp = load_who_budget(BUDGET_CSV, ISO3), load_who_expenditure(EXP_CSV, ISO3)
    itr = load_india_tb_report(ITR_CSV)
    rows = []

    def add(series, test, res, note=""):
        rows.append(dict(series=series, test=test, testable=res.testable,
                         score="" if res.score is None else round(res.score, 4), note=note))

    t1 = {}
    pick = [(k, bud[k]) for k in ("budget_tpt", "budget_tot", "cf_tot")] + \
           [(k, exp[k]) for k in ("exp_tot", "rcvd_tot", "rcvd_tot_by_source")]
    for key, s in pick:
        r = identity_score(s)
        t1[key] = r
        n = len(set(r.detail["identity"]) | set(r.detail["incomplete"]))
        note = f"{n} testable years"
        if r.detail["incomplete"]:
            note += f"; total reported with every component absent in {r.detail['incomplete']}"
        off = {y: round(v, 2) for y, v in r.detail["identity"].items() if abs(v - 1) > 0.10}
        if off:
            note += f"; implied/reported outside +-10% in {off}"
        add(key, "T1 identity+completeness", r, note)

    # T3/T4: bound derived from a reference of the same kind (budgeted unit cost) across countries.
    ref = _all_countries("budget_cpp_dstb")
    bound = derive_bound(ref, percentile=PERCENTILE)
    n_steps = sum(len(_changes(s)) for s in ref)
    cpp = bud["budget_cpp_xdr"]
    add("budget_cpp_xdr", "T3 implausibility", implausibility_score(cpp, bound=bound),
        f"bound {bound:.3f} = p{int(PERCENTILE * 100)} of {n_steps} steps, {len(ref)} countries (budget_cpp_dstb)")
    add("budget_cpp_xdr", "T4 declared", declared_score(cpp, bound=bound), "WHO file carries no notes")

    # T2, level mode, on dimensionless internal ratios (no exchange rate): two independent sources.
    years = [y for y in itr["itr_requested"].years if y in bud["budget_tot"].years]
    pairs = (("funding_gap",
              _gap(bud["budget_tot"], bud["cf_tot"], years, "who_funding_gap", "WHO (budget-expected)/budget"),
              _gap(itr["itr_requested"], itr["itr_approved"], years, "itr_funding_gap",
                   "ITR (requested-approved)/requested")),
             ("execution_gap",
              _gap(bud["budget_tot"], exp["exp_tot"], years, "who_exec_gap", "WHO (budget-expenditure)/budget"),
              _gap(itr["itr_approved"], itr["itr_spent"], years, "itr_exec_gap", "ITR (approved-spent)/approved")))
    t2 = {}
    for name, a, b in pairs:
        r = triangulate_score(a, b, mode="level")
        t2[name] = r
        add(name, "T2 triangulation (level)", r,
            f"WHO vs India TB Report, {years[0]}-{years[-1]}: agree in {len(r.detail.get('agree', []))} "
            f"of {len(r.detail.get('changes', {}))} years (tolerance 0.05)")
    return {"rows": rows, "t1": t1, "t2": t2, "bound": bound, "n_steps": n_steps,
            "n_countries": len(ref)}


def invisibility_rows() -> list[dict]:
    rep = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    out = []
    for rank, (key, label) in enumerate(NODE_LABELS.items(), start=1):
        out.append(dict(evidence_rank=rank, node=key, intervention=label,
                        budget_line=rep.mapped.get(key, ""), existence_score=rep.score[key],
                        coverage="none" if key not in rep.mapped
                        else ("partial" if key in TB_BUDGET_PARTIAL else "full"),
                        coverage_note=TB_BUDGET_PARTIAL.get(key, "")))
    return out


# ---------------------------------------------------------------- writing

def _write(path: Path, fields: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_rank_changes(path: Path, changes) -> None:
    """One row per cell that changed rank. A header-only file means ZERO changes; the count is
    also stated in the summary so the file is never the only evidence of a null."""
    _write(path, ["intervention", "target", "rank_before", "rank_after", "kind"],
           [dict(intervention=c.intervention, target=c.target, rank_before=c.rank_before,
                 rank_after=c.rank_after, kind=c.kind) for c in changes])


def _fmt(x, nd=3):
    return "n/a" if x is None else f"{x:.{nd}f}"


SCORE_FIELDS = ["series", "in_bopas_grid", "composite_geometric", "composite_arithmetic",
                "composite_minimum", "assessable", "n_testable", "observations", "min_observations",
                "collapsed_by", "T1_identity", "T2_triangulation", "T3_implausibility",
                "T4_declared", "t3_t4_bound"]


def score_rows(results, bounds, bopas_series):
    prov = provenance_from_results({k: composite_inputs(v) for k, v in results.items()})
    out = []
    for key, res in results.items():
        rep = composite_report(composite_inputs(res))
        sens = composite_sensitivity(composite_inputs(res))
        per = {n: ("untestable" if not r.testable else round(r.score, 4)) for n, r in zip(_TESTS, res)}
        out.append(dict(
            series=key, in_bopas_grid=key in bopas_series,
            composite_geometric="" if prov[key] is None else round(prov[key], 4),
            composite_arithmetic=round(sens["arithmetic"], 4) if sens else "",
            composite_minimum=round(sens["minimum"], 4) if sens else "",
            assessable=prov[key] is not None, n_testable=rep.n_testable,
            observations=";".join(f"{k}={v}" for k, v in rep.observations.items()),
            min_observations="" if rep.min_observations is None else rep.min_observations,
            collapsed_by=";".join(rep.collapsed_by),
            T1_identity=per["identity"], T2_triangulation=per["triangulation"],
            T3_implausibility=per["implausibility"], T4_declared=per["declared"],
            t3_t4_bound=round(bounds[key], 4)))
    return out, prov


def build_summary(c: dict) -> str:
    rr = c["rank"]
    L = []
    P = L.append
    P("D1: PROVENANCE INSTRUMENT ON INDIA'S TB DATA")
    P("=" * 60)
    P("")
    P("SECTION 1. THE BOPAS INPUT SERIES (Ruling AA)")
    P("Audited: the six epidemiological series in ntep_trajectories.csv. Five feed BOPAS;")
    P("BDQ_res_pct (2 points, descriptive only) is audited but is not in the grid.")
    P("")
    P(f"T1 identity: value = scale * numerator / denominator reconciles in {c['t1_ok']} of "
      f"{c['t1_n']} rows (within +-10%). This checks the file's own arithmetic, not WHO's numbers: "
      "it would not catch a wrong numerator copied consistently.")
    P("T2 triangulation: UNTESTABLE for all six series. Every series comes from WHO global TB data and "
      "no independent second source for any of them exists in this repository; who_dataset names the "
      "WHO table, not an independent source. A legitimate outcome, not a pass.")
    P(f"T3/T4: bound derived leave-one-out from the other epidemiological series (p{int(PERCENTILE * 100)} "
      "of |year-on-year change|), so no series sets its own yardstick. "
      f"Pooled-reference sensitivity (not adopted): {c['pooled_note']}")
    P("")
    P("Composite = geometric mean of T1 and T4 (T3 when T4 is untestable). T3 is reported but not combined: "
      "T4 is T3 on the same steps plus credit for disclosure, so using both would count one implausible "
      "step twice (Ruling GG). T2 is untestable for all six series, so no composite contains a "
      "triangulation: the test behind the strongest financing finding has no power on the series the "
      "priority score consumes.")
    P(f"{'series':18} {'composite':>9} {'tests':>5} {'obs':>4} {'collapsed_by':>12}  observations")
    for r in c["score_rows"]:
        tot = sum(int(x.split("=")[1]) for x in r["observations"].split(";")) if r["observations"] else 0
        P(f"{r['series']:18} {_fmt(c['prov'][r['series']]):>9} {r['n_testable']:>5} {tot:>4} "
          f"{(r['collapsed_by'] or '-'):>12}  {r['observations']}")
    P("")
    P(f"Unassessable series: {rr['unassessable_series'] or 'none'}. Unassessable cells (excluded from the "
      f"ranking, never ranked as clean; Ruling CC): {len(rr['unassessable_cells'])}.")
    P("")
    P("RESULT: DOES PROVENANCE REORDER THE RANKING?")
    P(f"Rank changes by kind: inversions: {len(rr['inversions'])}; tie splits: {len(rr['tie_splits'])} "
      f"(of {rr['n_cells']} cells, {rr['n_live']} with a positive score).")
    P(f"Interventions that changed published rank, of any kind: {len(rr['changes'])}.")
    for ch in rr["changes"]:
        P(f"  {ch.kind}: {ch.intervention} / {ch.target}: rank {ch.rank_before} -> {ch.rank_after}")
    if rr["tie_splits"]:
        P("A tie split is a ROUNDING ARTEFACT, not a reordering: the published scores are rounded to "
          "3 decimals, so cells with different true scores can tie, and scaling then rounding can "
          "split or create ties. Rounding is monotone, so it can never make a higher-scoring cell "
          "fall below a lower one. An inversion is the only kind that reorders.")
    if c["structural_null"]:
        live = rr["live_series"][0]
        lo, hi = c["live_ci"]
        P("")
        P("Provenance cannot reorder this ranking. The instrument could not discriminate on this "
          f"instance because the priority score is degenerate. {rr['n_zero']} of {rr['n_cells']} cells score exactly 0.0, and all {rr['n_live']} positive "
          f"cells belong to one series ({live}). Provenance scales a series' cells uniformly, so it "
          "cannot change the order among cells of one series, and it cannot lift a zero cell. "
          "Reordering is impossible by construction.")
        P(f"Stress test: provenance of {live} swept from 0.0 to 1.0 in steps of 0.05. Inversions at "
          f"any value: {c['stress_max']}. Literal rank changes still occur at {len(c['stress_ties'])} of the "
          "19 interior values (rounding ties, as above); at 0.0 the series is wiped out and all its "
          "cells tie at zero, which destroys the ranking rather than reordering it.")
        P("")
        P("This is a finding about the PRIORITY SCORE, not about provenance. The national ranking rests "
          f"on a single axis: the slope of {live}, whose bootstrap CI is [{lo:+.2f}, {hi:+.2f}] and "
          "spans zero. A ranking that depends on one trend that cannot be told from flat is degenerate "
          "however clean the data behind it. Per the specification's anti-goal (a method that changes "
          "no ranking anywhere has failed, and the paper should say so), D1 does NOT support the claim "
          "that provenance reorders priorities. That claim needs a setting where several series carry "
          "positive cells: D2/D3.")
    elif not rr["inversions"]:
        P("No pair of cells traded places, but the grid is not the single-axis degenerate case.")
    else:
        P(f"{len(rr['inversions'])} pairs of cells traded places (see the grid).")
    P("")
    P("EVPR (expected value of resolving a series' provenance, in BOPAS points; Ruling FF)")
    P("Reported as value (standard error), rounded to the precision the draws support, all three priors.")
    for prior in PRIORS:
        P(f"  prior={prior:8} " + "  ".join(
            f"{s}={round_to_se(v, se):g} (se {se:g})" for s, (v, se) in c["evpr"][prior].items()))
    if all(v == 0.0 and se == 0.0 for d in c["evpr"].values() for v, se in d.values()):
        P("Every EVPR is exactly 0.0 with standard error 0.0: the decision cannot change, so no audit "
          "of any series is worth buying on this grid. Same cause as above.")
    P("")
    P("SECTION 2. THE FINANCING AUDIT (separate; not propagated)")
    P("WHO budget/expenditure and India TB Report Table 16.1. These results describe financing data "
      "only and bear on no BOPAS input.")
    for r in c["fin"]["rows"]:
        P(f"  {r['series']:18} {r['test']:26} score={r['score']!s:6} {r['note']}")
    inv = c["invis"]
    none = [r["evidence_rank"] for r in inv if r["coverage"] == "none"]
    P("")
    P(f"T5 existence: {len(none)} of {len(inv)} evidence-ranked interventions have no budget line "
      f"(ranks {', '.join(map(str, none))}); {sum(r['coverage'] == 'partial' for r in inv)} are mapped "
      "only partially (drugs-only or TB/HIV-only lines). Reported separately, not folded into any composite.")
    return "\n".join(L) + "\n"


def main() -> str:
    OUTPUTS.mkdir(exist_ok=True)
    counts, traj = load_bopas_inputs()
    bopas_series = [t["series"] for t in traj]
    results, bounds = audit_ntep()
    srows, prov = score_rows(results, bounds, bopas_series)
    grid_prov = {s: prov[s] for s in bopas_series}

    rr = rank_report(counts, traj, grid_prov)
    live_ci, stress_max, stress_tie_values = None, 0, []
    if len(rr["live_series"]) == 1:
        t = next(t for t in traj if t["series"] == rr["live_series"][0])
        live_ci = (t["primary_lo"], t["primary_hi"])
        sweep = stress_test(counts, traj, rr["live_series"][0])
        stress_max = max(inv for _, inv, _ in sweep)
        stress_tie_values = [p for p, inv, lit in sweep if lit and 0.0 < p < 1.0]

    obs = observations_from_results({s: composite_inputs(results[s]) for s in bopas_series})
    ev = evpr_prior_sensitivity(counts, traj, grid_prov, observations=obs, draws=DRAWS)

    rows = _ntep_rows()
    t1_n = t1_ok = 0
    for s in load_trajectories(NTEP_TRAJECTORIES_CSV).values():
        d = identity_score(_identity_view(s, rows)).detail["identity"]
        t1_n += len(d)
        t1_ok += sum(1 for v in d.values() if 0.9 <= v <= 1.1)

    pooled_results, pooled_bounds = audit_ntep(pooled_reference=True)
    pooled_prov = provenance_from_results({k: composite_inputs(v) for k, v in pooled_results.items()})
    pooled_note = ("RRMDR_notif_100k composite "
                   f"{_fmt(pooled_prov['RRMDR_notif_100k'])} (bound {pooled_bounds['RRMDR_notif_100k']:.3f}) "
                   f"against {_fmt(prov['RRMDR_notif_100k'])} (bound {bounds['RRMDR_notif_100k']:.3f}).")

    fin = audit_financing()
    invis = invisibility_rows()

    _write(SCORES_CSV, SCORE_FIELDS, srows)
    write_rank_changes(RANKS_CSV, rr["changes"])
    _write(EVPR_CSV, ["prior", "series", "evpr", "se", "evpr_rounded"],
           [dict(prior=pr, series=s, evpr=v, se=se, evpr_rounded=round_to_se(v, se))
            for pr, d in ev.items() for s, (v, se) in d.items()])
    _write(INVIS_CSV, ["evidence_rank", "node", "intervention", "budget_line", "existence_score",
                       "coverage", "coverage_note"], invis)
    _write(FIN_CSV, ["series", "test", "testable", "score", "note"], fin["rows"])

    text = build_summary(dict(rank=rr, score_rows=srows, prov=prov, t1_ok=t1_ok, t1_n=t1_n,
                              structural_null=is_structural_null(rr, live_ci), live_ci=live_ci,
                              stress_max=stress_max, stress_ties=stress_tie_values, evpr=ev, fin=fin, invis=invis,
                              pooled_note=pooled_note))
    SUMMARY.write_text(text, encoding="utf-8")
    print(text)
    return text


if __name__ == "__main__":
    main()
