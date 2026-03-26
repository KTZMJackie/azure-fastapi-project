data "azurerm_resource_group" "rg" {
  name = "rg-hello-aca-sg"
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "log-p16"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                       = "cae-p16"
  location                   = data.azurerm_resource_group.rg.location
  resource_group_name        = data.azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}

resource "azurerm_container_app" "app" {
  name                         = "aca-p16"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = data.azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity {
    type = "SystemAssigned"
  }

secret {
  name  = "acr-pwd"
  value = var.acr_password
}

  registry {
    server               = "acrhelloktzmjackie.azurecr.io"
    username             = "acrhelloktzmjackie"
    password_secret_name = "acr-pwd"
  }

  template {
    container {
      name   = "fastapi"
      image = "acrhelloktzmjackie.azurecr.io/p16-fastapi:v7"
      cpu    = 0.25
      memory = "0.5Gi"

    env {
        name  = "API_KEY"
        value = "dev-secret-key"
      }

      env {
        name  = "KEY_VAULT_NAME"
        value = "kvhello"
      }

      env {
        name  = "KEY_VAULT_SECRET_NAME"
        value = "hello-secret"
      }
    }

    min_replicas = 0
    max_replicas = 1
  }

  ingress {
    external_enabled = true
    target_port      = 80

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}