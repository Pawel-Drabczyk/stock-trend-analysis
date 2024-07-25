output "github_actions_tf_sa_email" {
  value = google_service_account.github_actions_tf_sa.email
}

output "github_actions_dags_sync_sa_email" {
  value = google_service_account.github_actions_dags_sync_sa.email
}
