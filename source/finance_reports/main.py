""" The main module for the finance_reports Cloud Function. It is responsible for checking the start_date and end_date
based on the content of the GCS bucket and the http request, importing the data into the local filesystem, and uploading
it to GCS. """
import logging
from typing import Dict, Tuple, Any

import functions_framework
import google.cloud.logging

from .constants import (
    INITIAL_DATE_FORMAT as FINANCE_REPORTS_INITIAL_DATE_FORMAT,
    OUTPUT_DATE_FORMAT as FINANCE_REPORTS_OUTPUT_DATE_FORMAT,
    DATA_DIR as FINANCE_REPORTS_DATA_DIR,
    OUTPUT_FILE_PREFIX as FINANCE_REPORTS_OUTPUT_FILE_PREFIX,
    DATA_SINK_BUCKET as FINANCE_REPORTS_DATA_SINK_BUCKET,
    DATA_START_DATE as FINANCE_REPORTS_DATA_START_DATE,
    DATE_RANGE as FINANCE_REPORTS_DATE_RANGE,
)
from .finance_report_day import FinanceReportDay
from shared.gcs_wrapper import GCSWrapper
from shared.utils import get_start_date_end_date

client = google.cloud.logging.Client()
client.setup_logging()


@functions_framework.http
def handle(request: Any) -> Tuple[str, int, Dict]:
    """The main function for the finance_reports Cloud Function.

    Args:
        request (functions_framework.Request): The http request object. It is used to get the start_date and end_date
            parameters provided by the user. If the parameters are not provided, the function will get the latest date
            from the GCS bucket and calculate the start_date and end_date based on the latest date and the date range
            provided in the constants.
    """
    # Getting the start_date and end_date parameters based on the http request and given content of the bucket
    start_date = request.args.get("start_date") if request else None
    end_date = request.args.get("end_date") if request else None
    if not start_date and not end_date:
        gcs = GCSWrapper(FINANCE_REPORTS_DATA_SINK_BUCKET)
        latest_date = gcs.list_files_and_find_latest(
            FINANCE_REPORTS_OUTPUT_FILE_PREFIX, FINANCE_REPORTS_OUTPUT_DATE_FORMAT
        )
        start_date, end_date = get_start_date_end_date(
            latest_date,
            FINANCE_REPORTS_INITIAL_DATE_FORMAT,
            FINANCE_REPORTS_DATE_RANGE,
            FINANCE_REPORTS_DATA_START_DATE,
            FINANCE_REPORTS_OUTPUT_DATE_FORMAT,
        )
    logging.info(f"Pulling finance report data from {start_date} to {end_date}.")

    # Importing data into local filesystem.
    financeReports = FinanceReportDay()
    financeReports.scrape_date_range(start_date, end_date)

    # Uploading data to GCS.
    gcs.upload_files(FINANCE_REPORTS_DATA_DIR, FINANCE_REPORTS_OUTPUT_FILE_PREFIX)

    return (
        f"Finance reports data from {start_date} to {end_date} has been successfully uploaded to GCS.",
        200,
        {},
    )


# the function will be executed when running on local machine for testing purposes
if __name__ == "__main__":
    handle(None)
