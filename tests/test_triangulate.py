from provenance.series import (BUDGET_CSV, ITR_CSV, IndicatorSeries, load_india_tb_report,
                               load_who_budget)
from provenance.triangulate import triangulate_score


def _s(values, source, years=None):
    years = years or list(range(2018, 2018 + len(values)))
    return IndicatorSeries("k", "k", years, values, source)


def test_absent_counterpart_is_untestable_not_clean():  # Review Focus 3
    r = triangulate_score(load_who_budget(BUDGET_CSV, "IND")["budget_oth"], None)
    assert r.testable is False and r.score is None


def test_units_cancel_proportional_moves_agree():
    a = _s([100.0, 110.0, 121.0], "A")
    b = _s([1000.0, 1100.0, 1210.0], "B")  # different level, same moves
    r = triangulate_score(a, b)
    assert r.testable and r.score == 1.0


def test_divergent_moves_disagree_and_tolerance_is_respected():
    a = _s([100.0, 110.0, 121.0], "A")
    b = _s([100.0, 110.0, 60.5], "B")  # second move -50% vs +10%
    assert triangulate_score(a, b).score == 0.5
    c = _s([100.0, 130.0, 169.0], "B")  # both moves +30% vs +10%: gap 0.20
    assert triangulate_score(a, c).score == 0.0
    assert triangulate_score(a, c, tolerance=0.25).score == 1.0


def test_same_source_is_not_independent_so_untestable():
    a = _s([1.0, 2.0], "A")
    r = triangulate_score(a, _s([1.0, 2.0], "A"))
    assert r.testable is False and r.score is None


def test_no_comparable_pair_is_untestable():
    a = _s([1.0, None, 3.0], "A")
    b = _s([1.0, 2.0, 3.0], "B")   # gaps break every consecutive pair
    assert triangulate_score(a, b).testable is False
    z = _s([0.0, 5.0], "A")        # zero base: change undefined
    assert triangulate_score(z, _s([1.0, 2.0], "B")).testable is False
    far = _s([1.0, 2.0], "B", years=[2030, 2031])  # no overlap
    assert triangulate_score(_s([1.0, 2.0], "A"), far).testable is False


def test_real_sources_differ():
    who = load_who_budget(BUDGET_CSV, "IND")["budget_tot"]
    itr = load_india_tb_report(ITR_CSV)["itr_approved"]
    assert who.source != itr.source


def test_real_data_who_vs_itr_approved_2022_disagrees():
    # Characterises measured behaviour; see task-4 report for the headline finding.
    who = load_who_budget(BUDGET_CSV, "IND")["budget_tot"]
    itr = load_india_tb_report(ITR_CSV)["itr_approved"]
    r = triangulate_score(who, itr)
    assert r.testable is True
    wa, ia = r.detail["changes"][2022]
    assert wa > 0 and ia < -0.4          # WHO up, ITR approved halves
    assert 2022 not in r.detail["agree"]
