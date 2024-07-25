"""The module to scrape stock candles from SCRAPE_URL.

The candles are downloaded for the date range between date_string_start and date_string_end. The dates should be
provided in format INITIAL_DATE_FORMAT.

The output is saved to csv files with filepath {DATA_DIR}/{OUTPUT_FILE_PREFIX}_{date_string in OUTPUT_DATE_FORMAT}.csv.
"""
import logging
import os
import random
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .constants import (
    SCRAPE_URL,
    INITIAL_DATE_FORMAT,
    OUTPUT_DATE_FORMAT,
    DATA_DIR,
    MAX_SLEEP_TIME,
    OUTPUT_FILE_PREFIX,
)
from shared.utils import save_to_csv, generate_date_range

logging.basicConfig(level=logging.INFO)


class StockCandles:
    @classmethod
    def scrape_stock_data(cls, date_string: str, data_dir: str = DATA_DIR) -> None:
        """Scrapes stock data from a table and save it to a csv file.

        Args:
            date_string (str): The date of the stock candles.
            data_dir (str): Destination for the scraped data.
        """
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        logging.info(f"Scraping stock data from {SCRAPE_URL + date_string}")
        result = requests.get(SCRAPE_URL + date_string)
        content = result.text

        # Check for no data across the entire HTML content
        if "Brak danych dla wybranych kryteriów." in content:
            logging.warning(f"No data available for {date_string}.")
            return

        soup = BeautifulSoup(result.text, "html.parser")
        table = soup.find("table", class_="table footable")

        headers = [
            "Name",
            "ISIN Code",
            "Currency",
            "Open Price",
            "High Price",
            "Low Price",
            "Close Price",
            "Price Change (%)",
            "Volume",
            "Transaction Count",
            "Turnover (k)",
        ]

        rows = []

        try:
            # if header exists it will be skipped
            header_position = 0
            if len(table.find_all("thead")):
                header_position = 1

            for row in table.find_all("tr")[
                header_position:
            ]:  # [1:] skips the header row
                cells = row.find_all("td")
                if len(cells) == 11:
                    rows.append([cell.text.strip() for cell in cells])
                else:
                    raise Exception(f"Unexpected number of cells in the row: {cells}")

        except Exception as e:
            raise Exception(f"Error occurred while parsing the table: {str(e)}")

        if rows:
            df = pd.DataFrame(rows, columns=headers)
            df["Date"] = date_string
            # Replace commas with dots
            df = df.replace({",": "."}, regex=True)
            # Remove spaces from column "Volume"
            df["Volume"] = df["Volume"].apply(lambda x: x.replace(" ", ""))

            # Save to CSV
            save_to_csv(
                df,
                date_string=date_string,
                destination_directory=data_dir,
                prefix=OUTPUT_FILE_PREFIX,
                initial_date_format=INITIAL_DATE_FORMAT,
                output_date_format=OUTPUT_DATE_FORMAT,
            )
        else:
            logging.warning("No data scraped - unknown issue!")

    @classmethod
    def scrape_date_range(
        cls, date_string_start: str, date_string_end: str, data_dir: str = DATA_DIR
    ) -> None:
        """Scrapes available stock candles for range of dates and save them to csv files in `date_dir` dir.

        Args:
            date_string_start (str): Starting date in format `INITIAL_DATE_FORMAT`.
            date_string_end (str): End -||-
            data_dir: Destination for the csv files.
        """
        for date in generate_date_range(
            date_string_start, date_string_end, date_format=INITIAL_DATE_FORMAT
        ):
            cls.scrape_stock_data(date, data_dir=data_dir)
            time.sleep(random.uniform(0, MAX_SLEEP_TIME))


# This is used for local execution
if __name__ == "__main__":
    stockCandles = StockCandles()
    stockCandles.scrape_date_range("01-12-2023", "28-12-2023")
