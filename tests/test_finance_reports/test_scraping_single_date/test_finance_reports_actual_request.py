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


def test_finance_reports_scrape_single_date_actual_request():
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-11-03", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-11-03", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    # Use the function to scrape the data
    FinanceReportDay.scrape_single_date(date_string_initial, data_dir=DATA_DIR_TESTS)

    # Check if the CSV was created
    file_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )
    assert os.path.exists(file_path)

    # Load the CSV and compare with expected output
    df = pd.read_csv(file_path)
    expected_content = [
        [
            "ING BANK ŚLĄSKI SA",
            "INGBSK",
            "raport",
            "Publikacja rozszerzonego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "ASBISc ENTERPRISES PLC",
            "ASBIS",
            "raport",
            "Publikacja skonsolidowanego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "BANK POLSKA KASA OPIEKI SPÓŁKA AKCYJNA",
            "PEKAO",
            "raport",
            "Publikacja rozszerzonego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "SILVA CAPITAL GROUP SPÓŁKA AKCYJNA",
            "SYNERGA",
            "raport",
            "Publikacja jednostkowego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "DINOPL",
            "DINOPL",
            "raport",
            "Publikacja rozszerzonego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "ROCCA SPÓŁKA AKCYJNA",
            "ROCCA",
            "raport",
            "Publikacja jednostkowego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "SHOPER",
            "SHOPER",
            "raport",
            "Publikacja rozszerzonego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "FOREVER ENTERTAINMENT SPÓŁKA AKCYJNA",
            "FOREVEREN",
            "raport",
            "Publikacja jednostkowego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
        [
            "MEGAPIXEL",
            "MEGAPIXEL",
            "raport",
            "Publikacja jednostkowego raportu kwartalnego za trzeci kwartał",
            "2022-11-03",
        ],
    ]

    for row in expected_content:
        assert row in df.values.tolist()


def test_finance_reports_scrape_single_date_no_data_actual_request():
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)

    date_string_initial = datetime.strptime("2022-12-24", "%Y-%m-%d").strftime(
        INITIAL_DATE_FORMAT
    )
    date_string_output = datetime.strptime("2022-12-24", "%Y-%m-%d").strftime(
        OUTPUT_DATE_FORMAT
    )

    FinanceReportDay.scrape_single_date(date_string_initial, data_dir=DATA_DIR_TESTS)

    file_path = os.path.join(
        DATA_DIR_TESTS, f"{OUTPUT_FILE_PREFIX}_{date_string_output}.csv"
    )

    # Assert that the CSV file was NOT created
    assert not os.path.exists(file_path)
