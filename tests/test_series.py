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


def _write_budget(tmp_path, rows, drop=()):
    """Synthetic budget CSV holding every column the loader maps (minus `drop`)."""
    from provenance.series import BUDGET_IDENTITIES
    cols = {"budget_tpt", "budget_lab"}
    cols.update(BUDGET_IDENTITIES)
    for _, parts in BUDGET_IDENTITIES.values():
        cols.update(parts.values())
    cols = sorted(cols - set(drop))
    p = tmp_path / "b.csv"
    lines = ["iso3,year," + ",".join(cols)]
    for r in rows:
        iso, yr, tpt, lab = r.split(",")
        vals = {"budget_tpt": tpt, "budget_lab": lab}
        lines.append(f"{iso},{yr}," + ",".join(vals.get(c, "") for c in cols))
    p.write_text(chr(10).join(lines) + chr(10))
    return p


def test_NA_token_is_none(tmp_path):
    p = _write_budget(tmp_path, ["IND,2020,NA,0", "IND,2021,5,"])
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


def test_exp_tot_2026_pathology_is_visible_as_sum_identity():
    e = load_who_expenditure(EXP_CSV, "IND")
    t = e["exp_tot"]
    assert t.identity == "sum"
    assert t.values[-1] == 0.0
    assert len(t.components) == 11
    assert all(part[-1] is None for part in t.components.values())


def test_sum_identity_reconciles_in_a_good_year():
    e = load_who_expenditure(EXP_CSV, "IND")
    t = e["exp_tot"]
    i = t.years.index(2022)
    assert sum(p[i] for p in t.components.values()) == t.values[i]


def test_budget_sum_and_product_identities_mapped():
    b = load_who_budget(BUDGET_CSV, "IND")
    assert b["budget_tpt"].identity == "product"
    assert b["budget_tot"].identity == "sum" and len(b["budget_tot"].components) == 11
    assert b["cf_tot"].identity == "sum"
    assert b["budget_lab"].identity is None


def test_rcvd_tot_has_both_identities():
    e = load_who_expenditure(EXP_CSV, "IND")
    assert e["rcvd_tot"].identity == "sum" and len(e["rcvd_tot"].components) == 11
    s = e["rcvd_tot_by_source"]
    assert s.identity == "sum" and len(s.components) == 4
    assert s.values == e["rcvd_tot"].values
    i = s.years.index(2022)
    assert sum(p[i] for p in s.components.values()) == s.values[i]


def test_mapped_but_absent_column_raises_naming_it(tmp_path):
    p = _write_budget(tmp_path, ["IND,2020,1,1"], drop=["tx_tpt"])
    with pytest.raises(ValueError, match="tx_tpt"):
        load_who_budget(p, "IND")


def test_default_identity_is_last_positional_field():
    s = IndicatorSeries("k", "l", [], [], "s", {}, {})
    assert s.identity is None
