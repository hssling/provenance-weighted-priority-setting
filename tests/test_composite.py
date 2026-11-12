import pytest

from provenance.composite import composite, composite_sensitivity
from provenance.series import TestResult


def clean(score):
    return TestResult(score, True, {})


def untestable():
    return TestResult(None, False, {"reason": "x"})


def test_geometric_mean_does_not_let_four_clean_tests_mask_one_catastrophic():
    rs = [clean(1.0), clean(1.0), clean(1.0), clean(1.0), clean(0.01)]
    assert composite(rs, rule="geometric") < composite(rs, rule="arithmetic")


def test_geometric_is_the_default_rule():
    rs = [clean(0.25), clean(1.0)]
    assert composite(rs) == pytest.approx(0.5)
    assert composite(rs) == composite(rs, rule="geometric")


def test_untestable_results_are_excluded_not_treated_as_clean():
    assert composite([clean(0.5), untestable()]) == composite([clean(0.5)])
    assert composite([clean(0.5), untestable()]) == pytest.approx(0.5)  # not pulled toward 1.0


@pytest.mark.parametrize("rule", ["geometric", "arithmetic", "minimum"])
def test_untestable_excluded_under_every_rule(rule):
    assert composite([clean(0.2), untestable(), clean(0.8)], rule=rule) == \
        composite([clean(0.2), clean(0.8)], rule=rule)


@pytest.mark.parametrize("rule", ["geometric", "arithmetic", "minimum"])
def test_all_untestable_returns_none(rule):
    assert composite([untestable(), untestable()], rule=rule) is None


@pytest.mark.parametrize("rule", ["geometric", "arithmetic", "minimum"])
def test_empty_list_is_unassessable(rule):
    assert composite([], rule=rule) is None


def test_exact_zero_collapses_geometric_without_math_error():
    # A zero means every testable year failed that test; the composite is 0, not an error.
    rs = [clean(0.0), clean(1.0), clean(1.0), clean(1.0)]
    assert composite(rs, rule="geometric") == 0.0
    assert composite(rs, rule="arithmetic") == pytest.approx(0.75)
    assert composite(rs, rule="minimum") == 0.0


def test_zero_is_a_score_not_unassessable():
    assert composite([clean(0.0)]) == 0.0


def test_known_values_per_rule():
    rs = [clean(0.5), clean(0.8), clean(1.0)]
    assert composite(rs, rule="arithmetic") == pytest.approx((0.5 + 0.8 + 1.0) / 3)
    assert composite(rs, rule="minimum") == 0.5
    assert composite(rs, rule="geometric") == pytest.approx((0.5 * 0.8) ** (1 / 3))


def test_all_clean_is_one_under_every_rule():
    rs = [clean(1.0)] * 4
    assert all(v == 1.0 for v in composite_sensitivity(rs).values())


def test_rule_ordering_min_le_geometric_le_arithmetic():
    rs = [clean(0.1), clean(0.6), clean(0.9), clean(1.0)]
    d = composite_sensitivity(rs)
    assert d["minimum"] <= d["geometric"] <= d["arithmetic"]


def test_unknown_rule_raises():
    with pytest.raises(ValueError, match="rule"):
        composite([clean(0.5)], rule="harmonic")


def test_unknown_rule_raises_even_when_unassessable():
    with pytest.raises(ValueError, match="rule"):
        composite([untestable()], rule="harmonic")


def test_sensitivity_reports_every_rule():
    d = composite_sensitivity([clean(0.5), clean(0.9)])
    assert set(d) == {"geometric", "arithmetic", "minimum"}


def test_sensitivity_custom_rules_and_unassessable_is_empty():
    assert set(composite_sensitivity([clean(0.5)], rules=("minimum",))) == {"minimum"}
    # Unassessable: no number exists under any rule, so report nothing rather than fake values.
    assert composite_sensitivity([untestable()]) == {}


# ---- composite_report: makes evidential thinness visible -------------------------------
from provenance.composite import CompositeReport, composite_report  # noqa: E402


def t1(score, n):      # identity: ratios and incomplete years
    return TestResult(score, True, {"identity": {2000 + i: 1.0 for i in range(n)}, "incomplete": []})


def t2(score, n):      # triangulate
    return TestResult(score, True, {"changes": {2000 + i: (0.0, 0.0) for i in range(n)}, "agree": []})


def t3(score, n):      # implausibility
    return TestResult(score, True, {"changes": {2000 + i: 0.1 for i in range(n)}, "exceed": [], "bound": 0.5})


def t4(score, n):      # declared
    return TestResult(score, True, {"changes": {2000 + i: 0.1 for i in range(n)},
                                    "declared": [], "silent": [], "bound": 0.5})


def test_report_zero_from_one_observation_is_named_and_thin():
    r = composite_report([t1(1.0, 6), t2(1.0, 5), t3(1.0, 8), t4(0.0, 1)])
    assert r.score == 0.0
    assert r.min_observations == 1
    assert r.collapsed_by == ["declared"]
    assert r.n_testable == 4


def test_report_zero_from_many_observations_has_larger_weight():
    thin = composite_report([t1(1.0, 6), t4(0.0, 1)])
    thick = composite_report([t1(1.0, 6), t4(0.0, 9)])
    assert thin.score == thick.score == 0.0
    assert thin.min_observations == 1 and thick.min_observations == 6
    assert thick.collapsed_by == ["declared"]


def test_report_collapsed_by_empty_without_exact_zero():
    r = composite_report([t1(0.01, 3), t3(1.0, 4)])
    assert r.collapsed_by == []


def test_report_unassessable():
    r = composite_report([untestable(), untestable()])
    assert r == CompositeReport(score=None, n_testable=0, observations={}, min_observations=None,
                             collapsed_by=[])


def test_report_score_matches_composite_and_ignores_untestable_observations():
    rs = [t1(0.5, 4), untestable(), t3(0.8, 2)]
    for rule in ("geometric", "arithmetic", "minimum"):
        assert composite_report(rs, rule=rule).score == composite(rs, rule=rule)
    assert composite_report(rs).min_observations == 2
    assert composite_report(rs).n_testable == 2


def test_report_names_all_four_tests():
    r = composite_report([t1(0.0, 2), t2(0.0, 2), t3(0.0, 2), t4(0.0, 2)])
    assert r.collapsed_by == ["identity", "triangulation", "implausibility", "declared"]


def test_report_identity_counts_incomplete_years_too():
    res = TestResult(0.0, True, {"identity": {2000: 1.0}, "incomplete": [2001, 2000]})
    assert composite_report([res]).min_observations == 2   # union {2000, 2001}


def test_report_unrecognised_detail_fails_loudly():
    with pytest.raises(ValueError, match="detail"):
        composite_report([clean(0.5)])


# ---- Ruling X: per-test observations ---------------------------------------------------
def test_observations_show_well_evidenced_test_behind_the_zero():
    # identity collapsed on 20 observations; a clean triangulation has only 1.
    r = composite_report([t1(0.0, 20), t2(1.0, 1)])
    assert r.collapsed_by == ["identity"]
    assert r.observations["identity"] == 20
    assert r.observations["triangulation"] == 1
    assert r.min_observations == 1  # summary only; observations is the field to read


def test_min_observations_is_derived_from_observations():
    r = composite_report([t1(0.5, 4), untestable(), t3(0.8, 2), t4(1.0, 9)])
    assert r.min_observations == min(r.observations.values()) == 2


def test_observations_only_for_testable_tests():
    r = composite_report([t1(0.5, 4), untestable(), t3(0.8, 2)])
    assert r.observations == {"identity": 4, "implausibility": 2}
    assert r.n_testable == len(r.observations)


def test_collapsed_by_subset_of_observations():
    r = composite_report([t1(0.0, 3), t2(0.0, 5), t4(0.7, 2)])
    assert set(r.collapsed_by) <= set(r.observations)


def test_unassessable_has_empty_observations():
    assert composite_report([untestable()]).observations == {}


def test_duplicate_test_in_results_fails_loudly():
    with pytest.raises(ValueError, match="identity"):
        composite_report([t1(0.5, 2), t1(0.9, 3)])


def test_unrecognised_detail_error_names_result_and_shapes():
    with pytest.raises(ValueError) as e:
        composite_report([t1(0.5, 2), clean(0.5)])
    msg = str(e.value)
    assert "results[1]" in msg and "identity" in msg and "exceed" in msg and "silent" in msg


def test_adding_a_testable_clean_test_raises_the_composite_so_n_testable_must_match():
    # I5: composites are not comparable across series with different n_testable.
    from provenance.composite import composite
    from provenance.series import TestResult
    a = TestResult(0.9, True, {"changes": {2001: 0.1}, "exceed": [], "bound": 0.5})
    clean = TestResult(1.0, True, {"identity": {2001: 1.0}, "incomplete": []})
    assert composite([a]) == 0.9
    assert composite([a, clean]) == pytest.approx(0.9 ** 0.5) and composite([a, clean]) > 0.9
