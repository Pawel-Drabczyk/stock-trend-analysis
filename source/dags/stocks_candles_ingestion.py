"""
DAG to trigger stocks candles HTTPS Cloud Function.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.timetables.trigger import CronTriggerTimetable

from airflow_utils import get_cf_metadata, default_args, trigger_cloud_function

CF_NAME, CF_PROJECT_ID, CF_REGION, CF_SERVICE_ACCOUNT_EMAIL = get_cf_metadata(
    "cf_stocks_candles"
)
CF_URL = f"https://{CF_REGION}-{CF_PROJECT_ID}.cloudfunctions.net/{CF_NAME}"


with DAG(
    "stocks_candles_data_ingestion",
    default_args=default_args,
    description="DAG to trigger stocks-candles Cloud Function",
    schedule=CronTriggerTimetable("0 3 * * *", timezone="UTC"),
    catchup=False,
    max_active_runs=1,
) as dag:
    stocks_candles_cf_run = PythonOperator(
        task_id="stocks_candles_cf_run",
        python_callable=trigger_cloud_function,
        op_kwargs={"url": CF_URL},
    )

stocks_candles_cf_run
