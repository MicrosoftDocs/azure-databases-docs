---
title: Restore with Azure CLI
description: This article describes how to perform restore operations in Azure Database for PostgreSQL - Flexible Server through the Azure CLI.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Point-in-time restore of an Azure Database for PostgreSQL - Flexible Server instance with Azure CLI


[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]


This article provides step-by-step procedure to perform point-in-time recoveries in Azure Database for PostgreSQL flexible server using backups.

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

## Restore a server from backup to a new server

You can run the following command to restore a server to an earliest existing backup.

**Usage**
```azurecli
az postgres flexible-server restore --restore-time
                                 --source-server
                                 [--ids]
                                 [--location]
                                 [--name]
                                 [--no-wait]
                                 [--resource-group]
                                 [--subscription]
```

**Example:**
Restore a server from this ```2021-03-03T13:10:00Z``` backup snapshot (ISO8601 format).
`--restore-time` is an optional parameter whose default corresponds to current date and time.

```azurecli
az postgres flexible-server restore \
--name mydemoserver-restored \
--resource-group myresourcegroup \
--restore-time "2021-05-05T13:10:00Z" \
--source-server mydemoserver
```

Time taken to restore will depend on the size of the data stored in the server.

## Geo-Restore a server from geo-backup to a new server

You can run the following command to restore a server to an earliest existing backup.

**Usage**
```azurecli
az postgres flexible-server geo-restore --source-server
                                 --location
                                 [--name]
                                 [--no-wait]
                                 [--resource-group]
                                 [--subscription]
                                 
```
**Example:** To perform a geo-restore of a source server 'mydemoserver' which is located in region East US to a new server 'mydemoserver-restored' in its geo-paired location West US with the same network setting you can run following command.

```azurecli
az postgres flexible-server geo-restore \
--name mydemoserver-restored \
--resource-group myresourcegroup \
--location "West US" \
--source-server mydemoserver
```

## Perform post-restore tasks
After the restore is completed, you should perform the following tasks to get your users and applications back up and running:

- If the new server is meant to replace the original server, redirect clients and client applications to the new server.
- Ensure appropriate VNet rules are in place for users to connect. These rules aren't copied over from the original server.
- Ensure appropriate logins and database level permissions are in place.
- Configure alerts as appropriate for the newly restore server.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).