from datetime import datetime

import pytest

from stock_candles.constants import INITIAL_DATE_FORMAT
from stock_candles.stock_candles import StockCandles
from tests.constants import DATA_DIR_TESTS


def test_stock_candles_scrape_single_date_extra_column(
    mock_stock_candles_malformed_data_additional_column_response,
):
    with pytest.raises(
        Exception,
        match=r"Unexpected number of cells in the row:*",
    ):
        date_string = datetime.strptime("2022-01-03", "%Y-%m-%d").strftime(
            INITIAL_DATE_FORMAT
        )

        StockCandles.scrape_stock_data(date_string, data_dir=DATA_DIR_TESTS)


def test_stock_candles_scrape_single_date_missing_column(
    mock_stock_candles_malformed_data_missing_column_response,
):
    with pytest.raises(
        Exception,
        match=r"Unexpected number of cells in the row:*",
    ):
        date_string = datetime.strptime("2022-01-04", "%Y-%m-%d").strftime(
            INITIAL_DATE_FORMAT
        )

        StockCandles.scrape_stock_data(date_string, data_dir=DATA_DIR_TESTS)


def test_stock_candles_scrape_single_date_missing_td_clossing_tag(
    mock_stock_candles_malformed_data_missing_td_closing_tag_response,
):
    with pytest.raises(
        Exception,
        match=r"Unexpected number of cells in the row:*",
    ):
        date_string = datetime.strptime("2022-01-05", "%Y-%m-%d").strftime(
            INITIAL_DATE_FORMAT
        )

        StockCandles.scrape_stock_data(date_string, data_dir=DATA_DIR_TESTS)


def test_stock_candles_scrape_single_date_missing_table(
    mock_stock_candles_malformed_data_missing_table_response,
):
    with pytest.raises(
        Exception,
        match=r"Error occurred while parsing the table: *",
    ):
        date_string = datetime.strptime("2022-01-06", "%Y-%m-%d").strftime(
            INITIAL_DATE_FORMAT
        )

        StockCandles.scrape_stock_data(date_string, data_dir=DATA_DIR_TESTS)
