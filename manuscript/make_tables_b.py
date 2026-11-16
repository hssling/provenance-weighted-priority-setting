"""Write paper B's vintage-analysis tables from the code, never by hand.

Tables 1-4 of paper B are rendered here from demos/d3_vintages.py and written
to manuscript/tables_paper_b.md. The manuscript carries the same blocks, and
verification/check_manuscript_numbers.py fails if any block in the manuscript
differs from a fresh rendering. Table 6 (the 443-variable screen) is checked
against demos/d2_who_data_screen.py as before.

Usage: python -I manuscript/make_tables_b.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "demos"))
import d3_vintages as d3                                       # noqa: E402

OUT = ROOT / "manuscript" / "tables_paper_b_tmih.md"   # TMIH version
RELEASE_NAME = {"2024": "Jul 2024", "2025": "Jul 2025", "2026": "Aug 2026"}
LABEL = {
    "hcfvisit_dstb": "Outpatient visits per patient, drug-susceptible TB",
    "hcfvisit_mdr": "Outpatient visits per patient, MDR/RR-TB",
    "hospd_dstb_prct": "Share hospitalised, drug-susceptible TB",
    "hospd_mdr_prct": "Share hospitalised, MDR/RR-TB",
    "hospd_dstb_dur": "Days in hospital, drug-susceptible TB",
    "hospd_mdr_dur": "Days in hospital, MDR/RR-TB",
    "exp_fld": "Expenditure on first-line drugs",
    "exp_lab": "Expenditure on laboratory equipment and supplies",
    "exp_staff": "Expenditure on programme staff",
    "exp_prog": "Expenditure on programme management",
}


def pc(a: float, b: float) -> str:
    return f"{100 * a / b:.1f}%"


def table1(R: dict) -> str:
    rows = ["**Table 1. Revision of published values between WHO releases.** Each value is one "
            "country-year of one variable present in both releases.", "",
            "| Variables | Releases compared | Values in both releases | Values changed |",
            "|---|---|---:|---:|"]
    for group, label in (("util", "Utilisation inputs (6)"), ("counted", "Expenditure lines (4)")):
        for a, b in (("2024", "2025"), ("2025", "2026")):
            sel = [r for r in R["revision"] if r["group"] == group and r["from"] == a]
            rows.append(f"| {label} | {RELEASE_NAME[a]} → {RELEASE_NAME[b]} | "
                        f"{sum(r['pairs'] for r in sel):,} | {sum(r['changed'] for r in sel):,} |")
    changed = changed_values()
    names = {r["iso3"]: r["country"] for r in d3.rows("pub2026")}
    iso = sorted({names[k[0]] for k, _, _, _ in changed})
    rows += ["", f"*The {len(changed)} changed values are the {', '.join(iso)}'s "
             f"{', '.join(sorted({str(k[1]) for k, _, _, _ in changed}))} expenditure "
             f"({', '.join(LABEL[v].replace('Expenditure on ', '') for _, v, _, _ in changed)}), "
             f"each by less than {max_rel_change(changed):.1f}%. Utilisation inputs: outpatient "
             "visits per patient, share hospitalised and days in hospital, each for drug-susceptible "
             "and MDR/RR-TB.*"]
    return "\n".join(rows)


def changed_values() -> list[tuple]:
    rel = d3.releases()["counted"]
    out = []
    for a, b in (("2024", "2025"), ("2025", "2026")):
        for k, rec in rel[a].items():
            for v in d3.COUNTED:
                x, y = rec[v], (rel[b].get(k) or {}).get(v)
                if x is not None and y is not None and x != y:
                    out.append((k, v, x, y))
    return out


def max_rel_change(changed: list[tuple]) -> float:
    worst = max(abs(y - x) / abs(x) for _, _, x, y in changed)
    # report the bound at one decimal, rounded up so it is never understated
    return (int(worst * 1000) + 1) / 10


def table2(R: dict) -> str:
    rows = ["**Table 2. Restatement: share of a country's values identical to its own value for "
            f"the previous year, by release, reporting years {d3.WINDOW_START} onwards.** "
            "Consecutive country-year pairs compared in brackets.",
            "", "| Variable | " + " | ".join(RELEASE_NAME.values()) + " |",
            "|---|---:|---:|---:|"]
    for v in d3.UTIL + d3.COUNTED:
        cells = []
        for rel in RELEASE_NAME:
            r = next(x for x in R["restatement"] if x["variable"] == v and x["release"] == rel)
            cells.append(f"{pc(r['identical'], r['pairs'])} ({r['pairs']:,})")
        rows.append(f"| {LABEL[v]} | " + " | ".join(cells) + " |")
    rr = R["restated_then_revised"]
    rows += ["", f"*Of the {sum(r['restated_2024'] for r in rr):,} utilisation values restated in "
             f"the July 2024 release, {sum(r['revised_by_2026'] for r in rr):,} had been revised by "
             "the August 2026 release.*"]
    return "\n".join(rows)


STATE_LABEL = [
    ("new", "Reported, differs from the previous year"),
    ("restated", "Reported, identical to the previous year"),
    ("filled_earlier", "Not reported; WHO used an earlier year's value"),
    ("filled_later", "Not reported; WHO used a later year's value"),
    ("filled_other", "Not reported; WHO value matches no reported year"),
    ("overridden", "Reported, but WHO used a different value"),
    ("absent", "No value used"),
]


def table3(R: dict) -> str:
    l25, l26 = R["latest"]["2025"], R["latest"]["2026"]
    rows = ["**Table 3. Where the utilisation inputs to WHO's spending estimate came from.** "
            f"Country-year values for the six inputs, {d3.WINDOW_START}–{l25} in the 2025 report "
            f"and {d3.WINDOW_START}–{l26} in the 2026 report, in the countries WHO includes.", "",
            f"| Provenance | 2025 report | 2026 report |", "|---|---:|---:|"]
    f25, f26 = R["filling"]["2025"], R["filling"]["2026"]
    t25, t26 = sum(f25.values()), sum(f26.values())
    for key, label in STATE_LABEL:
        rows.append(f"| {label} | {f25[key]:,} ({pc(f25[key], t25)}) | "
                    f"{f26[key]:,} ({pc(f26[key], t26)}) |")
    rows.append(f"| Total | {t25:,} | {t26:,} |")
    rows += ["", "*WHO's pipeline fills a missing value from the same country's nearest year, up "
             "to four years earlier and then up to four years later; the year is identified here by "
             "matching the value used to the country's reported values in that order.*"]
    return "\n".join(rows)


def table4(R: dict, release: str = "2026", label: str = "Table 4") -> str:
    rows = [f"**{label}. WHO's estimate of spending on inpatient and outpatient TB care, by "
            f"provenance of the inputs it was computed from, {release} report.** Each cost component "
            "(bed-days and outpatient visits, for drug-susceptible and MDR/RR-TB) is classed by its "
            "own inputs: WHO-supplied if any input was filled or replaced by WHO, restated if any "
            "other input repeats the previous year, otherwise newly reported.", "",
            "| Year | Total funding, US$ bn | Care estimate, US$ bn | Care, % of total | "
            "Newly reported | Restated | WHO-supplied | Any input newly reported |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in R["consequence"][release]:
        if not d3.WINDOW_START <= r["year"] <= R["latest"][release]:
            continue
        g = r["ghs"]
        rows.append(f"| {r['year']} | {r['total']/1e9:.2f} | {g/1e9:.2f} | {pc(g, r['total'])} | "
                    f"{pc(r['new'], g)} | {pc(r['restated'], g)} | {pc(r['WHO-supplied'], g)} | "
                    f"{pc(r['new_any'], g)} |")
    v = {(x["release"], x["year"]): x for x in R["validation"] if x["release"] == release}
    rows += ["", "*Total funding is funding received by national programmes plus the care "
             "estimate, as WHO computes it. The reconstruction reproduces WHO's published totals: "
             + "; ".join(f"US$ {x['published']} billion for {x['year']} in the {x['release']} "
                         f"report (reconstructed {x['reconstructed']:.2f})" for x in v.values())
             + ". The last column is a sensitivity analysis counting a component as current if any "
             "one of its inputs was newly reported.*"]
    return "\n".join(rows)


def table5() -> str:
    """Age of the inputs behind the care estimate, and the estimate adjusted for re-measurement
    (docs/paper_b_strengthening_plan.md, S1-S3), 2026 report, 2024 and 2025."""
    import d3_strengthen as ds
    S = {y: ds.summary(y) for y in (2024, 2025)}
    bn = lambda x: f"{x / 1e9:.2f}"
    sh = lambda s, k: f"{100 * s['age_share'].get(k, 0.0) / s['care']:.1f}%"
    rows = ["**Table 5. Age of the inputs behind WHO's care estimate, and the estimate adjusted for "
            "re-measurement, 2026 report.** Age is the number of years since an input's value last changed in "
            "the country's reported series; a cost component takes the age of its oldest input.", "",
            "| | 2024 | 2025 |", "|---|---:|---:|",
            f"| Care estimate, US$ bn | {bn(S[2024]['care'])} | {bn(S[2025]['care'])} |"]
    labels = {"0": "Inputs reported for the year (age 0)", "1": "Age 1 year", "2": "Age 2 years",
              "3": "Age 3 years", "4": "Age 4 years", "5+": "Age 5 years or more", "unknown": "Age not established"}
    for k in ds.AGE_BINS:
        rows.append(f"| {labels[k]} | {sh(S[2024], k)} | {sh(S[2025], k)} |")
    adj = lambda s: f"{bn(s['adjusted']['median'])} ({100 * (s['adjusted']['median'] / s['care'] - 1):+.1f}%)".replace("-", "−")
    rows.append(f"| Adjusted at the median re-measurement rate, US$ bn | {adj(S[2024])} | {adj(S[2025])} |")
    cty = lambda s: f"{len(s['old'])} of {s['countries']} ({100 * s['old_care'] / s['care']:.1f}%)"
    rows.append(f"| Countries with less than half of their estimate on inputs reported for the year "
                f"(share of the estimate) | {cty(S[2024])} | {cty(S[2025])} |")
    rows.append(f"| Of these, flagged high TB burden by WHO | {len(S[2024]['hb_old'])} of {len(S[2024]['hb'])} | "
                f"{len(S[2025]['hb_old'])} of {len(S[2025]['hb'])} |")
    rows += ["", "*Shares are of the care estimate in US dollars. The adjustment moves every input that was not "
             "reported for the year by the median annual rate of change observed when countries re-measure that "
             "input, for each year of its age; newly reported inputs are unchanged. High TB burden: the flag in "
             "WHO's processed file for the 2026 report, counted among countries with a care estimate.*"]
    return "\n".join(rows)


def table_s2() -> str:
    """Per high-burden country, 2025 (plan S3)."""
    import d3_strengthen as ds
    s = ds.summary(2025)
    names = {r["iso3"]: r["country"] for r in d3.rows("proc2026")}
    rows = ["**Supplementary Table S2. WHO's 2025 care estimate in the countries WHO flags as high TB burden, "
            "by the provenance of its inputs.**", "",
            "| Country | Care estimate, US$ million | Share on inputs reported for 2025 | "
            "Adjusted at the median rate | Adjusted at the 25th and 75th percentile rates |",
            "|---|---:|---:|---:|---:|"]
    for c in sorted(s["hb"], key=lambda c: -s["hb"][c]["care"]):
        d, a = s["hb"][c], s["adj_hb"][c]
        p = lambda x: f"{100 * (x / d['care'] - 1):+.1f}%".replace("-", "−")
        rows.append(f"| {names.get(c, c)} | {d['care'] / 1e6:.1f} | {100 * d['new'] / d['care']:.1f}% | {p(a['median'])} | "
                    f"{p(a['q25'])} to {p(a['q75'])} |")
    rows += ["", "*The percentile columns apply the 25th or 75th percentile rate to every non-current input at "
             "once; compounded over ages of five years or more they span a range too wide to bound the estimate "
             "and are shown to convey how uncertain a value is once it stops being re-measured.*"]
    return "\n".join(rows)


def render() -> dict[str, str]:
    R = d3.results()
    return {"Table 1": table1(R), "Table 2": table2(R), "Table 3": table3(R), "Table 4": table4(R),
            "Table 5": table5(),
            "Table S1": table4(R, "2025", "Supplementary Table S1"), "Table S2": table_s2()}


def main() -> int:
    blocks = render()
    OUT.write_text("\n\n".join(blocks.values()) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {', '.join(blocks)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
