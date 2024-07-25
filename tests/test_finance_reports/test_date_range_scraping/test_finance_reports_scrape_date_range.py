import logging
import os
import shutil
from datetime import datetime

from finance_reports.finance_report_day import (
    FinanceReportDay,
    INITIAL_DATE_FORMAT,
    OUTPUT_DATE_FORMAT,
    OUTPUT_FILE_PREFIX,
)
from tests.test_finance_reports.constants import DATA_DIR_TESTS


def test_finance_reports_scrape_date_range(
    mock_finance_reports_combined_response, caplog
):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    caplog.set_level(logging.INFO)
    # Using our existing mocked data for two consecutive dates
    start_date_initial_format = datetime.strptime("2022-01-01", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    end_date_initial_format = datetime.strptime("2022-01-02", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    end_date_output_format = datetime.strptime("2022-01-02", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )
    FinanceReportDay.scrape_date_range(
        start_date_initial_format, end_date_initial_format, data_dir=DATA_DIR_TESTS
    )

    # Verify log messages
    assert f"Scraping finance reports for {start_date_initial_format}" in caplog.text
    assert f"Scraping finance reports for {end_date_initial_format}" in caplog.text
    assert f"No data for date: {start_date_initial_format}" in caplog.text
    assert (
        f"Successfully saved data "
        f"to {os.path.join(DATA_DIR_TESTS, f'{OUTPUT_FILE_PREFIX}_{end_date_output_format}.csv')}"
        in caplog.text
    )
