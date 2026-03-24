output "resource_group_name" {
  value = data.azurerm_resource_group.rg.name
}

output "container_app_name" {
  value = azurerm_container_app.app.name
}