terraform {
  backend "azurerm" {
    resource_group_name = "dev-rg"  
    storage_account_name = "devopscosmostfstatesa"
    container_name = "tfstate"
    key = "dev.tfstate"
  }
}