# main.tf
terraform {
  required_version = ">= 0.14"

  required_providers {
    # Cloud Run support was added on 3.3.0
    google = ">= 3.3"
  }
  backend "gcs" {
    bucket = "global-ipr-terraform-state"
    # Structure:
    # state/<application/<entity>/<environment>/
    prefix = "state/socialclimatetech/editportal/test/"
  }
}