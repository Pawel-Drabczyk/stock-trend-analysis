import os
import shutil
from datetime import datetime

from stock_candles.constants import (
    INITIAL_DATE_FORMAT,
    OUTPUT_DATE_FORMAT,
    OUTPUT_FILE_PREFIX,
)
from stock_candles.stock_candles import StockCandles
from tests.constants import DATA_DIR_TESTS


def test_stock_candles_scrape_single_date_data(mock_stock_candles_no_data_response):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-02", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-01-02", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    StockCandles.scrape_stock_data(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Verify CSV file generation
    expected_csv_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    assert not os.path.exists(expected_csv_path), "CSV file was not created"
