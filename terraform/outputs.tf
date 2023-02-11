## GCP project I
output "url" {
  value = google_cloud_run_service.iprprotection.status[0].url
}