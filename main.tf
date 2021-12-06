terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>2.88.1"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "OWAResourceGroup" {
  name = "OWA"
  location = "uksouth"
}
