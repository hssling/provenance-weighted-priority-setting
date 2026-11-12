"""T5: structural existence. Standard library only.

Asks a different question from T1-T4. Those ask whether an indicator is trustworthy;
T5 asks whether an indicator exists for an intervention at all. A node maps to a WHO
budget line, or to None when no line item exists. The mapping is declared data, not
inferred from the series.

T5 is reported separately from the composite of T1-T4 and must not be folded into it.
An intervention with no measurable line is not a low-quality measurement: absence is
scored as absence, so it is not a TestResult.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass

from .series import BUDGET_CSV

# Node key -> label. Insertion order is evidence rank 1..11 (the order of the TB
# intervention table in the provenance spec); the order is part of the data.
NODE_LABELS: dict[str, str] = {
    "molecular_dx": "Molecular diagnostic scale-up (Xpert MTB/RIF, Xpert MTB/XDR)",    # rank 1
    "airborne_ipc": "Airborne infection prevention and control",                       # rank 2
    "tpt": "TB preventive therapy",                                                    # rank 3
    "wgs_dst": "Whole-genome sequencing for drug-susceptibility prediction",           # rank 4
    "acf": "Active case finding",                                                      # rank 5
    "short_regimen": "Shorter all-oral regimen rollout (BPaL/BPaL-M)",                 # rank 6
    "bovine_tb": "Bovine tuberculosis control",                                        # rank 7
    "private_sector": "Private-sector engagement",                                     # rank 8
    "nutrition": "Nutritional support",                                                # rank 9
    "milk_pasteurisation": "Milk pasteurisation / dairy food chain",                   # rank 10
    "tb_hiv_dm": "Integrated TB-HIV-diabetes care",                                    # rank 11
}

# WHO data dictionary definition of each budget column the mapping uses. Verbatim, transcribed
# from TB_dictionary_2026-08-25.csv (not in this repo's data/, which is immutable). A mapping
# is judged against this definition, never against the column name: budget_prog reads like
# "programme" but is defined as programme costs to TREAT drug-susceptible TB.
BUDGET_DEFINITIONS: dict[str, str] = {
    "budget_lab": "Budget required for laboratory infrastructure, equipment and supplies (US Dollars)",
    "budget_tpt": "Budget required for TB preventive treatment: drugs (US Dollars)",
    "budget_sld": "Budget required for drugs to treat drug-resistant TB (US Dollars)",
    "budget_patsup": "Budget required for patient support (US Dollars)",
    "budget_prog": "Budget required for programme costs to treat drug-susceptible TB (US Dollars)",
    "budget_tbhiv": "Budget required for collaborative TB/HIV activities (US Dollars)",
}

# Node key -> WHO TB budget column, or None for no line item. Each mapped column's definition
# is in BUDGET_DEFINITIONS above. check_mapping_targets() guards typos (a real intervention
# mistyped into a false "invisible"); it cannot catch a wrong-but-real column, so the
# definitions are the check against that.
TB_BUDGET_MAPPING: dict[str, str | None] = {
    "molecular_dx": "budget_lab",        # full match: Xpert is laboratory equipment and supplies
    "airborne_ipc": None,                # no WHO line
    "tpt": "budget_tpt",                 # partial: drugs only (see TB_BUDGET_PARTIAL)
    "wgs_dst": None,                     # no WHO line
    "acf": None,                         # no line. budget_prog is treatment, not finding (ruling S)
    "short_regimen": "budget_sld",       # partial: drugs only (see TB_BUDGET_PARTIAL)
    "bovine_tb": None,                   # no WHO line
    "private_sector": None,              # no WHO line
    "nutrition": "budget_patsup",        # full match: patient support is broader than nutrition but contains it
    "milk_pasteurisation": None,         # no WHO line
    "tb_hiv_dm": "budget_tbhiv",         # partial: TB/HIV arms only (see TB_BUDGET_PARTIAL)
}

# Node keys mapped to a budget line that covers only part of the node. Mapped, so not invisible
# (score 1.0), but the score does not mean the whole intervention is costed. Each note says what
# is and is not covered.
#
# CAVEAT FOR ANY BUDGET-SHARE COMPARISON: for these three nodes the comparison is against a
# DRUGS-ONLY line (or TB/HIV-only). A node can look underfunded simply because its non-drug cost
# (delivery, contact tracing, adherence, programme work) is pooled in a line that cannot be
# attributed to it. Read a low budget share for these nodes as a floor on tracked spending,
# not as a measure of spending on the intervention.
TB_BUDGET_PARTIAL: dict[str, str] = {
    "tpt": "budget_tpt covers TB preventive treatment drugs only. Delivery, contact tracing and adherence support are not covered.",
    "short_regimen": "budget_sld covers drugs to treat drug-resistant TB only. Rollout programme work is not covered; DR-TB programme costs sit in budget_mdrmgt, which no node maps to.",
    "tb_hiv_dm": "budget_tbhiv covers collaborative TB/HIV activities. The diabetes arm is not covered.",
}


@dataclass(frozen=True)
class ExistenceReport:
    """Existence of a budget line per node. Deliberately not a TestResult: there is no
    testable flag and no single composite score, because absence is not instability."""
    mapped: dict[str, str]     # node key -> budget column
    invisible: list[str]       # labels of nodes with no budget line, in node order
    score: dict[str, float]    # node key -> 1.0 mapped, 0.0 invisible


def existence_report(nodes: dict[str, str], mapping: dict[str, str | None]) -> ExistenceReport:
    if set(nodes) != set(mapping):
        missing = sorted(set(nodes) - set(mapping))
        extra = sorted(set(mapping) - set(nodes))
        raise ValueError(f"mapping must cover exactly the nodes: missing {missing}, extra {extra}")
    mapped: dict[str, str] = {}
    invisible: list[str] = []
    score: dict[str, float] = {}
    for key, label in nodes.items():
        target = mapping[key]
        if target is None:
            invisible.append(label)
            score[key] = 0.0
            continue
        if not target:
            raise ValueError(f"node {key!r}: empty budget line; use None for no line item")
        mapped[key] = target
        score[key] = 1.0
    return ExistenceReport(mapped, invisible, score)


def check_mapping_targets(mapping: dict[str, str | None], path=BUDGET_CSV) -> list[str]:
    """Return mapped budget lines that are not columns of the WHO budget CSV (sorted)."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        columns = set(next(csv.reader(fh)))
    return sorted({t for t in mapping.values() if t is not None and t not in columns})
