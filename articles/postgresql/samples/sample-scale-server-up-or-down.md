---
title: Monitor and Scale a Server by Using Azure CLI in Azure Database for PostgreSQL Flexible Server
description: Azure CLI Script Sample - Scale an Azure Database for PostgreSQL flexible server to a different performance level after querying the metrics.
#customer intent: As a user, I want to scale the compute of my PostgreSQL flexible server by using Azure CLI, so that I can match performance to my workload demands.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: azurecli
---
# Monitor and scale a server by using Azure CLI in Azure Database for PostgreSQL flexible server

This sample CLI script scales compute and storage for a single Azure Database for PostgreSQL flexible server after querying the metrics. You can scale compute up or down. You can only scale storage up.

> [!IMPORTANT]  
> You can only scale storage up, not down.

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
| [az group create](/cli/azure/group) | Creates a resource group that stores all resources. |
| [az postgres server create](/cli/azure/postgres/server#az-postgres-server-create) | Creates an Azure Database for PostgreSQL flexible server that hosts the databases. |
| [az postgres server update](/cli/azure/postgres/server#az-postgres-server-update) | Updates properties of the Azure Database for PostgreSQL flexible server. |
| [az monitor metrics list](/cli/azure/monitor/metrics) | Lists the metric value for the resources. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure Database for PostgreSQL flexible server compute and storage](../concepts-pricing-tiers.md)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server](../sample-scripts-azure-cli.md)
- [Azure CLI](/cli/azure)
