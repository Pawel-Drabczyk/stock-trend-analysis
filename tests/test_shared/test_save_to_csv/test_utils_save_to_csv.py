import os
import shutil
from datetime import datetime

import pandas as pd

from source.shared.utils import save_to_csv
from tests.test_shared.constants import (
    DATA_DIR_TESTS,
    TEST_INITIAL_DATE_FORMAT,
    TEST_OUTPUT_DATE_FORMAT,
    TEST_PREFIX,
)


def test_file_creation():
    # Cleanup for consistency
    if os.path.exists(DATA_DIR_TESTS):
        shutil.rmtree(DATA_DIR_TESTS)
    os.makedirs(DATA_DIR_TESTS)

    date_string = "2023-10-21"
    data = {"calories": [420, 380, 390], "duration": [50, 40, 45]}
    df = pd.DataFrame(data)

    save_to_csv(
        df,
        date_string,
        DATA_DIR_TESTS,
        TEST_PREFIX,
        TEST_INITIAL_DATE_FORMAT,
        TEST_OUTPUT_DATE_FORMAT,
    )

    assert os.path.exists(
        os.path.join(
            DATA_DIR_TESTS,
            f"{TEST_PREFIX}_"
            f"{datetime.strptime(date_string, TEST_INITIAL_DATE_FORMAT).strftime(TEST_OUTPUT_DATE_FORMAT)}.csv",
        )
    )
