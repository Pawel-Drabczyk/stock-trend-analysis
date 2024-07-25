""" The main module for the stock_canldes Cloud Function. It is responsible for checking the start_date and end_date
based on the content of the GCS bucket and the http request, importing the data into the local filesystem, and uploading
it to GCS. """
import logging
from typing import Dict, Tuple, Any

import functions_framework
import google.cloud.logging

from .constants import (
    DATA_DIR as STOCK_CANDLES_DATA_DIR,
    DATA_SINK_BUCKET as STOCK_CANDLES_DATA_SINK_BUCKET,
    OUTPUT_FILE_PREFIX as STOCK_CANDLES_OUTPUT_FILE_PREFIX,
    OUTPUT_DATE_FORMAT as STOCK_CANDLES_OUTPUT_DATE_FORMAT,
    INITIAL_DATE_FORMAT as STOCK_CANDLES_INITIAL_DATE_FORMAT,
    DATE_RANGE as STOCK_CANDLES_DATE_RANGE,
    DATA_START_DATE as STOCK_CANDLES_DATA_START_DATE,
)
from shared.gcs_wrapper import GCSWrapper
from shared.utils import get_start_date_end_date
from .stock_candles import StockCandles

client = google.cloud.logging.Client()
client.setup_logging()


@functions_framework.http
def handle(request: Any) -> Tuple[str, int, Dict]:
    """The main function for the stock_candles Cloud Function.

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
        gcs = GCSWrapper(STOCK_CANDLES_DATA_SINK_BUCKET)
        latest_date = gcs.list_files_and_find_latest(
            STOCK_CANDLES_OUTPUT_FILE_PREFIX, STOCK_CANDLES_OUTPUT_DATE_FORMAT
        )
        start_date, end_date = get_start_date_end_date(
            latest_date,
            STOCK_CANDLES_INITIAL_DATE_FORMAT,
            STOCK_CANDLES_DATE_RANGE,
            STOCK_CANDLES_DATA_START_DATE,
            STOCK_CANDLES_OUTPUT_DATE_FORMAT,
        )
    logging.info(f"Pulling stock candles data from {start_date} to {end_date}.")

    # Importing data into local filesystem.
    stockCandles = StockCandles()
    stockCandles.scrape_date_range(start_date, end_date)

    # Uploading data to GCS.
    gcs.upload_files(STOCK_CANDLES_DATA_DIR, STOCK_CANDLES_OUTPUT_FILE_PREFIX)

    return (
        f"Stock candles data from {start_date} to {end_date} has been successfully uploaded to GCS.",
        200,
        {},
    )


# the function will be executed when running on local machine for testing purposes
if __name__ == "__main__":
    handle(None)
