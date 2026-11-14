"""D3: a vintage analysis of WHO's tuberculosis finance and utilisation data.

Four questions, each answered from WHO's own archived files:

  1. Revision.    Is a country-year value, once published, ever changed in a
                  later release? Compared across three dated releases.
  2. Restatement. How often is a country's value for a year identical to its
                  own value for the year before, in the same release?
  3. Filling.     Where a country reported nothing, what does WHO's finance
                  pipeline put in its place, and from which year?
  4. Consequence. How much of WHO's published estimate of TB spending on
                  inpatient and outpatient care rests on inputs that were
                  newly reported, restated unchanged, or supplied by WHO?

Inputs (fetched at pinned commits by tools/fetch_vintages.py, converted by
tools/convert_vintages.R, never edited):
  release 2024  gtbreport2024 snapshot_2024-07-29/finance
  release 2025  gtbreport2025 snapshot_2025-07-30/finance, and WHO's processed
                finance_imputed_constantus_included for the 2025 report
  release 2026  data/TB_expenditure_utilisation_2026-08-25.csv (the public
                download of the same release; the 2026 snapshot splits the
                expenditure table without the utilisation fields), the
                gtbreport2026 snapshot_2026-08-25/expenditure for financial
                comparators, and WHO's processed file for the 2026 report

Standard library only. Usage: python -I demos/d3_vintages.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CSV = DATA / "vintages" / "csv"
OUT = ROOT / "outputs"

# The six utilisation inputs to WHO's estimate of inpatient and outpatient
# cost, in WHO's processed spelling.
UTIL = ["hcfvisit_dstb", "hcfvisit_mdr", "hospd_dstb_prct", "hospd_mdr_prct",
        "hospd_dstb_dur", "hospd_mdr_dur"]
# Counted financial comparators present in all three releases' snapshots.
COUNTED = ["exp_fld", "exp_lab", "exp_staff", "exp_prog"]
# Public-download spelling of the four hospitalisation fields.
PUBLIC = {"hospd_dstb_prct": "hospd_prct_dstb", "hospd_mdr_prct": "hospd_prct_mdr",
          "hospd_dstb_dur": "hospd_dur_dstb", "hospd_mdr_dur": "hospd_dur_mdr"}
# Each cost component of WHO's care estimate, and the inputs it is built from
# (gtbreport2026 finance/3_prepare_imputed_data.R, bed-days and visit costs).
COMPONENTS = {
    "c_hospital_nmdr": ["hospd_dstb_prct", "hospd_dstb_dur"],
    "c_hospital_mdr": ["hospd_mdr_prct", "hospd_mdr_dur"],
    "c_clinic_nmdr": ["hcfvisit_dstb"],
    "c_clinic_mdr": ["hcfvisit_mdr"],
}
# WHO's published totals for low- and middle-income countries, used only to
# validate the reconstruction below: Global Tuberculosis Report 2025, ch. 4.1
# (US$ 5.9 billion in 2024) and 2026, ch. 4.1 (US$ 6.03 billion in 2024 and
# US$ 6.6 billion in 2025). Rounded as WHO printed them.
PUBLISHED = {("2025", 2024): (5.9, 1), ("2026", 2024): (6.03, 2), ("2026", 2025): (6.6, 1)}
WHO_FILL_ORDER = [-1, -2, -3, -4, 1, 2, 3, 4]       # lag 1..4, then lead 1..4
# First reporting year every release can classify: the public 2026 download
# starts at 2017, so 2017 has no previous year to be "restated" from, and a
# processed value for 2015-2016 has no raw value to be compared with. An
# earlier pass without this window called 99% of 2017 "new".
WINDOW_START = 2018

FILES = {
    "raw2024": CSV / "gtbreport2024__data__gtb__snapshot_2024-07-29__finance__finance.csv",
    "raw2025": CSV / "gtbreport2025__data__gtb__snapshot_2025-07-30__finance__finance.csv",
    "snap2026": CSV / "gtbreport2026__data__gtb__snapshot_2026-08-25__expenditure__expenditure.csv",
    "pub2026": DATA / "TB_expenditure_utilisation_2026-08-25.csv",
    "proc2025": CSV / "gtbreport2025__finance__output__finance_imputed_constantus_included__finance_merged.csv",
    "proc2026": CSV / "gtbreport2026__finance__output__finance_imputed_constantus_included__finance_merged.csv",
}


def num(s: str | None) -> float | None:
    if s is None or s.strip() in ("", "NA"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


@lru_cache(maxsize=None)
def rows(key: str) -> tuple[dict, ...]:
    with FILES[key].open(encoding="utf-8-sig") as f:
        return tuple(csv.DictReader(f))


def table(key: str, variables: list[str], spelling: str) -> dict[tuple[str, int], dict]:
    """(iso3, year) -> {variable: value or None}. spelling: 'dot' (raw
    snapshots), 'public' (public download) or 'plain' (processed output)."""
    out = {}
    for r in rows(key):
        rec = {}
        for v in variables:
            col = (v.replace("_", ".") if spelling == "dot"
                   else PUBLIC.get(v, v) if spelling == "public" else v)
            rec[v] = num(r.get(col))
        out[(r["iso3"], int(r["year"]))] = rec
    return out


@lru_cache(maxsize=None)
def releases() -> dict[str, dict]:
    """Raw country-reported values, release by release."""
    util = {"2024": table("raw2024", UTIL, "dot"), "2025": table("raw2025", UTIL, "dot"),
            "2026": table("pub2026", UTIL, "public")}
    counted = {"2024": table("raw2024", COUNTED, "dot"),
               "2025": table("raw2025", COUNTED, "dot"),
               "2026": table("snap2026", COUNTED, "plain")}
    return {"util": util, "counted": counted}


# ---------------------------------------------------------------- 1. revision
def revision() -> list[dict]:
    """Share of the same country-year value that differs between releases."""
    out = []
    rel = releases()
    for group, variables in (("util", UTIL), ("counted", COUNTED)):
        for a, b in (("2024", "2025"), ("2025", "2026")):
            for v in variables:
                both = changed = 0
                for k, rec in rel[group][a].items():
                    x, y = rec[v], rel[group][b].get(k, {}).get(v)
                    if x is not None and y is not None:
                        both += 1
                        changed += x != y
                out.append({"group": group, "from": a, "to": b, "variable": v,
                            "pairs": both, "changed": changed})
    return out


def added_later() -> dict:
    """Country-years absent in an earlier release and present in a later one:
    the history grows by late reports even though it is never corrected."""
    rel = releases()["util"]
    out = {}
    for a, b in (("2024", "2025"), ("2025", "2026")):
        out[f"{a}->{b}"] = sum(
            1 for k, rec in rel[b].items()
            if k[1] <= int(a) - 1 and any(rec[v] is not None for v in UTIL)
            and not any((rel[a].get(k) or {}).get(v) is not None for v in UTIL))
    return out


# ------------------------------------------------------------- 2. restatement
def restatement() -> list[dict]:
    """Share of consecutive country-year pairs holding an identical value,
    within each release."""
    out = []
    rel = releases()
    for group, variables in (("util", UTIL), ("counted", COUNTED)):
        for name, t in rel[group].items():
            for v in variables:
                pairs = same = 0
                for (c, y), rec in t.items():
                    if y < WINDOW_START:        # the same years in every release
                        continue
                    x, p = rec[v], (t.get((c, y - 1)) or {}).get(v)
                    if x is not None and p is not None:
                        pairs += 1
                        same += x == p
                out.append({"group": group, "release": name, "variable": v,
                            "pairs": pairs, "identical": same})
    return out


def restated_then_revised() -> list[dict]:
    """Values restated in the 2024 release: were any revised by 2026?"""
    rel = releases()["util"]
    out = []
    for v in UTIL:
        restated = revised = 0
        for (c, y), rec in rel["2024"].items():
            x, p = rec[v], (rel["2024"].get((c, y - 1)) or {}).get(v)
            later = (rel["2026"].get((c, y)) or {}).get(v)
            if y < WINDOW_START:
                continue
            if x is not None and p is not None and x == p and later is not None:
                restated += 1
                revised += later != x
        out.append({"variable": v, "restated_2024": restated, "revised_by_2026": revised})
    return out


# ---------------------------------------------------------------- 3. filling
def provenance(release: str) -> dict[tuple[str, int, str], str]:
    """For every utilisation value WHO's processed file uses, where it came
    from: 'new' (reported, differs from the country's previous year),
    'restated' (reported, identical to the previous year), 'overridden'
    (reported, but WHO used a different value), 'filled_earlier' or
    'filled_later' (not reported; equals the country's value k years before
    or after, searched in WHO's fill order), 'filled_other' (not reported,
    no matching year) or 'absent'."""
    raw = releases()["util"][release]
    proc = table(f"proc{release}", UTIL, "plain")
    out = {}
    for (c, y), rec in proc.items():
        for v in UTIL:
            pv = rec[v]
            rv = (raw.get((c, y)) or {}).get(v)
            if pv is None:
                state = "absent"
            elif rv is None:
                state = "filled_other"
                for k in WHO_FILL_ORDER:
                    if (raw.get((c, y + k)) or {}).get(v) == pv:
                        state = "filled_earlier" if k < 0 else "filled_later"
                        break
            elif pv != rv:
                state = "overridden"
            else:
                prev = (raw.get((c, y - 1)) or {}).get(v)
                state = "restated" if prev is not None and prev == rv else "new"
            out[(c, y, v)] = state
    return out


def filling(release: str, last_year: int) -> Counter:
    return Counter(s for (c, y, v), s in provenance(release).items()
                   if WINDOW_START <= y <= last_year)


# ------------------------------------------------------------- 4. consequence
COMPONENT_CLASS = ("WHO-supplied", "restated", "new")


def component_class(states: list[str]) -> str:
    """A cost component is WHO-supplied if any input was filled or overridden,
    restated if any input (and none WHO-supplied) was restated, else new."""
    if any(s.startswith("filled") or s == "overridden" for s in states):
        return "WHO-supplied"
    if "restated" in states:
        return "restated"
    return "new"


def consequence(release: str) -> list[dict]:
    """Per year: WHO's reconstructed total, the care estimate, and the care
    estimate split by the provenance of the inputs each component uses.
    Only cost that reaches the published total is apportioned: WHO sets the
    care estimate to zero for countries believed to report it already, and
    there the components do not contribute."""
    prov = provenance(release)
    by_year: dict[int, dict] = defaultdict(lambda: defaultdict(float))
    for r in rows(f"proc{release}"):
        c, y = r["iso3"], int(r["year"])
        ghs = num(r["c_ghs"]) or 0.0
        acc = by_year[y]
        acc["total"] += (num(r["rcvd_tot"]) or 0.0) + ghs
        acc["ghs"] += ghs
        acc["countries"] += 1
        if ghs == 0:
            continue
        parts = {k: num(r.get(k)) or 0.0 for k in COMPONENTS}
        assert abs(sum(parts.values()) - ghs) <= 1.0, (c, y, ghs, parts)
        for comp, inputs in COMPONENTS.items():
            states = [prov[(c, y, v)] for v in inputs]
            cls = component_class(states)
            acc[cls] += parts[comp]
            acc[f"{cls}:{'inpatient' if 'hospital' in comp else 'outpatient'}"] += parts[comp]
            # Sensitivity: the most lenient reading counts a component as
            # current if ANY of its inputs was newly reported that year.
            if "new" in states:
                acc["new_any"] += parts[comp]
    out = []
    for y in sorted(by_year):
        a = by_year[y]
        out.append({"release": release, "year": y, "countries": int(a["countries"]),
                    "total": a["total"], "ghs": a["ghs"],
                    **{k: a[k] for k in COMPONENT_CLASS}, "new_any": a["new_any"]})
    return out


def last_reported(release: str, iso3: str) -> dict:
    """The latest year a country reported any utilisation input, the run of
    years over which WHO's processed file uses that same set of values, and
    the care estimate those years carry."""
    raw = releases()["util"][release]
    proc = table(f"proc{release}", UTIL, "plain")
    years = sorted(y for (c, y), rec in raw.items()
                   if c == iso3 and any(rec[v] is not None for v in UTIL))
    last = years[-1]
    values = [raw[(iso3, last)][v] for v in UTIL]
    same_from = last
    while (iso3, same_from - 1) in raw and [raw[(iso3, same_from - 1)][v] for v in UTIL] == values:
        same_from -= 1
    used_to = last
    while [(proc.get((iso3, used_to + 1)) or {}).get(v) for v in UTIL] == values:
        used_to += 1
    care = {int(r["year"]): num(r["c_ghs"]) or 0.0 for r in rows(f"proc{release}")
            if r["iso3"] == iso3}
    return {"iso3": iso3, "last_reported": last, "first_year_of_values": same_from,
            "used_through": used_to, "care_latest": care.get(RELEASE_LATEST[release], 0.0)}


RELEASE_LATEST = {"2025": 2024, "2026": 2025}


def validation() -> list[dict]:
    """The reconstruction must reproduce WHO's published totals."""
    out = []
    for (release, year), (value, places) in PUBLISHED.items():
        got = next(r["total"] for r in consequence(release) if r["year"] == year) / 1e9
        out.append({"release": release, "year": year, "published": value,
                    "reconstructed": got, "match": round(got, places) == value})
    return out


# -------------------------------------------------------------------- report
def results() -> dict:
    """Every number the manuscript states about the vintage analysis."""
    rev = revision()
    rst = restatement()
    cons = {r: consequence(r) for r in ("2025", "2026")}
    latest = RELEASE_LATEST
    return {
        "revision": rev, "restatement": rst, "restated_then_revised": restated_then_revised(),
        "added_later": added_later(), "filling": {r: filling(r, latest[r]) for r in latest},
        "consequence": cons, "validation": validation(), "latest": latest,
        "india": last_reported("2026", "IND"),
    }


def pct(a: float, b: float) -> str:
    return f"{100 * a / b:.1f}%" if b else "n/a"


def main() -> int:
    R = results()
    OUT.mkdir(exist_ok=True)
    print("1. REVISION between releases (same country-year, both present)")
    for g in ("util", "counted"):
        sel = [r for r in R["revision"] if r["group"] == g]
        print(f"   {g:<8} {sum(r['changed'] for r in sel)} changed of "
              f"{sum(r['pairs'] for r in sel):,} value pairs")
    print(f"   country-years added to the history later: {R['added_later']}")
    print("2. RESTATEMENT within release (identical to own previous year)")
    for g in ("util", "counted"):
        for rel in ("2024", "2025", "2026"):
            sel = [r for r in R["restatement"] if r["group"] == g and r["release"] == rel]
            lo = min(100 * r["identical"] / r["pairs"] for r in sel)
            hi = max(100 * r["identical"] / r["pairs"] for r in sel)
            print(f"   {g:<8} release {rel}: {lo:.1f}-{hi:.1f}% across variables")
    rr = R["restated_then_revised"]
    print(f"   restated in 2024, revised by 2026: {sum(r['revised_by_2026'] for r in rr)} "
          f"of {sum(r['restated_2024'] for r in rr):,}")
    print("3. FILLING by WHO (utilisation inputs, years up to the latest complete year)")
    for rel, c in R["filling"].items():
        used = sum(n for s, n in c.items() if s != "absent")
        print(f"   release {rel}: " + ", ".join(f"{s} {n:,}" for s, n in c.most_common())
              + f"  (WHO-supplied {pct(c['filled_earlier'] + c['filled_later'] + c['filled_other'] + c['overridden'], used)})")
    print("4. CONSEQUENCE: WHO's care estimate by provenance of its inputs")
    for rel, cons in R["consequence"].items():
        for r in cons:
            if r["year"] < WINDOW_START or r["year"] > R["latest"][rel]:
                continue
            print(f"   release {rel} {r['year']}: total ${r['total']/1e9:.2f} bn, care "
                  f"${r['ghs']/1e9:.2f} bn ({pct(r['ghs'], r['total'])}); new "
                  f"{pct(r['new'], r['ghs'])}, restated {pct(r['restated'], r['ghs'])}, "
                  f"WHO-supplied {pct(r['WHO-supplied'], r['ghs'])}; any input new "
                  f"{pct(r['new_any'], r['ghs'])}")
    i = R["india"]
    print(f"   India: last reported {i['last_reported']}; the same values since "
          f"{i['first_year_of_values']}, used by WHO through {i['used_through']}; care "
          f"estimate {RELEASE_LATEST['2026']} US$ {i['care_latest']/1e6:.0f} million")
    print("VALIDATION against WHO's published totals")
    ok = True
    for v in R["validation"]:
        ok &= v["match"]
        print(f"   {v['release']} report, {v['year']}: published US$ {v['published']} bn, "
              f"reconstructed {v['reconstructed']:.3f} -> {'match' if v['match'] else 'MISMATCH'}")
    with (OUT / "d3_consequence.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(R["consequence"]["2026"][0]))
        w.writeheader()
        for rel in R["consequence"]:
            w.writerows(R["consequence"][rel])
    if not ok:
        print("FAILED: the reconstruction does not reproduce WHO's published totals")
        return 1
    print(f"wrote {(OUT / 'd3_consequence.csv').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
