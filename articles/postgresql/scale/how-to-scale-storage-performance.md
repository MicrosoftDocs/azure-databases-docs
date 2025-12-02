---
title: Scale storage performance
description: This article describes how to scale the storage performance of an Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to scale the storage performance of an Azure Database for PostgreSQL.
---

# Scale storage performance

This article provides step-by-step instructions to perform scaling operations of the performance related aspects of the storage attached to an Azure Database for PostgreSQL flexible server.

If your server is using [Premium SSD disk](/azure/virtual-machines/disks-types#premium-ssds), you can use a performance tier higher than the original baseline to meet higher demand. The baseline performance tier is set based on the provisioned disk size. For more information, see [Performance tiers for managed disks](/azure/virtual-machines/disks-change-performance).

If your server is using [Premium SSD v2 disk](/azure/virtual-machines/disks-types#premium-ssd-v2), you can also adjust, independently, the IOPS and throughput of your disk. For more information, see [Premium SSD v2 performance](/azure/virtual-machines/disks-types#premium-ssd-v2-performance).

## Steps to scale storage performance tier (Premium SSD)

> [!IMPORTANT]
> If you increase the performance tier of your disk, you can only decrease it to a lower tier 12 hours after the last increase. [This restriction](/azure/virtual-machines/disks-change-performance#restrictions) is in place to ensure stability and performance after any changes to your server's configuration.

Any attempt to decrease the performance tier within the 12 hours after increasing it, produces the following error:

```output
Code: PerformanceTierCannotBeDowngradedBefore12HoursError
Message: Unable to downgrade storage tier: A higher tier was explicitly set on the server at <mm/dd/yyyy hh:mm:ss AM|PM +00:00>. Tier can only be downgraded after 12 hours
```

### [Portal](#tab/portal-scale-storage-performance-tier-ssd)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd.png":::

3. If you want to increase the performance tier of the disk allocated to your server, expand the **Performance tier** drop-down and select the tier that suits your needs. Smallest tier that can be assigned to a disk, depends on the allocated size of the disk. That smallest tier is referred to as the baseline performance tier of a disk of that size. If you increase the performance tier, you're increasing the maximum IOPS and throughput of the disk. To learn about the baseline performance tiers set for each size of a disk, and the tiers to which you can upgrade, see [what Premium SSD disk performance tiers can be changed](/azure/virtual-machines/disks-change-performance#what-tiers-can-be-changed).

    :::image type="content" source="./media/how-to-scale-storage/storage-performance-tier-ssd.png" alt-text="Screenshot showing where to select a different storage performance tier for Premium SSD disks." lightbox="./media/how-to-scale-storage/storage-performance-tier-ssd.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-performance-tier-ssd.png" alt-text="Screenshot showing the Save button enabled after changing performance tier for a Premium SSD disk." lightbox="./media/how-to-scale-storage/save-performance-tier-ssd.png":::

5. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-peformance-tier-ssd.png" alt-text="Screenshot showing a deployment is in progress to scale the performance tier of a Premium SSD disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-peformance-tier-ssd.png":::

6. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-peformance-tier-ssd.png" alt-text="Screenshot showing that the deployment to scale the performance tier of the Premium SSD disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-peformance-tier-ssd.png":::

### [CLI](#tab/cli-scale-storage-performance-tier-ssd)

You can initiate the scaling of your storage, to increase the performance tier of your Premium SSD disk, via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --performance-tier <performance_tier>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The allowed values that you can pass to the `--performance-tier` parameter depend on the size of the disk.

If you pass an incorrect value to `--performance-tier`, you get the following error with the list of allowed values:

```output
Incorrect value for --performance-tier for storage-size: <storage_size>. Allowed values : ['<performance_tier_1>', '<performance_tier_2>', ..., '<performance_tier_n>']
```

You can determine the performance tier currently set for the storage of your server via the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query storage.tier
```

---

## Steps to scale storage IOPS (Premium SSD v2)

### [Portal](#tab/portal-scale-storage-iops-ssd-v2)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd-v2.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd-v2.png":::

3. If you want to change the IOPS assigned to the disk allocated to your server, type the desired value in the **IOPS (operations/sec)** text box. Range of IOPS that can be assigned to a disk, depends on the allocated size of the disk. To learn more about it, see [Premium SSD v2 - IOPS](../configure-maintain/concepts-storage-premium-ssd-v2.md#premium-ssd-v2---iops).

    :::image type="content" source="./media/how-to-scale-storage/storage-iops-ssd-v2.png" alt-text="Screenshot showing where to specify a different number of IOPS for Premium SSD v2 disks." lightbox="./media/how-to-scale-storage/storage-iops-ssd-v2.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-iops-ssd-v2.png" alt-text="Screenshot showing the Save button enabled after changing IOPS for a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/save-iops-ssd-v2.png":::

> [!IMPORTANT]
> The operation to change the IOPS assigned to Premium SSD v2 disks is always performed as an online operation, which doesn't produce any downtime of your server.

5. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-iops-ssd-v2.png" alt-text="Screenshot showing a deployment is in progress to scale the IOPS of a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-iops-ssd-v2.png":::

6. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-iops-ssd-v2.png" alt-text="Screenshot showing that the deployment to scale the IOPS of the Premium SSD v2 disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-iops-ssd-v2.png":::

### [CLI](#tab/cli--scale-storage-iops-ssd-v2)

You can initiate the scaling of your storage, to change the IOPS of your Premium SSD v2 disk, via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --iops <iops>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The allowed range of values that you can pass to the `--iops` parameter depend on the size of the disk.

If you pass an incorrect value to `--iops`, you get the following error with the allowed range of values:

```output
The requested value for IOPS does not fall between 3000 and <maximum_allowed_iops> operations/sec.
```

You can determine the IOPS currently set for the storage of your server via the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show --resource-group <resource_group> --name <server> --query '{"storageType":storage.type,"iops":storage.iops}'

```

---

## Steps to scale storage throughput (Premium SSD v2)

### [Portal](#tab/portal-scale-storage-throughput-ssd-v2)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd-v2.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd-v2.png":::

3. If you want to change the throughput assigned to the disk allocated to your server, type the desired value in the **Throughput (MB/sec)** text box. Range of throughput that can be assigned to a disk, depends on the size of the disk and the IOPS assigned. To learn more about it, see [Premium SSD v2 - Throughput](../configure-maintain/concepts-storage-premium-ssd-v2.md#premium-ssd-v2---throughput).

    :::image type="content" source="./media/how-to-scale-storage/storage-throughput-ssd-v2.png" alt-text="Screenshot showing where to specify a different number of throughput for Premium SSD v2 disks." lightbox="./media/how-to-scale-storage/storage-throughput-ssd-v2.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-throughput-ssd-v2.png" alt-text="Screenshot showing the Save button enabled after changing throughput for a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/save-throughput-ssd-v2.png":::

> [!IMPORTANT]
> The operation to change the throughput assigned to Premium SSD v2 disks is always performed as an online operation, which doesn't produce any downtime of your server.

5. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-throughput-ssd-v2.png" alt-text="Screenshot showing a deployment is in progress to scale the throughput of a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-throughput-ssd-v2.png":::

6. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-throughput-ssd-v2.png" alt-text="Screenshot showing that the deployment to scale the throughput of the Premium SSD v2 disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-throughput-ssd-v2.png":::

### [CLI](#tab/cli--scale-storage-throughput-ssd-v2)

You can initiate the scaling of your storage, to change the throughput of your Premium SSD v2 disk, via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --throughput <throughput>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The allowed range of values that you can pass to the `--throughput` parameter depend on the size of the disk and the IOPS configured.

If you pass an incorrect value to `--throughput`, you get the following error with the allowed range of values:

```output
The requested value for throughput does not fall between 125 and <maximum_allowed_throughput> MB/sec.
```

You can determine the throughput currently set for the storage of your server via the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{"storageType":storage.type,"throughput":storage.throughput}'

```

---

## Related content

- [Scale storage size](how-to-scale-storage-size.md).
- [Storage options](../extension-module/concepts-storage.md).
- [Limits in Azure Database for PostgreSQL flexible server](../configure-maintain/concepts-limits.md).
