"""
DAG to trigger finance reports HTTPS Cloud Function.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.timetables.trigger import CronTriggerTimetable

from airflow_utils import get_cf_metadata, default_args, trigger_cloud_function

CF_NAME, CF_PROJECT_ID, CF_REGION, CF_SERVICE_ACCOUNT_EMAIL = get_cf_metadata(
    "cf_finance_reports"
)
CF_URL = f"https://{CF_REGION}-{CF_PROJECT_ID}.cloudfunctions.net/{CF_NAME}"


with DAG(
    "finance_reports_data_ingestion",
    default_args=default_args,
    description="DAG to trigger finance reports Cloud Function",
    schedule=CronTriggerTimetable("0 3 * * *", timezone="UTC"),
    catchup=False,
    max_active_runs=1,
) as dag:
    finance_reports_cf_run = PythonOperator(
        task_id="finance_reports_cf_run",
        python_callable=trigger_cloud_function,
        op_kwargs={"url": CF_URL},
    )

finance_reports_cf_run
