data "google_project" "current" {}

# Create a GCS bucket to store Terraform state
resource "google_storage_bucket" "terraform_state" {
  name     = var.state_bucket_name
  location = var.state_bucket_location
}

# Enable the required services
resource "google_project_service" "project_services" {
  for_each = toset(var.services)
  service  = each.value
}

# Create a GCS bucket to store the source code
resource "google_storage_bucket" "source_code" {
  name     = var.source_bucket_name
  location = var.location
}

module "github_actions_service_accounts" {
  source             = "./GA_service_accounts_module"
  project_id         = data.google_project.current.project_id
  state_bucket_name  = google_storage_bucket.terraform_state.name
  source_bucket_name = google_storage_bucket.source_code.name
}

module "dbt_service_account" {
  source     = "./DBT_SA_module"
  name       = "dbt-dev"
  location   = var.location
  project_id = data.google_project.current.project_id
}

module "stocks_candles_module" {
  source            = "./CF_GCS_module"
  name              = "stocks_candles"
  source_cf_dir     = abspath("../source/stock_candles")
  source_shared_dir = abspath("../source/shared")
  cron_schedule     = "0 3 * * *"
  location          = var.location
  source_bucket     = google_storage_bucket.source_code.name
  dbt_sa_email      = module.dbt_service_account.dbt_sa_email
  project_id        = data.google_project.current.project_id
}

module "finance_reports_module" {
  source            = "./CF_GCS_module"
  name              = "finance_reports"
  source_cf_dir     = abspath("../source/finance_reports")
  source_shared_dir = abspath("../source/shared")
  cron_schedule     = "0 3 * * *"
  location          = var.location
  source_bucket     = google_storage_bucket.source_code.name
  dbt_sa_email      = module.dbt_service_account.dbt_sa_email
  project_id        = data.google_project.current.project_id
}

#module "cloud_composer_module" {
#  source                            = "./composer_module"
#  name                              = "airflow-dev"
#  location                          = var.location
#  zone                              = var.zone
#  project_id                        = data.google_project.current.project_id
#  project_number                    = data.google_project.current.number
#  github_actions_dags_sync_sa_email = module.github_actions_service_accounts.github_actions_dags_sync_sa_email
#  dbt_sa_key_secret_name            = module.dbt_service_account.dbt_sa_key_secret_name
#  cf_data                           = {
#    "cf_stocks_candles" = {
#      "cf_name"       = module.stocks_candles_module.cf_name
#      "cf_project_id" = module.stocks_candles_module.cf_project_id
#      "cf_region"     = module.stocks_candles_module.cf_region
#      "cf_sa_email"   = module.stocks_candles_module.cf_sa_email
#    },
#    "cf_finance_reports" = {
#      "cf_name"       = module.finance_reports_module.cf_name
#      "cf_project_id" = module.finance_reports_module.cf_project_id
#      "cf_region"     = module.finance_reports_module.cf_region
#      "cf_sa_email"   = module.finance_reports_module.cf_sa_email
#    },
#  }
#}
