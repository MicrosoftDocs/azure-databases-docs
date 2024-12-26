---
title: Restart - Azure CLI
description: This article describes how to restart operations in Azure Database for PostgreSQL - Flexible Server through the Azure CLI.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Restart an instance of Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article shows you how to perform restart, start and stop an Azure Database for PostgreSQL flexible server instance using Azure CLI.

## Prerequisites

- If you don't have an Azure subscription, create a [free](https://azure.microsoft.com/free/) account before you begin.
- Install or upgrade Azure CLI to the latest version. See [Install Azure CLI](/cli/azure/install-azure-cli).
-  Login to Azure account using [az login](/cli/azure/reference-index#az-login) command. Note the **id** property, which refers to **Subscription ID** for your Azure account.

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

## Restart a server
To restart a server, run the ```az postgres flexible-server restart``` command. If you're using [local context](/cli/azure/config/param-persist), you don't need to provide any arguments.

**Usage:**
```azurecli
az postgres flexible-server restart [--name]
                                 [--resource-group]
                                 [--subscription]
```

**Example without local context:**
```azurecli
az postgres flexible-server restart  --resource-group --name myservername
```

**Example with local context:**
```azurecli
az postgres flexible-server restart
```

> [!IMPORTANT]
> Once the server has restarted successfully, all management operations are now available for the Azure Database for PostgreSQL flexible server instance.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Stop/Start an instance of Azure Database for PostgreSQL flexible server](how-to-stop-start-server-portal.md).
- [Enable, list and download server logs in Azure Database for PostgreSQL - Flexible Server](how-to-server-logs-portal.md).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
