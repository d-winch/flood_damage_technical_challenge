"""Script to get the expected damage from a risk within a postcode experiencing flooding

This script allows the user to provide a path to a csv file.
It is assumed that the first row of the spreadsheet is a header
and the data follows immediatedly below.

This tool accepts comma separated value files (.csv) only.

A secondary, optional argument is accepted for the number of non-inundated areas.
i.e., those areas which have a depth of 0, which are not included in the csv.
Providing this argument will adjust the mean depth correctly.

This script requires that `pandas` and `numpy` be installed within the Python
environment you are running this script in.

The damage costs are set within the damage.py file to keep them separate.
See that file for more information on its use.
"""
import argparse
import logging
import math
from cmath import log
from pathlib import Path

import pandas as pd

from damage import damage_cost

Path("./log/").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="./log/out.log",
    filemode="a",
)


def read_data_file_to_df(filepath: str) -> pd.DataFrame:
    """Read a csv file and return a Pandas DataFrame. Combines with a second DataFrame of non-inundated properties if provided.

    Args:
        filepath (str): The file path of the data csv.add()
        non_damaged_count (int, optional): The number of properties in the location which are not included in the data file,
        i.e., non-inundated properties. Defaults to 0.

    Returns:
        pd.DataFrame: A Pandas DataFrame consisting of the depth data and any non-inundated properties if provided.
        The only column is "depth_m"
    """
    logging.info(f"Reading file - {filepath}")
    df = pd.read_csv(filepath, header=0, names=["depth_m"])

    logging.info(f"Successfully read {filepath} to a Pandas DataFrame")
    return df


def guard_against_missing_file(filepath: str) -> None:
    if not Path(filepath).is_file():
        logging.warning(f"File doesn't exist. Please check the filepath - {filepath}")
        raise Exception(f"File doesn't exist. Please check the filepath - {filepath}")


def guard_against_non_csv_file(filepath: str) -> None:
    if not Path(filepath).suffix == ".csv":
        logging.warning(
            f"{filepath} is not a csv. Please ensure you provide a comma separated file."
        )
        raise Exception(
            f"{filepath} is not a csv. Please ensure you provide a comma separated file."
        )


def get_mean_depth(df: pd.DataFrame, percent_inundated: float) -> float:
    if percent_inundated <= 0:
        raise Exception(
            f"Percent inundated must be a positive float: {percent_inundated}."
        )
    if percent_inundated > 100:
        raise Exception(
            f"Percent inundated must be a positive float less than or equal to 100: {percent_inundated}."
        )
    return df["depth_m"].mean() * (percent_inundated / 100)


def get_damage_cost(mean: float) -> int:

    index = math.ceil(mean)

    # Prevent using a non existing key above max in the dictionary
    if index > max(damage_cost.keys()):
        index = max(damage_cost.keys())

    cost = damage_cost.get(index, None)
    if cost == None:
        logging.warning(
            f"Something went wrong when assigning the cost to value {index}. Please check it exists in the damage table."
        )
        raise Exception(
            f"Something went wrong when assigning the cost to value {index}. Please check it exists in the damage table."
        )

    return cost


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-f",
        "--filepath",
        type=str,
        help="The local file containing the data to analyse",
    )
    parser.add_argument(
        "-p",
        "--percent_inundated",
        type=float,
        default="100",
        help="The percentage of inundated properties included in the file",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=int,
        default=40,
        help="The level for the log level - See https://docs.python.org/3/library/logging.html#logging-levels",
    )
    args = parser.parse_args()
    logging.info(f"Parsed arguments: {args}")

    return args


def set_logging_level(log_level: int):
    if log_level not in [0, 10, 20, 30, 40, 50]:
        raise Exception(f"Incorrect log level value: {log_level}")

    logging.getLogger().setLevel(log_level)


def main() -> None:

    args = get_args()

    set_logging_level(args.log_level)

    guard_against_missing_file(args.filepath)
    guard_against_non_csv_file(args.filepath)

    df = read_data_file_to_df(filepath=args.filepath)

    mean = get_mean_depth(df, args.percent_inundated)
    logging.info(f"Mean: {mean}")

    expected_damage = get_damage_cost(mean)

    logging.info(f"Expected damage cost £{expected_damage:,}")
    print(f"Expected damage cost £{expected_damage:,}")


if __name__ == "__main__":
    main()  # pragma: no cover
