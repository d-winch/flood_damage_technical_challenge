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
import math
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from damage import damage_cost


def read_data_to_df(
    filepath: str, non_damaged_count: Optional[int] = 0
) -> pd.DataFrame:
    """Read a csv file and return a Pandas DataFrame. Combines with a second DataFrame on non-inundated properties if provided.

    Args:
        filepath (str): The file path of the data csv.add()
        non_damaged_count (int, optional): The number of properties in the location which are not included in the data file,
        i.e., non-inundated properties. Defaults to 0.

    Returns:
        pd.DataFrame: A Pandas DataFrame consisting of the depth data and any non-inundated properties if provided.
        The only column is "depth_m"
    """
    df = pd.read_csv(filepath, header=0, names=["depth_m"])

    if non_damaged_count:
        non_damaged = pd.DataFrame({"depth_m": np.repeat(0, non_damaged_count)})
        df = pd.concat([df, non_damaged], ignore_index=True)

    return df


def check_file_exists(filepath: str) -> bool:
    if not Path(filepath).is_file():
        raise Exception("File doesn't exist. Please check the filepath.")
    return True


def check_file_is_csv(filepath: str) -> bool:
    if not Path(filepath).suffix == ".csv":
        raise Exception(
            "File is not a csv. Please ensure you provide a comma separated file."
        )
    return True


def get_mean_depth(df: pd.DataFrame) -> float:
    return df["depth_m"].mean()


def get_damage_cost(index: int) -> int:
    # If the mean/index is greater than the max value, assign it to the max to prevent returning None from the dictionary
    if index > max(damage_cost.keys()):
        index = max(damage_cost.keys())

    cost = damage_cost.get(index, -1)
    if cost == -1:
        raise Exception(
            f"Something went wrong when assigning the cost to value {index}. Please check it exists in the damage table."
        )
    return cost


def main() -> None:

    # Prepare command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-f",
        "--filepath",
        type=str,
        help="The local file containing the data to analyse",
    )
    parser.add_argument(
        "-n",
        "--non_inundated_count",
        type=int,
        default="0",
        help="The number of non-inundated properties which are not included in the data file",
    )
    args = parser.parse_args()

    print(
        args.filepath, args.non_inundated_count
    )  ######################################### Temporary check

    # Check whether the file exists, and is a csv - error is raised if not
    check_file_exists(args.filepath)
    check_file_is_csv(args.filepath)

    # Read the csv and add any non-inundated
    df = read_data_to_df(
        filepath=args.filepath, non_damaged_count=args.non_inundated_count
    )

    # Get the mean from the DataFrame and get the damage for it using the ceiling.
    mean = get_mean_depth(df)
    print(mean)
    d = get_damage_cost(math.ceil(mean))
    print(f"£{d:,}")


if __name__ == "__main__":
    main()
