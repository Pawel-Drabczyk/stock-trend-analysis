/*
  Terraform module to create a service account for DBT and grant necessary permissions to the service account.
 */
locals {
  dataset_id  = replace(var.name, "-", "_")
  name_sa     = "${replace(var.name, "_", "-")}-sa"
  name_sercet = "${replace(var.name, "_", "-")}-sa-key"
}

resource "google_service_account" "service_account" {
  account_id   = local.name_sa
  display_name = "Service Account for Cloud Function"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = local.dataset_id
  location   = var.location
}

resource "google_project_iam_member" "project_bigquery_iam" {
  for_each = toset([
    "roles/bigquery.jobUser",
    "roles/bigquery.dataViewer"
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_bigquery_dataset_iam_member" "editor" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_service_account_key" "dbt_sa_key" {
  service_account_id = google_service_account.service_account.name
}

resource "google_secret_manager_secret" "dbt_sa_key_secret" {
  secret_id = local.name_sercet
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "dbt_sa_key_version" {
  secret      = google_secret_manager_secret.dbt_sa_key_secret.id
  secret_data = base64decode(google_service_account_key.dbt_sa_key.private_key)
}
