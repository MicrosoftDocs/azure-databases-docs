---
title: Create resource lock for a Cassandra keyspace and table for Azure Cosmos DB
description: Create resource lock for a Cassandra keyspace and table for Azure Cosmos DB
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.custom: devx-track-azurecli
ms.topic: sample
ms.date: 02/21/2022
---

# Create a resource lock for Azure Cosmos DB Cassandra API keyspace and table using Azure CLI

[!INCLUDE[Cassandra](../../../includes/appliesto-cassandra.md)]

The script in this article demonstrates preventing resources from being deleted with resource locks.

> [!IMPORTANT]
>
> To create resource locks, you must have membership in the owner role in the subscription.
>
> Resource locks do not work for changes made by users connecting using any Cassandra SDK, CQL Shell, or the Azure Portal unless the Azure Cosmos DB account is first locked with the `disableKeyBasedMetadataWriteAccess` property enabled. To learn more about how to enable this property see, [Preventing changes from SDKs](../../../cassandra/security/how-to-disable-key-based-authentication.md).

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

- This article requires Azure CLI version 2.12.1 or later. Run `az --version` to find the version. If you need to install or upgrade, see [Install Azure CLI](/cli/azure/install-azure-cli). If using Azure Cloud Shell, the latest version is already installed.

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/cosmosdb/cassandra/lock.sh" id="FullScript":::

## Clean up resources

[!INCLUDE [cli-clean-up-resources.md](~/reusable-content/ce-skilling/azure/includes/cli-clean-up-resources.md)]

```azurecli
az group delete --name $resourceGroup
```

## Sample reference

This script uses the following commands. Each command in the table links to command specific documentation.

| Command | Notes |
|---|---|
| [az lock create](/cli/azure/lock#az-lock-create) | Creates a lock. |
| [az lock list](/cli/azure/lock#az-lock-list) | List lock information. |
| [az lock show](/cli/azure/lock#az-lock-show) | Show properties of a lock. |
| [az lock delete](/cli/azure/lock#az-lock-delete) | Deletes a lock. |

## Next steps

- [Lock resources to prevent unexpected changes](/azure/azure-resource-manager/management/lock-resources)

- [Azure Cosmos DB CLI documentation](/cli/azure/cosmosdb).

- [Azure Cosmos DB CLI GitHub Repository](https://github.com/Azure-Samples/azure-cli-samples/tree/master/cosmosdb).
