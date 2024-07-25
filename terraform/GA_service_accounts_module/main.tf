/*
  Terraform module to create service accounts for GitHub Actions and grant necessary
  permissions to the service accounts. The module creates the following resources:
    - google_service_account - for terraform GitHub Actions
    - google_service_account - for zipping Cloud Functions code and pushing it to GCS bucket
    - google_service_account - for dags sync GitHub Actions
    - google_project_iam_member - to grant the necessary permissions to the terraform GitHub Actions service account
    - google_storage_bucket_iam_binding - to grant the necessary permissions to the dags sync GitHub Actions service account
    - google_storage_bucket_iam_binding - to grant the necessary permissions to the zipping Cloud Functions code service account
 */

resource "google_service_account" "github_actions_tf_sa" {
  account_id   = var.github_actions_tf_sa_name
  display_name = "Service Account for terraform GitHub Actions"
}

resource "google_service_account" "github_actions_cf_zip_sa" {
  account_id   = var.github_actions_cf_zip_sa_name
  display_name = "Service Account for zipping Cloud Functions code and pushing it to GCS bucket"
}

resource "google_project_iam_member" "composer_worker" {
  project = var.project_id
  role    = "roles/owner"
  member  = "serviceAccount:${google_service_account.github_actions_tf_sa.email}"
}

resource "google_service_account" "github_actions_dags_sync_sa" {
  account_id   = var.github_actions_dags_sync_sa_name
  display_name = "Service Account for dags sync GitHub Actions"
}

resource "google_storage_bucket_iam_binding" "bucket_iam_binding" {
  bucket = var.state_bucket_name
  role   = "roles/storage.objectViewer"

  members = [
    "serviceAccount:${google_service_account.github_actions_dags_sync_sa.email}",
  ]
}

resource "google_storage_bucket_iam_binding" "source_code_bucket_iam_binding" {
  bucket = var.source_bucket_name
  role   = "roles/storage.objectUser"

  members = [
    "serviceAccount:${google_service_account.github_actions_cf_zip_sa.email}",
  ]
}
