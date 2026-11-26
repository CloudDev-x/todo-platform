output "acr_login_server" {
  value = azurerm_container_registry.this.login_server
}

output "app_url" {
  value = "https://${azurerm_container_app.this.ingress[0].fqdn}"
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.this.fqdn
}
