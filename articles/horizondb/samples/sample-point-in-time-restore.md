---
title: Azure CLI Script - Restore in Azure HorizonDB
description: This sample Azure CLI script shows how to restore an Azure HorizonDB instance and its databases to a previous point in time.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: "azurecli"
---

# Restore an Azure HorizonDB instance using Azure CLI in Azure HorizonDB

This sample CLI script restores a single Azure HorizonDB instance to a previous point in time.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-run-local-sign-in.md](../../../includes/cli-run-local-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/postgresql/backup-restore/backup-restore.sh" id="FullScript":::

## Clean up deployment

[!INCLUDE [cli-clean-up-resources.md](~/reusable-content/ce-skilling/azure/includes/cli-clean-up-resources.md)]

```azurecli
az group delete --name $resourceGroup
```

## Sample reference

This script uses the commands outlined in the following table:

| **Command** | **Notes** |
| --- | --- |
| [az group create](/cli/azure/group) | Creates a resource group in which all resources are stored. |
| [az postgresql server create](/cli/azure/postgres/server#az-postgres-server-create) | Creates an Azure HorizonDB instance that hosts the databases. |
| [az postgresql server restore](/cli/azure/postgres/server#az-postgres-server-restore) | Restore a server from backup. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure HorizonDB](/azure/postgresql/single-server/sample-scripts-azure-cli)
- [Restore full backup (fast restore) in Azure HorizonDB](../backup-restore/how-to-restore-full-backup.md)
