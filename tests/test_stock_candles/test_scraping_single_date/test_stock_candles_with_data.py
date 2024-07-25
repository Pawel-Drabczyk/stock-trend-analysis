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


def test_stock_candles_scrape_single_date_with_header_data(
    mock_stock_candles_data_with_header_response,
):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-01", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-01-01", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    StockCandles.scrape_stock_data(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Verify CSV file generation
    expected_csv_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    assert os.path.exists(expected_csv_path), "CSV file was not created"

    # Load the CSV and verify its contents
    df = pd.read_csv(expected_csv_path)
    assert df.shape == (2, 12)
    assert df["Name"].tolist() == ["Sample Company", "Another Company"]
    assert df["ISIN Code"].tolist() == ["ISIN1", "ISIN2"]
    assert df["Currency"].tolist() == ["PLN", "EUR"]
    assert df["Open Price"].tolist() == [1.1100, 1.0800]
    assert df["High Price"].tolist() == [2.2200, 1.0800]
    assert df["Low Price"].tolist() == [2.8000, 1.0800]
    assert df["Close Price"].tolist() == [1.0000, 1.0800]
    assert df["Price Change (%)"].tolist() == [-1.04, 4.85]
    assert df["Volume"].tolist() == [4443, 100]
    assert df["Transaction Count"].tolist() == [12, 2]
    assert df["Turnover (k)"].tolist() == [12.56, 0.11]


def test_stock_candles_scrape_single_date_without_header_data(
    mock_stock_candles_data_without_header_response,
):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-01", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-01-01", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    StockCandles.scrape_stock_data(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Verify CSV file generation
    expected_csv_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    assert os.path.exists(expected_csv_path), "CSV file was not created"

    # Load the CSV and verify its contents
    df = pd.read_csv(expected_csv_path, delimiter=",", quotechar='"')
    assert df.shape == (2, 12)
    assert df["Name"].tolist() == ["Sample Company", "Another Company"]
    assert df["ISIN Code"].tolist() == ["ISIN1", "ISIN2"]
    assert df["Currency"].tolist() == ["PLN", "EUR"]
    assert df["Open Price"].tolist() == [1.1100, 1.0800]
    assert df["High Price"].tolist() == [2.2200, 1.0800]
    assert df["Low Price"].tolist() == [2.8000, 1.0800]
    assert df["Close Price"].tolist() == [1.0000, 1.0800]
    assert df["Price Change (%)"].tolist() == [-1.04, 4.85]
    assert df["Volume"].tolist() == [4443, 100]
    assert df["Transaction Count"].tolist() == [12, 2]
    assert df["Turnover (k)"].tolist() == [12.56, 0.11]
