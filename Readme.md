# Stocks trend analysis

This project is a stock trend analysis tool. It focuses on trend analysis
near to the important dates for the company e.g. publishing the annual report.
The tool is designed to be used to make decisions based on recent stock trend.
The analysis part is not ready yet, for now the tool serves as a data
engineering portfolio project.

#### Table of contents
1. Data sources
2. Cloud infrastructure
3. ELT process
4. Testing
5. CI/CD
6. Installation and execution
7. Cloud installation and execution

## 1.Data sources:

The data sources are:
- [Stock candles](https://www.gpw.pl/): the official website of the Warsaw
Stock Exchange.
- [Finance reports](): calendar of the events related to the companies
listed on the Warsaw Stock Exchange. Among other data this source contains
the dates of the annual reports publication.

## 2. Cloud infrastructure

The project can be run both locally or on the Google Cloud Platform. Terraform
is used to manage the cloud infrastructure. I have focused on supporting the
reusability and clean code principles by using:
- Terraform modules: to define the reusable infrastructure components.
- `source/shared`: to share the python code across the cloud functions.

The infrastructure is defined in
the `terraform` directory. The infrastructure consists of the following
components:
- **Google Cloud Storage** buckets: to store the data in csv format.
- **Google Cloud Functions**: to run the data collection
- **Google Cloud Scheduler**: to trigger the data collection
- **Google BigQuery**: to store the data in a data warehouse.
- **Service accounts and IAM** roles: to manage the permissions using the least
privilege principle.
- **OPTIONAL: Google Cloud Composer**: The Composer is used to orchestrate the ELT.
For now, it was commented out in the `main.tf` file to reduce the costs of the
infrastructure. The Airflow dag defined in the `source/dags` directory orchestrate
the execution of Cloud Functions and the data loading to the BigQuery. In the future
the Composer will be used to orchestrate the data transformations with DBT and the
live analysis of the stock trends.

## 3. ELT process
The general ELT process is as follows:
- The data are scraped from source websites using the `requests` and `beautifulsoup4`.
The data scraping process is run in Google Cloud Functions trigger by the Google Cloud
Scheduler. The scraping code can also be run from the local machine.
- The data are then stored in the Google Cloud Storage as a CSV files.
- The data are exposed using the BigQuery External Tables via Data Build Tool(DBT)
package `dbt_external_tables`.
- Then data are further transformed using DBT. For now only the very initial steps of
transformations are added.
- In `source/dags` directory there are DAGs that orchestrate the running of Cloud Function.
However, the terraform Google Cloud Composer is commented out to reduce the costs of the
infrastructure.


## 4. Testing
The 34 tests are run using the `pytest` package. The tests are run in the `tests` directory.
The tests are run in the CI/CD pipeline. They are testing the various steps of the ELT
processes by isolating them using the mocking and patching techniques.

Some of the tests are also running actual data scraping process to ensure that the
data are scraped correctly. Those tests are very valuable to catch the changes in
the source websites.

## 5. CI/CD
To ensure the quality of the code the pre-commit hooks are used. The pre-commit hooks
are run locally and in the GitHub Actions CI/CD pipeline. They are checking the code formatting using
the `black` package and the code quality using the `flake8` package.

The following GitHub Actions CI/CD pipelines are defined:
- **pre-commit**: to check the code formatting and quality.
- **pytest**: to run the tests.
- **terraform**: to check the terraform code formatting, validate the terraform code,
plan the terraform changes and apply the terraform changes.
- **sync-dags**: to sync the dags to the Google Cloud Composer bucket. This pipeline is
turned off once the Google Cloud Composer is commented out in the `main.tf` file.

## 6. Installation and execution
### 6.1 pre-commit hooks
To install the pre-commit hooks run the following command:
```bash
pip install --upgrade pre-commit black
```
### 6.2 Virtual environment
The venv should be created using command line of IDE. The file `requirements.txt` contains
the list of the required packages to run all the ELT processes and tests. While the files
`source/finance_reports/requirements.txt` and `source/stock_candles/requirements.txt`
contain the list of the required packages to run each individual data pipeline.

The directories `source` and `source/shared` have to be added to PYTHONPATH. It is
necessary to run the ELT processes both from the local machine and from the Google Cloud
Functions. PYTHONPATH can be modified via IDE settings or by running the shell command.

### 6.3 Running the tests
Tests can be run using the following command:
```bash
pytest tests/
```

### 6.4 Running the ELT processes locally
After finishing previous configuration steps the ELT processes can be run locally from
the IDE or from the command line. The files `source/finance_reports/finance_report_day.py`
and `source/stock_candles/stock_candles.py` contain the main functions that run the ELT
process and store the csv files locally. The date range of the data to be scraped is
hardcoded in the `finance_report_day.py` and `stock_candles.py` files.

The ELT processes are run using the following commands:
```bash
cd source/finance_reports && python finance_report_day.py
```
```bash
cd source/stock_candles && python stock_candles.py
```
## 7. Cloud installation and execution
### 7.1 Creating terraform state bucket
There are a few ways to create the terraform state bucket. The easiest way is to install
terraform locally, authenticate with the Google Cloud Platform and run the following
steps:
- Set the `project` variable in the `terraform/variables.tf` file.
- Comment out the backend configuration in the `terraform/backend.tf` file.
This will make terraform use the local state file.

- Navigate to the Terraform directory:

    ```bash
    cd terraform
    ```

- Initialize Terraform:

    ```bash
    terraform init
    ```

- Apply the configuration to create the state bucket:

    ```bash
    terraform apply -target=google_storage_bucket.terraform_state
  -target=google_storage_bucket.source_code -target=module.github_actions_service_accounts
    ```

This will create the necessary GCS bucket to store your Terraform state files securely.

### 7.2 Moving the State into the Bucket

If you already have an existing Terraform state file and you want to move it to the
newly created GCS bucket, follow these steps:

- Uncomment the backend configuration in the `terraform/backend.tf` file.
- Initialize Terraform with the new backend configuration:
    ```bash
    terraform init -migrate-state
    ```
This command will migrate your existing Terraform state to the new GCS bucket. You will be prompted to confirm the migration.

- Verify that the state has been moved successfully. After running the above command,
Terraform will provide output indicating the success of the state migration. You can
also check the GCS bucket to ensure the state files are present.

### 7.2 Setting GitHub secrets and variables

GitHub secrets are used to store the sensitive information like the Google Cloud
credentials. The service account keys can be downloaded via UI. The following secrets
have to be set:
- `TERRAFORM_GCP_SA_KEY` - the `github-actions-tf@<project_id>.iam.gserviceaccount.com`
service account key in the JSON format.
- `TERRAFORM_GCP_ZIP_CF_SA_KEY` - the `github-actions-cf-zip@<project_Id>.iam.gserviceaccount.com`
service account key in the JSON format.

Nonsensitive variables have to be set in the GitHub repository settings:
- `GCP_PROJECT_ID`
- `TF_STATE_BUCKET_NAME`

### 7.4 Creating the Infrastructure

Once the state bucket is set up and the secrets are configured, you can proceed to create the infrastructure using Terraform. You have two options to apply your Terraform configuration: manually via command line or through GitHub Actions.

#### 7.4.1. Using Command Line

Run Terraform command:
    ```bash
    terraform apply
    ```

#### 7.4.2. Using GitHub Actions
- Navigate to the GitHub Actions tab in your repository.
- Find the `Terraform GitHub Actions` workflow in the list.
- Click on the `Run workflow` button on the right-hand side.
- Select the branch you want to run the workflow on (if applicable).
- Click the `Run workflow` button to start the workflow.
    The workflow will execute the following steps:
    - Checkout the repository
    - Set up Terraform
    - Initialize Terraform
    - Plan the Terraform changes
    - Apply the Terraform changes if the event is a push to the `master` branch
