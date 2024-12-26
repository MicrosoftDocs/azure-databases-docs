---
title: CLI Script - Create and Enable Public Access Connectivity
description: This Azure CLI sample script shows how to create a Azure Database for MySQL - Flexible Server instance, configure a server-level firewall rule (public access connectivity method), and connect to the server.
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

# Create an Azure Database for MySQL - Flexible Server instance and enable public access connectivity using Azure CLI

This sample CLI script creates an Azure Database for MySQL - Flexible Server, configures a server-level firewall rule ([public access connectivity method](../concepts-networking-public.md)) and connects to the server after creation.

Once the script runs successfully, the MySQL Flexible Server will be accessible by all Azure services and the configured IP address, and you will be connected to the server in an interactive mode.

> [!NOTE]  
> The connectivity method cannot be changed after creating the server. For example, if you create server using *Public access (allowed IP addresses)*, you cannot change to *Private access (VNet Integration)* after creation. To learn more about connectivity methods, see [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](../concepts-networking.md).

[!INCLUDE [quickstarts-free-trial-note](../../includes/flexible-server-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/mysql/flexible-server/create-server-public-access/create-connect-burstable-server-public-access.sh" id="FullScript":::

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
| [az mysql flexible-server firewall-rule create](/cli/azure/mysql/flexible-server/firewall-rule#az-mysql-flexible-server-firewall-rule-create) | Creates a firewall rule to allow access to the Flexible Server and its databases from the entered IP address range. |
| [az mysql flexible-server connect](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-connect) | Connects to a Flexible Server to perform server or database operations. |
| [az mysql flexible-server delete](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-delete) | Deletes a Flexible Server. |
| [az group delete](/cli/azure/group#az-group-delete) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI samples for Azure Database for MySQL - Flexible Server](../sample-scripts-azure-cli.md)
- [Azure CLI documentation](/cli/azure)
