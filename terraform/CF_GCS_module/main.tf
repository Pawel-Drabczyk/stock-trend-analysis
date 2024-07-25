/*
  The terraform module the following resources:
    - google_cloudfunctions_function
    - google_storage_bucket - to store the imported data
    - google_service_account - for the cloud function authentication
    - google_service_account - for the cloud scheduler authentication
    - google_bigquery_dataset - to store the transformed data
    - iam_binding - to grant minimal necessary permissions to dbt service account,
        cloud function service account, and cloud scheduler service account
 */
locals {
  name_bucket       = "${replace(var.name, "_", "-")}-data-sink"
  name_sa_cf        = "${replace(var.name, "_", "-")}-sa"
  name_sa_scheduler = "${replace(var.name, "_", "-")}-scheduler"
  name_cf           = "${replace(var.name, "_", "-")}-cf"
  name_scheduler    = "${replace(var.name, "_", "-")}-scheduler-job"
  temp_source_dir   = "temp_${var.name}"
  source_dirs_hash = sha256(join("", flatten([
    [
      for file in fileset(var.source_cf_dir, "**") : filesha256("${var.source_cf_dir}/${file}")
      if !contains(["__pycache__/"], file)
    ],
    [
      for file in fileset(var.source_shared_dir, "**") : filesha256("${var.source_shared_dir}/${file}")
      if !contains(["__pycache__/"], file)
    ]
  ])))
  local_zip_file = "${local.name_cf}-source-${local.source_dirs_hash}.zip"
  gcs_zip_file   = "${local.temp_source_dir}/${local.local_zip_file}"
}

# this null_resource is used to prepare the source code and upload it to GCS bucket in zipped format
resource "null_resource" "prepare_source" {
  triggers = {
    source_dirs_hash = local.source_dirs_hash
  }

  provisioner "local-exec" {
    command = <<EOT
    # Authenticate using the service account key
    gcloud auth activate-service-account --key-file=${var.sa_key_file}

    # remove the zip file and __pychache__, clean temp_dir
    rm -rf ${local.local_zip_file} ${var.source_cf_dir}/__pycache__ && mkdir -p ${local.temp_source_dir}

    # copy the source code to the temp directory
    cp -r ${var.source_shared_dir} ${var.source_cf_dir}/* ${local.temp_source_dir}

    # create the local zip file
    cd ${local.temp_source_dir} && zip -r ${local.local_zip_file}  * && cd ..

    # Copy the zip file to the GCS bucket
    gsutil cp ${local.temp_source_dir}/${local.local_zip_file} gs://${var.source_bucket}/${local.gcs_zip_file}
    EOT
  }
}

resource "google_cloudfunctions_function" "function" {
  depends_on = [null_resource.prepare_source]

  name                  = local.name_cf
  runtime               = var.cf_runtime
  available_memory_mb   = var.cf_available_memory
  source_archive_bucket = var.source_bucket
  source_archive_object = local.gcs_zip_file
  service_account_email = google_service_account.service_account_cf.email
  trigger_http          = true
  entry_point           = var.cf_entry_point
  timeout               = var.cf_timeout

  environment_variables = {
    DATA_SINK_BUCKET = google_storage_bucket.bucket.name
    DATA_DIR         = "/tmp"
  }
}

resource "google_storage_bucket" "bucket" {
  name     = local.name_bucket
  location = var.location
}

resource "google_service_account" "service_account_cf" {
  account_id   = local.name_sa_cf
  display_name = "Service Account for Cloud Function"
}

resource "google_service_account" "service_account_scheduler" {
  account_id   = local.name_sa_scheduler
  display_name = "Service Account for Cloud Scheduler"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.name
  location   = var.location
}

resource "google_bigquery_dataset_iam_member" "editor" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.dbt_sa_email}"
}

resource "google_storage_bucket_iam_binding" "bucket_iam_binding" {
  bucket = google_storage_bucket.bucket.name
  role   = "roles/storage.objectAdmin"

  members = [
    "serviceAccount:${google_service_account.service_account_cf.email}",
  ]
}

resource "google_storage_bucket_iam_binding" "bucket_iam_binding_dbt" {
  for_each = toset([
    "roles/storage.objectViewer",
    "roles/storage.legacyBucketReader",
  ])
  bucket = google_storage_bucket.bucket.name
  role   = each.key

  members = [
    "serviceAccount:${var.dbt_sa_email}",
  ]
}

resource "google_cloudfunctions_function_iam_binding" "function_aim_binding_scheduler" {
  project        = var.project_id
  region         = var.location
  cloud_function = google_cloudfunctions_function.function.name
  role           = "roles/cloudfunctions.invoker"

  members = [
    "serviceAccount:${google_service_account.service_account_scheduler.email}",
  ]
}

resource "google_cloud_scheduler_job" "scheduler" {
  name     = local.name_scheduler
  schedule = var.cron_schedule

  http_target {
    uri         = google_cloudfunctions_function.function.https_trigger_url
    http_method = "GET"

    oidc_token {
      service_account_email = google_service_account.service_account_scheduler.email
    }
  }
}
