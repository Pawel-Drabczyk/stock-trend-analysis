"""Constants used in the stock_candles module. Most of the values are set as environment variables, but they also
have the default values."""
import os

SCRAPE_URL: str = "https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=&date="
"""URL of the scraped website. The date should be appended to it in order to format full URL."""
INITIAL_DATE_FORMAT: str = "%d-%m-%Y"
"""Date format required by website do properly format the URL."""
OUTPUT_DATE_FORMAT: str = "%Y-%m-%d"
"""Date format included in output csv filenames. Should support further data partitioning."""
DATA_DIR: str = os.getenv("DATA_DIR", "../../data/stock_candles")
"""Output directory in the filesystem."""
MAX_SLEEP_TIME: float = float(os.getenv("MAX_SLEEP_TIME", 2))
"""Sleep time between requests is in range from 0 to MAX_SLEEP_TIME seconds."""
OUTPUT_FILE_PREFIX: str = os.getenv("OUTPUT_FILE_PREFIX", "stock_candles")
"""The prefix of output csv files."""
DATA_SINK_BUCKET: str = os.getenv("DATA_SINK_BUCKET", "stocks-candles-data-sink")
"""The name of data sink GCS bucket."""
DATA_START_DATE: str = os.getenv("DATA_START_DATE", "01-01-2015")
"""ETL start date in INITIAL_DATE_FORMAT. Works only if the GCS bucket is empty."""
DATE_RANGE: int = os.getenv("DATE_RANGE", 30)
"""Number of days to import data about."""
