module "rg" {
  source = "../../modules/resource_group"
  rg_name = out.rg_name
  rg_location = var.rg_location
}