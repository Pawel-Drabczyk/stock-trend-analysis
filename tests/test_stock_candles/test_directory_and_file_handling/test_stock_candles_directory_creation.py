import os
import shutil
from datetime import datetime

from stock_candles.constants import INITIAL_DATE_FORMAT
from stock_candles.stock_candles import StockCandles
from tests.constants import DATA_DIR_TESTS


def test_stock_candles_directory_creation(mock_stock_candles_data_with_header_response):
    """This test is doing actual request."""
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-01", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )

    # Now, run the scraping function
    StockCandles.scrape_stock_data(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Check if the directory has been created
    assert os.path.exists(DATA_DIR_TESTS), "Directory was not created"

    # Cleanup after the test
    shutil.rmtree(DATA_DIR_TESTS)
