"""The module contains utility functions for the Airflow DAGs."""

import json
import os

import google.auth.transport as transport
import pendulum
import requests
from google.auth import compute_engine

from constants import CF_DATA_ENV_VARIABLE_NAME

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": pendulum.datetime(year=2024, month=1, day=1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}


def get_cf_metadata(cf_name: str) -> [str, str, str, str]:
    """
    Get Cloud Function metadata from the environment variables.

    CF name, project_id, location, and service account email are loaded during terraform apply into the
    CF_DATA_ENV_VARIABLE_NAME json env variable, so it automatically updates the metadata of the Cloud Function. If the
    environment variable is not found, the function will raise an exception.

    Args:
        cf_name: the name of the Cloud Function terraform module in format "cf_<name>"
    Returns:
        [str, str, str, str]: the Cloud Function metadata in the following order: CF name, project_id, region, and
        service account email
    """
    #
    cf_data_json = os.getenv(CF_DATA_ENV_VARIABLE_NAME)
    cf_data = json.loads(cf_data_json)
    cf_data = cf_data[cf_name]

    return [
        cf_data["cf_name"],
        cf_data["cf_project_id"],
        cf_data["cf_region"],
        cf_data["cf_sa_email"],
    ]


def identity_token_from_metadata_server(url: str) -> str:
    """
    Use the Google Cloud metadata server in the Cloud Function, Cloud Run, AppEngine or Kubernetes etc., to obtain an
    environment to create an identity token. The token can be later added to the HTTP request as part of an
    Authorization header.

    Args:
        url (str): The url or target audience to obtain the ID token for.
            Examples: "https://europe-central2-metal-lantern-344112.cloudfunctions.net/stocks-candles-cf"
    Returns:
        str: The identity token. It lives for 3600 seconds and can be used one time.

    """
    request = transport.requests.Request()
    credentials = compute_engine.IDTokenCredentials(
        request=request, target_audience=url, use_metadata_identity_endpoint=True
    )

    credentials.refresh(request)

    return credentials.token


def trigger_cloud_function(url: str) -> str:
    """
    Authenticate, trigger a Cloud Function with a GET request and return the response.

    Args:
        url (str): The url of the Cloud Function to trigger.
    Returns:
        str: The message with the status code and the response text.s
    """
    headers = {
        "Authorization": f"Bearer {identity_token_from_metadata_server(url)}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return f"Status code: {response.status_code}.\n Response text: {response.text}"
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
