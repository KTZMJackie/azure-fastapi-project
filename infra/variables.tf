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

variable "key_vault_name" {
  description = "Name of the Azure Key Vault instance"
  type        = string
  default     = "kvhello"
}

variable "key_vault_secret_name" {
  description = "Name of the secret in Key Vault to retrieve"
  type        = string
  default     = "hello-secret"
}
