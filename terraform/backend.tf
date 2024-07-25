terraform {
  backend "gcs" {
    bucket = "stocks-trends-tf-state"
    prefix = "terraform/state"
  }
}
