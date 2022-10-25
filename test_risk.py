# Testing for risk.py using mypy

from decimal import Decimal
import pandas as pd
import pytest

from risk import (
    guard_against_missing_file,
    guard_against_non_csv_file,
    get_damage_cost,
    get_mean_depth,
    set_logging_level,
    main,
)


def test_exception_raised_when_file_does_not_exist():
    with pytest.raises(Exception):
        guard_against_missing_file("./csv/notreal.csv")


def test_no_exception_raised_when_file_does_exist():
    try:
        guard_against_missing_file("./csv/depths.csv")
    except Exception:
        pytest.fail("Exception raised when file does exist.")


def test_exception_raised_when_file_is_not_csv():
    with pytest.raises(Exception):
        guard_against_non_csv_file("./csv/depths.xls")


def test_no_exception_raised_when_file_is_csv():
    try:
        guard_against_non_csv_file("./csv/depths.csv")
    except Exception:
        pytest.fail("Exception raised when file is a csv")


def test_exception_raised_when_get_mean_percentage_below_zero_percent():
    with pytest.raises(Exception):
        df = pd.DataFrame(data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["depth_m"])
        get_mean_depth(df, -1)


def test_exception_raised_when_get_mean_depth_zero_percent():
    with pytest.raises(Exception):
        df = pd.DataFrame(data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["depth_m"])
        get_mean_depth(df, 0)


def test_exception_raised_when_get_mean_percentage_over_one_hundred_percent():
    with pytest.raises(Exception):
        df = pd.DataFrame(data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["depth_m"])
        get_mean_depth(df, 101)


def test_correct_mean_depth_returned_when_100_percent():
    df = pd.DataFrame(data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["depth_m"])
    assert get_mean_depth(df, 100) == 5


def test_correct_mean_depth_returned_when_float_percentage_provided():
    df = pd.DataFrame(data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["depth_m"])
    assert get_mean_depth(df, 47.2) == 2.36


def test_exception_raised_damage_cost_with_minus_value():
    with pytest.raises(Exception):
        assert get_damage_cost(-1)


def test_correct_get_damage_cost_with_zero_mean():
    assert get_damage_cost(0) == 0


def test_correct_get_damage_cost_with_one_mean():
    assert get_damage_cost(1) == 50_000


def test_correct_get_damage_cost_with_float_mean():
    assert get_damage_cost(5.5) == 120_000


def test_correct_get_damage_cost_above_max_mean():
    assert get_damage_cost(99999) == 134_000


def test_exception_raised_on_minus_logging_level():
    with pytest.raises(Exception):
        set_logging_level(-1)


def test_exception_raised_on_positive_invalid_logging_level():
    with pytest.raises(Exception):
        set_logging_level(25)


def test_no_exception_raised_on_valid_logging_level():
    try:
        set_logging_level(20)
    except Exception:
        pytest.fail("Exception raise when logging level is valid")


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["risk.py", "-f", "./csv/depths.csv", "-p", "75"])
    main()
    out, _ = capsys.readouterr()
    assert out == "Expected damage cost £105,000\n"
