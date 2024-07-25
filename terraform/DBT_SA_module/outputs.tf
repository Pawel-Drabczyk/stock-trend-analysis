output "dbt_sa_email" {
  value = google_service_account.service_account.email
}

output "dbt_sa_key_secret_name" {
  value = google_secret_manager_secret.dbt_sa_key_secret.name
}

output "dbt_sa_key_secret_version_name" {
  value = google_secret_manager_secret_version.dbt_sa_key_version.name
}
