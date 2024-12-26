---
title: CLI Script - Create and Manage Read Replicas
description: This Azure CLI sample script shows how to create and manage read replicas in Azure Database for MySQL - Flexible Server.
author: shreyaaithal
ms.author: shaithal
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: sample
ms.custom:
  - mvc
  - devx-track-azurecli
ms.devlang: azurecli
---

# Create and manage read replicas in Azure Database for MySQL - Flexible Server using Azure CLI

This sample CLI script creates and manages [read replicas](../concepts-read-replicas.md) in an Azure Database for MySQL - Flexible Server.

> [!IMPORTANT]  
> When you create a replica for a source that has no existing replicas, the source will first restart to prepare itself for replication. Take this into consideration and perform these operations during an off-peak period.

[!INCLUDE [quickstarts-free-trial-note](../../includes/flexible-server-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/mysql/flexible-server/read-replicas/create-manage-read-replicas.sh" id="FullScript":::

## Clean up resources

[!INCLUDE [cli-clean-up-resources.md](~/reusable-content/ce-skilling/azure/includes/cli-clean-up-resources.md)]

```azurecli
az group delete --name $resourceGroup
```

## Sample reference

This script uses the following commands. Each command in the table links to command specific documentation.

| **Command** | **Notes** |
| --- | --- |
| [az group create](/cli/azure/group#az-group-create) | Creates a resource group in which all resources are stored |
| [az mysql flexible-server create](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-create) | Creates a Flexible Server that hosts the databases. |
| [az mysql flexible-server replica create](/cli/azure/mysql/flexible-server/replica#az-mysql-flexible-server-replica-create) | Create a read replica for a server. |
| [az mysql flexible-server replica list](/cli/azure/mysql/flexible-server/replica#az-mysql-flexible-server-replica-list) | List all read replicas for a given server. |
| [az mysql flexible-server replica stop-replication](/cli/azure/mysql/flexible-server/replica#az-mysql-flexible-server-replica-stop-replication) | Stop replication to a read replica and make it a read/write server. |
| [az mysql flexible-server delete](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-delete) | Deletes a Flexible Server. |
| [az group delete](/cli/azure/group#az-group-delete) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI samples for Azure Database for MySQL - Flexible Server](../sample-scripts-azure-cli.md)
- [Azure CLI documentation](/cli/azure)
