"""Recompute every number in paper A's Health Empirics tables from the archived inputs.

The Health Empirics version of paper A presents India's two financing records year by
year (Table 1), the national accounts in rupees (an appendix) and the countries by how
they report the two WHO budget fields (an appendix). None of those cells is typed: this
script recomputes each from the raw CSVs and, where the local manuscript source exists,
compares it cell by cell. The manuscript stays local (it is git-ignored); without it the
script prints the computed values and passes.

Sources (all archived, SHA-256 in data/raw_file_manifest.csv):
  data/TB_budget_2026-11-12.csv                   budget_tot, cf_tot by country-year
  data/TB_expenditure_utilisation_2026-08-25.csv  exp_tot, rcvd_tot and rcvd_tot_<source>
  data/india_tb_report_table16_1.csv              India TB Report 2024, table 16.1

Usage: python -I verification/check_paper_a_he.py
Exit 1 on any mismatch, naming the cell.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOURCE = ROOT / "manuscript" / "manuscript_a_he.md"


def _f(x: str) -> float | None:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def pct(x: float | None) -> str:
    return "—" if x is None else f"{100 * x:.1f}"


def india_series() -> dict[int, dict[str, float | None]]:
    out: dict[int, dict[str, float | None]] = defaultdict(dict)
    for r in csv.DictReader((DATA / "TB_budget_2026-11-12.csv").open(encoding="utf-8-sig")):
        if r["iso3"] == "IND":
            b, c = _f(r["budget_tot"]), _f(r["cf_tot"])
            y = int(r["year"])
            out[y]["budget"] = b
            out[y]["who_gap"] = (b - c) / b
    for r in csv.DictReader((DATA / "TB_expenditure_utilisation_2026-08-25.csv").open(encoding="utf-8-sig")):
        if r["iso3"] == "IND":
            y = int(r["year"])
            e, rc = _f(r["exp_tot"]), _f(r["rcvd_tot"])
            if not e:            # 2026: total reported as 0 with every component blank
                continue
            out[y]["exp"] = e
            out[y]["gf_share"] = _f(r["rcvd_tot_gf"]) / rc
            out[y]["dom_share"] = _f(r["rcvd_tot_domestic"]) / rc
    for r in csv.DictReader((DATA / "india_tb_report_table16_1.csv").open(encoding="utf-8-sig")):
        y = int(r["year"])
        req, app, spent = float(r["requested"]), float(r["approved"]), float(r["spent"])
        out[y].update(requested=req, approved=app, spent=spent, released=_f(r["released"]),
                      nat_short=(req - app) / req, nat_exec=spent / app)
    for y, d in out.items():
        if d.get("exp") and d.get("budget"):
            d["who_exec"] = d["exp"] / d["budget"]
    return dict(sorted(out.items()))


def table1_rows(s: dict[int, dict]) -> list[list[str]]:
    """Year | WHO gap | national shortfall | WHO exp/budget | national spent/approved |
    Global Fund share | domestic share (shares of funding received, WHO)."""
    rows = []
    for y in range(2017, 2026):
        d = s.get(y, {})
        rows.append([str(y), pct(d.get("who_gap")), pct(d.get("nat_short")), pct(d.get("who_exec")),
                     pct(d.get("nat_exec")), pct(d.get("gf_share")), pct(d.get("dom_share"))])
    return rows


def aggregates(s: dict[int, dict]) -> dict[str, float]:
    nat = [d for d in s.values() if "requested" in d]
    who = [d for y, d in s.items() if 2018 <= y <= 2025 and "who_exec" in d]
    req = sum(d["requested"] for d in nat)
    app = sum(d["approved"] for d in nat)
    spent = sum(d["spent"] for d in nat)
    rel = sum(d["released"] for d in nat if d["released"] is not None)
    spent_rel_years = sum(d["spent"] for d in nat if d["released"] is not None)
    return {"requested": req, "approved": app, "spent": spent, "approved/requested": app / req,
            "shortfall overall": (req - app) / req, "spent/approved": spent / app,
            "spent/requested": spent / req, "released (years printed)": rel,
            "spent (same years)": spent_rel_years,
            "WHO exp/budget 2018-2025": sum(d["exp"] for d in who) / sum(d["budget"] for d in who),
            "WHO exp/budget min": min(d["who_exec"] for d in who),
            "WHO exp/budget max": max(d["who_exec"] for d in who)}


def reporting_practice() -> dict[str, object]:
    by: dict[str, list[tuple[int, float, float]]] = defaultdict(list)
    names: dict[str, str] = {}
    for r in csv.DictReader((DATA / "TB_budget_2026-11-12.csv").open(encoding="utf-8-sig")):
        b, c = _f(r["budget_tot"]), _f(r["cf_tot"])
        if b is None or c is None:
            continue
        by[r["iso3"]].append((int(r["year"]), b, c))
        names[r["iso3"]] = r["country"]
    eligible = {k: v for k, v in by.items() if len(v) >= 5}
    always = sorted(k for k, v in eligible.items() if all(b == c for _, b, c in v))
    never = sorted(k for k, v in eligible.items() if not any(b == c for _, b, c in v))

    def mean_gap(iso: str) -> float:
        v = [(b - c) / b for _, b, c in by[iso] if b]
        return sum(v) / len(v)

    pak = {y: (b - c) / b for y, b, c in sorted(by["PAK"])}
    return {"eligible": len(eligible), "always": always, "never": never,
            "mixed": len(eligible) - len(always) - len(never), "names": names,
            "mean_gap": {k: mean_gap(k) for k in ("VNM", "NGA", "IDN", "CHN")}, "PAK": pak}


# ---------------------------------------------------------------- manuscript comparison
def md_table(text: str, caption_start: str) -> list[list[str]]:
    """Rows of the first pipe table after a line beginning with caption_start."""
    i = text.find(caption_start)
    if i == -1:
        return []
    rows = []
    for line in text[i:].splitlines()[1:]:
        if line.startswith("|"):
            cells = [c.strip().replace("**", "") for c in line.strip().strip("|").split("|")]
            if not set("".join(cells)) <= set("-: "):
                rows.append(cells)
        elif rows:
            break
    return rows[1:]  # drop header


def compare(s, prac) -> list[str]:
    text = SOURCE.read_text(encoding="utf-8")
    errs = []
    got = md_table(text, "**Table 1.")
    want = table1_rows(s)
    if [r[0] for r in got] != [r[0] for r in want]:
        errs.append(f"  Table 1: years {[r[0] for r in got]} != {[r[0] for r in want]}")
    for g, w in zip(got, want):
        for j, (a, b) in enumerate(zip(g, w)):
            if a.replace("%", "") != b:
                errs.append(f"  Table 1 {w[0]} col {j}: manuscript {a!r}, data {b!r}")
    acc = md_table(text, "**Table C1.")
    for row in acc:
        y = int(row[0])
        d = s[y]
        want_row = [str(y), f"{d['approved']:,.2f}", f"{d['requested']:,.2f}",
                    f"{d['spent']:,.2f}",
                    "not printed" if d["released"] is None else f"{d['released']:,.2f}"]
        if row[:5] != want_row:
            errs.append(f"  Table C1 {y}: manuscript {row[:5]}, data {want_row}")
    if len(acc) != 7:
        errs.append(f"  Table C1: {len(acc)} fiscal years, data has 7")
    for label, isos in (("Always equal", prac["always"]), ("Never equal", prac["never"])):
        m = re.search(rf"\*\*{label} \((\d+)\):\*\*\s*(.+)", text)
        if not m:
            errs.append(f"  appendix list {label!r} not found")
            continue
        listed = sorted(x.strip().rstrip(".") for x in m.group(2).split(";"))
        expected = sorted(prac["names"][k] for k in isos)
        if int(m.group(1)) != len(isos) or listed != expected:
            errs.append(f"  appendix list {label!r}: {len(listed)} names do not match the "
                        f"{len(isos)} computed; missing {sorted(set(expected) - set(listed))}, "
                        f"extra {sorted(set(listed) - set(expected))}")
    return errs


def main() -> int:
    s = india_series()
    prac = reporting_practice()
    print("Table 1 (computed): year | WHO gap | national shortfall | WHO exp/budget | "
          "national spent/approved | GF share | domestic share")
    for r in table1_rows(s):
        print("  " + " | ".join(r))
    for k, v in aggregates(s).items():
        print(f"  {k}: {v:,.4f}")
    print(f"countries with >=5 years: {prac['eligible']}; always equal {len(prac['always'])}; "
          f"never equal {len(prac['never'])}; mixed {prac['mixed']}")
    print("  mean gaps: " + ", ".join(f"{k} {v:.1%}" for k, v in prac["mean_gap"].items()))
    print("  Pakistan: " + ", ".join(f"{y} {g:.1%}" for y, g in prac["PAK"].items()))
    print("  always equal: " + "; ".join(prac["names"][k] for k in prac["always"]))
    print("  never equal: " + "; ".join(prac["names"][k] for k in prac["never"]))
    if not SOURCE.exists():
        print(f"PASSED (no local {SOURCE.name}; computed values printed only)")
        return 0
    errs = compare(s, prac)
    if errs:
        print(f"FAILED: {len(errs)} mismatch(es) between {SOURCE.name} and the data")
        print("\n".join(errs))
        return 1
    print(f"PASSED: Table 1, Table C1 and both country lists in {SOURCE.name} match the archived data")
    return 0


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
