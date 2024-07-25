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


def test_finance_reports_scrape_single_date_no_data(
    mock_finance_reports_no_data_response,
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

    FinanceReportDay.scrape_single_date(date_string_initial, data_dir=DATA_DIR_TESTS)

    file_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )

    # Assert that the CSV file was NOT created
    assert not os.path.exists(file_path)
