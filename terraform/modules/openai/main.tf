resource "azurerm_cognitive_account" "openai" {
  name                = "openai-rag-northcentralus"
  location            = "northcentralus"
  resource_group_name = "rg-ai-rag"
  kind                = "OpenAI"
  sku_name            = "S0"
}

resource "azurerm_cognitive_deployment" "deployments" {
  for_each = toset(var.models)

  name                 = each.value
  cognitive_account_id = azurerm_cognitive_account.openai.id
  sku {
    name = "S0"
  }
  model {
    format  = "OpenAI"
    name    = each.value
    version = "1"
  }

}