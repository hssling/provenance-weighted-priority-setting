import csv
from pathlib import Path

import pytest

from provenance.existence import (
    BUDGET_DEFINITIONS,
    DCF_DEFINITIONS,
    NODE_LABELS,
    TB_BUDGET_COMMODITY_ONLY,
    TB_BUDGET_MAPPING,
    TB_BUDGET_PARTIAL,
    TB_BUDGET_POOLED,
    TB_BUDGET_SEPARABLE,
    ExistenceReport,
    existence_report,
    check_mapping_targets,
)
from provenance.series import TestResult

# Only two interventions have no WHO budget line, and both sit outside the TB
# programme entirely. An earlier version of this file asserted six, because the
# mapping was judged against the data dictionary's abbreviated definition of
# budget_prog ("programme costs to treat drug-susceptible TB") instead of the
# data collection form, which is the instrument countries complete and which
# names active case-finding, infection control and public-private mix among the
# activities that line covers.
NO_LINE_AT_ALL = {
    "Bovine tuberculosis control",
    "Milk pasteurisation / dairy food chain",
}


def test_two_of_eleven_tb_nodes_have_no_budget_line():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert len(NODE_LABELS) == 11
    assert len(r.invisible) == 2
    assert set(r.invisible) == NO_LINE_AT_ALL
    # Both sit outside the TB programme's own budget, not omitted within it.
    assert "Bovine tuberculosis control" in r.invisible


def test_no_intervention_has_a_budget_line_of_its_own():
    # The finding. Two have no line; the other nine share a line with activities
    # that are not theirs, so none can be costed from the published figure.
    assert len(TB_BUDGET_SEPARABLE) == 11
    assert not any(TB_BUDGET_SEPARABLE.values())
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert len(r.invisible) + len(r.mapped) == 11


def test_the_three_pooled_activities_are_named_by_the_form():
    # Each is named verbatim in the form's definition of the line it maps to.
    for key, phrase in (("acf", "active case-finding"),
                        ("airborne_ipc", "infection control"),
                        ("private_sector", "public-private mix")):
        assert key in TB_BUDGET_POOLED
        line = TB_BUDGET_MAPPING[key]
        assert line == "budget_prog"
        assert phrase in DCF_DEFINITIONS[line].lower(), key


def test_dictionary_and_form_disagree_about_budget_prog():
    # The divergence that produced the earlier error, asserted so it cannot be
    # quietly reconciled later: the dictionary says this line is for treatment,
    # the form says it also covers finding and prevention.
    assert "to treat" in BUDGET_DEFINITIONS["budget_prog"]
    assert "active case-finding" not in BUDGET_DEFINITIONS["budget_prog"].lower()
    assert "active case-finding" in DCF_DEFINITIONS["budget_prog"].lower()
    assert "infection control" in DCF_DEFINITIONS["budget_prog"].lower()


def test_active_case_finding_maps_to_the_pooled_programme_line():
    # It has a line, and the line cannot be attributed to it. Both halves matter:
    # claiming no line would be false, claiming it is costed would be false too.
    assert TB_BUDGET_MAPPING["acf"] == "budget_prog"
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert "acf" in r.mapped
    assert NODE_LABELS["acf"] not in r.invisible
    assert TB_BUDGET_SEPARABLE["acf"] is False


def test_rank_two_intervention_is_pooled_not_absent():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert "airborne_ipc" in r.mapped
    assert TB_BUDGET_SEPARABLE["airborne_ipc"] is False


def test_ranks_of_the_interventions_with_no_line_at_all():
    keys = list(NODE_LABELS)  # insertion order is the favourability rank 1..11
    no_line = sorted(i + 1 for i, k in enumerate(keys) if TB_BUDGET_MAPPING[k] is None)
    assert no_line == [7, 10]
    # Neither is in the top five, so the earlier "three of the top five are
    # invisible" observation does not survive and is not made anywhere.
    assert not [r for r in no_line if r <= 5]


def test_mapped_nodes_point_at_their_budget_lines():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.mapped == {
        "molecular_dx": "budget_lab",
        "airborne_ipc": "budget_prog",
        "tpt": "budget_tpt",
        "wgs_dst": "budget_lab",
        "acf": "budget_prog",
        "short_regimen": "budget_sld",
        "private_sector": "budget_prog",
        "nutrition": "budget_patsup",
        "tb_hiv_dm": "budget_tbhiv",
    }
    assert set(r.score.values()) == {0.0, 1.0}
    assert sum(r.score.values()) == 9.0
    # Three of the nine share one line, which is why a mapped score of 1.0
    # must not be read as "this intervention is costed".
    assert sum(1 for v in r.mapped.values() if v == "budget_prog") == 3


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
    # Commodity-only coverage is a fact about the mapping, not an invisibility.
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert len(r.invisible) == 2
    assert TB_BUDGET_PARTIAL is TB_BUDGET_COMMODITY_ONLY
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
