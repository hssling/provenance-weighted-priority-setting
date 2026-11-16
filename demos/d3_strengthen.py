"""D3 strengthening: how much WHO's 2025 TB care estimate depends on inputs that are not current.

Implements docs/paper_b_strengthening_plan.md (S1 input age, S2 re-measurement adjustment, S3
concentration) on top of demos/d3_vintages.py, whose provenance classification and reconstruction (which
reproduces WHO's published totals) are reused unchanged. Standard library only.
Usage: python -I demos/d3_strengthen.py
"""
from __future__ import annotations

import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d3_vintages as d3                                   # noqa: E402

RELEASE, YEAR, CHECK_YEAR = "2026", 2025, 2024
HOSPITAL = {"c_hospital_nmdr": ("hospd_dstb_prct", "hospd_dstb_dur"),
            "c_hospital_mdr": ("hospd_mdr_prct", "hospd_mdr_dur")}
CLINIC = {"c_clinic_nmdr": ("hcfvisit_dstb",), "c_clinic_mdr": ("hcfvisit_mdr",)}
AGE_BINS = ["0", "1", "2", "3", "4", "5+", "unknown"]


def raw() -> dict:
    return d3.releases()["util"][RELEASE]


def run_start(c: str, y: int, v: str) -> int | None:
    """First year of the unchanged run of reported values that ends at (c, y)."""
    r = raw()
    val = (r.get((c, y)) or {}).get(v)
    if val is None:
        return None
    s = y
    while (r.get((c, s - 1)) or {}).get(v) == val:
        s -= 1
    return s


def input_age(c: str, y: int, v: str, state: str) -> int | None:
    """Plan S1. None means the age cannot be established (overridden, or filled from no matching year)."""
    if state == "new":
        return 0
    if state == "restated":
        return y - run_start(c, y, v)
    if state in ("filled_earlier", "filled_later"):
        proc_val = d3.table(f"proc{RELEASE}", d3.UTIL, "plain")[(c, y)][v]
        for k in d3.WHO_FILL_ORDER:
            if (raw().get((c, y + k)) or {}).get(v) == proc_val:
                if k < 0:
                    return -k + (y + k - run_start(c, y + k, v))
                return k
    return None


def rates() -> dict[str, list[float]]:
    """Plan S2: annual log rate of change at each re-measurement, pooled by variable, 2018-2025."""
    r = raw()
    out: dict[str, list[float]] = defaultdict(list)
    series = defaultdict(list)
    for (c, y), rec in r.items():
        if d3.WINDOW_START - 1 <= y <= YEAR:
            for v in d3.UTIL:
                if rec.get(v) is not None:
                    series[(c, v)].append((y, rec[v]))
    for (c, v), pts in series.items():
        pts.sort()
        for (y0, a), (y1, b) in zip(pts, pts[1:]):
            if y1 >= d3.WINDOW_START and b != a and a > 0 and b > 0:
                out[v].append(math.log(b / a) / (y1 - y0))
    return out


def quartiles(xs: list[float]) -> tuple[float, float, float]:
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return q[0], statistics.median(xs), q[2]


def components(year: int) -> list[dict]:
    """Every cost component that reaches the published total in `year`, with its inputs' provenance."""
    prov = d3.provenance(RELEASE)
    proc = d3.table(f"proc{RELEASE}", d3.UTIL, "plain")
    out = []
    for row in d3.rows(f"proc{RELEASE}"):
        c, y = row["iso3"], int(row["year"])
        if y != year:
            continue
        ghs = d3.num(row["c_ghs"]) or 0.0
        if ghs == 0:
            continue
        for comp, inputs in {**HOSPITAL, **CLINIC}.items():
            cost = d3.num(row.get(comp)) or 0.0
            if cost == 0:
                continue
            states = [prov[(c, y, v)] for v in inputs]
            ages = [input_age(c, y, v, s) for v, s in zip(inputs, states)]
            out.append({"iso3": c, "hb": row.get("g_hb_tb") in ("TRUE", "True", "1", "true"), "comp": comp,
                        "cost": cost, "inputs": inputs, "values": [proc[(c, y)][v] for v in inputs],
                        "states": states, "ages": ages, "cls": d3.component_class(states),
                        "age": None if any(a is None for a in ages) else max(ages)})
    return out


def adjusted(comps: list[dict], q: dict[str, tuple[float, float, float]], which: int) -> float:
    """Plan S2: rescale each component by the ratio of adjusted to original input product."""
    total = 0.0
    for k in comps:
        factor = 1.0
        for v, val, s, a in zip(k["inputs"], k["values"], k["states"], k["ages"]):
            if s == "new" or a is None or a == 0 or not val:
                continue
            factor *= math.exp(q[v][which] * a)
        total += k["cost"] * factor
    return total


def summary(year: int) -> dict:
    comps = components(year)
    care = sum(k["cost"] for k in comps)
    age_share = defaultdict(float)
    for k in comps:
        b = "unknown" if k["age"] is None else ("5+" if k["age"] >= 5 else str(k["age"]))
        age_share[b] += k["cost"]
    rt = rates()
    q = {v: quartiles(rt[v]) for v in d3.UTIL}
    adj = {name: adjusted(comps, q, i) for i, name in enumerate(("q25", "median", "q75"))}
    by_c = defaultdict(lambda: {"care": 0.0, "new": 0.0, "hb": False})
    for k in comps:
        by_c[k["iso3"]]["care"] += k["cost"]
        by_c[k["iso3"]]["hb"] = by_c[k["iso3"]]["hb"] or k["hb"]
        if k["cls"] == "new":
            by_c[k["iso3"]]["new"] += k["cost"]
    old = {c: d for c, d in by_c.items() if d["new"] < 0.5 * d["care"]}
    hb = {c: d for c, d in by_c.items() if d["hb"]}
    hb_old = {c: d for c, d in old.items() if d["hb"]}
    adj_c = {}
    for c in sorted(hb, key=lambda c: -hb[c]["care"]):
        cc = [k for k in comps if k["iso3"] == c]
        adj_c[c] = {n: adjusted(cc, q, i) for i, n in enumerate(("q25", "median", "q75"))}
    return {"year": year, "care": care, "n_components": len(comps), "age_share": dict(age_share),
            "rates": {v: (len(rt[v]), q[v]) for v in d3.UTIL}, "adjusted": adj,
            "countries": len(by_c), "old": old, "old_care": sum(d["care"] for d in old.values()),
            "hb": hb, "hb_old": hb_old, "adj_hb": adj_c}


def main() -> int:
    for year in (YEAR, CHECK_YEAR):
        s = summary(year)
        care = s["care"]
        print(f"\n===== release {RELEASE}, year {year}: care estimate US$ {care / 1e9:.3f} bn "
              f"({s['n_components']} components, {s['countries']} countries)")
        print("S1 age share:", {k: f"{100 * v / care:.1f}%" for k, v in sorted(s["age_share"].items(), key=lambda kv: AGE_BINS.index(kv[0]))})
        print("S2 rates (n, q25, median, q75):", {v: (n, tuple(round(x, 3) for x in q)) for v, (n, q) in s["rates"].items()})
        print("S2 adjusted care (bn): " + ", ".join(f"{k} {v / 1e9:.3f} ({100 * (v / care - 1):+.1f}%)" for k, v in s["adjusted"].items()))
        print(f"S3 countries with <50% newly reported: {len(s['old'])} of {s['countries']}, "
              f"{100 * s['old_care'] / care:.1f}% of the care estimate; high-burden among them: "
              f"{len(s['hb_old'])} of {len(s['hb'])}")
        for c in sorted(s["hb"], key=lambda c: -s["hb"][c]["care"]):
            d = s["hb"][c]; a = s["adj_hb"][c]
            print(f"   {c} care US$ {d['care'] / 1e6:7.1f} m  new {100 * d['new'] / d['care']:5.1f}%  "
                  f"adjusted median {100 * (a['median'] / d['care'] - 1):+6.1f}% "
                  f"[{100 * (a['q25'] / d['care'] - 1):+.1f}%, {100 * (a['q75'] / d['care'] - 1):+.1f}%]")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
