---
title: Manage Zone Redundant high-availability - Azure CLI
description: This article describes how to configure zone redundant high-availability in Azure Database for MySQL - Flexible Server by using the Azure CLI.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 08/11/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - references_regions
  - devx-track-azurecli
---

# Manage zone redundant high-availability in Azure Database for MySQL with Azure CLI

This article describes how to enable or disable zone redundant high-availability configuration when you create a server in your Azure Database for MySQL flexible server instance. You can also disable zone redundant high-availability after server creation. Enabling zone redundant high-availability after server creation isn't supported.

The high-availability feature provisions physically separate primary and standby replicas in different zones. For more information, see [high-availability concepts documentation](concepts-high-availability.md). Enabling or disabling high-availability doesn't change your other settings, including virtual network configuration, firewall settings, and backup retention. Disabling high-availability doesn't impact your application connectivity and operations.

> [!IMPORTANT]  
> Zone redundant high-availability is available in a limited [set of regions](./overview.md#azure-regions).

## Prerequisites

- An Azure account with an active subscription.

    [!INCLUDE [flexible-server-free-trial-note](../includes/flexible-server-free-trial-note.md)]

- Install or upgrade Azure CLI to the latest version. See [Install Azure CLI](/cli/azure/install-azure-cli).

- Sign in to your Azure account with [az login](/cli/azure/reference-index#az-login). Note the **id** property, which refers to the **Subscription ID** for your Azure account.

    ```azurecli-interactive
    az login
    ````

- If you have multiple subscriptions, choose the appropriate subscription in which you want to create the Azure Database for MySQL flexible server instance by using the `az account set` command.

    ```azurecli
    az account set --subscription <subscription id>
    ```

## Enable high-availability during server creation

You can only create an Azure Database for MySQL flexible server instance with high-availability by using the General Purpose or Memory-Optimized pricing tiers. You can enable zone redundant high-availability for a server only during creation.

**Usage:**

   ```azurecli
    az mysql flexible-server create [--high-availability {Disabled, SameZone, ZoneRedundant}]
                                    [--sku-name]
                                    [--tier]
                                    [--resource-group]
                                    [--location]
                                    [--name]
   ```

**Example:**

   ```azurecli
  
        az mysql flexible-server create \
          --name myservername \
          --sku-name Standard_D2ds_v4 \
          --tier GeneralPurpose \
          --resource-group myresourcegroup \
          --high-availability ZoneRedundant \
          --location eastus
   ```

## Disable high-availability

You can disable high-availability by using the [az mysql flexible-server update](/cli/azure/mysql/flexible-server#az-mysql-flexible-server-update) command. You can disable high-availability only if the server was created with high-availability.

```azurecli
az mysql flexible-server update [--high-availability {Disabled, SameZone, ZoneRedundant}]
                                [--resource-group]
                                [--name]
```
> [!NOTE]  
> To move from `ZoneRedundant` to `SameZone`, first disable high-availability, then enable same zone.

**Example:**

   ```azurecli
   
        az mysql flexible-server update \
          --resource-group myresourcegroup \
          --name myservername \
          --high-availability Disabled
   ```

## Related content

- [business continuity](concepts-business-continuity.md)
- [zone redundant high-availability](concepts-high-availability.md)
