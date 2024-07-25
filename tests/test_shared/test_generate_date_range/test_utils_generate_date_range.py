import re

from tests.test_shared.constants import TEST_INITIAL_DATE_FORMAT
from utils import generate_date_range


def test_generate_date_range():
    start_date = "2022-01-01"
    end_date = "2022-01-03"

    expected_dates = ["2022-01-01", "2022-01-02", "2022-01-03"]
    assert (
        generate_date_range(start_date, end_date, TEST_INITIAL_DATE_FORMAT)
        == expected_dates
    )


def test_generate_date_range_single_day():
    # Date range of a single day should return a list containing only that date
    dates = generate_date_range("2022-01-01", "2022-01-01", TEST_INITIAL_DATE_FORMAT)
    assert dates == ["2022-01-01"]


def test_generate_date_range_incorrect_order():
    # Date range with end date before start date should return an empty list
    dates = generate_date_range("2022-01-02", "2022-01-01", TEST_INITIAL_DATE_FORMAT)
    assert dates == []


def test_generate_date_range_format():
    # This test will validate the format of the generated dates
    dates = generate_date_range("2022-01-01", "2022-01-03", TEST_INITIAL_DATE_FORMAT)
    for date in dates:
        assert re.match(r"\d{4}-\d{2}-\d{2}", date), f"Incorrect date format for {date}"
