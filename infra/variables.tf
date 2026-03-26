variable "location" {
  default = "Southeast Asia"
}

variable "acr_password" {
  description = "ACR admin password"
  sensitive   = true
}