---
title: Bulk add or remove firewall rules for Azure Cosmos DB
description: Add or remove firewall rule IP addresses in bulk for one or all accounts in a subscription or resource group
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.custom: devx-track-azurecli
ms.topic: sample
ms.date: 12/06/2024
---

# Add or remove IP firewall rules in bulk

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](../../../includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

The scripts in this article demonstrate how to add and remove IP Firewall Rules in bulk for Azure Cosmos DB accounts. 
There are two separate scripts on this page, one for adding IP addresses, and another for removing. 

The scripts add or remove the following IP addresses for access.
- Azure portal access to your accounts.
- Managed services in Azure datacenters (for example, Azure Functions)
- Any custom IP address or CIDR (Classless Inter-Domain Routing) ranges.
- Your local IP address.

By default, this script adds or removes all listed IP addresses to every account in every resource group in the current subscription. You can also specify a single resource group and one or more Cosmos DB accounts within that resource group to process.


[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

- This article requires version 2.9.1 or later of the Azure CLI. If using Azure Cloud Shell, the latest version is already installed.

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script to bulk add IP addresses

:::code language="azurecli" source="~/azure_cli_scripts/cosmosdb/common/ipfirewall-bulk-add.sh" :::

### Run the script to bulk remove IP addresses

:::code language="azurecli" source="~/azure_cli_scripts/cosmosdb/common/ipfirewall-bulk-remove.sh" :::

## Sample reference

This script uses the following commands. Each command in the table links to command specific documentation.

| Command | Notes |
|---|---|
| [az group list](/cli/azure/group#az-group-list) | Lists all resource groups in an Azure subscription. |
| [az cosmosdb list](/cli/azure/cosmosdb#az-cosmosdb-list) | Lists all Azure Cosmos DB accounts in a resource group. |
| [az cosmosdb show](/cli/azure/cosmosdb#az-cosmosdb-show) | Show the details for an Azure Cosmos DB account. |
| [az cosmosdb update](/cli/azure/cosmosdb#az-cosmosdb-update) | Update an Azure Cosmos DB account. |


## Next steps

For more information on the Azure Cosmos DB CLI, see [Azure Cosmos DB CLI documentation](/cli/azure/cosmosdb).

For Azure CLI samples for specific APIs, see:

- [CLI Samples for Cassandra](../../../cassandra/cli-samples.md)
- [CLI Samples for Gremlin](../../../graph/cli-samples.md)
- [CLI Samples for API for MongoDB](../../../mongodb/cli-samples.md)
- [CLI Samples for SQL](../../../sql/cli-samples.md)
- [CLI Samples for Table](../../../table/cli-samples.md)
