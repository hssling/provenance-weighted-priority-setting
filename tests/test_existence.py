import csv
from pathlib import Path

import pytest

from provenance.existence import (
    BUDGET_DEFINITIONS,
    NODE_LABELS,
    TB_BUDGET_MAPPING,
    TB_BUDGET_PARTIAL,
    ExistenceReport,
    existence_report,
    check_mapping_targets,
)
from provenance.series import TestResult

SIX_INVISIBLE = {
    "Airborne infection prevention and control",
    "Whole-genome sequencing for drug-susceptibility prediction",
    "Active case finding",
    "Bovine tuberculosis control",
    "Private-sector engagement",
    "Milk pasteurisation / dairy food chain",
}


def test_six_of_eleven_tb_nodes_are_fiscally_invisible():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert len(NODE_LABELS) == 11
    assert len(r.invisible) == 6
    assert set(r.invisible) == SIX_INVISIBLE
    assert "Airborne infection prevention and control" in r.invisible
    assert "Active case finding" in r.invisible


def test_active_case_finding_has_no_budget_line():
    # WHO data dictionary: budget_prog is "Budget required for programme costs to treat
    # drug-susceptible TB". Active case FINDING is not treatment, so ACF is invisible.
    # Name-matching budget_prog to ACF was the error; the definition is the evidence.
    assert TB_BUDGET_MAPPING["acf"] is None
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.score["acf"] == 0.0
    assert "acf" not in r.mapped


def test_rank_two_intervention_has_no_budget_line():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.score["airborne_ipc"] == 0.0
    assert "airborne_ipc" not in r.mapped


def test_top_five_evidence_ranked_interventions_include_three_invisible():
    # The finding that matters: three of the five best-evidenced interventions (ranks 2, 4
    # and 5) cannot be tracked, defended at budget time, or evaluated for value.
    keys = list(NODE_LABELS)  # insertion order is evidence rank 1..11
    invisible_ranks = sorted(
        i + 1 for i, k in enumerate(keys) if TB_BUDGET_MAPPING[k] is None)
    assert invisible_ranks == [2, 4, 5, 7, 8, 10]
    top_five_invisible = [i + 1 for i in range(5) if TB_BUDGET_MAPPING[keys[i]] is None]
    assert top_five_invisible == [2, 4, 5]


def test_mapped_nodes_point_at_their_budget_lines():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.mapped == {
        "molecular_dx": "budget_lab",
        "tpt": "budget_tpt",
        "short_regimen": "budget_sld",
        "nutrition": "budget_patsup",
        "tb_hiv_dm": "budget_tbhiv",
    }
    assert set(r.score.values()) == {0.0, 1.0}
    assert sum(r.score.values()) == 5.0


def test_tb_hiv_diabetes_is_mapped_but_recorded_as_partial():
    # Mapped (a TB/HIV line exists) but not the whole node: diabetes has no line.
    # Partial coverage is a recorded fact, not a reason to score the node invisible.
    assert TB_BUDGET_MAPPING["tb_hiv_dm"] == "budget_tbhiv"
    assert "diabetes" in TB_BUDGET_PARTIAL["tb_hiv_dm"]
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.score["tb_hiv_dm"] == 1.0


def test_every_mapping_target_is_a_real_who_budget_column():
    # A typo here would silently turn a mapped intervention into a false "invisible".
    assert check_mapping_targets(TB_BUDGET_MAPPING) == []


def test_typo_in_budget_line_is_caught():
    assert check_mapping_targets({"x": "budget_labb", "y": None}) == ["budget_labb"]


def test_report_is_not_a_test_result():
    # T5 scores absence, not instability: it must not look like a T1-T4 TestResult,
    # so it cannot be folded into the composite by accident.
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert isinstance(r, ExistenceReport)
    assert not isinstance(r, TestResult)
    assert not hasattr(r, "testable")


def test_node_missing_from_mapping_is_an_error():
    with pytest.raises(ValueError):
        existence_report(NODE_LABELS, {k: v for k, v in TB_BUDGET_MAPPING.items() if k != "tpt"})


def test_mapping_key_without_node_is_an_error():
    with pytest.raises(ValueError):
        existence_report(NODE_LABELS, {**TB_BUDGET_MAPPING, "ghost": None})


def test_empty_budget_line_is_an_error_not_a_mapping():
    with pytest.raises(ValueError):
        existence_report(NODE_LABELS, {**TB_BUDGET_MAPPING, "tpt": ""})


DICTIONARY_CSV = Path(__file__).resolve().parents[1] / "data" / "TB_dictionary_2026-08-25.csv"


def _who_definitions() -> dict[str, str]:
    # The file has a non-UTF-8 byte (near position 5333); errors="replace" keeps it readable.
    with open(DICTIONARY_CSV, encoding="utf-8", errors="replace", newline="") as fh:
        return {r["variable_name"]: r["definition"]
                for r in csv.DictReader(fh) if r["dataset"] == "Budget"}


WHO_DEFINITIONS = _who_definitions()


def test_partial_mappings_are_exactly_tpt_sld_and_tb_hiv_diabetes():
    # Keys are node keys: "short_regimen" is the BPaL/BPaL-M node, mapped to budget_sld.
    assert set(TB_BUDGET_PARTIAL) == {"tpt", "short_regimen", "tb_hiv_dm"}
    for node, note in TB_BUDGET_PARTIAL.items():
        assert note.strip(), f"partial note for {node!r} is empty"
        assert TB_BUDGET_MAPPING[node] in note, f"partial note for {node!r} omits its column"


def test_partial_nodes_are_mapped_not_invisible():
    # Partial coverage is a fact about the mapping, not an invisibility: the count stays 6.
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert len(r.invisible) == 6
    for node in TB_BUDGET_PARTIAL:
        assert node in r.mapped and r.score[node] == 1.0
        assert NODE_LABELS[node] not in r.invisible


def test_budget_definitions_match_who_dictionary_verbatim():
    # Compared against the dictionary file in data/, not a second hand-typed copy.
    assert set(BUDGET_DEFINITIONS) <= set(WHO_DEFINITIONS)
    for col, text in BUDGET_DEFINITIONS.items():
        assert text == WHO_DEFINITIONS[col], col


def test_every_mapped_budget_line_has_a_nonempty_who_definition():
    targets = {t for t in TB_BUDGET_MAPPING.values() if t is not None}
    assert targets <= set(WHO_DEFINITIONS)  # budget_prog is defined but deliberately unmapped (ruling S)
    for col in targets:
        assert BUDGET_DEFINITIONS[col].strip(), f"{col} has no definition"
