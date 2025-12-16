---
title: Create and Manage Azure Cosmos DB with Terraform
description: Learn how to use Terraform to create and configure Azure Cosmos DB for NoSQL.
author: ginsiucheng
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: devx-track-terraform
ms.topic: how-to
ms.date: 07/11/2025
ms.author: mjbrown
appliesto:
  - ✅ NoSQL
---

# Manage Azure Cosmos DB for NoSQL resources with Terraform

In this article, you learn how to use Terraform to deploy and manage your Azure Cosmos DB accounts, databases, and containers.

This article shows Terraform samples for NoSQL accounts.

> [!IMPORTANT]
>
> * Account names are limited to 44 characters, all lowercase.
> * To change the throughput values, redeploy the Terraform file with updated Request Units per second (RU/s).
> * When you add or remove locations to an Azure Cosmos account, you can't simultaneously modify other properties. These operations must be done separately.
> * To provision throughput at the database level and share across all containers, apply the throughput values to the database options property.

To create any of the following Azure Cosmos DB resources, copy the example into a new Terraform file (*main.tf*). Alternatively, have two separate files for resources (*main.tf*) and variables (*variables.tf*). Be sure to include the azurerm provider, either in the main Terraform file or split out to a separate providers file. All examples can be found on the [Terraform samples repository](https://github.com/Azure/terraform).

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-autoscale/providers.tf":::

## <a id="create-autoscale"></a>Azure Cosmos account with autoscale throughput

Create an Azure Cosmos account in two regions with options for consistency and failover, with database and container configured for autoscale throughput that has the most index policy options enabled.

### `main.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-autoscale/main.tf":::

### `variables.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-autoscale/variables.tf":::

## <a id="create-analytical-store"></a>Azure Cosmos account with analytical store

Create an Azure Cosmos account in one region with a container with analytical time to live enabled and options for manual or autoscale throughput.

### `main.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-analyticalstore/main.tf":::

### `variables.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-analyticalstore/variables.tf":::

## <a id="create-manual"></a>Azure Cosmos account with standard provisioned throughput

Create an Azure Cosmos account in two regions with options for consistency and failover, with database and container configured for standard throughput that has the most policy options enabled.

### `main.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-manualscale/main.tf":::

### `variables.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-manualscale/variables.tf":::

## <a id="create-sproc"></a>Azure Cosmos DB container with server-side functionality

Create an Azure Cosmos account, database, and container with a stored procedure, trigger, and user-defined function.

### `main.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-serverside-functionality/main.tf":::

### `variables.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-serverside-functionality/variables.tf":::

## <a id="create-rbac"></a>Azure Cosmos DB account with Microsoft Entra ID and role-based access control

Create an Azure Cosmos account, a natively maintained role definition, and a natively maintained role assignment for a Microsoft Entra identity.

### `main.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-aad-rbac/main.tf":::

### `variables.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-aad-rbac/variables.tf":::

## <a id="free-tier"></a>Free-tier Azure Cosmos DB account

Create a free-tier Azure Cosmos account and a database with shared throughput that can be shared with up to 25 containers.

### `main.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-free-tier/main.tf":::

### `variables.tf`

:::code language="terraform" source="~/terraform_samples/quickstart/101-cosmos-db-free-tier/variables.tf":::

## Next steps

* [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
* [Terraform Azure tutorial](https://learn.hashicorp.com/collections/terraform/azure-get-started)
* [Terraform tools](https://www.terraform.io/docs/terraform-tools)
* [Azure Provider Terraform documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* [Terraform documentation](https://www.terraform.io/docs)
