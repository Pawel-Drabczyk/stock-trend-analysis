"""Constants used in the finance_reports module. Most of the values are set as environment variables, but they also
have the default values."""
import os

SCRAPE_URL = "https://www.stockwatch.pl/kalendarium/raporty/d/"
"""URL of the scraped website. The date should be appended to it in order to format full URL."""
INITIAL_DATE_FORMAT: str = "%Y-%m-%d"
"""Date format required by website do properly format the URL."""
OUTPUT_DATE_FORMAT: str = "%Y-%m-%d"
"""Date format included in output csv filenames. Should support further data partitioning."""
DATA_DIR: str = os.getenv("DATA_DIR", "../../data/finance_reports")
"""Destination data dir."""
MAX_SLEEP_TIME: float = float(os.getenv("MAX_SLEEP_TIME", 2))
"""Scraping next date will happen after random time between 0 and `MAX_SLEEP_TIME` seconds."""
OUTPUT_FILE_PREFIX: str = os.getenv("OUTPUT_FILE_PREFIX", "finance_report")
"""The prefix of output csv files."""
HIVE_PARTITIONING_PREFIX: str = os.getenv("HIVE_PARTITIONING_PREFIX", "date=")
"""Prefix used for Hive partitioning."""
DATA_SINK_BUCKET: str = os.getenv("DATA_SINK_BUCKET", "finance-reports-data-sink")
"""The name of data sink GCS bucket."""
DATA_START_DATE: str = os.getenv("DATA_START_DATE", "2015-01-01")
"""ETL start date in INITIAL_DATE_FORMAT. Works only if the GCS bucket is empty."""
DATE_RANGE: int = os.getenv("DATE_RANGE", 30)
"""Number of days to import data about."""
