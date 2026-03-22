terraform {
  backend "azurerm" {
    resource_group_name = var.out_rg_name   
    storage_account_name = "tfstatesa"
    container_name = "tfstate"
    key = "dev.tfstate"
  }
}