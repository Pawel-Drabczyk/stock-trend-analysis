import os
import shutil
from datetime import datetime

from finance_reports.finance_report_day import (
    FinanceReportDay,
    INITIAL_DATE_FORMAT,
)
from tests.test_finance_reports.constants import DATA_DIR_TESTS


def test_finance_reports_directory_creation():
    """This test is doing actual request."""
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-15", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )

    # Now, run the scraping function
    FinanceReportDay.scrape_single_date(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Check if the directory has been created
    assert os.path.exists(DATA_DIR_TESTS), "Directory was not created"

    # Cleanup after the test
    shutil.rmtree(DATA_DIR_TESTS)
