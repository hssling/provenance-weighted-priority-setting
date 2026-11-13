"""Screen every numeric variable in six WHO TB datasets for signatures of
carried-forward estimation rather than annual measurement.

Motivation
----------
These datasets are analysed widely, and their variables are treated
interchangeably as annual country reports. They are not. Some columns carry
genuine year-specific figures; others carry a value entered once and repeated,
or a round-number estimate standing in for a measurement. Nothing in the
distributed files marks which is which.

The consequence is not hypothetical. Using `hospd_prct_mdr` (70% of consecutive
country-year pairs identical) as if it varied annually, or computing a funding
share against expenditure rather than receipts, each yields a clean and
entirely spurious result.

Screens, each computable from the published file alone
------------------------------------------------------
S0  CATEGORICAL   5 or fewer distinct values: a status flag or a code, not a
                  measure. Runs FIRST; such a variable is reported separately
                  and never enters the measurement/mixed/estimate
                  classification. The cut-off of 5 is a convention.
S0b UNTESTABLE    no comparable adjacent country-year pair (every country
                  reports at most once), so S1 is undefined. Reported
                  separately and NEVER counted as measurement-like: a test
                  that could not run is not evidence of cleanliness.
S1  REPETITION    share of consecutive country-year pairs with an identical value
S2  GRANULARITY   distinct values / observations, and share on round numbers
S3  IDENTITY      do stated components reconcile with their stated total?
S4  BOUNDS        do values stay inside the range their definition implies?

No screen alone condemns a variable: a genuinely stable quantity repeats, and a
small integer count is legitimately round. The signature is several at once.

Why S0 exists (correction, 2026-11-13)
--------------------------------------
The first version had no S0. A yes/no flag ("is the national reference
laboratory accredited?") answers "yes" for years on end, takes two values, and
is trivially round: it trips the repetition, distinct-ratio, modal-share and
roundness tests legitimately, and was classified estimate-like. Replication on
TB_contact_tpt exposed it: its 12 flags made that dataset look estimate-like
(59.7% median repetition, 12 estimate-like variables); with flags excluded it
is 3.5% with none. That was a false positive created by the screen itself.

Second correction (2026-11-13)
------------------------------
An exploratory run silently dropped variables with no adjacent pair (a
zero-division guard). That inclusion rule was accidental. It is replaced by the
explicit `untestable_s1` class, adopted after the discrepancy was found, on the
principle that an unscreenable variable is unscreenable. It raises the median
repetition of `laboratory` and `outcomes`, so the screen also reports the
median under the inclusive alternative (untestable variables scored 0%,
classed measurement-like) as a sensitivity.

Run:  python demos/d2_who_data_screen.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE.parent / "outputs"

DATASETS = [
    ("budget", DATA / "TB_budget_2026-11-12.csv"),
    ("expenditure", DATA / "TB_expenditure_utilisation_2026-08-25.csv"),
    ("notifications", DATA / "TB_notifications_2026-08-25.csv"),
    ("outcomes", DATA / "TB_outcomes_2026-08-25.csv"),
    ("laboratory", DATA / "TB_laboratory_diagnostic_services_2026-08-25.csv"),
    ("contact_tpt", DATA / "TB_contact_tpt_2026-08-25.csv"),
]

# S0: a variable with this many distinct values or fewer is categorical.
# A convention, not a derived quantity.
CATEGORICAL_MAX_DISTINCT = 5
# Minimum adjacent pairs with at least one non-zero side before the
# zero-excluded repetition is reported. Below this it is noise.
MIN_NONZERO_PAIRS = 20

ID_COLS = {"country", "iso2", "iso3", "iso_numeric", "g_whoregion", "year"}
ABSENT = {"", "NA", "na", "N/A", "-"}

# Variables whose definition bounds them to a percentage.
PERCENT_VARS = {"hospd_prct_dstb", "hospd_prct_mdr"}


def num(v):
    if v is None or v.strip() in ABSENT:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load(path: Path) -> list[dict]:
    # Some WHO files are Windows-1252 rather than UTF-8; fall back (read-only).
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="cp1252", errors="replace")
    return list(csv.DictReader(text.splitlines()))


def median(xs: list[float]) -> float:
    xs = sorted(xs)
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def screen_column(rows: list[dict], col: str) -> dict | None:
    """Return the screens for one column, or None if too sparse to judge."""
    vals, by_country = [], defaultdict(list)
    for r in rows:
        v = num(r.get(col))
        if v is None:
            continue
        vals.append(v)
        by_country[r["iso3"]].append((int(r["year"]), v))
    if len(vals) < 100:
        return None

    # S0 categorical: runs first and short-circuits everything below.
    n_distinct = len(set(vals))
    if n_distinct <= CATEGORICAL_MAX_DISTINCT:
        return {"column": col, "n": len(vals), "countries": len(by_country),
                "n_distinct": n_distinct, "categorical": True, "untestable": False,
                "repetition": None, "repetition_nz": None,
                "distinct_ratio": None, "modal_share": None,
                "modal_is_zero": None, "roundish": None, "out_of_bounds": None}

    # S1 repetition. We also count repetition over the subset of pairs where
    # at least one side is non-zero. A repeated zero is an absence, not a
    # carried-forward estimate, and 71 of the 84 estimate-like variables have
    # zero as their modal value, so the unrestricted statistic partly measures
    # "this programme element does not exist here". The restricted statistic is
    # reported as a sensitivity; it does NOT feed classify(), which is left as
    # specified so the published verdicts stand.
    same = pairs = same_nz = pairs_nz = 0
    for series in by_country.values():
        series.sort()
        for (_, a), (_, b) in zip(series, series[1:]):
            pairs += 1
            same += a == b
            if a or b:
                pairs_nz += 1
                same_nz += a == b
    if pairs == 0:
        return {"column": col, "n": len(vals), "countries": len(by_country),
                "n_distinct": n_distinct, "categorical": False,
                "untestable": True, "repetition": None, "repetition_nz": None,
                "distinct_ratio": None, "modal_share": None,
                "modal_is_zero": None, "roundish": None, "out_of_bounds": None}
    repetition = same / pairs
    repetition_nz = same_nz / pairs_nz if pairs_nz >= MIN_NONZERO_PAIRS else None

    # S2 granularity
    distinct = n_distinct / len(vals)
    counts = Counter(vals)
    modal_share = counts.most_common(1)[0][1] / len(vals)
    nonzero = [v for v in vals if v]
    # "round" is scale-relative: a multiple of 10 for small numbers,
    # a multiple of 1000 for monetary ones.
    scale = 1000.0 if max(abs(v) for v in nonzero) > 1e5 else 10.0
    roundish = sum(1 for v in nonzero if v % scale == 0) / len(nonzero)

    # S4 bounds
    out_of_bounds = None
    if col in PERCENT_VARS:
        out_of_bounds = sum(1 for v in vals if v < 0 or v > 100) / len(vals)

    return {
        "column": col,
        "n": len(vals),
        "countries": len(by_country),
        "n_distinct": n_distinct,
        "categorical": False,
        "untestable": False,
        "repetition": repetition,
        "repetition_nz": repetition_nz,
        "distinct_ratio": distinct,
        "modal_share": modal_share,
        "modal_is_zero": counts.most_common(1)[0][0] == 0,
        "roundish": roundish,
        "out_of_bounds": out_of_bounds,
    }


def classify(s: dict) -> str:
    """Label a continuous column by how many screens it trips. Thresholds are
    conventions, stated so a reader can move them; the ranking is insensitive
    to small changes because the distribution is strongly bimodal."""
    flags = 0
    flags += s["repetition"] >= 0.40        # repeats more often than not
    flags += s["distinct_ratio"] <= 0.30    # few distinct values for many obs
    flags += s["modal_share"] >= 0.15       # one value dominates
    flags += s["roundish"] >= 0.40          # mostly round numbers
    return {0: "measurement-like", 1: "measurement-like",
            2: "mixed", 3: "estimate-like", 4: "estimate-like"}[flags]


def identity_screen(rows: list[dict], total: str, parts: list[str]) -> dict:
    """S3 — do the stated components reconcile with the stated total?"""
    ok = bad = untestable = 0
    for r in rows:
        t = num(r.get(total))
        ps = [num(r.get(p)) for p in parts]
        if t is None or all(p is None for p in ps) or t == 0:
            untestable += 1
            continue
        s = sum(p for p in ps if p is not None)
        if abs(s - t) <= 0.01 * abs(t):
            ok += 1
        else:
            bad += 1
    return {"total": total, "ok": ok, "bad": bad, "untestable": untestable}


def main() -> int:
    global CATEGORICAL_MAX_DISTINCT
    OUT.mkdir(exist_ok=True)
    tables = {label: load(path) for label, path in DATASETS}
    budget, expend = tables["budget"], tables["expenditure"]

    allres = []
    for label, rows in tables.items():
        for col in rows[0]:
            if col in ID_COLS:
                continue
            s = screen_column(rows, col)
            if s:
                s["dataset"] = label
                s["verdict"] = ("categorical" if s["categorical"]
                                else "untestable_s1" if s["untestable"]
                                else classify(s))
                allres.append(s)

    results = sorted((s for s in allres
                      if not s["categorical"] and not s["untestable"]),
                     key=lambda s: (s["dataset"], -s["repetition"], s["column"]))
    cats = [s for s in allres if s["categorical"]]
    unt = [s for s in allres if s["untestable"]]
    print("S0b untestable on S1 (no adjacent country-year pair; excluded)")
    for s in sorted(unt, key=lambda s: (s["dataset"], s["column"])):
        print(f"  {s['dataset']:<14}{s['column']:<34}n={s['n']:<6}"
              f"countries={s['countries']}")
    print()

    print(f"S0 categorical variables (<= {CATEGORICAL_MAX_DISTINCT} distinct "
          "values; excluded from classification)")
    for s in sorted(cats, key=lambda s: (s["dataset"], s["column"])):
        print(f"  {s['dataset']:<14}{s['column']:<34}n={s['n']:<6}"
              f"distinct={s['n_distinct']}")

    print(f"\n{'dataset':<14}{'column':<34}{'n':>6}{'dist':>6}{'rep':>7}"
          f"{'d/n':>6}{'modal':>7}{'round':>7}  verdict")
    print("-" * 100)
    for s in results:
        print(f"{s['dataset']:<14}{s['column']:<34}{s['n']:>6}{s['n_distinct']:>6}"
              f"{s['repetition']:>7.1%}{s['distinct_ratio']:>6.2f}"
              f"{s['modal_share']:>7.1%}{s['roundish']:>7.1%}  {s['verdict']}")

    print("\nPer-dataset summary (continuous variables only; categorical excluded)")
    print(f"{'dataset':<14}{'cont':>5}{'cat':>5}{'untst':>6}{'median rep':>12}"
          f"{'meas':>6}{'mixed':>6}{'est':>5}{'incl. median':>14}"
          f"{'excl. 0-0':>11}{'zero-modal':>11}")
    for label in tables:
        c = [s for s in results if s["dataset"] == label]
        k = sum(1 for s in cats if s["dataset"] == label)
        u = sum(1 for s in unt if s["dataset"] == label)
        t = Counter(s["verdict"] for s in c)
        incl = median([s["repetition"] for s in c] + [0.0] * u)
        nz = [s["repetition_nz"] for s in c if s["repetition_nz"] is not None]
        zm = sum(1 for s in c if s["modal_is_zero"])
        print(f"{label:<14}{len(c):>5}{k:>5}{u:>6}"
              f"{median([s['repetition'] for s in c]):>12.1%}"
              f"{t['measurement-like']:>6}{t['mixed']:>6}{t['estimate-like']:>5}"
              f"{incl:>14.1%}{median(nz):>11.1%}{zm:>7}/{len(c):<3}")
    tot = Counter(s["verdict"] for s in results)
    print(f"{'ALL':<14}{len(results):>5}{len(cats):>5}{len(unt):>6}"
          f"{median([s['repetition'] for s in results]):>12.1%}"
          f"{tot['measurement-like']:>6}{tot['mixed']:>6}{tot['estimate-like']:>5}")

    orig = [s for s in allres if s["dataset"] in ("budget", "expenditure")]
    oc = [s for s in orig if not s["categorical"] and not s["untestable"]]
    t = Counter(s["verdict"] for s in orig)
    print(f"\nOriginal two files: {len(orig)} variables screened -> "
          f"{len(oc)} continuous, {t['categorical']} categorical, "
          f"{t['untestable_s1']} untestable on S1; "
          f"{t['measurement-like']} measurement-like, {t['mixed']} mixed, "
          f"{t['estimate-like']} estimate-like")
    print("Estimate-like, original two files:")
    for s in sorted((s for s in oc if s["verdict"] == "estimate-like"),
                    key=lambda s: -s["repetition"]):
        print(f"  {s['column']:<18}n={s['n']:<6}distinct={s['n_distinct']:<5}"
              f"rep={s['repetition']:.1%}  d/n={s['distinct_ratio']:.2f}  "
              f"modal={s['modal_share']:.1%}  round={s['roundish']:.1%}")
    print("Least repetitive, original two files:")
    for s in sorted(oc, key=lambda s: s["repetition"])[:6]:
        print(f"  {s['column']:<18}n={s['n']:<6}rep={s['repetition']:.1%}  "
              f"d/n={s['distinct_ratio']:.2f}")

    # Counterfactual: what the screen said about contact_tpt BEFORE S0 existed.
    saved, CATEGORICAL_MAX_DISTINCT = CATEGORICAL_MAX_DISTINCT, 0
    cf = []
    for col in tables["contact_tpt"][0]:
        if col in ID_COLS:
            continue
        r = screen_column(tables["contact_tpt"], col)
        if r:
            r["verdict"] = "untestable_s1" if r["untestable"] else classify(r)
            cf.append(r)
    CATEGORICAL_MAX_DISTINCT = saved
    cft = [r for r in cf if not r["untestable"]]
    cfv = Counter(r["verdict"] for r in cf)
    print(f"\ncontact_tpt WITHOUT S0 (counterfactual): {len(cft)} testable "
          f"variables, median repetition "
          f"{median([r['repetition'] for r in cft]):.1%}; "
          f"{cfv['estimate-like']} estimate-like, {cfv['mixed']} mixed, "
          f"{cfv['measurement-like']} measurement-like, "
          f"{cfv['untestable_s1']} untestable; median "
          f"{median([r['repetition'] for r in cft] + [0.0] * cfv['untestable_s1']):.1%} "
          f"if untestable scored 0%")

    # Section 3.3 of the manuscript: hospd_prct_mdr in detail.
    series = defaultdict(list)
    vals33 = []
    for r in expend:
        v = num(r.get("hospd_prct_mdr"))
        if v is not None:
            vals33.append(v)
            series[r["iso3"]].append((int(r["year"]), v))
    long_ = [sorted(x) for x in series.values() if len(x) >= 4]
    unchanged = sum(1 for x in long_ if x[0][1] == x[-1][1])
    print(f"\nhospd_prct_mdr: {len(series)} countries, {len(vals33)} obs, "
          f"{len(set(vals33))} distinct; exactly 100: "
          f"{sum(v == 100 for v in vals33) / len(vals33):.1%}; exactly 0: "
          f"{sum(v == 0 for v in vals33) / len(vals33):.1%}; multiples of 10: "
          f"{sum(v % 10 == 0 for v in vals33) / len(vals33):.1%}; "
          f"{unchanged}/{len(long_)} = {unchanged / len(long_):.0%} of countries "
          f"with >=4 years unchanged first-to-last")

    print("\nS3 identity screens")
    LINES = ["lab", "staff", "fld", "prog", "sld", "mdrmgt", "tpt",
             "tbhiv", "patsup", "orsrvy", "oth"]
    for rows, total, parts in (
        (budget, "budget_tot", [f"budget_{x}" for x in LINES]),
        (budget, "cf_tot", [f"cf_{x}" for x in LINES]),
        (expend, "exp_tot", [f"exp_{x}" for x in LINES]),
        (expend, "rcvd_tot", [f"rcvd_{x}" for x in LINES]),
        (expend, "rcvd_tot", ["rcvd_tot_domestic", "rcvd_tot_gf",
                              "rcvd_tot_usaid", "rcvd_tot_grnt"]),
    ):
        r = identity_screen(rows, total, parts)
        n = r["ok"] + r["bad"]
        rate = r["ok"] / n if n else 0
        print(f"  {total:<16} vs {len(parts):>2} parts: "
              f"{r['ok']}/{n} reconcile ({rate:.1%}), {r['untestable']} untestable")

    with (OUT / "d2_variable_screen.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["dataset", "column", "n", "countries",
                                           "n_distinct", "repetition",
                                           "repetition_nz", "distinct_ratio",
                                           "modal_share", "modal_is_zero",
                                           "roundish", "out_of_bounds", "verdict"],
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(allres, key=lambda s: (s["dataset"], s["column"])))
    print(f"\nwrote {OUT / 'd2_variable_screen.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
