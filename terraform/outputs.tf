output "url" {
  value = {
    app  = google_cloud_run_service.service.status[0].url
  }
}
