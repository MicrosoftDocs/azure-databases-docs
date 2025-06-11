---
title: |
  Quickstart: Create a cluster with Terraform
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: In this quickstart, create a new Azure Cosmos DB for MongoDB vCore cluster to store databases, collections, and documents by using Terraform.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: quickstart
ms.date: 06/11/2025
ms.custom: devx-track-terraform
---

# Azure Cosmos DB for MongoDB (vCore) with Terraform
This document provides instructions on using Terraform to deploy Azure Cosmos DB for MongoDB vCore resources. This involves directly calling the ARM API through Terraform. Full support for Terraform is targetted for the second half of 2024.

## Prerequisites
- Terraform installed on your machine.
- An Azure subscription.

## Terraform Configuration
Create a new '.tf' file in your Terraform project directory. Copy the example code and replace the resource group placeholder values with your own:

```hcl
resource "azurerm_resource_group" "example" {
  name     = "example-rg"
  location = "East US"
}

resource "azurerm_mongo_cluster" "example" {
  name                   = "example-mc"
  resource_group_name    = azurerm_resource_group.example.name
  location               = azurerm_resource_group.example.location
  administrator_username = "adminTerraform"
  administrator_password = "QAZwsx123"
  shard_count            = "1"
  compute_tier           = "Free"
  high_availability_mode = "Disabled"
  storage_size_in_gb     = "32"
}
```

For a complete list of parameters, including required and optional arguments, please visit the official [Terraform Registry documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mongo_cluster#arguments-reference).


## Next steps

> [!div class="nextstepaction"]
> [Migration options for Azure Cosmos DB for MongoDB vCore](migration-options.md)
