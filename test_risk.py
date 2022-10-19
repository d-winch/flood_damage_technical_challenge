# Testing for risk.py using mypy

import pandas as pd
# import pandas.testing as pdt
import pytest

from risk import (check_file_exists, check_file_is_csv, get_damage_cost,
                  get_mean_depth, main)


def test_check_file_exists():
    assert check_file_exists("./csv/depths.csv") == True


def test_not_check_file_exists():
    with pytest.raises(Exception):
        check_file_exists("notreal.csv")


def test_check_file_is_csv():
    assert check_file_is_csv("./csv/depths.csv") == True


def test_not_check_file_is_csv():
    with pytest.raises(Exception):
        check_file_is_csv("./csv/depths.xlsx")


def test_get_mean_depth():
    df = pd.DataFrame(data=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["depth_m"])
    assert get_mean_depth(df) == 5.0


def test_get_damage_cost_minus_1():
    with pytest.raises(Exception):
        assert get_damage_cost(-1)

def test_get_damage_cost_0():
    assert get_damage_cost(0) == 0

def test_get_damage_cost_1():
    assert get_damage_cost(1) == 50_000


def test_get_damage_cost_above_max():
    assert get_damage_cost(99999) == 134_000

def test_main(monkeypatch):
    monkeypatch.setattr("sys.argv", ["risk.py", "-f", "./csv/depths.csv", "-n", "2500"])
    main()
