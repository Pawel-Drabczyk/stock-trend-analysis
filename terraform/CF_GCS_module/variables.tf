variable "name" {
  description = "The name used to define GCS name, BQ dataset name, SA name, CF name and Scheduler Job name"
  type        = string
}

variable "location" {
  description = "The location of the GCS bucket, BQ dataset, and CF"
  type        = string
}

variable "source_cf_dir" {
  description = "Path to source code directory for the CF."
  type        = string
}

variable "source_shared_dir" {
  description = "Path to shared source code directory for the all the CFs."
  type        = string
}

variable "source_bucket" {
  description = "Name of the bucket for temporary storage of source code."
  type        = string
}

variable "cron_schedule" {
  description = "Cron string for Cloud Scheduler. Format * * * * *."
  type        = string
}

variable "dbt_sa_email" {
  description = "Email of the service account for DBT."
  type        = string
}

variable "project_id" {
  description = "GCP project to create resources in."
  type        = string
}

variable "cf_runtime" {
  description = "The environment to run the CF in."
  type        = string
  default     = "python311"
}

variable "cf_available_memory" {
  description = "RAM memory for CF in format XMB."
  type        = number
  default     = 256
}

variable "cf_entry_point" {
  description = "Python function from main.py file to be executed."
  type        = string
  default     = "handle"
}

variable "cf_timeout" {
  description = "Maximum time to execute the CF."
  type        = number
  default     = 540
}

variable "sa_key_file" {
  description = "Path to the service account key file in local filesystem."
  type        = string
  default     = "caution/terraform-cf-zip-sa-keyfile.json"
}
