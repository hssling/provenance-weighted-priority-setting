"""Screen every numeric variable in WHO's TB financing and utilisation datasets
for signatures of carried-forward estimation rather than annual measurement.

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

Four screens, each computable from the published file alone
-----------------------------------------------------------
S1  REPETITION    share of consecutive country-year pairs with an identical value
S2  GRANULARITY   distinct values / observations, and share on round numbers
S3  IDENTITY      do stated components reconcile with their stated total?
S4  BOUNDS        do values stay inside the range their definition implies?

No screen alone condemns a variable: a genuinely stable quantity repeats, and a
small integer count is legitimately round. The signature is several at once.

Run:  python demos/d2_who_data_screen.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
BUDGET = DATA / "TB_budget_2026-11-12.csv"
EXPEND = DATA / "TB_expenditure_utilisation_2026-08-25.csv"
OUT = HERE.parent / "outputs"

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
    with path.open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def screen_column(rows: list[dict], col: str) -> dict | None:
    """Return the four screens for one column, or None if too sparse to judge."""
    vals, by_country = [], defaultdict(list)
    for r in rows:
        v = num(r.get(col))
        if v is None:
            continue
        vals.append(v)
        by_country[r["iso3"]].append((int(r["year"]), v))
    if len(vals) < 100:
        return None

    # S1 repetition
    same = pairs = 0
    for series in by_country.values():
        series.sort()
        for (_, a), (_, b) in zip(series, series[1:]):
            pairs += 1
            same += a == b
    repetition = same / pairs if pairs else 0.0

    # S2 granularity
    distinct = len(set(vals)) / len(vals)
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
        "repetition": repetition,
        "distinct_ratio": distinct,
        "modal_share": modal_share,
        "roundish": roundish,
        "out_of_bounds": out_of_bounds,
    }


def classify(s: dict) -> str:
    """Label a column by how many screens it trips. Thresholds are conventions,
    stated so a reader can move them; the ranking is insensitive to small
    changes because the distribution is strongly bimodal."""
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
    OUT.mkdir(exist_ok=True)
    budget, expend = load(BUDGET), load(EXPEND)

    results = []
    for label, rows in (("budget", budget), ("expenditure", expend)):
        for col in rows[0]:
            if col in ID_COLS:
                continue
            s = screen_column(rows, col)
            if s:
                s["dataset"] = label
                s["verdict"] = classify(s)
                results.append(s)

    results.sort(key=lambda s: (-s["repetition"], s["column"]))

    print(f"{'dataset':<12}{'column':<22}{'n':>6}{'rep':>7}{'distinct':>10}"
          f"{'modal':>7}{'round':>7}  verdict")
    print("-" * 86)
    for s in results:
        print(f"{s['dataset']:<12}{s['column']:<22}{s['n']:>6}"
              f"{s['repetition']:>7.1%}{s['distinct_ratio']:>10.2f}"
              f"{s['modal_share']:>7.1%}{s['roundish']:>7.1%}  {s['verdict']}")

    tally = Counter(s["verdict"] for s in results)
    print(f"\n{len(results)} variables screened: "
          + ", ".join(f"{v} {k}" for k, v in tally.most_common()))

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
                                           "repetition", "distinct_ratio",
                                           "modal_share", "roundish",
                                           "out_of_bounds", "verdict"])
        w.writeheader()
        w.writerows(results)
    print(f"\nwrote {OUT / 'd2_variable_screen.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
