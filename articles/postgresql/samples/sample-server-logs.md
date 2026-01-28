---
title: Azure CLI Script - Download Server Logs
description: This sample Azure CLI script shows how to enable and download the server logs of an Azure Database for PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/06/2025
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: azurecli
---

# Enable and download server slow query logs of an Azure Database for PostgreSQL flexible server instance using Azure CLI

This sample CLI script enables and downloads the slow query logs of a single Azure Database for PostgreSQL flexible server instance.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/postgresql/server-logs/server-logs.sh" id="FullScript":::

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
| [az postgres server create](/cli/azure/postgres/server) | Creates an Azure Database for PostgreSQL flexible server instance that hosts the databases. |
| [az postgres server configuration list](/cli/azure/postgres/server/configuration) | Lists the configuration values for a server. |
| [az postgres server configuration set](/cli/azure/postgres/server/configuration) | Updates the configuration of a server. |
| [az postgres server-logs list](/cli/azure/postgres/server-logs) | Lists log files for a server. |
| [az postgres server-logs download](/cli/azure/postgres/server-logs) | Downloads log files. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server instance](../sample-scripts-azure-cli.md)
- [Configure and access server logs in the Azure portal](../howto-configure-server-logs-in-portal.md)
