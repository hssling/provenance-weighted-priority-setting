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

# Node key -> WHO TB budget column, or None for no line item.
#
# Each mapping must be checked against the WHO data dictionary DEFINITION of the column,
# not against its name. A plausible name is not evidence: budget_prog reads like
# "programme" and was once mapped to active case finding, but WHO defines it as
# "Budget required for programme costs to treat drug-susceptible TB", so ACF is invisible.
# check_mapping_targets() guards against typos in the other direction (a real intervention
# mistyped into a false "invisible"); it cannot catch a wrong-but-real column.
#
# Definitions quoted from the WHO data dictionary are marked "WHO:". Entries marked
# "UNVERIFIED" still need their definition pulled from the dictionary before publication.
#
# Partial coverage (mapped, but not the whole node): recorded here in a comment rather than
# as a field on ExistenceReport, so the report keeps the fields the spec defines and T5
# stays a plain existence score. Partial entries are listed in TB_BUDGET_PARTIAL below.
TB_BUDGET_MAPPING: dict[str, str | None] = {
    "molecular_dx": "budget_lab",        # lab line; UNVERIFIED definition
    "airborne_ipc": None,                # no WHO line; UNVERIFIED that no column under another name covers it
    "tpt": "budget_tpt",                 # TPT line; UNVERIFIED definition
    "wgs_dst": None,                     # no WHO line for sequencing; UNVERIFIED
    "acf": None,                         # WHO: budget_prog is "Budget required for programme costs to treat drug-susceptible TB". Active case finding is not treatment, so no line.
    "short_regimen": "budget_sld",       # second-line drugs line; UNVERIFIED definition
    "bovine_tb": None,                   # no WHO line; UNVERIFIED
    "private_sector": None,              # no WHO line; UNVERIFIED
    "nutrition": "budget_patsup",        # patient support line; UNVERIFIED definition
    "milk_pasteurisation": None,         # no WHO line; UNVERIFIED
    "tb_hiv_dm": "budget_tbhiv",         # WHO: "collaborative TB/HIV activities". Mapped but partial: covers the TB and HIV arms, not diabetes.
}

# Node keys whose mapping is mapped but only partly covers the node, with what is not covered.
TB_BUDGET_PARTIAL: dict[str, str] = {
    "tb_hiv_dm": "diabetes arm has no budget line; the TB/HIV arms are covered by budget_tbhiv",
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
