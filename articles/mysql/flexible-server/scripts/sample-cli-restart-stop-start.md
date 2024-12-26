---
title: CLI Script - Restart/stop/start
description: This Azure CLI sample script shows how to restart/stop/start an Azure Database for MySQL - Flexible Server instance.
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

# Restart/stop/start an Azure Database for MySQL - Flexible Server instance using Azure CLI

This sample CLI script performs restart, start and stop operations on an Azure Database for MySQL - Flexible Server.

> [!IMPORTANT]  
> When you **Stop** the server it remains in that state for the next 30 days in a stretch. If you do not manually **Start** it during this time, the server will automatically be started at the end of 30 days. You can chose to **Stop** it again if you are not using the server.

During the time server is stopped, no management operations can be performed on the server. In order to change any configuration settings on the server, you will need to start the server.

Also, see [stop/start limitations](../concepts-limitations.md#stopstart-operations) before performing stop/start operations.

[!INCLUDE [quickstarts-free-trial-note](../../includes/flexible-server-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/mysql/flexible-server/manage-server/restart-start-stop.sh" id="FullScript":::

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
| [az mysql flexible-server stop](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-stop) | Stops a Flexible Server. |
| [az mysql flexible-server start](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-start) | Starts a Flexible Server. |
| [az mysql flexible-server restart](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-restart) | Restarts a Flexible Server. |
| [az mysql flexible-server delete](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-delete) | Deletes a Flexible Server. |
| [az group delete](/cli/azure/group#az-group-delete) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI samples for Azure Database for MySQL - Flexible Server](../sample-scripts-azure-cli.md)
- [Azure CLI documentation](/cli/azure)
