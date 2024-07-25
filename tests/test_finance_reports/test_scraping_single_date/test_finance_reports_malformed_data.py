from datetime import datetime

import pytest

from finance_reports.finance_report_day import FinanceReportDay, INITIAL_DATE_FORMAT
from tests.test_finance_reports.constants import DATA_DIR_TESTS


def test_finance_reports_scrape_single_date_malformed_data(
    mock_finance_reports_malformed_data_response,
):
    with pytest.raises(
        Exception,
        match=r"Something is wrong with the HTML, cannot format a dataframe from*",
    ):
        date_string = datetime.strptime("2022-01-03", "%Y-%m-%d").strftime(
            INITIAL_DATE_FORMAT
        )

        FinanceReportDay.scrape_single_date(date_string, data_dir=DATA_DIR_TESTS)
