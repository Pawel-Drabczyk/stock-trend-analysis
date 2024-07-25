variable "state_bucket_name" {
  description = "The name of the GCS bucket for Terraform state"
  type        = string
  default     = "stocks-trends-tf-state"
}

variable "state_bucket_location" {
  description = "The location of the state GCS bucket"
  type        = string
  default     = "europe-central2"
}

variable "services" {
  description = "List of Google Cloud services to be enabled"
  type        = list(string)
  default = [
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com"
  ]
}

variable "source_bucket_name" {
  description = "The name of the GCS bucket for temporary storage of CF source code."
  type        = string
  default     = "stocks-trends-cf-source"
}

variable "project" {
  description = "GCP project"
  type        = string
  default     = "metal-lantern-344112"
}

variable "location" {
  description = "The default location of resources"
  type        = string
  default     = "europe-central2"
}

variable "zone" {
  description = "The default zone of resources"
  type        = string
  default     = "europe-central2-c"
}

variable "github_actions_terraform_sa_name" {
  description = "The name of the Service Account for running GithHub actions."
  type        = string
  default     = "github-actions-terraform-sa-dev"
}

variable "github_actions_dag_sync_sa_name" {
  description = "The name of the Service Account for running GithHub actions."
  type        = string
  default     = "github-actions--dags-sync-sa-dev"
}
