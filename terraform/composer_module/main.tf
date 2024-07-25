/*
  Terraform module to create a Composer environment in GCP. Together with the role bindings
  for the environment, the module also creates the necessary role bindings for the CI step.
 */
locals {
  name_cc = replace(var.name, "_", "-")
  name_sa = "${replace(var.name, "_", "-")}-sa"
}

resource "google_project_service" "composer_api" {
  service                    = "composer.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_iam_member" "composer_google_managed_sa_role" {
  project = var.project_id
  role    = "roles/composer.ServiceAgentV2Ext"
  member  = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_service_account" "cloud_composer_sa" {
  account_id   = local.name_sa
  display_name = "Service Account for Composer Instance ${local.name_cc}"
}

resource "google_project_iam_member" "composer_project_roles" {
  for_each = toset([
    "roles/composer.worker",
    "roles/cloudfunctions.invoker"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloud_composer_sa.email}"
}

resource "google_composer_environment" "small_composer" {
  name   = local.name_cc
  region = var.location
  config {
    software_config {
      image_version = "composer-2.6.0-airflow-2.6.3"
      env_variables = {
        CF_DATA_JSON                 = jsonencode(var.cf_data)
        AIRFLOW_CONN_CLOUD_FUNCTIONS = "http://${var.location}-${var.project_id}.cloudfunctions.net"
      }
    }

    workloads_config {
      scheduler {
        cpu        = 0.5
        memory_gb  = 1
        storage_gb = 10
        count      = 1
      }
      web_server {
        cpu        = 0.5
        memory_gb  = 1.5
        storage_gb = 10
      }
      worker {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 10
        min_count  = 1
        max_count  = 1
      }
    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    node_config {
      service_account = google_service_account.cloud_composer_sa.name
    }
  }

  depends_on = [google_project_service.composer_api, google_project_iam_member.composer_google_managed_sa_role]
}

# The role binding necessary for CI step to sync dags to the composer environment
resource "google_storage_bucket_iam_binding" "bucket_iam_binding" {
  bucket = split("/", google_composer_environment.small_composer.config.0.dag_gcs_prefix)[2]
  role   = "roles/storage.objectAdmin"
  members = [
    "serviceAccount:${var.github_actions_dags_sync_sa_email}",
  ]
}

resource "google_secret_manager_secret_iam_member" "secret_access" {
  secret_id = var.dbt_sa_key_secret_name
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_composer_sa.email}"
}
