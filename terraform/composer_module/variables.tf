variable "name" {
  description = "The name used to define Cloud Composer Instance."
  type        = string
}

variable "project_id" {
  description = "GCP project to create resources in."
  type        = string
}

variable "project_number" {
  description = "GCP project number to create resources in."
  type        = string
}

variable "location" {
  description = "The region of the Cloud Composer Instance."
  type        = string
}

variable "zone" {
  description = "The zone of the Cloud Composer Instance."
  type        = string
}

variable "github_actions_dags_sync_sa_email" {
  description = "The email of the service account used to sync dags from github actions."
  type        = string
}

variable "machine_type" {
  description = "The machine type of the Cloud Composer Instance."
  type        = string
  default     = "e2-small"
}

variable "disk_size_gb" {
  description = "The disk size of the Cloud Composer Instance."
  type        = number
  default     = 20
}

variable "python_version" {
  description = "The python version of the Cloud Composer Instance."
  type        = string
  default     = "311"
}

variable "cf_data" {
  description = "Map of Cloud Functions data"
  type = map(object({
    cf_name       = string
    cf_project_id = string
    cf_region     = string
    cf_sa_email   = string
  }))
  default = {}
}

variable "dbt_sa_key_secret_name" {
  description = "The name of the secret containing the dbt service account key."
  type        = string
}
