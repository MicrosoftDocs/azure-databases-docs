---
title: Create Virtual Endpoints for Read Replicas With Terraform
description: This article describes the virtual endpoints for read replica feature using Terraform for Azure Database for PostgreSQL - Flexible Server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 12/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Create virtual endpoints for read replicas with Terraform

Using Terraform, you can create and manage virtual endpoints for read replicas in Azure Database for PostgreSQL—Flexible Server. Terraform is an open-source infrastructure-as-code tool that allows you to define and provision infrastructure using a high-level configuration language.

## Prerequisites

Before you begin, ensure you have the following:

- An Azure account with an active subscription.
- Terraform installed on your local machine. You can download it from the [official Terraform website](https://www.terraform.io/downloads.html).
- Azure CLI installed and authenticated. Instructions are in the [Azure CLI documentation](/cli/azure/install-azure-cli).

Ensure you have a basic understanding of Terraform syntax and Azure resource provisioning.

## Configuring virtual endpoints

Follow these steps to create virtual endpoints for read replicas in Azure Database for PostgreSQL - Flexible Server:

### Initialize the Terraform configuration

Create a `main.tf` file and define the Azure provider.

```terraform
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}
```

### Create the primary Azure Database for PostgreSQL

Define the primary PostgreSQL server resource.

```terraform
resource "azurerm_postgresql_flexible_server" "primary" {
  name                = "primary-server"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  version             = "12"
  administrator_login = "adminuser"
  administrator_password = "password"
  sku_name            = "Standard_D4s_v3"

  storage_mb = 32768
  backup_retention_days = 7
  geo_redundant_backup = "Disabled"
  high_availability {
    mode = "ZoneRedundant"
  }
}
```

### Create read replicas

Define the read replicas for the primary server.

```terraform
resource "azurerm_postgresql_flexible_server" "replica" {
  name                = "replica-server"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  source_server_id    = azurerm_postgresql_flexible_server.primary.id
}
```

### Configure virtual endpoints

To configure virtual endpoints, define the necessary resources.

```terraform
resource "azurerm_postgresql_flexible_server_virtual_endpoint" "example" {
  name                = "example-virtual-endpoint"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_flexible_server.primary.name
}
```

## Apply the configuration

Initialize Terraform and apply the configuration.

```bash
terraform init
terraform apply
```

Confirm the apply action when prompted. Terraform provisions the resources and configures the virtual endpoints as specified.

## Related content

- [Read replicas in Azure Database for PostgreSQL - Flexible Server](concepts-read-replicas.md)
- [Geo-replication in Azure Database for PostgreSQL - Flexible Server](concepts-read-replicas-geo.md)
- [Promote read replicas in Azure Database for PostgreSQL - Flexible Server](concepts-read-replicas-promote.md)
- [Virtual endpoints for read replicas in Azure Database for PostgreSQL - Flexible Server](concepts-read-replicas-virtual-endpoints.md)
- [Create and manage read replicas in Azure Database for PostgreSQL - Flexible Server](how-to-read-replicas-portal.md)
- [Terraform Azure provider documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
