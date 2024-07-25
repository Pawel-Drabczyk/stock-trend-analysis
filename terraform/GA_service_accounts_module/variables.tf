variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "state_bucket_name" {
  description = "Terraform state GCS bucket name"
  type        = string
}

variable "source_bucket_name" {
  description = "Cloud Function source code bucket name"
  type        = string
}

variable "github_actions_tf_sa_name" {
  description = "The name of the service account to tf GitHub Actions."
  type        = string
  default     = "github-actions-tf"
}

variable "github_actions_cf_zip_sa_name" {
  description = "The name of the service account to cf-zip GitHub Actions."
  type        = string
  default     = "github-actions-cf-zip"
}

variable "github_actions_dags_sync_sa_name" {
  description = "The name of the service account to dags-sync GitHub Actions."
  type        = string
  default     = "github-actions-dags-sync"
}
