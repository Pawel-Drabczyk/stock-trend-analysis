output "cf_name" {
  value = google_cloudfunctions_function.function.name
}

output "cf_project_id" {
  value = google_cloudfunctions_function.function.project
}

output "cf_region" {
  value = google_cloudfunctions_function.function.region
}

output "cf_sa_email" {
  value = google_service_account.service_account_cf.email
}
