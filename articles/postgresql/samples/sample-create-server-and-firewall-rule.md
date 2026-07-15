---
title: Create a Server and Configure a Firewall by Using Azure CLI in Azure Database for PostgreSQL Flexible Server
description: Azure CLI Script Sample - Creates an Azure Database for PostgreSQL flexible server and configures a server-level firewall rule.
#customer intent: As a user, I want to create an Azure Database for PostgreSQL flexible server by using Azure CLI, so that I can automate server provisioning instead of using the portal.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.devlang: azurecli
---

# Create a server and configure a firewall by using Azure CLI in Azure Database for PostgreSQL flexible server

This sample CLI script creates an Azure Database for PostgreSQL flexible server and configures a server-level firewall rule. After you run the script, you can access the Azure Database for PostgreSQL flexible server from all Azure services and the configured IP address.

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
| [az group create](/cli/azure/group) | Creates a resource group that stores all resources. |
| [az postgres server create](/cli/azure/postgres/server) | Creates an Azure Database for PostgreSQL flexible server that hosts the databases. |
| [az postgres server firewall create](/cli/azure/postgres/server/firewall-rule) | Creates a firewall rule to allow access to the server and databases under it from the entered IP address range. |
| [az group delete](/cli/azure/group) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server](../sample-scripts-azure-cli.md)
