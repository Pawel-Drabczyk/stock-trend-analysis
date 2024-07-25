from datetime import datetime, timedelta

from finance_reports.main import (
    handle,
    FINANCE_REPORTS_OUTPUT_DATE_FORMAT,
    FINANCE_REPORTS_DATA_DIR,
    FINANCE_REPORTS_OUTPUT_FILE_PREFIX,
)
from finance_reports.constants import (
    DATA_START_DATE as FINANCE_REPORTS_DATA_START_DATE,
    DATE_RANGE as FINANCE_REPORTS_DATE_RANGE,
    INITIAL_DATE_FORMAT as FINANCE_REPORTS_INITIAL_DATE_FORMAT,
)
from shared.utils import LOOKBACK as UTILS_LOOKBACK


def test_finance_reports_main_initial_load(
    mock_gcs_wrapper_from_finance_reports, mock_finance_report_day
):
    """Test the case when the latest date is None."""
    # GIVEN
    mock_gcs_wrapper_from_finance_reports.list_files_and_find_latest.return_value = None

    # WHEN
    response = handle(None)

    # THEN
    mock_gcs_wrapper_from_finance_reports.list_files_and_find_latest.assert_called_once_with(
        FINANCE_REPORTS_OUTPUT_FILE_PREFIX, FINANCE_REPORTS_OUTPUT_DATE_FORMAT
    )
    mock_finance_report_day.scrape_date_range.assert_called_once_with(
        FINANCE_REPORTS_DATA_START_DATE,
        (
            datetime.strptime(
                FINANCE_REPORTS_DATA_START_DATE, FINANCE_REPORTS_INITIAL_DATE_FORMAT
            )
            + timedelta(days=FINANCE_REPORTS_DATE_RANGE)
        ).strftime(FINANCE_REPORTS_INITIAL_DATE_FORMAT),
    )
    mock_gcs_wrapper_from_finance_reports.upload_files.assert_called_once_with(
        FINANCE_REPORTS_DATA_DIR, FINANCE_REPORTS_OUTPUT_FILE_PREFIX
    )
    assert "successfully uploaded to GCS" in response[0]


def test_finance_reports_main_incremental_load(
    mock_gcs_wrapper_from_finance_reports, mock_finance_report_day
):
    """Test the case when the latest date is older than the lookback period."""
    # GIVEN
    initial_latest_date = datetime(2021, 1, 1)
    mock_gcs_wrapper_from_finance_reports.list_files_and_find_latest.return_value = (
        initial_latest_date
    )

    # WHEN
    response = handle(None)

    # THEN
    mock_gcs_wrapper_from_finance_reports.list_files_and_find_latest.assert_called_once_with(
        FINANCE_REPORTS_OUTPUT_FILE_PREFIX, FINANCE_REPORTS_OUTPUT_DATE_FORMAT
    )
    mock_finance_report_day.scrape_date_range.assert_called_once_with(
        (initial_latest_date - timedelta(days=UTILS_LOOKBACK)).strftime(
            FINANCE_REPORTS_INITIAL_DATE_FORMAT
        ),
        (
            initial_latest_date
            - timedelta(days=UTILS_LOOKBACK)
            + timedelta(days=FINANCE_REPORTS_DATE_RANGE)
        ).strftime(FINANCE_REPORTS_INITIAL_DATE_FORMAT),
    )
    mock_gcs_wrapper_from_finance_reports.upload_files.assert_called_once_with(
        FINANCE_REPORTS_DATA_DIR, FINANCE_REPORTS_OUTPUT_FILE_PREFIX
    )
    assert "successfully uploaded to GCS" in response[0]


def test_finance_reports_main_incremental_load_fresh(
    mock_gcs_wrapper_from_finance_reports, mock_finance_report_day
):
    """Test the case when the latest date is not older than the lookback period."""
    # GIVEN
    initial_latest_date = datetime.today() - timedelta(days=2)
    mock_gcs_wrapper_from_finance_reports.list_files_and_find_latest.return_value = (
        initial_latest_date
    )

    # WHEN
    response = handle(None)

    # THEN
    mock_gcs_wrapper_from_finance_reports.list_files_and_find_latest.assert_called_once_with(
        FINANCE_REPORTS_OUTPUT_FILE_PREFIX, FINANCE_REPORTS_OUTPUT_DATE_FORMAT
    )
    mock_finance_report_day.scrape_date_range.assert_called_once_with(
        (initial_latest_date - timedelta(days=UTILS_LOOKBACK)).strftime(
            FINANCE_REPORTS_INITIAL_DATE_FORMAT
        ),
        datetime.today().strftime(FINANCE_REPORTS_INITIAL_DATE_FORMAT),
    )
    mock_gcs_wrapper_from_finance_reports.upload_files.assert_called_once_with(
        FINANCE_REPORTS_DATA_DIR, FINANCE_REPORTS_OUTPUT_FILE_PREFIX
    )
    assert "successfully uploaded to GCS" in response[0]
