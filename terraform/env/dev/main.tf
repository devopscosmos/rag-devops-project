module "rg" {
  source = "../../modules/resource_group"
  rg_name = var.rg_name
  rg_location = var.rg_location
}

module "openai" {
  source              = "../../modules/openai"
  name                = var.openai_name
  location            = var.rg_location
  resource_group_name = var.rg_name

  models = [
    "gpt-4.1-mini",
    "text-embedding-3-small"
  ]
}

module "kv" {
  source              = "../../modules/keyvault"
  name                = "rag-dev-kv"
  location            = var.rg_location
  resource_group_name = var.rg_name

  openai_key      = module.openai.primary_key
  openai_endpoint = module.openai.endpoint
}

module "plan" {
  source              = "../../modules/app_service_plan"
  name                = "rag-dev-plan"
  location            = var.rg_location
  resource_group_name = module.rg.out_rg_name
}

module "app" {
  source              = "../../modules/app_service"
  name                = "rag-dev-devopscosmos-app"
  location            = var.rg_location
  resource_group_name = module.rg.out_rg_name
  service_plan_id     = module.plan.plan_id
}