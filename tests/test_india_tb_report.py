from provenance.series import DATA_DIR, load_india_tb_report

ITR_CSV = DATA_DIR / "india_tb_report_table16_1.csv"


def test_series_keys_and_years():
    s = load_india_tb_report(ITR_CSV)
    assert set(s) == {"itr_requested", "itr_approved", "itr_released", "itr_spent"}
    for series in s.values():
        assert series.years == list(range(2017, 2024))
        assert len(series.values) == 7


def test_released_is_none_for_2022_and_2023():
    s = load_india_tb_report(ITR_CSV)
    assert s["itr_released"].values[5:] == [None, None]
    assert s["itr_released"].values[0] == 871.36


def test_row_totals_reconcile_to_published_totals():
    s = load_india_tb_report(ITR_CSV)
    assert round(sum(v for v in s["itr_requested"].values if v), 2) == 23169.14
    assert round(sum(v for v in s["itr_approved"].values if v), 2) == 18388.23
    assert round(sum(v for v in s["itr_spent"].values if v), 2) == 15063.46


def test_declared_breaks_attached_to_2022_and_2023():
    s = load_india_tb_report(ITR_CSV)
    assert 2022 in s["itr_approved"].notes and "Flexible Pool" in s["itr_approved"].notes[2022]
    assert 2023 in s["itr_approved"].notes and "Flexible Pool" in s["itr_approved"].notes[2023]
    assert "15.03.2024" in s["itr_spent"].notes[2023]
