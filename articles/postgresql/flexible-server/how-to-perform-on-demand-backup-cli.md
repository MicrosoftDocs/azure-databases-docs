---
title: On-demand-backup - Azure CLI Preview
description: This article describes how to perform on-demand backup in Azure Database for PostgreSQL - Flexible Server through Azure CLI.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 11/05/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---


# On-demand backup Azure Database for PostgreSQL - Flexible Server using Azure CLI Preview

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step procedure to perform on-demand backup of the Azure Database for PostgreSQL flexible server instance through Azure cli. The procedure is same for servers configured with zone redundant high availability. 

> [!IMPORTANT]
> On-demand backups are retained according to your configured retention window, but you can delete them earlier if they’re no longer needed.



## Prerequisites

- Make sure that Microsoft.DBforPostgreSQL/flexibleServers/backups/write permission is granted to the role performing on-demand backup. 
- If you don't have an Azure subscription, create a [free](https://azure.microsoft.com/free/) account before you begin.
- Install or upgrade Azure CLI to the latest version. See [Install Azure CLI](/cli/azure/install-azure-cli).
-  Log in to Azure account using [az login](/cli/azure/reference-index#az-login) command. 

    ```azurecli-interactive
    az login
    ````

- If you have multiple subscriptions, choose the appropriate subscription in which you want to create the server using the `az account set` command.
`
    ```azurecli
    az account set --subscription <subscription id>
    ```

## Perform On-demand backup

You can run the following command to perform on-demand backup a server.

**Usage**
```azurecli
az postgres flexible-server backup create
                                 [--source-server-name]
                                 [--resource-group]
                                 [--backup-name]
```

**Example:**
Restore a server from this ```2021-03-03T13:10:00Z``` backup snapshot (ISO8601 format).
`--restore-time` is an optional parameter whose default corresponds to current date and time.

```azurecli
az postgres flexible-server backup create --name mysourceservername --resource-group myresourcegroup --backup-name mybackupfilename
```

## Delete On-demand backup

You can run the following command to delete an on-demand backup for a server.

**Usage**
```azurecli
az postgres flexible-server backup delete
                                 [--source-server-name]
                                 [--resource-group]
                                 [--backup-name]
```


```azurecli
az postgres flexible-server backup delete --name mysourceservername --resource-group myresourcegroup --backup-name mybackupfilename
```

> [!IMPORTANT]
>You can only delete on-demand backups but not the scheduled automated backups.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).
