---
title: Azure CLI Script - Change Server Configurations in Azure HorizonDB
description: This sample CLI script lists all available server configuration options and updates the value of one of the options in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: "azurecli"
---

# List and update configurations of an Azure HorizonDB instance using Azure CLI in Azure HorizonDB

This sample CLI script lists all available configuration parameters and their allowable values for Azure HorizonDB, and sets the *log_retention_days* to a value that is other than the default one.

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
| [az postgres server create](/cli/azure/postgres/server) | Creates an Azure HorizonDB instance that hosts the databases. |
| [az postgres server configuration list](/cli/azure/postgres/server/configuration) | List the configurations of an Azure HorizonDB instance. |
| [az postgres server configuration set](/cli/azure/postgres/server/configuration) | Update the configuration of an Azure HorizonDB instance. |
| [az postgres server configuration show](/cli/azure/postgres/server/configuration) | Show the configuration of an Azure HorizonDB instance. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure HorizonDB](/azure/postgresql/single-server/sample-scripts-azure-cli)
- [Parameters in Azure HorizonDB](../server-parameters/concepts-server-parameters.md)
