from datetime import datetime
from unittest.mock import Mock

# Mock data for testing
mock_files = [
    "dt=2021-01-01/stock_candles_2021-01-01.csv",
    "dt=2021-01-02/stock_candles_2021-01-02.csv",
    "dt=2021-01-03/stock_candles_2021-01-03.csv",
]


def test_list_files_and_find_latest(mock_gcs_wrapper):
    prefix = "stock_candles"
    date_format = "%Y-%m-%d"

    # Configure Mock objects to have a 'name' attribute
    mock_blobs = [Mock(name=file, spec=["name"]) for file in mock_files]
    for mock_blob, file_name in zip(mock_blobs, mock_files):
        mock_blob.name = file_name

    # Mock the list_blobs method
    mock_gcs_wrapper.bucket.list_blobs.return_value = mock_blobs

    latest_date = mock_gcs_wrapper.list_files_and_find_latest(prefix, date_format)
    assert latest_date == datetime(2021, 1, 3), "Incorrect latest date found"


test_list_files_and_find_latest


def test_upload_files(mock_gcs_wrapper, tmp_path):
    prefix = "stock_candles"
    file = tmp_path / "stock_candles_2021-01-04.csv"
    file.write_text("test content")

    # Mock the blob upload method
    mock_gcs_wrapper.bucket.blob.return_value.upload_from_filename = Mock()

    mock_gcs_wrapper.upload_files(str(tmp_path), prefix)

    # Check if upload_from_filename was called
    mock_gcs_wrapper.bucket.blob.assert_called_with(
        "dt=2021-01-04/stock_candles_2021-01-04.csv"
    )
    mock_gcs_wrapper.bucket.blob.return_value.upload_from_filename.assert_called_with(
        str(file)
    )


def test_no_files_in_bucket(mock_gcs_wrapper):
    prefix = "stock_candles"
    date_format = "%Y-%m-%d"

    mock_gcs_wrapper.bucket.list_blobs.return_value = []
    latest_date = mock_gcs_wrapper.list_files_and_find_latest(prefix, date_format)
    assert latest_date is None, "Expected None when no files are in the bucket"


def test_empty_upload_directory(mock_gcs_wrapper, tmp_path):
    prefix = "stock_candles"

    mock_gcs_wrapper.bucket.blob.return_value.upload_from_filename = Mock()
    mock_gcs_wrapper.upload_files(str(tmp_path), prefix)

    mock_gcs_wrapper.bucket.blob.return_value.upload_from_filename.assert_not_called()
