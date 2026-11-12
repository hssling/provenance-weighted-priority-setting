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

# Node key -> WHO TB budget column (a line of the budget CSV), or None for no line item.
# Rationale per entry is the spec's mapping; check_mapping_targets() confirms each target
# is a real column so a typo cannot silently create a false "invisible".
# Caveats, to be confirmed by the project owner rather than assumed here:
#   acf -> budget_prog: the WHO column is a general programme-management line, not an
#          active-case-finding line; mapping it makes ACF "visible" by proxy.
#   tb_hiv_dm -> budget_tbhiv: the column covers TB/HIV only, not diabetes.
TB_BUDGET_MAPPING: dict[str, str | None] = {
    "molecular_dx": "budget_lab",
    "airborne_ipc": None,
    "tpt": "budget_tpt",
    "wgs_dst": None,
    "acf": "budget_prog",
    "short_regimen": "budget_sld",
    "bovine_tb": None,
    "private_sector": None,
    "nutrition": "budget_patsup",
    "milk_pasteurisation": None,
    "tb_hiv_dm": "budget_tbhiv",
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
