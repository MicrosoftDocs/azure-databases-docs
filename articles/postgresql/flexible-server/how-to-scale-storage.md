---
title: Scale storage
description: Learn how to scale storage in Azure Database for PostgreSQL - Flexible Server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 01/22/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to scale the storage used by my Azure Database for PostgreSQL flexible server.
---

# Scale storage

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to perform manual scaling operations for the storage of an Azure Database for PostgreSQL flexible server.

To configure your server so that the storage grows automatically when it's running out of available space, see [Configure storage autogrow](how-to-auto-grow-storage.md).

Whether you use the manual or automatic approach, you're only allowed to increase the size of the storage assigned to your Azure Database for PostgreSQL flexible server. Decreasing the size of the storage isn't supported.

If your server is using [Premium SSD disk](/virtual-machines/disks-types#premium-ssds), you can also use a performance tier higher than the original baseline to meet higher demand. The baseline performance tier is set based on the provisioned disk size. For more information, see [Performance tiers for managed disks](/azure/virtual-machines/disks-change-performance).

If your server is using [Premium SSD v2 disk](/virtual-machines/disks-types#premium-ssd-v2), you can also adjust, independently, the IOPS and throughput of your disk. For more information, see [Premium SSD v2 performance](/azure/virtual-machines/disks-types#premium-ssd-v2-performance).

> [!IMPORTANT]
> You can only scale down the Performance Tier of your server 12 hours after scaling up. This restriction is in place to ensure stability and performance after any changes to your server's configuration.

## Scale storage size (Premium SSD)

### [Portal](#tab/portal-scale-storage-size-ssd)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd.png":::

3. If you want to increase the size of the disk allocated to your server, expand the **Storage size** drop-down and select the required size. Smallest size that can be assigned to a disk is 32 GiB. Each value in the list is double of the previous one. The first value shown in the list corresponds to current disk size. Values smaller than current size aren't shown, because it isn't supported to reduce the size of the disk assigned to a server.

    :::image type="content" source="./media/how-to-scale-storage/storage-size-ssd.png" alt-text="Screenshot showing where to select a different storage size for Premium SSD disks." lightbox="./media/how-to-scale-storage/storage-size-ssd.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-ssd.png" alt-text="Screenshot showing the Save button enabled after changing disk size for a Premium SSD disk." lightbox="./media/how-to-scale-storage/save-ssd.png":::

5. If you grow the disk from any size between 32 GiB and 4 TiB, to any other size in the same range, the disk size increase operation occurs without causing any server downtime. That's also the case if you grow the disk from any size between 8 TiB and 32 TiB. In all those cases, the operation is performed while the server is online. However, if you increased the size of disk from any value lower or equal to 4096 GiB, to any size higher than 4096 GiB, a server restart is required. In that case, you are required to confirm that you understand the understand the consequences of performing the operation at that point in time.

    :::image type="content" source="./media/how-to-scale-storage/confirmation-ssd.png" alt-text="Screenshot showing the confirmation dialog displayed when a Premium SSD disk is grown from a size smaller to 4 TiB to a size larger than 4 TiB." lightbox="./media/how-to-scale-storage/confirmation-ssd.png":::

6. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-ssd.png" alt-text="Screenshot showing a deployment is in progress to scale the size of a Premium SSD disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-ssd.png":::

7. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-ssd.png" alt-text="Screenshot showing that the deployment to scale the size of the Premium SSD disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-ssd.png":::

### [CLI](#tab/cli-scale-storage-size-ssd)

You can initiate the scaling of your compute via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --tier <tier> --sku-name <sku_name>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The list of allowed values for the `--sku-name` parameter is dependent of the value passed to the `--tier` parameter, and of the region in which you're trying to deploy your server.

If you pass an incorrect value to `--sku-name`, you get the following error with the list of 

```output
Incorrect value for --sku-name. The SKU name does not match <tier> tier. Specify --tier if you did not. Or CLI will set GeneralPurpose as the default tier. Allowed values : ['<sku_name_1>', '<sku_name_2>', ..., 'sku_name_n']
```

---

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
