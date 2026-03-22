provider "azurerm" {
  features {
    
  }
  resource_provider_registrations = "none"  ##to avoid error registering resource provider "Microsoft.Web": unexpected status 409 (409 Conflict) with error: ConflictingConcurrentWriteNotAllowed:
}