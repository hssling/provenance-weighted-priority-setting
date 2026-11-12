from pathlib import Path

import pytest

from provenance.series import (
    BUDGET_CSV,
    EXP_CSV,
    IndicatorSeries,
    TestResult,
    load_who_budget,
    load_who_expenditure,
)

TestResult.__test__ = False  # not a pytest class


def test_data_files_exist():
    assert Path(BUDGET_CSV).is_file() and Path(EXP_CSV).is_file()


def test_loads_india_budget_series_for_every_line_item():
    s = load_who_budget(BUDGET_CSV, "IND")
    assert "budget_tpt" in s and "budget_lab" in s
    assert s["budget_tpt"].years == list(range(2018, 2026))


def test_blank_becomes_none_and_reported_zero_stays_zero():
    b = load_who_budget(BUDGET_CSV, "IND")
    # budget_tpt is BLANK in 2018-19 (TPT not yet budgeted) -> None, not 0.0
    assert b["budget_tpt"].values[0] is None
    assert b["budget_tpt"].values[2] == 20596100.0  # 2020, first real value
    assert any(v is None for v in b["budget_cpp_tpt"].values)
    e = load_who_expenditure(EXP_CSV, "IND")
    # the 2026 row reports a literal "0" total with blank components:
    # a reported zero, faithfully loaded as 0.0, NOT collapsed to None
    assert e["exp_tot"].values[-1] == 0.0
    assert e["exp_lab"].values[-1] is None


def test_NA_token_is_none(tmp_path):
    p = tmp_path / "b.csv"
    p.write_text("iso3,year,budget_tpt,budget_lab\nIND,2020,NA,0\nIND,2021,5,\n")
    s = load_who_budget(p, "IND")
    assert s["budget_tpt"].values == [None, 5.0]
    assert s["budget_lab"].values == [0.0, None]


def test_components_attached_for_identity_testable_series():
    s = load_who_budget(BUDGET_CSV, "IND")
    assert s["budget_tpt"].components["unit_cost"] is not None
    assert s["budget_tpt"].components["volume"] is not None
    assert s["budget_tpt"].components["unit_cost"] == s["budget_cpp_tpt"].values
    assert s["budget_tpt"].components["volume"][2] == 1150000.0


def test_expenditure_loader_covers_2017_to_2026():
    s = load_who_expenditure(EXP_CSV, "IND")
    assert s["exp_tot"].years[0] == 2017 and s["exp_tot"].years[-1] == 2026


def test_unknown_country_gives_empty():
    assert load_who_budget(BUDGET_CSV, "ZZZ") == {}


def test_indicator_series_field_order():
    s = IndicatorSeries("k", "l", [2020], [1.0], "src", {}, {})
    assert (s.key, s.label, s.years, s.values, s.source, s.notes, s.components) == (
        "k", "l", [2020], [1.0], "src", {}, {})


def test_untestable_result_has_no_score():
    r = TestResult(score=None, testable=False, detail={})
    assert r.score is None and r.testable is False


def test_testresult_rejects_out_of_range_score():
    with pytest.raises(ValueError):
        TestResult(1.5, True, {})
    with pytest.raises(ValueError):
        TestResult(-0.1, True, {})


def test_testresult_rejects_inconsistent_combinations():
    with pytest.raises(ValueError):
        TestResult(0.5, False, {})
    with pytest.raises(ValueError):
        TestResult(None, True, {})
