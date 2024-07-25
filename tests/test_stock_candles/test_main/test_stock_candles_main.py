from datetime import datetime, timedelta

from stock_candles.main import (
    handle,
    STOCK_CANDLES_OUTPUT_DATE_FORMAT,
    STOCK_CANDLES_DATA_DIR,
    STOCK_CANDLES_OUTPUT_FILE_PREFIX,
)
from stock_candles.constants import (
    DATA_START_DATE as STOCK_CANDLES_DATA_START_DATE,
    DATE_RANGE as STOCK_CANDLES_DATE_RANGE,
    INITIAL_DATE_FORMAT as STOCK_CANDLES_INITIAL_DATE_FORMAT,
)
from shared.utils import LOOKBACK as UTILS_LOOKBACK


def test_stock_candles_main_initial_load(
    mock_gcs_wrapper_from_stock_candles, mock_stock_candles
):
    """Test the case when the latest date is None."""
    # GIVEN
    mock_gcs_wrapper_from_stock_candles.list_files_and_find_latest.return_value = None

    # WHEN
    response = handle(None)

    # THEN
    mock_gcs_wrapper_from_stock_candles.list_files_and_find_latest.assert_called_once_with(
        STOCK_CANDLES_OUTPUT_FILE_PREFIX, STOCK_CANDLES_OUTPUT_DATE_FORMAT
    )
    mock_stock_candles.scrape_date_range.assert_called_once_with(
        STOCK_CANDLES_DATA_START_DATE,
        (
            datetime.strptime(
                STOCK_CANDLES_DATA_START_DATE, STOCK_CANDLES_INITIAL_DATE_FORMAT
            )
            + timedelta(days=STOCK_CANDLES_DATE_RANGE)
        ).strftime(STOCK_CANDLES_INITIAL_DATE_FORMAT),
    )
    mock_gcs_wrapper_from_stock_candles.upload_files.assert_called_once_with(
        STOCK_CANDLES_DATA_DIR, STOCK_CANDLES_OUTPUT_FILE_PREFIX
    )
    assert "successfully uploaded to GCS" in response[0]


def test_stock_candles_main_incremental_load(
    mock_gcs_wrapper_from_stock_candles, mock_stock_candles
):
    """Test the case when the latest date is older than the lookback period."""
    # GIVEN
    initial_latest_date = datetime(2021, 1, 1)
    mock_gcs_wrapper_from_stock_candles.list_files_and_find_latest.return_value = (
        initial_latest_date
    )

    # WHEN
    response = handle(None)

    # THEN
    mock_gcs_wrapper_from_stock_candles.list_files_and_find_latest.assert_called_once_with(
        STOCK_CANDLES_OUTPUT_FILE_PREFIX, STOCK_CANDLES_OUTPUT_DATE_FORMAT
    )
    mock_stock_candles.scrape_date_range.assert_called_once_with(
        (initial_latest_date - timedelta(days=UTILS_LOOKBACK)).strftime(
            STOCK_CANDLES_INITIAL_DATE_FORMAT
        ),
        (
            initial_latest_date
            - timedelta(days=UTILS_LOOKBACK)
            + timedelta(days=STOCK_CANDLES_DATE_RANGE)
        ).strftime(STOCK_CANDLES_INITIAL_DATE_FORMAT),
    )
    mock_gcs_wrapper_from_stock_candles.upload_files.assert_called_once_with(
        STOCK_CANDLES_DATA_DIR, STOCK_CANDLES_OUTPUT_FILE_PREFIX
    )
    assert "successfully uploaded to GCS" in response[0]


def test_stock_candles_main_incremental_load_fresh(
    mock_gcs_wrapper_from_stock_candles, mock_stock_candles
):
    """Test the case when the latest date is not older than the lookback period."""
    # GIVEN
    initial_latest_date = datetime.today() - timedelta(days=2)
    mock_gcs_wrapper_from_stock_candles.list_files_and_find_latest.return_value = (
        initial_latest_date
    )

    # WHEN
    response = handle(None)

    # THEN
    mock_gcs_wrapper_from_stock_candles.list_files_and_find_latest.assert_called_once_with(
        STOCK_CANDLES_OUTPUT_FILE_PREFIX, STOCK_CANDLES_OUTPUT_DATE_FORMAT
    )
    mock_stock_candles.scrape_date_range.assert_called_once_with(
        (initial_latest_date - timedelta(days=UTILS_LOOKBACK)).strftime(
            STOCK_CANDLES_INITIAL_DATE_FORMAT
        ),
        datetime.today().strftime(STOCK_CANDLES_INITIAL_DATE_FORMAT),
    )
    mock_gcs_wrapper_from_stock_candles.upload_files.assert_called_once_with(
        STOCK_CANDLES_DATA_DIR, STOCK_CANDLES_OUTPUT_FILE_PREFIX
    )
    assert "successfully uploaded to GCS" in response[0]
