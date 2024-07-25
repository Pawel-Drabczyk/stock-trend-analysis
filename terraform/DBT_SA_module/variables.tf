variable "name" {
  description = "The name used to define SA name and dataset name."
  type        = string
}

variable "project_id" {
  description = "GCP project to create resources in."
  type        = string
}

variable "location" {
  description = "The location of the BQ dataset"
  type        = string
}
