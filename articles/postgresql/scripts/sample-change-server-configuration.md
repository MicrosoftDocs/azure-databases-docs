---
title: Azure CLI Script - Change Server Configurations
description: This sample CLI script lists all available server configuration options and updates the value of one of the options.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/06/2025
ms.service: azure-database-postgresql
ms.topic: how-to
ms.devlang: azurecli
---

# List and update configurations of an Azure Database for PostgreSQL flexible server instance using Azure CLI

[!INCLUDE [applies-to-postgresql-flexible-server](../includes/applies-to-postgresql-flexible-server.md)]

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
| [az group create](/cli/azure/group) | Creates a resource group in which all resources are stored. |
| [az postgres server create](/cli/azure/postgres/server) | Creates an Azure Database for PostgreSQL flexible server instance that hosts the databases. |
| [az postgres server configuration list](/cli/azure/postgres/server/configuration) | List the configurations of an Azure Database for PostgreSQL flexible server instance. |
| [az postgres server configuration set](/cli/azure/postgres/server/configuration) | Update the configuration of an Azure Database for PostgreSQL flexible server instance. |
| [az postgres server configuration show](/cli/azure/postgres/server/configuration) | Show the configuration of an Azure Database for PostgreSQL flexible server instance. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server](../single-server/sample-scripts-azure-cli.md)
- [How to configure server parameters in Azure portal](../flexible-server/how-to-configure-server-parameters-using-portal.md)
