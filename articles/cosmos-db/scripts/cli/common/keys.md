---
title: Work with account keys for an Azure Cosmos DB account
description: Work with account keys and connection strings for an Azure Cosmos DB account including listing and regenerating
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.custom: devx-track-azurecli
ms.topic: sample
ms.date: 10/22/2024
---

# Work with account keys and connection strings for an Azure Cosmos DB account using Azure CLI

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](../../../includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

The script in this article demonstrates four operations.

- List all account keys
- List read only account keys
- List connection strings
- Regenerate account keys

 This script shows Azure Cosmos DB for NoSQL examples, but these operations are identical across all database APIs in Azure Cosmos DB.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

- This article requires version 2.9.1 or later of the Azure CLI. If using Azure Cloud Shell, the latest version is already installed.

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/cosmosdb/common/keys.sh" id="FullScript":::

## Clean up resources

[!INCLUDE [cli-clean-up-resources.md](~/reusable-content/ce-skilling/azure/includes/cli-clean-up-resources.md)]

```azurecli
az group delete --name $resourceGroup
```

## Sample reference

This script uses the following commands. Each command in the table links to command specific documentation.

| Command | Notes |
|---|---|
| [az group create](/cli/azure/group#az-group-create) | Creates a resource group in which all resources are stored. |
| [az cosmosdb create](/cli/azure/cosmosdb#az-cosmosdb-create) | Creates an Azure Cosmos DB account. |
| [az cosmosdb keys list](/cli/azure/cosmosdb/keys#az-cosmosdb-keys-list) | List the keys for an Azure Cosmos DB account. |
| [az cosmosdb keys list --type read-only-keys](/cli/azure/cosmosdb/keys#az-cosmosdb-keys-list) | List the read only keys for an Azure Cosmos DB account. |
| [az cosmosdb keys list --type connection-strings](/cli/azure/cosmosdb/keys#az-cosmosdb-keys-list) | List the connection strings for an Azure Cosmos DB account. |
| [az cosmosdb keys regenerate](/cli/azure/cosmosdb/keys#az-cosmosdb-keys-regenerate) | Regenerate an access key for an Azure Cosmos DB database account. |
| [az group delete](/cli/azure/resource#az-resource-delete) | Deletes a resource group including all nested resources. |

## Next steps

For more information on the Azure Cosmos DB CLI, see [Azure Cosmos DB CLI documentation](/cli/azure/cosmosdb).

For Azure CLI samples for specific APIs see:

- [CLI Samples for Cassandra](../../../cassandra/cli-samples.md)
- [CLI Samples for Gremlin](../../../graph/cli-samples.md)
- [CLI Samples for API for MongoDB](../../../mongodb/cli-samples.md)
- [CLI Samples for SQL](../../../sql/cli-samples.md)
- [CLI Samples for Table](../../../table/cli-samples.md)
