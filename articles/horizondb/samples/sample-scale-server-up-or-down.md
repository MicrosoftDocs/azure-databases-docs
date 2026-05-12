---
title: Azure CLI Script - Scale and Monitor in Azure HorizonDB
description: Azure CLI Script Sample - Scale to a different performance level after querying the metrics in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: "azurecli"
---
# Monitor and scale a single Azure HorizonDB instance using Azure CLI in Azure HorizonDB

This sample CLI script scales compute and storage for a single Azure HorizonDB instance after querying the metrics. Compute can scale up or down. Storage can only scale up.

> [!IMPORTANT]  
> Storage can only be scaled up, not down.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/postgresql/scale-postgresql-server/scale-postgresql-server.sh" id="FullScript":::

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
| [az postgres server create](/cli/azure/postgres/server#az-postgres-server-create) | Creates an Azure HorizonDB instance that hosts the databases. |
| [az postgres server update](/cli/azure/postgres/server#az-postgres-server-update) | Updates properties of the Azure HorizonDB instance. |
| [az monitor metrics list](/cli/azure/monitor/metrics) | Lists the metric value for the resources. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure HorizonDB compute and storage](/azure/postgresql/single-server/concepts-pricing-tiers)
- [Azure CLI samples for Azure HorizonDB](/azure/postgresql/single-server/sample-scripts-azure-cli)
- [Azure CLI](/cli/azure)
