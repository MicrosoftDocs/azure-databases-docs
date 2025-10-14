---
title: List and Download Server Logs With Azure CLI
description: This article describes how to list and download Azure Database for MySQL - Flexible Server logs by using the Azure CLI.
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
# List and download Azure Database for MySQL - Flexible Server logs by using the Azure CLI

This article shows you how to list and download Azure Database for MySQL Flexible Server logs using Azure CLI.

## Prerequisites

This article requires that you're running the Azure CLI version 2.39.0 or later locally. To see the version installed, run the `az --version` command. If you need to install or upgrade, see [Install Azure CLI](/cli/azure/install-azure-cli).

You need to sign in to your account using the [az login](/cli/azure/reference-index#az-login) command. Note the **id** property, which refers to **Subscription ID** for your Azure account.

```azurecli-interactive
az login
```

Select the specific subscription under your account using [az account set](/cli/azure/account) command. Make a note of the **id** value from the **az login** output to use as the value for **subscription** argument in the command. If you have multiple subscriptions, choose the appropriate subscription in which the resource should be billed. To get all your subscription, use [az account list](/cli/azure/account#az-account-list).

```azurecli
az account set --subscription <subscription id>
```

## List server logs using Azure CLI

After you configure the prerequisites and connect to your subscription, run the following command to list the server logs from your Azure Database for MySQL Flexible Server instance.
Here are the details for the command output.

```azurecli
az mysql flexible-server server-logs list --resource-group <myresourcegroup> --server-name <serverlogdemo> --out <table>
```

Here are the details for the above command

| LastModifiedTime | Name | ResourceGroup | SizeInKb | TypePropertiesType | Url |
| --- | --- | --- | --- | --- | --- |
| 2022-08-01T11:09:48+00:00 | mysql-slow-serverlogdemo-2022073111.log | myresourcegroup | 10947 | `slowlog` | `https://00000000000.file.core.windows.net/0000000serverlog/`slowlog`s/mysql-slow-serverlogdemo-2022073111.log?` |
| 2022-08-02T11:10:00+00:00 | mysql-slow-serverlogdemo-2022080111.log | myresourcegroup | 10927 | `slowlog` | `https://00000000000.file.core.windows.net/0000000serverlog/`slowlog`s/mysql-slow-serverlogdemo-2022080111.log?` |
| 2022-08-03T11:10:12+00:00 | mysql-slow-serverlogdemo-2022080211.log | myresourcegroup | 10936 | `slowlog` | `https://00000000000.file.core.windows.net/0000000serverlog/`slowlog`s/mysql-slow-serverlogdemo-2022080211.log?` |
| 2022-08-03T11:12:00+00:00 | mysql-slow-serverlogdemo-2022080311.log | myresourcegroup | 8920 | `slowlog` | `https://00000000000.file.core.windows.net/0000000serverlog/`slowlog`s/mysql-slow-serverlogdemo-2022080311.log?` |

The list shows the LastModifiedTime, Name, ResourceGroup, SizeInKb, and download URL for the available server logs.
The default LastModifiedTime is set to 72 hours. To list files older than 72 hours, use the `--file-last-written <Time:HH>` flag.

```azurecli
az mysql flexible-server server-logs list --resource-group <myresourcegroup>  --server-name <serverlogdemo> --out table --file-last-written <144>
```

## Download server logs using Azure CLI

The following command downloads the preceding server logs to your current directory.

```azurecli
az mysql flexible-server server-logs download --resource-group <myresourcegroup> --server-name <serverlogdemo>  --name <mysql-slow-serverlogdemo-2022073111.log>
```

## Related content

- [article.](how-to-server-logs-portal.md)
- [Configure slow logs using Azure CLI](./tutorial-query-performance-insights.md#configure-slow-query-logs-by-using-the-azure-cli)
