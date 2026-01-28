---
title: CLI Script - Create a Virtual Network Rule
description: This sample CLI script creates an Azure Database for PostgreSQL flexible server instance with a service endpoint on a virtual network and configures a virtual network rule.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/06/2025
ms.service: azure-database-postgresql
ms.subservice: development
ms.topic: how-to
ms.custom:
  - mvc
  - devx-track-azurecli
ms.devlang: azurecli
---

# Create an Azure Database for PostgreSQL flexible server instance and configure a virtual network rule using the Azure CLI

This sample CLI script creates an Azure Database for PostgreSQL flexible server instance and configures a virtual network rule.

[!INCLUDE [quickstarts-free-trial-note](~/reusable-content/ce-skilling/azure/includes/quickstarts-free-trial-note.md)]

[!INCLUDE [azure-cli-prepare-your-environment.md](~/reusable-content/azure-cli/azure-cli-prepare-your-environment.md)]

## Sample script

[!INCLUDE [cli-launch-cloud-shell-sign-in.md](~/reusable-content/ce-skilling/azure/includes/cli-launch-cloud-shell-sign-in.md)]

### Run the script

:::code language="azurecli" source="~/azure_cli_scripts/postgresql/create-postgresql-server-vnet/create-postgresql-server.sh" id="FullScript":::

## Clean up resources

[!INCLUDE [cli-clean-up-resources.md](~/reusable-content/ce-skilling/azure/includes/cli-clean-up-resources.md)]

```azurecli
az group delete --name $resourceGroup
```

## Sample reference

This script uses the commands outlined in the following table:

| **Command** | **Notes** |
| --- | --- |
| [az group create](/cli/azure/group#az-group-create) | Creates a resource group in which all resources are stored. |
| [az postgresql server create](/cli/azure/postgres/server/vnet-rule#az-postgres-server-vnet-rule-create) | Creates an Azure Database for PostgreSQL flexible server instance that hosts the databases. |
| [az network virtual network list-endpoint-services](/cli/azure/network/vnet#az-network-vnet-list-endpoint-services#az-network-vnet-list-endpoint-services) | Lists which services support virtual network service tunneling in a given region. |
| [az network virtual network create](/cli/azure/network/vnet#az-network-vnet-create) | Creates a virtual network. |
| [az network virtual network subnet create](/cli/azure/network/vnet#az-network-vnet-subnet-create) | Creates a subnet and associates an existing NSG and route table. |
| [az network virtual network subnet show](/cli/azure/network/vnet#az-network-vnet-subnet-show) | Shows details of a subnet. |
| [az postgresql server vnet-rule create](/cli/azure/postgres/server/vnet-rule#az-postgres-server-vnet-rule-create) | Creates a virtual network rule to allow access to an Azure Database for PostgreSQL flexible server instance. |
| [az group delete](/cli/azure/group#az-group-delete) | Deletes a resource group including all nested resources. |

## Related content

- [Azure CLI documentation](/cli/azure)
- [Azure CLI samples for Azure Database for PostgreSQL flexible server](../sample-scripts-azure-cli.md)
