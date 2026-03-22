resource "azurerm_linux_web_app" "app" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = var.service_plan_id

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "WEBSITES_PORT" = "8000"
  }
}