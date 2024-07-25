"""The module to scrape calendary of financial reports from SCRAPE_URL. The content of reports in not downloaded, only
the date and the type of report are downloaded.

The reports are downloaded for the date range between date_string_start and date_string_end. The dates should be
provided in format INITIAL_DATE_FORMAT.

The output is saved to csv files with filepath {DATA_DIR}/{OUTPUT_FILE_PREFIX}_{date_string in OUTPUT_DATE_FORMAT}.csv.
"""

import logging
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
from shared.utils import generate_date_range, save_to_csv, create_or_empty_directory

logging.basicConfig(level=logging.INFO)


class FinanceReportDay:
    @classmethod
    def scrape_single_date(cls, date_string: str, data_dir: str = DATA_DIR) -> None:
        """Scrape financial reports for a single date and saves it to the csv file.

        Args:
            date_string (str): The date of the report.
            data_dir (str): Destination for the scraped data. Subdirs for each year will be created.
        """
        create_or_empty_directory(data_dir)

        logging.info(
            f"Scraping finance reports for {date_string} from {SCRAPE_URL + date_string}"
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        result = requests.get(SCRAPE_URL + date_string, headers=headers)

        # Check if the table contains the "No events to display" message
        if "Brak wydarzeń do wyświetlenia" in result.text:
            logging.info(f"No data for date: {date_string}")
        else:
            soup = BeautifulSoup(result.text, "html.parser")
            table = soup.find("table", class_="cctabdt")

            headers = ["Company Name", "Symbol", "Type", "Description"]
            rows = []

            try:
                for row in table.find_all("tr"):
                    if not row.has_attr("class"):  # This will skip the date row
                        cells = row.find_all("td")
                        if len(cells) == 4:
                            company_name = cells[0].a.text.strip()
                            symbol = cells[1].a.text.strip()
                            report_type = cells[2].text.strip()
                            description = cells[3].text.strip()

                            rows.append(
                                [company_name, symbol, report_type, description]
                            )
                        else:
                            raise Exception(
                                f"len(cells) in the table is not equal to 4! Cells: {cells}"
                            )
            except Exception as e:
                raise Exception(
                    f"Something is wrong with the HTML, cannot format a dataframe from {cells}! Exception: \n {str(e)}"
                )

            # Converting the data to a DataFrame
            if rows:
                df = pd.DataFrame(rows, columns=headers)
                df["Date"] = date_string

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
                logging.warning(
                    f"Cannot scrape data for date {date_string} - unknown issue!"
                )

    @classmethod
    def scrape_date_range(
        cls, date_string_start: str, date_string_end: str, data_dir: str = DATA_DIR
    ) -> None:
        """Scrape available financial reports for range of dates and save them to csv files.

        Args:
            date_string_start (str): Starting date in format DATE_FORMAT. This date will be included into output list.
            date_string_end (str): End -||-
            data_dir: Destination for the csv files.
        """
        for date in generate_date_range(
            date_string_start, date_string_end, date_format=INITIAL_DATE_FORMAT
        ):
            cls.scrape_single_date(date, data_dir=data_dir)
            time.sleep(random.uniform(0, MAX_SLEEP_TIME))


# This is used for local execution
if __name__ == "__main__":
    financeReportDay = FinanceReportDay()
    financeReportDay.scrape_date_range("2023-12-01", "2023-12-24")
