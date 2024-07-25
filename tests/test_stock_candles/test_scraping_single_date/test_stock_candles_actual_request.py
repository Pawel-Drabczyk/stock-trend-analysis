import os
import shutil
from datetime import datetime

import pandas as pd

from stock_candles.constants import (
    INITIAL_DATE_FORMAT,
    OUTPUT_DATE_FORMAT,
    OUTPUT_FILE_PREFIX,
)
from stock_candles.stock_candles import StockCandles
from tests.constants import DATA_DIR_TESTS


def test_stock_candles_scrape_single_date_actual_request():
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-11-03", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-11-03", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    # Use the function to scrape the data
    StockCandles.scrape_stock_data(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Check if the CSV was created
    file_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    assert os.path.exists(file_path)

    # Load the CSV and compare with expected output
    df = pd.read_csv(file_path, delimiter=",", quotechar='"')
    expected_content = [
        [
            "06MAGNA",
            "PLNFI0600010",
            "PLN",
            "2.8800",
            "2.8800",
            "2.8000",
            "2.8500",
            -1.04,
            4443,
            "12",
            "12.56",
            "03-11-2022",
        ],
        [
            "ALTA",
            "PLTRNSU00013",
            "PLN",
            "1.6200",
            "1.6200",
            "1.5500",
            "1.6200",
            -1.82,
            4904,
            "4",
            "7.61",
            "03-11-2022",
        ],
    ]

    print(df.values.tolist()[0])

    for row in expected_content:
        assert row in df.values.tolist()


def test_stock_candles_scrape_single_date_no_data_actual_request():
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-12-24", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-12-24", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    StockCandles.scrape_stock_data(date_string_initial, data_dir=DATA_DIR_TESTS)

    file_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )

    # Assert that the CSV file was NOT created
    assert not os.path.exists(file_path)
