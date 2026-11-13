"""The variable screen, and in particular the zero-excluded repetition.

The screen's headline statistic is `repetition`: the share of adjacent
country-year pairs holding an identical value, read as evidence that a value
was carried forward rather than re-measured. A repeated *zero*, though, is an
absence, not a carried-forward estimate, and most estimate-like variables in
these files are zero-dominated. `repetition_nz` restricts the statistic to
pairs with at least one non-zero side. It is reported, never classified on:
`classify()` must be unchanged so the published verdicts stand.

Fixtures here all carry more than CATEGORICAL_MAX_DISTINCT distinct values,
because S0 runs first. A column that is *entirely* zero is categorical and
never reaches the repetition test at all; zero-inflation only matters for
columns that also carry enough real values to look continuous.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demos"))
from d2_who_data_screen import (                                   # noqa: E402
    MIN_NONZERO_PAIRS, CATEGORICAL_MAX_DISTINCT, classify, screen_column,
)


def rows(series, col="x"):
    """Build screen input from {iso3: [values in consecutive years]}."""
    return [{"iso3": iso3, "year": str(2000 + i), col: str(v)}
            for iso3, vals in series.items() for i, v in enumerate(vals)]


def zeros(n=30, years=4, prefix="Z"):
    """n countries reporting zero every year: n*(years-1) zero-to-zero pairs."""
    return {f"{prefix}{i:03d}": [0] * years for i in range(n)}


# --- repetition_nz excludes zero-to-zero pairs --------------------------------

def test_zero_padding_inflates_the_unrestricted_statistic():
    """The failure mode the statistic exists to expose: a column whose real
    values never repeat still scores 75% because most countries report zero
    every year."""
    series = {f"A{i:03d}": [i * 10 + j for j in range(4)] for i in range(10)}
    series.update(zeros(30))
    s = screen_column(rows(series), "x")
    assert s["repetition"] == pytest.approx(90 / 120)   # 90 zero + 30 changing
    assert s["repetition_nz"] == 0.0


def test_restricted_statistic_keeps_genuine_repetition():
    """Removing zero-to-zero pairs must not remove real repetition: countries
    that hold a non-zero value still count."""
    series = {f"A{i:03d}": [i + 1] * 3 for i in range(20)}
    series.update(zeros(20, years=3))
    s = screen_column(rows(series), "x")
    assert s["repetition"] == 1.0
    assert s["repetition_nz"] == 1.0


def test_a_pair_counts_when_either_side_is_non_zero():
    """0 -> 5 is a real change and must be counted, not discarded along with
    the zero-to-zero pairs."""
    series = {f"A{i:03d}": [0, i + 1, 0, i + 1] for i in range(40)}
    s = screen_column(rows(series), "x")
    assert s["repetition"] == 0.0
    assert s["repetition_nz"] == 0.0      # every pair survived, none repeat


def test_restricted_statistic_withheld_below_the_minimum():
    """Too few informative pairs is reported as unknown, not as a number."""
    series = zeros(30)
    series.update({f"S{i:03d}": [i + 1] for i in range(10)})   # no pairs
    series["A"] = [7, 7, 7]                                    # 2 non-zero pairs
    s = screen_column(rows(series), "x")
    assert MIN_NONZERO_PAIRS > 2
    assert s["repetition"] > 0.9
    assert s["repetition_nz"] is None


def test_at_the_minimum_the_statistic_is_reported():
    series = zeros(30)
    series.update({f"A{i:03d}": [i + 1, i + 1] for i in range(MIN_NONZERO_PAIRS)})
    s = screen_column(rows(series), "x")
    assert s["repetition_nz"] == 1.0


# --- modal_is_zero ------------------------------------------------------------

def test_modal_is_zero_identifies_the_dominant_value():
    series = {f"Z{i:03d}": [0, 0, 0, i + 1] for i in range(30)}
    assert screen_column(rows(series), "x")["modal_is_zero"] is True

    series = {f"A{i:03d}": [5, 5, 5, 0] for i in range(30)}
    series.update({f"S{i:03d}": [i + 10] for i in range(10)})
    assert screen_column(rows(series), "x")["modal_is_zero"] is False


# --- the new fields must not change any published verdict ---------------------

def test_classify_ignores_the_new_fields():
    """classify() reads four screens. Adding repetition_nz and modal_is_zero
    must not reach it: the verdicts in the paper were computed before these
    existed and must not move."""
    base = {"repetition": 0.9, "distinct_ratio": 0.1,
            "modal_share": 0.5, "roundish": 0.9}
    assert classify(dict(base)) == "estimate-like"
    for extra in ({"repetition_nz": 0.0, "modal_is_zero": True},
                  {"repetition_nz": 1.0, "modal_is_zero": False}):
        assert classify({**base, **extra}) == "estimate-like"


def test_every_return_path_carries_the_new_keys():
    """Three paths leave screen_column: categorical, untestable, and scored.
    A missing key crashes the summary, but only on a file containing that
    case -- so each path is checked explicitly."""
    KEYS = {"repetition", "repetition_nz", "modal_share", "modal_is_zero"}

    categorical = screen_column(rows({f"C{i:03d}": [1, 2, 1, 2]
                                      for i in range(40)}), "x")
    assert categorical["categorical"] is True
    assert KEYS <= categorical.keys()

    untestable = screen_column(rows({f"C{i:03d}": [i + 0.5]
                                     for i in range(120)}), "x")
    assert untestable["untestable"] is True
    assert KEYS <= untestable.keys()

    scored = screen_column(rows({f"C{i:03d}": [i + 0.5, i + 1.5, i + 2.5]
                                 for i in range(40)}), "x")
    assert scored["categorical"] is False and scored["untestable"] is False
    assert KEYS <= scored.keys()


def test_categorical_short_circuit_still_runs_first():
    """S0 precedes S1, so a two-valued column is set aside before repetition
    is ever computed -- the contact-tracing false positive."""
    s = screen_column(rows({f"C{i:03d}": [0, 1, 0, 1] for i in range(40)}), "x")
    assert s["categorical"] is True
    assert s["n_distinct"] <= CATEGORICAL_MAX_DISTINCT
    assert s["repetition"] is None and s["repetition_nz"] is None
