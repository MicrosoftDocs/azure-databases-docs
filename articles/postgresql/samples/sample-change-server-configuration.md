---
title: List and Update Configurations by Using Azure CLI in Azure Database for PostgreSQL Flexible Server
description: This sample CLI script lists all available server configuration options and updates the value of one of the options.
#customer intent: As a user, I want to list all available server configuration parameters for my PostgreSQL flexible server, so that I can review which settings I can adjust.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: azurecli
---

# List and update configurations by using Azure CLI in Azure Database for PostgreSQL flexible server

This sample CLI script lists all available configuration parameters and their allowable values for Azure Database for PostgreSQL flexible server, and sets the *log_retention_days* to a value that is other than the default one.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/postgresql/change-server-configurations/change-server-configurations.sh" id="FullScript":::

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
| [az postgres server create](/cli/azure/postgres/server) | Creates an Azure Database for PostgreSQL flexible server instance that hosts the databases. |
| [az postgres server configuration list](/cli/azure/postgres/server/configuration) | Lists the configurations of an Azure Database for PostgreSQL flexible server instance. |
| [az postgres server configuration set](/cli/azure/postgres/server/configuration) | Updates the configuration of an Azure Database for PostgreSQL flexible server instance. |
| [az postgres server configuration show](/cli/azure/postgres/server/configuration) | Shows the configuration of an Azure Database for PostgreSQL flexible server instance. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server](../single-server/sample-scripts-azure-cli.md)
- [How to configure parameters in Azure portal](../parameters/how-to-parameters-list-all.md)
