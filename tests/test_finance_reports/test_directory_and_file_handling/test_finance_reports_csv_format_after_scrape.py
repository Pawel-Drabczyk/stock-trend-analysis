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


def test_finance_reports_csv_format_after_scrape(
    mock_finance_reports_content_extraction_response,
):
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-01-03", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-01-03", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    FinanceReportDay.scrape_single_date(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Check the content of the CSV file
    filepath = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    with open(filepath, "r") as file:
        lines = file.readlines()
        assert len(lines) == 3
        assert lines[0] == "Company Name,Symbol,Type,Description,Date\n"
        assert "Sample Company,SYM1,Report Type 1,Description 1,2022-01-03\n" in lines
