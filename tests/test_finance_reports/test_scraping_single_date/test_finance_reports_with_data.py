import os
import shutil
from datetime import datetime

import pandas as pd

from finance_reports.finance_report_day import (
    FinanceReportDay,
    INITIAL_DATE_FORMAT,
    OUTPUT_DATE_FORMAT,
    OUTPUT_FILE_PREFIX,
)
from tests.test_finance_reports.constants import DATA_DIR_TESTS


def test_finance_reports_scrape_single_date_data(mock_finance_reports_data_response):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-02", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-01-02", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    FinanceReportDay.scrape_single_date(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Verify CSV file generation
    expected_csv_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    assert os.path.exists(expected_csv_path), "CSV file was not created"

    # Load the CSV and verify its contents
    df = pd.read_csv(expected_csv_path)
    assert df.shape == (2, 5)
    assert df["Company Name"].tolist() == ["Sample Company", "Another Company"]
    assert df["Symbol"].tolist() == ["SYM1", "SYM2"]
    assert df["Date"].tolist() == [date_string_initial, date_string_initial]
