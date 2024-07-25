import logging
import os
import shutil
from datetime import datetime

from stock_candles.constants import (
    INITIAL_DATE_FORMAT,
    SCRAPE_URL,
    OUTPUT_DATE_FORMAT,
    OUTPUT_FILE_PREFIX,
)
from stock_candles.stock_candles import StockCandles
from tests.constants import DATA_DIR_TESTS


def test_stock_candles_scrape_date_range(mock_stock_candles_combined_response, caplog):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    caplog.set_level(logging.INFO)
    # Using our existing mocked data for two consecutive dates
    start_date_initial_format = datetime.strptime("2022-09-11", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    end_date_initial_format = datetime.strptime("2022-09-12", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    end_date_output_format = datetime.strptime("2022-09-12", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )
    StockCandles.scrape_date_range(
        start_date_initial_format, end_date_initial_format, data_dir=DATA_DIR_TESTS
    )

    # Verify log messages
    assert (
        f"Scraping stock data from {SCRAPE_URL + start_date_initial_format}"
        in caplog.text
    )
    assert (
        f"Scraping stock data from {SCRAPE_URL + end_date_initial_format}"
        in caplog.text
    )
    assert f"No data available for {start_date_initial_format}" in caplog.text
    assert (
        f"Successfully saved data "
        f"to {os.path.join(DATA_DIR_TESTS, f'{OUTPUT_FILE_PREFIX}_{end_date_output_format}.csv')}"
        in caplog.text
    )
