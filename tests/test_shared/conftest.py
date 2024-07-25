from unittest.mock import Mock, patch

import pytest

from shared.gcs_wrapper import GCSWrapper


@pytest.fixture
def mock_gcs_wrapper():
    with patch("shared.gcs_wrapper.storage.Client") as mock_client:
        # Set up the mock client and bucket
        mock_bucket = Mock()
        mock_client().bucket.return_value = mock_bucket

        # Create an instance of your wrapper
        wrapper = GCSWrapper("mock-bucket")
        return wrapper
