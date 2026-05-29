terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.65"
    }
  }
  required_version = ">= 1.5.0"

  backend "azurerm" {
    resource_group_name  = "rg-hello-aca-sg"
    storage_account_name = "tfstatektzmjackie"
    container_name       = "tfstate"
    key                  = "azure-fastapi-project.tfstate"
  }
}

provider "azurerm" {
  features {}
}
