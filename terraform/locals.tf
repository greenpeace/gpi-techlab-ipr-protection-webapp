locals {
  image = "eu.gcr.io/${var.project_id}/${var.image_name}:v0.2"
  app_name = "iprprotection"
  services = [
    "run.googleapis.com",
    "iam.googleapis.com",
  ]
}
