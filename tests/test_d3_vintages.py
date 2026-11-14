"""Tests for the vintage analysis (demos/d3_vintages.py).

The data are WHO's archived releases, fetched at pinned commits and not
redistributed; without them these tests skip, saying how to fetch them.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "demos"))
import d3_vintages as d3  # noqa: E402

need_data = pytest.mark.skipif(
    not all(p.exists() for p in d3.FILES.values()),
    reason="run tools/fetch_vintages.py and tools/convert_vintages.R first")


# ---- the classifier, without data -------------------------------------------
def test_component_class_precedence():
    # WHO-supplied outranks restated, which outranks new
    assert d3.component_class(["new", "filled_earlier"]) == "WHO-supplied"
    assert d3.component_class(["restated", "overridden"]) == "WHO-supplied"
    assert d3.component_class(["new", "restated"]) == "restated"
    assert d3.component_class(["new", "new"]) == "new"
    assert d3.component_class(["filled_later"]) == "WHO-supplied"


def test_every_component_input_is_a_utilisation_variable():
    assert set(sum(d3.COMPONENTS.values(), [])) == set(d3.UTIL)


WHO_CODE = (ROOT / "data" / "vintages" / "raw" /
            "gtbreport2026__finance__3_prepare_imputed_data.R")


def test_fill_order_matches_who_code():
    # gtbreport2026 finance/3_prepare_imputed_data.R: lag 1..4, then lead 1..4
    assert d3.WHO_FILL_ORDER == [-1, -2, -3, -4, 1, 2, 3, 4]
    if not WHO_CODE.exists():
        pytest.skip("WHO's code not fetched")
    text = WHO_CODE.read_text(encoding="utf-8")
    positions = [text.index(f"lag(.x,{k})") for k in range(1, 5)] + \
                [text.index(f"lead(.x,{k})") for k in range(1, 5)]
    assert positions == sorted(positions), "WHO's fill order is not lag 1-4 then lead 1-4"


# ---- with the archived releases ------------------------------------------------
@need_data
def test_reconstruction_reproduces_who_published_totals():
    assert all(v["match"] for v in d3.validation())


@need_data
def test_utilisation_values_are_never_revised_between_releases():
    util = [r for r in d3.revision() if r["group"] == "util"]
    assert sum(r["pairs"] for r in util) > 10_000
    assert sum(r["changed"] for r in util) == 0


@need_data
def test_restated_utilisation_far_exceeds_counted_expenditure():
    rst = d3.restatement()
    for rel in ("2024", "2025", "2026"):
        u = [r["identical"] / r["pairs"] for r in rst if r["group"] == "util" and r["release"] == rel]
        c = [r["identical"] / r["pairs"] for r in rst if r["group"] == "counted" and r["release"] == rel]
        assert min(u) > 0.6 and max(c) < 0.12, rel


@need_data
def test_care_components_sum_to_the_published_care_estimate():
    # consequence() asserts this per country-year; the class shares must close
    for rel in ("2025", "2026"):
        for r in d3.consequence(rel):
            if r["ghs"]:
                parts = r["new"] + r["restated"] + r["WHO-supplied"]
                assert abs(parts - r["ghs"]) < 1e3, (rel, r["year"])


@need_data
def test_the_window_excludes_years_a_release_cannot_classify():
    # the public 2026 download starts in 2017, so 2017 cannot be "restated"
    prov = d3.provenance("2026")
    early = [s for (c, y, v), s in prov.items() if y < d3.WINDOW_START]
    assert early, "the processed file should reach back before the window"
    # Before the window the raw release has no previous year, so nothing there
    # can be classed "restated": the reason the window exists.
    assert not [s for (c, y, v), s in prov.items() if y == 2017 and s == "restated"]
    f = d3.filling("2026", 2025)
    in_window = sum(1 for (c, y, v) in prov if d3.WINDOW_START <= y <= 2025)
    assert sum(f.values()) == in_window


@need_data
def test_india_values_carried_forward():
    i = d3.last_reported("2026", "IND")
    assert i["last_reported"] == 2022
    assert i["first_year_of_values"] == 2020
    assert i["used_through"] >= 2025
