output "dbt_sa_email" {
  value = google_service_account.cloud_composer_sa.email
}

output "dag_gcs_prefix" {
  value = google_composer_environment.small_composer.config.0.dag_gcs_prefix
}

output "composer_environment_id" {
  value = google_composer_environment.small_composer.id
}
