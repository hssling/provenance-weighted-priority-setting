import pytest

from provenance.implausibility import derive_bound, implausibility_score
from provenance.series import BUDGET_CSV, IndicatorSeries, load_who_budget


def _s(values, years=None, key="k"):
    years = years or list(range(2018, 2018 + len(values)))
    return IndicatorSeries(key, key, years, values, "t", {}, {})


def test_cpp_xdr_flagged_at_an_explicit_bound():
    # Mechanism test at a stated bound of 0.5. It does NOT say what derive_bound returns.
    # Seven steps 2019-2025: -76%, +50%, +50%, -77%, +98%, then -5% and +3%. The two
    # +50% steps sit exactly at the bound and do not exceed it; three steps exceed.
    s = load_who_budget(BUDGET_CSV, "IND")["budget_cpp_xdr"]
    r = implausibility_score(s, bound=0.5)
    assert r.testable
    assert r.detail["exceed"] == [2019, 2022, 2023]
    assert r.score == pytest.approx(4 / 7)


def test_change_exactly_at_bound_is_not_a_violation():
    r = implausibility_score(_s([100.0, 150.0, 225.0]), bound=0.5)
    assert r.score == 1.0


def test_single_point_series_is_untestable():   # Review Focus 1
    s = IndicatorSeries(key="x", label="x", years=[2020], values=[1.0],
                        source="t", notes={}, components={})
    r = implausibility_score(s, bound=0.5)
    assert r.testable is False and r.score is None


def test_empty_series_is_untestable():
    r = implausibility_score(_s([], years=[]), bound=0.5)
    assert r.testable is False and r.score is None


def test_none_and_zero_base_steps_are_skipped_not_raised():
    # None breaks two steps each side; 0 -> 5 has a zero base; only 5 -> 5.5 is comparable.
    r = implausibility_score(_s([1.0, None, 0.0, 5.0, 5.5]), bound=0.5)
    assert r.testable and r.score == 1.0 and list(r.detail["changes"]) == [2022]


def test_all_steps_uncomparable_is_untestable():
    r = implausibility_score(_s([None, 1.0, None, 0.0, 2.0]), bound=0.5)
    assert r.testable is False and r.score is None


def test_year_gap_is_not_an_adjacent_period():
    r = implausibility_score(_s([1.0, 100.0], years=[2018, 2020]), bound=0.5)
    assert r.testable is False


def test_zero_to_value_and_value_to_zero():
    # 4 -> 0 is a -100% change (comparable, exceeds); 0 -> 4 has a zero base (skipped).
    r = implausibility_score(_s([4.0, 0.0, 4.0]), bound=0.5)
    assert r.testable and r.score == 0.0 and r.detail["exceed"] == [2019]


def test_bound_is_derived_from_reference_series_not_hardcoded():
    ref = [_s([100.0, 102.0, 99.0, 101.0, 103.0]), _s([50.0, 51.0, 50.5, 49.0, 50.0])]
    b = derive_bound(ref)
    assert 0.0 < b < 1.0
    # Depends on the data: a more volatile reference gives a larger bound.
    wild = [_s([100.0, 150.0, 80.0, 160.0, 90.0])]
    assert derive_bound(wild) > b


def test_derive_bound_is_the_percentile_of_pooled_absolute_changes():
    # abs changes: 0.1, 0.2, 0.3, 0.4, 0.5  -> 95th pct (linear interp) = 0.48
    ref = [_s([1.0, 1.1, 1.1 * 1.2, 1.1 * 1.2 * 1.3, 1.1 * 1.2 * 1.3 * 1.4,
               1.1 * 1.2 * 1.3 * 1.4 * 1.5])]
    assert derive_bound(ref) == pytest.approx(0.48)
    assert derive_bound(ref, percentile=0.5) == pytest.approx(0.3)


def test_derive_bound_without_comparable_changes_raises():
    with pytest.raises(ValueError):
        derive_bound([_s([1.0]), _s([None, 2.0])])
    with pytest.raises(ValueError):
        derive_bound([_s([1.0, 2.0])], percentile=1.5)


def test_recorded_real_data_result_reference_cpp_dstb_all_countries():
    # RECORDS an outcome; it is not a target. Reference set, fixed in advance of looking at
    # the result: budget_cpp_dstb (DS-TB cost per patient) for every country in the WHO
    # budget file, i.e. the same kind of quantity as the known case (a unit cost) but a
    # different regimen. The derived bound is ~1.92 (a 192% year-on-year change), and it
    # catches NOTHING in India's budget_cpp_xdr. That null is reported, not tuned away:
    # the reference is itself too volatile for T3 to discriminate unit-cost series.
    import csv
    with open(BUDGET_CSV, newline="", encoding="utf-8-sig") as fh:
        isos = sorted({r["iso3"] for r in csv.DictReader(fh)})
    ref = [load_who_budget(BUDGET_CSV, i)["budget_cpp_dstb"] for i in isos]
    b = derive_bound(ref)
    assert len(ref) == 215 and b == pytest.approx(1.917, abs=0.001)
    r = implausibility_score(load_who_budget(BUDGET_CSV, "IND")["budget_cpp_xdr"], bound=b)
    assert r.score == 1.0 and r.detail["exceed"] == []
