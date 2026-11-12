import pytest

from provenance.identity import identity_score
from provenance.series import (
    BUDGET_CSV,
    EXP_CSV,
    IndicatorSeries,
    load_who_budget,
    load_who_expenditure,
)


def _sum_series(values, a, b):
    years = list(range(2000, 2000 + len(values)))
    return IndicatorSeries("t", "t", years, values, "synthetic", {}, {"a": a, "b": b}, "sum")


def test_tpt_identity_clean_2020_to_2023_and_broken_2024_2025():
    r = identity_score(load_who_budget(BUDGET_CSV, "IND")["budget_tpt"])
    assert 0.8 <= r.detail["identity"][2022] <= 1.2  # reported ~ implied
    assert r.detail["identity"][2025] > 3.0          # 9.1x divergence
    assert r.score < 0.8


def test_absent_value_is_untestable_not_failing():
    r = identity_score(load_who_budget(BUDGET_CSV, "IND")["budget_tpt"])
    assert 2018 not in r.detail["identity"]  # reported absent, ratio undefined
    assert 2018 not in r.detail["incomplete"]
    assert r.testable is True                # other years are testable


def test_reported_total_with_all_components_absent_fails_completeness():
    # exp_tot == 0 with every component blank: 0 == 0 reconciles, so identity
    # alone calls it clean. "Not yet reported" is not "spent nothing".
    r = identity_score(load_who_expenditure(EXP_CSV, "IND")["exp_tot"])
    assert 2026 in r.detail["incomplete"]
    assert 2026 not in r.detail["identity"]  # zero total: no ratio, no ZeroDivisionError
    assert r.score < 1.0


def test_sum_identity_reconciles_on_real_data():
    r = identity_score(load_who_expenditure(EXP_CSV, "IND")["exp_tot"])
    assert r.detail["identity"]
    assert all(0.9 <= v <= 1.1 for y, v in r.detail["identity"].items() if y != 2026)
    # 9 clean years of 10 testable (2026 incomplete)
    assert abs(r.score - 0.9) < 1e-9


def test_series_with_no_components_is_untestable():
    r = identity_score(load_who_budget(BUDGET_CSV, "IND")["budget_oth"])
    assert r.testable is False and r.score is None


def test_nonzero_total_with_all_components_absent_is_incomplete_even_with_ratio():
    s = _sum_series([100.0, 100.0], [100.0, None], [None, None])
    r = identity_score(s)
    assert r.detail["incomplete"] == [2001]
    assert r.detail["identity"][2001] == 0.0  # absent parts count as zero
    assert r.score == 0.5


def test_absent_parts_count_as_zero_when_some_present():
    s = _sum_series([100.0], [60.0], [None])
    r = identity_score(s)
    assert r.detail["identity"][2000] == 0.6
    assert r.detail["incomplete"] == []
    assert r.score == 0.0


def test_zero_or_none_total_never_raises():
    s = _sum_series([0.0, None], [5.0, 5.0], [5.0, 5.0])
    r = identity_score(s)
    assert r.detail["identity"] == {}
    assert r.testable is False and r.score is None


def test_tolerance_boundary_is_inclusive_ten_percent():
    s = _sum_series([100.0, 100.0, 100.0], [110.0, 90.0, 111.0], [0.0, 0.0, 0.0])
    r = identity_score(s)
    assert abs(r.score - 2 / 3) < 1e-9


def test_product_with_missing_factor_has_no_ratio():
    s = IndicatorSeries("p", "p", [2000, 2001], [50.0, 50.0], "x", {},
                        {"unit_cost": [5.0, 5.0], "volume": [10.0, None]}, "product")
    r = identity_score(s)
    assert r.detail["identity"] == {2000: 1.0}
    assert r.detail["incomplete"] == []
    assert r.score == 1.0


def test_no_identity_is_untestable():
    s = IndicatorSeries("n", "n", [2000], [1.0], "x")
    r = identity_score(s)
    assert r.testable is False and r.score is None


def test_tpt_2023_clean_because_unit_cost_of_one_carries_50pct_rounding():
    # budget_cpp_tpt is an integer; 1 means [0.5, 1.5], so ratio 0.896 is rounding, not a discrepancy.
    r = identity_score(load_who_budget(BUDGET_CSV, "IND")["budget_tpt"])
    assert abs(r.detail["identity"][2023] - 0.896) < 0.001
    assert r.score is not None and abs(r.score - 4 / 6) < 1e-9


def test_tpt_2024_2025_still_fail_after_rounding_allowance():
    s = load_who_budget(BUDGET_CSV, "IND")["budget_tpt"]
    r = identity_score(s)
    assert r.detail["identity"][2024] > 3.0 and r.detail["identity"][2025] > 9.0
    # Only 2024 and 2025 fail: drop them and the rest is fully clean.
    keep = [i for i, y in enumerate(s.years) if y < 2024]
    s2 = IndicatorSeries(s.key, s.label, [s.years[i] for i in keep], [s.values[i] for i in keep],
                         s.source, {}, {k: [v[i] for i in keep] for k, v in s.components.items()}, "product",
                         s.unit_rounding)
    assert identity_score(s2).score == 1.0


def test_large_unit_cost_does_not_get_widened_band():
    s = IndicatorSeries("p", "p", [2000], [1000.0 * 10 / 1.12], "x", {},
                        {"unit_cost": [1000.0], "volume": [10.0]}, "product")
    r = identity_score(s)
    assert abs(r.detail["identity"][2000] - 1.12) < 1e-9
    assert r.score == 0.0


def _unit_one(ratio):
    # unit cost 1, volume 10, so implied = 10 and reported = 10 / ratio
    return IndicatorSeries("p", "p", [2000], [10.0 / ratio], "x", {},
                           {"unit_cost": [1.0], "volume": [10.0]}, "product", 0.5)


def test_unit_cost_one_ratio_1_8_is_clean_under_asymmetric_band():
    # c_true in [0.5, 1.5) => ratio = 1/c_true in (0.667, 2.0]. A symmetric +-0.5 band
    # (max 1.5) would have wrongly failed 1.8.
    assert identity_score(_unit_one(1.8)).score == 1.0


def test_unit_cost_one_ratio_0_6_fails_lower_bound():
    assert identity_score(_unit_one(0.6)).score == 0.0


def test_integral_unit_cost_without_a_declared_rounding_model_gets_the_flat_band():
    # M4: an integral unit cost is not evidence of rounding (a derived scale/denominator can be
    # integral by accident). Same numbers as _unit_one(1.8), no rounding declared: 1.8 fails.
    s = IndicatorSeries("p", "p", [2000], [10.0 / 1.8], "x", {},
                        {"unit_cost": [1.0], "volume": [10.0]}, "product")
    assert s.unit_rounding is None and identity_score(s).score == 0.0


def test_loader_declares_rounding_for_budget_tpt_only():
    b = load_who_budget(BUDGET_CSV, "IND")
    assert b["budget_tpt"].unit_rounding == 0.5 and b["budget_tot"].unit_rounding is None


def test_tolerance_sweep_on_real_identities():
    # M3: TOLERANCE has no derivation, so its effect is recorded. Sum identities are flat across
    # 0.01-0.15; budget_tpt (the only product identity) is not: 2/6 up to 0.05, 4/6 from 0.08.
    from provenance.series import EXP_CSV, load_who_expenditure
    b, e = load_who_budget(BUDGET_CSV, "IND"), load_who_expenditure(EXP_CSV, "IND")
    sums = {"budget_tot": (b["budget_tot"], 1.0), "cf_tot": (b["cf_tot"], 1.0),
            "exp_tot": (e["exp_tot"], 0.9), "rcvd_tot": (e["rcvd_tot"], 0.9),
            "rcvd_tot_by_source": (e["rcvd_tot_by_source"], 0.9)}
    for tol in (0.01, 0.02, 0.05, 0.10, 0.15):
        for name, (s, want) in sums.items():
            assert identity_score(s, tolerance=tol).score == pytest.approx(want), (name, tol)
    tpt = {tol: identity_score(b["budget_tpt"], tolerance=tol).score for tol in (0.01, 0.05, 0.08, 0.10, 0.15)}
    assert tpt[0.01] == tpt[0.05] == pytest.approx(2 / 6)
    assert tpt[0.10] == tpt[0.15] == pytest.approx(4 / 6)


def test_self_derived_identity_is_untestable_but_still_reports_ratios():
    # I1: components built from the same record as the total cannot discriminate.
    s = _sum_series([100.0, 100.0], [60.0, 60.0], [40.0, 40.0])
    assert identity_score(s).score == 1.0
    r = identity_score(s, independent=False)
    assert r.testable is False and r.score is None
    assert r.detail["identity"] == {2000: 1.0, 2001: 1.0} and "reason" in r.detail
