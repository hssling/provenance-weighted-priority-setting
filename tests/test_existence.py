import pytest

from provenance.existence import (
    NODE_LABELS,
    TB_BUDGET_MAPPING,
    ExistenceReport,
    existence_report,
    check_mapping_targets,
)
from provenance.series import TestResult

FIVE_INVISIBLE = {
    "Airborne infection prevention and control",
    "Whole-genome sequencing for drug-susceptibility prediction",
    "Bovine tuberculosis control",
    "Private-sector engagement",
    "Milk pasteurisation / dairy food chain",
}


def test_five_of_eleven_tb_nodes_are_fiscally_invisible():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert len(NODE_LABELS) == 11
    assert len(r.invisible) == 5
    assert set(r.invisible) == FIVE_INVISIBLE
    assert "Airborne infection prevention and control" in r.invisible


def test_rank_two_intervention_has_no_budget_line():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.score["airborne_ipc"] == 0.0
    assert "airborne_ipc" not in r.mapped


def test_high_ranked_interventions_without_budget_line_are_ranks_two_and_four():
    # The finding that matters: the second- and fourth-best-evidenced interventions
    # cannot be tracked, defended at budget time, or evaluated for value.
    keys = list(NODE_LABELS)  # insertion order is evidence rank 1..11
    invisible_ranks = sorted(
        i + 1 for i, k in enumerate(keys) if TB_BUDGET_MAPPING[k] is None)
    assert invisible_ranks == [2, 4, 7, 8, 10]
    assert TB_BUDGET_MAPPING[keys[1]] is None and TB_BUDGET_MAPPING[keys[3]] is None


def test_mapped_nodes_point_at_their_budget_lines():
    r = existence_report(NODE_LABELS, TB_BUDGET_MAPPING)
    assert r.mapped == {
        "molecular_dx": "budget_lab",
        "tpt": "budget_tpt",
        "acf": "budget_prog",
        "short_regimen": "budget_sld",
        "nutrition": "budget_patsup",
        "tb_hiv_dm": "budget_tbhiv",
    }
    assert set(r.score.values()) == {0.0, 1.0}
    assert sum(r.score.values()) == 6.0


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
