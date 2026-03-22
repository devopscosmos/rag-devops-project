module "rg" {
  source = "../../modules/resource_group"
  rg_name = var.rg_name
  rg_location = var.rg_location
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