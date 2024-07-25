import logging
import os
import re
from datetime import datetime
from typing import Optional

from google.cloud import storage

logging.basicConfig(level=logging.INFO)


class GCSWrapper:
    """Wrapper class for Google Cloud Storage operations.

    Attributes:
        client: Instance of the Google Cloud Storage Client.
        bucket: Google Cloud Storage Bucket object.

    Methods:
        list_files_and_find_latest: Lists files with a given prefix in the bucket and finds the latest date in the
            filenames.
        upload_files: Uploads files from the local disk to the specified GCS bucket.
    """

    def __init__(self, bucket_name: str):
        """Initializes the GCS client and sets the bucket.

        Args:
            bucket_name: The name of the Google Cloud Storage bucket.
        """
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def list_files_and_find_latest(
        self,
        prefix: str,
        date_format: str,
        hive_partitioning_prefix: str = "dt",
        date_regex: str = r"(\d{4}-\d{2}-\d{2})",
    ) -> Optional[datetime]:
        """Lists files in the bucket with the specified prefix and finds the latest date in the filenames.

        Args:
            prefix: The prefix to filter the files in the bucket.
            date_format: The format of the date in the filenames.

        Returns:
            The latest date found in the filenames, or None if no dates are found.
        """
        blobs = self.bucket.list_blobs()
        latest_date = None
        # date_pattern = re.compile(rf"{hive_partitioning_prefix}={date_regex}/{prefix}_{date_regex}\.csv$")
        date_pattern = re.compile(
            rf"{hive_partitioning_prefix}={date_regex}/{prefix}_{date_regex}\.csv$"
        )

        for blob in blobs:
            match = date_pattern.search(blob.name)
            if match:
                file_date = datetime.strptime(match.group(2), date_format)
                if latest_date is None or file_date > latest_date:
                    latest_date = file_date

        return latest_date

    def upload_files(
        self, local_folder: str, prefix: str, hive_partitioning_prefix: str = "dt"
    ) -> None:
        """Uploads files from the local disk to the GCS bucket.

        Args:
            local_folder: The path to the local folder containing the files.
            prefix: The prefix to filter which files to upload.
            hive_partitioning_prefix: The prefix to use for Hive partitioning.
        Returns:
            None
        """
        for filename in os.listdir(local_folder):
            if filename.startswith(prefix) and filename.endswith(".csv"):
                gcs_filename = (
                    f"{hive_partitioning_prefix}={filename[-14:-4]}/{filename}"
                )
                logging.info(f"Uploading file {filename} to {gcs_filename}")
                local_path = os.path.join(local_folder, filename)
                blob = self.bucket.blob(gcs_filename)
                blob.upload_from_filename(local_path)
