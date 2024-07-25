"""This module contains utility functions used in the ETL pipeline."""
import logging
import os
from datetime import datetime, timedelta
from typing import List, Tuple

import pandas as pd

LOOKBACK: int = 3
"""Number of days to download data from the past to make sure that the data are complete and up to date."""


def get_start_date_end_date(
    latest_date: datetime,
    initial_date_format: str,
    date_range: int,
    data_start_date: str,
    output_date_format: str,
) -> Tuple[str, str]:
    """Generate start_date and end_date for next data import, based on the latest_date for which the data are already
    imported. The output datetime strings are in initial_date_format.

    The following algorithm is used to determine start_date and end_date:
        - if the bucket is empty:
            - start_date is set to data_start_date
            - end_date is set to data_start_date + date_range days
        - if the bucket is not empty:
            - start_date is set to latest_date - 3 days
            - end_date is set to latest_date - 3 days + date_range days
            - if end_date exceeds current date, end_date is set to current date

    Args:
        latest_date (datetime): The object representing latest date for which the data are already impprted.
        initial_date_format (str): Datetime format string required to do requests to data source.
        date_range (int): Number of days to import in one ETL run.
        data_start_date (str): Datetime string representing the minimal start_date for this data source.
        output_date_format (str): Datetime format string used to save datetime in file names.

    Returns:
        Tuple[str]: start_date and end_date for ETL run in initial_date_format.
    """
    if latest_date:
        start_date = (latest_date - timedelta(days=LOOKBACK)).strftime(
            initial_date_format
        )
        end_date = latest_date + timedelta(days=date_range) - timedelta(days=LOOKBACK)
        if end_date > datetime.today():
            end_date = datetime.today().strftime(initial_date_format)
        else:
            end_date = end_date.strftime(initial_date_format)
    else:
        start_date = data_start_date
        end_date = (
            datetime.strptime(start_date, initial_date_format)
            + timedelta(days=date_range)
        ).strftime(initial_date_format)

    return start_date, end_date


def generate_date_range(
    start_date_str: str, end_date_str: str, date_format: str
) -> List[str]:
    """Generates a list of dates in string `date_format` between `start_date_str` and `end_date_str`.

    Args:
        start_date_str (str): Starting date in format `date_format`. This date will be included into output list.
        end_date_str (str): End -||-
        date_format (str): Format string for dates e.g. '%d-%m-%Y'

    Returns:
        List[str]: The resulting list of dates (including start_date and end_date).
    """
    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)
    date_range = [
        start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)
    ]
    return [date.strftime(date_format) for date in date_range]


def save_to_csv(
    df: pd.DataFrame,
    date_string: str,
    destination_directory: str,
    prefix: str,
    initial_date_format: str,
    output_date_format: str,
) -> None:
    """Saves the pandas DataFrame to a CSV file.

    The pandas `df` is saved in destination `{destination_directory}/{prefix}_{date_string}.csv. The `date_string` is
    formatted in `output_date_format`. While setting `output_date_format`, one should have on mind further data
    partitioning.

    Args:
        df (pd.DataFrame): Pandas dataframe with data and column names as headers.
        date_string (str): Date string in format `initial_date_format`.
        destination_directory (str): Directory for saving the file.
        prefix (str): Prefix at the begging of the file name.
        initial_date_format (str): The format in this the `date_string` is given.
        output_date_format (str): The format in which the `date_string` is formatted in the file name.
    """
    file_name = f"{prefix}_{datetime.strptime(date_string, initial_date_format).strftime(output_date_format)}.csv"
    file_path = os.path.join(destination_directory, file_name)
    df.to_csv(file_path, index=False)
    logging.info(f"Successfully saved data to {file_path}")


def create_or_empty_directory(dir_path: str):
    """Creates or empties the directory.

    Args:
        dir_path (str): The path to the directory.
    """
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file))
    else:
        os.mkdir(dir_path)
