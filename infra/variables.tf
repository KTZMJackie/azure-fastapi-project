variable "acr_password" {
  description = "ACR admin password"
  sensitive   = true
}

variable "api_key" {
  description = "API key for the FastAPI write endpoint"
  sensitive   = true
}

variable "acr_name" {
  description = "Azure Container Registry name"
  type        = string
  default     = "acrhelloktzmjackie"
}
