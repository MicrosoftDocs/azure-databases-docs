---
title: Azure CLI Script - Create
description: Azure CLI Script Sample - Creates an Azure Database for PostgreSQL flexible server instance and configures a server-level firewall rule.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/06/2025
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: azurecli
---

# Create an Azure Database for PostgreSQL flexible server instance and configure a firewall rule using the Azure CLI

This sample CLI script creates an Azure Database for PostgreSQL flexible server instance and configures a server-level firewall rule. Once the script has been successfully run, the Azure Database for PostgreSQL flexible server instance can be accessed from all Azure services and the configured IP address.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/postgresql/create-postgresql-server-and-firewall-rule/create-postgresql-server-and-firewall-rule.sh" id="FullScript":::

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
| [az postgres server firewall create](/cli/azure/postgres/server/firewall-rule) | Creates a firewall rule to allow access to the server and databases under it from the entered IP address range. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server](../sample-scripts-azure-cli.md)
