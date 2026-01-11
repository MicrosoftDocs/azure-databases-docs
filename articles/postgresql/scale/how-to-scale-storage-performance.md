---
title: Scale Storage Performance
description: This article describes how to scale the storage performance of an Azure Database for PostgreSQL.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 12/19/2025
ms.service: azure-database-postgresql
ms.topic: how-to
# customer intent: As a user, I want to learn how to scale the storage performance of an Azure Database for PostgreSQL.
---

# Scale storage performance

This article provides step-by-step instructions to perform scaling operations on the performance aspects of the storage attached to an Azure Database for PostgreSQL flexible server.

If your server uses [Premium SSD disk](/azure/virtual-machines/disks-types#premium-ssds), you can use a performance tier higher than the original baseline to meet higher demand. The provisioned disk size sets the baseline performance tier. For more information, see [Performance tiers for managed disks](/azure/virtual-machines/disks-change-performance).

If your server uses [Premium SSD v2 disk](/azure/virtual-machines/disks-types#premium-ssd-v2), you can also adjust the IOPS and throughput of your disk independently. For more information, see [Premium SSD v2 performance](/azure/virtual-machines/disks-types#premium-ssd-v2-performance).

## Steps to scale storage performance tier (Premium SSD)

> [!IMPORTANT]  
> If you increase the performance tier of your disk, you can only decrease it to a lower tier 12 hours after the last increase. [This restriction](/azure/virtual-machines/disks-change-performance#restrictions) ensures stability and performance after any changes to your server's configuration.

Any attempt to decrease the performance tier within 12 hours of increasing it results in the following error:

```output
Code: PerformanceTierCannotBeDowngradedBefore12HoursError
Message: Unable to downgrade storage tier: A higher tier was explicitly set on the server at <mm/dd/yyyy hh:mm:ss AM|PM +00:00>. Tier can only be downgraded after 12 hours
```

### [Portal](#tab/portal-scale-storage-performance-tier-ssd)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Compute + storage**.

   :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd.png":::

1. If you want to increase the performance tier of the disk allocated to your server, expand the **Performance tier** dropdown and select the tier that suits your needs. The smallest tier that you can assign to a disk depends on the allocated size of the disk. The smallest tier is the baseline performance tier of a disk of that size. If you increase the performance tier, you increase the maximum IOPS and throughput of the disk. To learn about the baseline performance tiers set for each size of a disk, and the tiers to which you can upgrade, see [what Premium SSD disk performance tiers can be changed](/azure/virtual-machines/disks-change-performance#what-tiers-can-be-changed).

   :::image type="content" source="./media/how-to-scale-storage/storage-performance-tier-ssd.png" alt-text="Screenshot showing where to select a different storage performance tier for Premium SSD disks." lightbox="./media/how-to-scale-storage/storage-performance-tier-ssd.png":::

1. Select **Save**.

   :::image type="content" source="./media/how-to-scale-storage/save-performance-tier-ssd.png" alt-text="Screenshot showing the Save button enabled after changing performance tier for a Premium SSD disk." lightbox="./media/how-to-scale-storage/save-performance-tier-ssd.png":::

1. A notification shows that a deployment is in progress.

   :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-peformance-tier-ssd.png" alt-text="Screenshot showing a deployment is in progress to scale the performance tier of a Premium SSD disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-peformance-tier-ssd.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

   :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-peformance-tier-ssd.png" alt-text="Screenshot showing that the deployment to scale the performance tier of the Premium SSD disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-peformance-tier-ssd.png":::

### [CLI](#tab/cli-scale-storage-performance-tier-ssd)

To scale your storage and increase the performance tier of your Premium SSD disk, use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --performance-tier <performance_tier>
```

> [!NOTE]  
> Depending on how you want to configure other features of the existing server, you might need to add other parameters to the previous command.

The size of the disk determines the allowed values for the `--performance-tier` parameter.

If you provide an incorrect value to `--performance-tier`, you receive the following error with the list of allowed values:

```output
Incorrect value for --performance-tier for storage-size: <storage_size>. Allowed values : ['<performance_tier_1>', '<performance_tier_2>', ..., '<performance_tier_n>']
```

Use the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command to find the performance tier currently set for your server's storage.

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

1. Select your Azure Database for PostgreSQL.

1. In the resource menu, select **Compute + storage**.

   :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd-v2.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd-v2.png":::

1. If you want to change the IOPS assigned to the disk allocated to your server, type the desired value in the **IOPS (operations/sec)** text box. The range of IOPS that you can assign to a disk depends on the allocated size of the disk. For more information, see [Premium SSD v2 - IOPS](../configure-maintain/concepts-storage-premium-ssd-v2.md#iops).

   :::image type="content" source="./media/how-to-scale-storage/storage-iops-ssd-v2.png" alt-text="Screenshot showing where to specify a different number of IOPS for Premium SSD v2 disks." lightbox="./media/how-to-scale-storage/storage-iops-ssd-v2.png":::

1. Select **Save**.

   :::image type="content" source="./media/how-to-scale-storage/save-iops-ssd-v2.png" alt-text="Screenshot showing the Save button enabled after changing IOPS for a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/save-iops-ssd-v2.png":::

> [!IMPORTANT]  
> The operation to change the IOPS assigned to Premium SSD v2 disks is always an online operation. It doesn't cause any downtime for your server.

1. A notification shows that a deployment is in progress.

   :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-iops-ssd-v2.png" alt-text="Screenshot showing a deployment is in progress to scale the IOPS of a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-iops-ssd-v2.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

   :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-iops-ssd-v2.png" alt-text="Screenshot showing that the deployment to scale the IOPS of the Premium SSD v2 disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-iops-ssd-v2.png":::

### [CLI](#tab/cli--scale-storage-iops-ssd-v2)

To change the IOPS of your Premium SSD v2 disk, start scaling your storage by using the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --iops <iops>
```

> [!NOTE]  
> Depending on how you want to configure other features of the existing server, you might need to add other parameters to the previous command.

The size of the disk determines the allowed range of values for the `--iops` parameter.

If you provide an incorrect value for `--iops`, you get the following error with the allowed range of values:

```output
The requested value for IOPS does not fall between 3000 and <maximum_allowed_iops> operations/sec.
```

You can use the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command to find the IOPS currently set for your server's storage.

```azurecli-interactive
az postgres flexible-server show --resource-group <resource_group> --name <server> --query '{"storageType":storage.type,"iops":storage.iops}'
```

---

## Steps to scale storage throughput (Premium SSD v2)

### [Portal](#tab/portal-scale-storage-throughput-ssd-v2)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Compute + storage**.

   :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd-v2.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd-v2.png":::

1. If you want to change the throughput assigned to the disk allocated to your server, type the desired value in the **Throughput (MB/sec)** text box. The range of throughput that you can assign to a disk depends on the size of the disk and the IOPS assigned. For more information, see [Premium SSD v2 - Throughput](../configure-maintain/concepts-storage-premium-ssd-v2.md#throughput).

   :::image type="content" source="./media/how-to-scale-storage/storage-throughput-ssd-v2.png" alt-text="Screenshot showing where to specify a different number of throughput for Premium SSD v2 disks." lightbox="./media/how-to-scale-storage/storage-throughput-ssd-v2.png":::

1. Select **Save**.

   :::image type="content" source="./media/how-to-scale-storage/save-throughput-ssd-v2.png" alt-text="Screenshot showing the Save button enabled after changing throughput for a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/save-throughput-ssd-v2.png":::

> [!IMPORTANT]  
> The operation to change the throughput assigned to Premium SSD v2 disks is always an online operation. It doesn't cause any downtime for your server.

1. A notification shows that a deployment is in progress.

   :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-throughput-ssd-v2.png" alt-text="Screenshot showing a deployment is in progress to scale the throughput of a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-throughput-ssd-v2.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

   :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-throughput-ssd-v2.png" alt-text="Screenshot showing that the deployment to scale the throughput of the Premium SSD v2 disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-throughput-ssd-v2.png":::

### [CLI](#tab/cli--scale-storage-throughput-ssd-v2)

To scale your storage and change the throughput of your Premium SSD v2 disk, use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --throughput <throughput>
```

> [!NOTE]  
> Depending on how you want to configure other features of the existing server, you might need to add other parameters to the previous command.

The allowed range of values that you can pass to the `--throughput` parameter depends on the size of the disk and the IOPS configured.

If you pass an incorrect value to `--throughput`, you get the following error with the allowed range of values:

```output
The requested value for throughput does not fall between 125 and <maximum_allowed_throughput> MB/sec.
```

To find the throughput currently set for the storage of your server, use the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{"storageType":storage.type,"throughput":storage.throughput}'
```

---

## Related content

- [Scale storage size](how-to-scale-storage-size.md)
- [Storage options](../extensions/concepts-storage.md)
- [Limits in Azure Database for PostgreSQL flexible server](../configure-maintain/concepts-limits.md)
