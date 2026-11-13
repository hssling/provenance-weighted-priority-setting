"""Generate paper A's supplementary material from the data and the code.

Nothing here is typed. The mapping table is rendered from the declared
mapping and the two WHO definition sets; the financial table is read from the
archived India TB Report extract; the cross-country counts are recomputed
from the WHO budget file. A supplementary file that is hand-maintained drifts
from the paper it supports, which is the failure this whole project is about.

Usage: python -I manuscript/make_supplementary_a.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from provenance.existence import (                                  # noqa: E402
    BUDGET_DEFINITIONS, DCF_DEFINITIONS, NODE_LABELS, TB_BUDGET_MAPPING,
    TB_BUDGET_COMMODITY_ONLY, TB_BUDGET_NO_LINE_BY_DICTIONARY, TB_BUDGET_POOLED,
)

# Table 2 and Figure 2 list interventions in the order of the budget lines they
# reach; the supplement follows the same order so a reader can read across.
LINE_ORDER = ["budget_lab", "budget_prog", "budget_tpt", "budget_sld",
              "budget_patsup", "budget_tbhiv", None]

OUT = ROOT / "manuscript" / "supplementary_paper_a.md"


def condition(key: str) -> str:
    if TB_BUDGET_MAPPING[key] is None:
        return "no line"
    if key in TB_BUDGET_POOLED:
        return "pooled"
    if key in TB_BUDGET_COMMODITY_ONLY:
        return "commodity only"
    return "dominant"


def main() -> int:
    L: list[str] = [
        "# Supplementary material (for online publication only)",
        "",
        "**What a tuberculosis budget cannot see: fiscal invisibility and the limits of "
        "the WHO funding-gap indicator in India, 2017-2025**",
        "",
        "Every table in this file is generated from the archived input files and the "
        "deposited code by `manuscript/make_supplementary_a.py`; none is hand-entered. "
        "Section numbers refer to the main text.",
        "",
        "---",
        "",
        "## S1. The intervention-to-budget-line mapping, with both WHO definitions",
        "",
        "Table 2 of the main text classifies each intervention. This table gives the "
        "evidence: the WHO budget column each intervention maps to, the definition of "
        "that column in the **data dictionary** distributed with the datasets, and the "
        "definition of the same column in the **data collection form** that countries "
        "complete [9]; the dictionary is reference [8] of the main text. Where the two "
        "differ, the form governs (SS2.3). The last column applies the dictionary's "
        "definitions instead, which SS3.5 reports.",
        "",
        "| Intervention | Column | Coverage (form) | Dictionary definition | "
        "Collection-form definition | Coverage if the dictionary governed |",
        "|---|---|---|---|---|---|",
    ]
    keys = sorted(NODE_LABELS, key=lambda k: (LINE_ORDER.index(TB_BUDGET_MAPPING[k]),
                                              list(NODE_LABELS).index(k)))
    for key in keys:
        label = NODE_LABELS[key]
        col = TB_BUDGET_MAPPING[key]
        dic = BUDGET_DEFINITIONS.get(col, "—") if col else "—"
        dcf = DCF_DEFINITIONS.get(col, "—") if col else "—"
        by_dict = "no line" if key in TB_BUDGET_NO_LINE_BY_DICTIONARY else condition(key)
        L.append(f"| {label} | {col or '—'} | {condition(key)} | {dic} | {dcf} | {by_dict} |")
    L += ["", f"Under the form, {sum(TB_BUDGET_MAPPING[k] is None for k in keys)} "
          f"interventions have no line; under the dictionary, "
          f"{len(TB_BUDGET_NO_LINE_BY_DICTIONARY)}."]

    L += ["", "Notes on the pooled and commodity-only conditions, verbatim from the code:", ""]
    for key, note in {**TB_BUDGET_POOLED, **TB_BUDGET_COMMODITY_ONLY}.items():
        L.append(f"- **{NODE_LABELS[key]}** — {note}")

    # ---- S2: the national financial series behind Figure 1 -------------------
    rows = list(csv.DictReader(
        (ROOT / "data" / "india_tb_report_table16_1.csv").open(encoding="utf-8-sig")))
    L += ["", "---", "", "## S2. India's national programme accounts, year by year",
          "",
          "The series behind Figure 1, as published in the India TB Report 2024, "
          "Table 16.1 (p.174). Amounts are in INR crore. The shortfall column is "
          "(requested - approved) / requested. Two cells of the source table were "
          "damaged in text extraction and were restored digit by digit against the "
          "printed page. Released amounts are not printed for 2022 and 2023.",
          "",
          "| Fiscal year | Requested | Approved | Released | Spent | Shortfall |",
          "|---|---:|---:|---:|---:|---:|"]
    tot = defaultdict(float)
    for r in rows:
        req, app = float(r["requested"]), float(r["approved"])
        short = f"{100 * (req - app) / req:.1f}%" if req else "—"
        num = lambda k: f"{float(r[k]):,.2f}" if r[k].strip() else "not published"
        L.append(f"| {r['year']} | {num('requested')} | {num('approved')} | "
                 f"{num('released')} | {num('spent')} | {short} |")
        for k in ("requested", "approved", "released", "spent"):
            if r[k].strip():
                tot[k] += float(r[k])
    L.append(f"| **Total** | **{tot['requested']:,.2f}** | **{tot['approved']:,.2f}** | "
             f"**{tot['released']:,.2f}** | **{tot['spent']:,.2f}** | "
             f"**{100 * (tot['requested'] - tot['approved']) / tot['requested']:.1f}%** |")

    # ---- S3: how every country reports the two fields ------------------------
    brows = list(csv.DictReader(
        (ROOT / "data" / "TB_budget_2026-11-12.csv").open(encoding="utf-8-sig")))
    by = defaultdict(list)
    for r in brows:
        try:
            b, c = float(r["budget_tot"]), float(r["cf_tot"])
        except (ValueError, KeyError):
            continue
        by[r["iso3"]].append(b == c)
    eligible = {k: v for k, v in by.items() if len(v) >= 5}
    always = sorted(k for k, v in eligible.items() if all(v))
    never = sorted(k for k, v in eligible.items() if not any(v))
    L += ["", "---", "", "## S3. How countries report the two fields",
          "",
          f"Of the **{len(eligible)}** countries with five or more years of both "
          f"`budget_tot` and `cf_tot`, **{len(always)}** report expected funding exactly "
          f"equal to budget required in every year, so their published funding gap is "
          f"zero by construction; **{len(never)}** report a non-zero gap in every year. "
          "The remainder do both at different times.",
          "",
          f"**Always equal ({len(always)}):** " + ", ".join(always) + ".",
          "",
          f"**Never equal ({len(never)}):** " + ", ".join(never) + ".",
          ""]

    OUT.write_text("\n".join(L).replace("SS", chr(0xA7)) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(NODE_LABELS)} interventions, "
          f"{len(rows)} fiscal years, {len(eligible)} countries "
          f"({len(always)} always equal, {len(never)} never equal)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
