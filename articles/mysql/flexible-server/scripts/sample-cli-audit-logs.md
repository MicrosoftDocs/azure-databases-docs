---
title: CLI Script - Configure Audit Logs
description: This Azure CLI sample script shows how to configure audit logs on Azure Database for MySQL - Flexible Server.
author: VandhanaMehta
ms.author: vamehta
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

# Configure audit logs on Azure Database for MySQL - Flexible Server using Azure CLI

This sample CLI script enables [audit logs](../concepts-audit-logs.md) on an Azure Database for MySQL - Flexible Server.

[!INCLUDE [quickstarts-free-trial-note](../../includes/flexible-server-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

- This article requires version 2.0 or later of the Azure CLI. If using Azure Cloud Shell, the latest version is already installed.

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/mysql/flexible-server/configure-logs/configure-audit-logs.sh" id="FullScript":::

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
| [az mysql flexible-server parameter set](/cli/azure/mysql/flexible-server/parameter#az-mysql-flexible-server-parameter-set) | Updates the parameter of a flexible server. |
| [az mysql flexible-server delete](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-delete) | Deletes a Flexible Server. |
| [az group delete](/cli/azure/group#az-group-delete) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI samples for Azure Database for MySQL - Flexible Server](../sample-scripts-azure-cli.md)
- [Azure CLI documentation](/cli/azure)
