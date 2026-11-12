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
    # budget file, the same kind of quantity as the known case (a unit cost). Under the
    # symmetric step size the derived bound is ~4.13 (a 5.1-fold swing at p95; the old
    # asymmetric statistic gave 1.917, which could not flag any fall). A reference that swings
    # five-fold at its 95th percentile is not stable, so the precondition fails and T3 is
    # NOT TESTABLE on budget_cpp_xdr: not 1.0. That is reported, not tuned away.
    import csv
    with open(BUDGET_CSV, newline="", encoding="utf-8-sig") as fh:
        isos = sorted({r["iso3"] for r in csv.DictReader(fh)})
    ref = [load_who_budget(BUDGET_CSV, i)["budget_cpp_dstb"] for i in isos]
    b = derive_bound(ref)
    assert len(ref) == 215 and b == pytest.approx(4.132, abs=0.001)
    cpp = load_who_budget(BUDGET_CSV, "IND")["budget_cpp_xdr"]
    r = implausibility_score(cpp, bound=b)
    assert r.testable is False and r.score is None and "not stable" in r.detail["reason"]
    # With the precondition waived the symmetric statistic does see the falls the old one hid.
    forced = implausibility_score(cpp, bound=b, max_bound=None)
    assert forced.testable and forced.detail["exceed"] == []     # still within a 5-fold bound


def test_a_fall_is_as_flaggable_as_the_equal_fold_rise():
    # C2: |v/prev - 1| is capped at 1 for any fall, so no bound >= 1 could ever flag one.
    fall, rise = _s([100.0, 25.0]), _s([100.0, 400.0])
    for bound in (0.5, 2.9):
        a = implausibility_score(fall, bound=bound, max_bound=None)
        b = implausibility_score(rise, bound=bound, max_bound=None)
        assert a.score == b.score == 0.0 and a.detail["exceed"] == b.detail["exceed"] == [2019]
    assert implausibility_score(fall, bound=3.0, max_bound=None).score == 1.0   # exactly at 3-fold-1
    # the failure that was verified: a 1000x collapse is beyond a bound of 1.917
    assert implausibility_score(_s([1000.0, 0.001]), bound=1.917, max_bound=None).score == 0.0


def test_step_size_is_inversion_symmetric():
    from provenance.triangulate import _steps
    up, down = _steps(_s([4.0, 10.0])), _steps(_s([10.0, 4.0]))
    assert up[2019] == pytest.approx(down[2019]) == pytest.approx(1.5)


def test_unstable_reference_is_untestable_not_clean():
    # I3: a bound >= STABLE_BOUND_MAX means the reference is not stable; "no violations" would be
    # an artefact of the reference.
    s = _s([100.0, 101.0, 102.0])
    assert implausibility_score(s, bound=0.5).score == 1.0
    r = implausibility_score(s, bound=1.0)
    assert r.testable is False and r.score is None


def test_step_to_zero_is_infinite_and_derive_bound_survives_infinities():
    from provenance.triangulate import _steps
    assert _steps(_s([4.0, 0.0]))[2019] == float("inf")
    ref = [_s([4.0, 0.0, 4.0, 4.0, 4.0, 4.0])]          # one +inf step among comparable steps
    assert derive_bound(ref, percentile=0.5) == 0.0      # no nan from inf * 0
    assert derive_bound(ref, percentile=0.99) == float("inf")
