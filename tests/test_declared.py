import pytest

from provenance.declared import DECLARED_CREDIT, declared_score
from provenance.series import IndicatorSeries, load_trajectories
from provenance.implausibility import implausibility_score

NTEP_CSV = __import__("pathlib").Path(__file__).resolve().parents[2] / "tb_bopas_repo" / "data" / "ntep_trajectories.csv"
YRS = [2019, 2020, 2021, 2022, 2023]
VALS = [1.0, 1.0, 1.0, 3.0, 3.0]


def _s(notes, vals=VALS, yrs=YRS):
    return IndicatorSeries("k", "k", list(yrs), list(vals), "t", notes, {})


def test_declared_break_scores_better_than_identical_silent_break():   # Review Focus 5
    silent = _s({})
    declared = _s({2022: "definition changed in 2022"})
    assert declared_score(declared, bound=0.5).score > declared_score(silent, bound=0.5).score


def test_rrmdr_notification_break_is_declared_in_source_data():
    s = load_trajectories(NTEP_CSV)["RRMDR_notif_100k"]
    assert any("changed at 2020" in n for n in s.notes.values())


def test_series_with_no_breaks_scores_one():
    flat = _s({}, [1.0, 1.01, 1.02], [2019, 2020, 2021])
    assert declared_score(flat, bound=0.5).score == 1.0


def test_declared_break_is_still_worse_than_no_break():
    declared = declared_score(_s({2022: "changed"}), bound=0.5).score
    assert declared < 1.0


def test_declared_never_scores_below_silent_over_credit_range():
    assert 0.0 < DECLARED_CREDIT < 1.0


def test_note_on_a_different_year_does_not_declare_the_break():
    off = _s({2020: "unrelated note"})
    assert declared_score(off, bound=0.5).score == declared_score(_s({}), bound=0.5).score


def test_silent_score_equals_t3_score():
    s = _s({})
    assert declared_score(s, bound=0.5).score == implausibility_score(s, bound=0.5).score


def test_detail_lists_declared_and_silent():
    r = declared_score(_s({2022: "x"}), bound=0.5)
    assert r.detail["declared"] == [2022] and r.detail["silent"] == []


def test_no_comparable_step_is_not_testable():
    r = declared_score(_s({}, [1.0], [2020]), bound=0.5)
    assert not r.testable and r.score is None


def test_trajectory_note_pinned_only_to_named_year():
    t = load_trajectories(NTEP_CSV)
    assert list(t["RRMDR_notif_100k"].notes) == [2020]
    # real data: the 2019->2020 step is a drop that the note covers
    r = declared_score(t["RRMDR_notif_100k"], bound=0.2)
    assert 2020 in r.detail["declared"]


def test_trajectory_notes_without_a_break_year_are_not_pinned():
    t = load_trajectories(NTEP_CSV)
    assert t["RR_new_pct"].notes == {}
    assert t["RR_new_pct"].values and t["RR_new_pct"].years
