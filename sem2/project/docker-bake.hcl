group "default" {
  targets = ["image"]
}

target "image" {
  target = "image"
  tags = [
    "ghcr.io/un1uckyyy/fast-api-fa:dev"
  ]
}