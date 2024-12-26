---
title: Restore a Server With Azure CLI
description: This article describes how to perform restore operations in Azure Database for MySQL - Flexible Server through the Azure CLI.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
---

# Point-in-time restore in Azure Database for MySQL - Flexible Server with Azure CLI

This article provides step-by-step procedure to perform point-in-time recoveries in Azure Database for MySQL Flexible Server using backups.

## Prerequisites

- An Azure account with an active subscription.

[!INCLUDE [flexible-server-free-trial-note](../includes/flexible-server-free-trial-note.md)]

- Install or upgrade Azure CLI to the latest version. See [Install Azure CLI](/cli/azure/install-azure-cli).

- Login to Azure account using [az login](/cli/azure/reference-index#az-login) command. Note the **id** property, which refers to **Subscription ID** for your Azure account.

    ```azurecli-interactive
    az login
    ````

- If you have multiple subscriptions, choose the appropriate subscription in which you want to create the server using the `az account set` command.
`

    ```azurecli
    az account set --subscription <subscription id>
    ```

- Create an Azure Database for MySQL Flexible Server instance if you haven't already created one by using the `az mysql flexible-server create` command.

    ```azurecli
    az mysql flexible-server create --resource-group myresourcegroup --name myservername
    ```

## Restore a server from backup to a new server

You can run the following command to restore a server to an earliest existing backup.

**Usage**

```azurecli
az mysql flexible-server restore --restore-time
                                 --source-server
                                 [--ids]
                                 [--location]
                                 [--name]
                                 [--no-wait]
                                 [--resource-group]
                                 [--subscription]
```

**Example:**
Restore a server from this ```2021-03-03T13:10:00Z``` backup snapshot.

```azurecli
az mysql flexible-server restore \
--name mydemoserver-restored \
--resource-group myresourcegroup \
--restore-time "2021-03-03T13:10:00Z" \
--source-server mydemoserver
```

Time taken to restore will depend on the size of the data stored in the server.

## Geo-Restore a server from geo-backup to a new server

You can run the following command to geo-restore a server to the most recent backup available.

**Usage**

```azurecli
az mysql flexible-server geo-restore --source-server
                                 --location
                                 [--name]
                                 [--no-wait]
                                 [--resource-group]
                                 [--subscription]
```

**Example:**
Geo-restore 'mydemoserver' in region East US to a new server 'mydemoserver-restored' in its geo-paired location West US with the same network setting.

```azurecli
az mysql flexible-server geo-restore \
--name mydemoserver-restored \
--resource-group myresourcegroup \
--location "West US" \
--source-server mydemoserver
```

## Perform post-restore tasks

After the restore is completed, you should perform the following tasks to get your users and applications back up and running:

- If the new server is meant to replace the original server, redirect clients and client applications to the new server.
- Ensure appropriate VNet rules are in place for users to connect. These rules are not copied over from the original server.
- Ensure appropriate logins and database level permissions are in place.
- Configure alerts as appropriate for the newly restore server.

## Next step

> [!div class="nextstepaction"]
> [business continuity](concepts-business-continuity.md)
