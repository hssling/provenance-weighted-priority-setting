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
import re
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
# from data/TB_dictionary_2026-08-25.csv (checked against that file in the tests). A mapping
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

# The data dictionary is an abbreviation of the data collection form, and for budget_prog
# the abbreviation changes the meaning. The form (doc/who_tb_dcf2026.pdf in WHO's own
# gtbreport2026 repository) is the instrument countries actually complete, so it governs.
# Transcribed verbatim; the divergence is itself a finding and is reported, not smoothed.
DCF_DEFINITIONS: dict[str, str] = {
    "budget_lab": "Building, maintaining, and renovating TB laboratories, laboratory equipment "
                  "purchase and maintenance, consumables for all tests (including TB screening "
                  "for people living with HIV/AIDS and diagnosis of latent TB infection), "
                  "quality assurance, retooling and the transportation of specimens.",
    "budget_prog": "The management and supervision of the TB control programme, training, policy "
                   "development, meetings, visits for supervision, purchase of office "
                   "equipment/vehicles, construction of buildings for use by programme staff, "
                   "routine surveillance, advocacy and communication, public-private mix "
                   "activities, community engagement, active case-finding, infection control, "
                   "management of TB drug procurement and distribution, and programme activities "
                   "linked to contact investigation for TB preventive treatment",
    "budget_tpt": "Drugs for TB preventive treatment, as per latest WHO guidance "
                  "(6H, 9H, 4R, 3HR and Levofloxacin)",
    "budget_sld": "Drugs to treat drug-resistant TB (RR-TB, MDR-TB, pre-XDR-TB or XDR-TB). "
                  "Include drugs to deal with adverse event",
    "budget_patsup": "Cash transfers, food packages, transportation vouchers, educational and "
                     "emotional support to patient or other in-kind benefits given to TB "
                     "patients, mobile phone (airtime or device for V.O.T), medications "
                     "monitors (digital box, 99 DOTS)",
    "budget_tbhiv": "Collaboration between TB and HIV programmes aimed at reducing the impact of "
                    "HIV-related TB.",
}

# How many distinct activities the form pools into budget_prog, counted from its
# own definition rather than typed. A typed "fourteen" was wrong by one -- the form
# lists fifteen -- and had spread into the paper, a figure and the notes below
# before anyone counted.
BUDGET_PROG_ACTIVITIES: int = len(
    [x for x in re.split(r",\s*(?:and\s+)?", DCF_DEFINITIONS["budget_prog"].rstrip("."))
     if x.strip()])

# Node key -> WHO TB budget column, or None when no line covers the activity at all. Judged
# against DCF_DEFINITIONS, not against the column name and not against the dictionary's
# abbreviation. check_mapping_targets() guards typos; it cannot catch a wrong-but-real column,
# so the definitions are the check against that.
TB_BUDGET_MAPPING: dict[str, str | None] = {
    "molecular_dx": "budget_lab",        # "consumables for all tests", equipment purchase
    "airborne_ipc": "budget_prog",       # the form names "infection control" (see TB_BUDGET_POOLED)
    "tpt": "budget_tpt",                 # commodity only (see TB_BUDGET_COMMODITY_ONLY)
    "wgs_dst": "budget_lab",             # sequencing is laboratory equipment and consumables
    "acf": "budget_prog",                # the form names "active case-finding" (TB_BUDGET_POOLED)
    "short_regimen": "budget_sld",       # commodity only (see TB_BUDGET_COMMODITY_ONLY)
    "bovine_tb": None,                   # animal health; outside the TB programme budget
    "private_sector": "budget_prog",     # the form names "public-private mix" (TB_BUDGET_POOLED)
    "nutrition": "budget_patsup",        # the form names "food packages"
    "milk_pasteurisation": None,         # food safety; outside the TB programme budget
    "tb_hiv_dm": "budget_tbhiv",         # TB/HIV arms only (see TB_BUDGET_COMMODITY_ONLY)
}

# Activities the form names inside a line that pools many unrelated activities. The form
# acknowledges them; the published data cannot separate them, because the whole line is one
# number. This is a different condition from having no line, and from having a line that
# covers only a commodity, so it is recorded separately rather than collapsed into either.
TB_BUDGET_POOLED: dict[str, str] = {
    "airborne_ipc": f"budget_prog names 'infection control' among {BUDGET_PROG_ACTIVITIES} "
                    "activities pooled in one figure, from staff supervision to drug procurement "
                    "management.",
    "acf": f"budget_prog names 'active case-finding' among {BUDGET_PROG_ACTIVITIES} pooled "
           "activities.",
    "private_sector": f"budget_prog names 'public-private mix activities' among "
                      f"{BUDGET_PROG_ACTIVITIES} pooled activities.",
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
TB_BUDGET_COMMODITY_ONLY: dict[str, str] = {
    "tpt": "budget_tpt covers TB preventive treatment drugs only. Delivery, contact tracing and adherence support are not covered; the form puts contact investigation in budget_prog, pooled.",
    "short_regimen": "budget_sld covers drugs to treat drug-resistant TB only. Rollout programme work is not covered; DR-TB programme costs sit in budget_mdrmgt, which no node maps to.",
    "tb_hiv_dm": "budget_tbhiv covers collaborative TB/HIV activities. The diabetes arm is not covered.",
}

# Kept under the old name so nothing that imported it breaks silently.
TB_BUDGET_PARTIAL = TB_BUDGET_COMMODITY_ONLY

# The same eleven nodes classified against the data dictionary instead of the form. Only
# budget_prog differs in substance between the two documents: the dictionary defines it as
# programme costs "to treat" drug-susceptible TB, so each pooled node -- none of which is
# treatment -- loses its line, and every other mapping stands under either document.
# Derived, not typed: a typed "six" once counted whole-genome sequencing here, but its
# exclusion had been a separate mapping error, since the dictionary's budget_lab
# ("laboratory infrastructure, equipment and supplies") covers sequencing as well as the form
# does. The dictionary's own effect is the pooled nodes, no more.
TB_BUDGET_NO_LINE_BY_DICTIONARY: frozenset[str] = frozenset(
    k for k, v in TB_BUDGET_MAPPING.items() if v is None or k in TB_BUDGET_POOLED)

# No WHO budget line is specific to any one of these interventions: every line pools several
# activities. This is the finding, and it is stated as data rather than left to prose.
TB_BUDGET_SEPARABLE: dict[str, bool] = {key: False for key in TB_BUDGET_MAPPING}


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
