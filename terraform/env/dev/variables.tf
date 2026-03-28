variable "rg_name" {
  description = "The name of the resource group."
  type        = string
  
}
variable "rg_location" {
  description = "location"
  type = string
}

variable "openai_name" {
  description = "The name of the OpenAI resource."
  type        = string
}

variable "kv_name" {
  description = "The name of the Key Vault resource."
  type        = string
}