"""Assemble paper B's supplement from its template and generated content.

The prose lives in manuscript/supplementary_paper_b_template.md. The parts
that are facts about files or code are generated here, so they cannot drift:

  {{NOTE1_TABLE}}  every fetched file with its repository, commit and SHA-256,
                   read from data/vintages/vintage_manifest.csv
  {{NOTE2_FACTS}}  WHO's fill rule, the countries whose care estimate WHO sets
                   to zero, and the number of hand-coded substitutions, read
                   from WHO's own R code
  {{TABLE_S1}}     Table 4 repeated on the 2025 report, from make_tables_b.py

Usage: python -I manuscript/make_supplementary_b.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "manuscript"
TEMPLATE = HERE / "supplementary_paper_b_template.md"
OUT = HERE / "supplementary_paper_b.md"
MANIFEST = ROOT / "data" / "vintages" / "vintage_manifest.csv"
RAW = ROOT / "data" / "vintages" / "raw"


def note1() -> str:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    out = ["| Repository | Commit | File | Bytes | SHA-256 (first 16) |", "|---|---|---|---:|---|"]
    for r in rows:
        out.append(f"| {r['repository'].split('/')[-1]} | {r['commit'][:7]} | "
                   f"`{r['source_path']}` | {int(r['bytes']):,} | `{r['sha256'][:16]}` |")
    return "\n".join(out)


def note2() -> str:
    clean = (RAW / "gtbreport2026__finance__2a_clean_raw_data.R").read_text(encoding="utf-8")
    prep = (RAW / "gtbreport2026__finance__3_prepare_imputed_data.R").read_text(encoding="utf-8")
    # the fill rule: lag 1..4 then lead 1..4, applied to the six inputs
    block = prep[prep.index("Missing outpatient utilization data set to previous year"):]
    block = block[:block.index("ungroup()")]
    lags = re.findall(r"lag\(\.x,(\d)\)", block)
    leads = re.findall(r"lead\(\.x,(\d)\)", block)
    assert lags == ["1", "2", "3", "4"] and leads == ["1", "2", "3", "4"], (lags, leads)
    assert "SET GHS to 0 for countries where it is believed to be already reported" in prep
    # Which country-years WHO zeroed is read from WHO's processed output, not
    # parsed from the code: the code zeroes some countries in one block and
    # others elsewhere, and a parse of the block missed one. Zeroed means the
    # care estimate is 0 while its own components are not.
    sys.path.insert(0, str(ROOT / "demos"))
    import d3_vintages as d3
    years: dict[str, list[int]] = {}
    for r in d3.rows("proc2026"):
        comp = sum(d3.num(r.get(k)) or 0.0 for k in d3.COMPONENTS)
        if (d3.num(r["c_ghs"]) or 0.0) == 0 and comp > 0:
            years.setdefault(r["iso3"], []).append(int(r["year"]))
    zeroed = [f"{c} ({min(y)}–{max(y)})" for c, y in sorted(years.items())]
    n_lag = len(re.findall(r"\blag\(", clean))
    return "\n".join([
        f"- **Fill rule.** A missing value of any of the six inputs is replaced by the same "
        f"country's value from the previous year, then from up to {len(lags)} years earlier, then "
        f"from up to {len(leads)} years later, in that order (`lag(.x,1)` … `lag(.x,{lags[-1]})`, "
        f"then `lead(.x,1)` … `lead(.x,{leads[-1]})`).",
        f"- **Hand-coded substitutions.** The cleaning script contains {n_lag} uses of `lag()`, "
        "most replacing a specific country-year's value with the previous year's, alongside "
        "fixed values written into the code for named countries.",
        "- **Care estimate set to zero.** In WHO's processed file the care estimate is zero, "
        "although its components are not, for " + "; ".join(zeroed) + ". The code's comment on "
        "the main block of these reads \"SET GHS to 0 for countries where it is believed to be "
        "already reported\", that is, where national spending is thought to include it.",
    ])


def main() -> int:
    sys.path.insert(0, str(HERE))
    import make_tables_b as mt
    text = TEMPLATE.read_text(encoding="utf-8")
    parts = {"{{NOTE1_TABLE}}": note1(), "{{NOTE2_FACTS}}": note2(),
             "{{TABLE_S1}}": mt.render()["Table S1"]}
    for k, v in parts.items():
        assert k in text, k
        text = text.replace(k, v)
    assert "{{" not in text
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
