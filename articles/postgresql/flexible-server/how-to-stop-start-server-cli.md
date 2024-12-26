---
title: Stop/start - Azure CLI
description: This article describes how to stop/start operations in Azure Database for PostgreSQL - Flexible Server through the Azure CLI.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Stop/Start an instance of Azure Database for PostgreSQL flexible server using Azure CLI

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article shows you how to perform restart, start and stop Azure Database for PostgreSQL flexible server using Azure CLI.

## Prerequisites

- If you don't have an Azure subscription, create a [free](https://azure.microsoft.com/free/) account before you begin.
- Install or upgrade Azure CLI to the latest version. See [Install Azure CLI](/cli/azure/install-azure-cli).
-  Log in to Azure account using [az login](/cli/azure/reference-index#az-login) command. Note the **id** property, which refers to **Subscription ID** for your Azure account.

    ```azurecli-interactive
    az login
    ````

- If you have multiple subscriptions, choose the appropriate subscription in which you want to create the server using the `az account set` command.
`
    ```azurecli
    az account set --subscription <subscription id>
    ```

- Create an Azure Database for PostgreSQL flexible server instance if you haven't already created one using the `az postgres flexible-server create` command.

    ```azurecli
    az postgres flexible-server create --resource-group myresourcegroup --name myservername
    ```

## Stop a running server
To stop a server, run  `az postgres flexible-server stop` command. If you're using [local context](/cli/azure/config/param-persist), you don't need to provide any arguments.

**Usage:**
```azurecli
az postgres flexible-server stop  [--name]
                               [--resource-group]
                               [--subscription]
```

**Example without local context:**
```azurecli
az postgres flexible-server stop  --resource-group resourcegroupname --name myservername
```

**Example with local context:**
```azurecli
az postgres flexible-server stop
```

## Start a stopped server
To start a server, run  `az postgres flexible-server start` command. If you're using [local context](/cli/azure/config/param-persist), you don't need to provide any arguments.

**Usage:**
```azurecli
az postgres flexible-server start [--name]
                               [--resource-group]
                               [--subscription]
```

**Example without local context:**
```azurecli
az postgres flexible-server start  --resource-group --name myservername
```

**Example with local context:**
```azurecli
az postgres flexible-server start
```

> [!IMPORTANT]
> Once the server has restarted successfully, all management operations are now available for the Azure Database for PostgreSQL flexible server instance.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Restart an instance of Azure Database for PostgreSQL flexible server](how-to-restart-server-portal.md).
- [Enable, list and download server logs in Azure Database for PostgreSQL - Flexible Server](how-to-server-logs-portal.md).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
