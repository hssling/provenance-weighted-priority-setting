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
