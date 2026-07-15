---
title: Scale Storage Size in Azure Database for PostgreSQL Flexible Server
description: This article describes how to scale the storage size of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to increase the storage size of my Azure Database for PostgreSQL flexible server, so that my server has enough space for growing data.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: scale-out
ms.topic: how-to
---

# Scale storage size in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to increase the size allocated to the storage of an Azure Database for PostgreSQL flexible server.

To configure your server so that the storage grows automatically when it's running out of available space, see [storage autogrow](how-to-auto-grow-storage.md).

Whether you use the manual or automatic approach, you can only increase the size of the storage assigned to your Azure Database for PostgreSQL flexible server. Decreasing the size of the storage isn't supported.

If your server uses [Premium SSD disk](/azure/virtual-machines/disks-types#premium-ssds), you can also use a performance tier that's higher than the original baseline to meet higher demand. The baseline performance tier is set based on the provisioned disk size. For more information, see [Performance tiers for managed disks](/azure/virtual-machines/disks-change-performance).

If your server uses [Premium SSD v2 disk](/azure/virtual-machines/disks-types#premium-ssd-v2), you can also adjust, independently, the IOPS and throughput of your disk. For more information, see [Premium SSD v2 performance](/azure/virtual-machines/disks-types#premium-ssd-v2-performance).

To configure the performance-related aspects of storage, see [scale storage performance](how-to-scale-storage-performance.md).

## Steps to scale storage size (Premium SSD)

### [Portal](#tab/portal-scale-storage-size-ssd)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd.png":::

1. If you want to increase the size of the disk allocated to your server, expand the **Storage size** dropdown and select the size you want. The smallest size that you can assign to a disk is 32 GiB. Each value in the list is double the previous one. The first value shown in the list corresponds to the current disk size. The list doesn't show values smaller than the current size, because reducing the size of the disk assigned to a server isn't supported.

    :::image type="content" source="./media/how-to-scale-storage/storage-size-ssd.png" alt-text="Screenshot showing where to select a different storage size for Premium SSD disks." lightbox="./media/how-to-scale-storage/storage-size-ssd.png":::

1. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-size-ssd.png" alt-text="Screenshot showing the Save button enabled after changing disk size for a Premium SSD disk." lightbox="./media/how-to-scale-storage/save-size-ssd.png":::

1. If you grow the disk from any size between 32 GiB and 4 TiB, to any other size in the same range, the operation is performed without causing any server downtime. It's also the case if you grow the disk from any size between 8 TiB and 32 TiB. In all those cases, the operation is performed while the server is online. However, if you increase the size of disk from any value lower or equal to 4096 GiB, to any size higher than 4096 GiB, a server restart is required. In that case, you need to confirm that you understand the consequences of performing the operation.

    :::image type="content" source="./media/how-to-scale-storage/confirmation-ssd.png" alt-text="Screenshot showing the confirmation dialog displayed when a Premium SSD disk is grown from a size smaller to 4 TiB to a size larger than 4 TiB." lightbox="./media/how-to-scale-storage/confirmation-ssd.png":::

    > [!IMPORTANT]
    > Setting the size of the disk from the Azure portal to any size higher than 4 TiB disables disk caching.
    
1. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification.png" alt-text="Screenshot showing a deployment is in progress to scale the size of a Premium SSD disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification.png" alt-text="Screenshot showing that the deployment to scale the size of the Premium SSD disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification.png":::

### [CLI](#tab/cli-scale-storage-size-ssd)

To scale your storage and increase the size of your Premium SSD disk, use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-size <storage_size>
```

> [!NOTE]
> You might need to include other parameters with the previous command. The presence and values of these parameters depend on how you want to configure other features of the existing server.

The value you pass to the `--storage-size` parameter represents the size in GiB that you want to increase the disk to.

If you pass an incorrect value to `--storage-size`, you get the following error with the list of allowed values:

```output
Incorrect value for --storage-size : Allowed values(in GiB) : [32, 64, 128, 256, 512, 1024, 2048, 4095, 4096, 8192, 16384, 32767]
```

If you try to set `--storage-size` to a value smaller than the one currently assigned, you get the following error:

```output
Updating storage cannot be smaller than the original storage size <current_storage_size> GiB.
```

You can determine the current storage size of your server by using the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query storage.storageSizeGb
```

> [!IMPORTANT]
> Setting the size of the disk from the CLI to any size equal to or higher than 4 TiB disables disk caching.
> If the current size of the disk is lower or equal to 4,096 GiB and you increase its size to any value higher than 4,096 GiB, a server restart is required.

---

## Steps to scale storage size (Premium SSD v2)

### [Portal](#tab/portal-scale-storage-size-ssd-v2)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd-v2.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd-v2.png":::

1. To increase the size of the disk allocated to your server, enter the new size in the **Storage size (GiB)**. The smallest size that you can assign to a disk is 32 GiB. The value shown in the text box before you modify it corresponds to the current disk size. You can't set it to a value smaller than the current size, because reducing the size of the disk assigned to a server isn't supported.

    :::image type="content" source="./media/how-to-scale-storage/storage-size-ssd-v2.png" alt-text="Screenshot showing where to set a different storage size for Premium SSD v2 disks." lightbox="./media/how-to-scale-storage/storage-size-ssd-v2.png":::

1. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-size-ssd-v2.png" alt-text="Screenshot showing the Save button enabled after changing disk size for a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/save-size-ssd-v2.png":::

   > [!IMPORTANT]
   > Premium SSD v2 disks don't support host caching. For more information, see [Premium SSD v2 limitations](/azure/virtual-machines/disks-types##premium-ssd-v2-limitations).

1. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification.png" alt-text="Screenshot showing a deployment is in progress to scale the size of a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification.png" alt-text="Screenshot showing that the deployment to scale the size of the Premium SSD v2 disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification.png":::

### [CLI](#tab/cli-scale-storage-size-ssd-v2)

To scale your storage and increase the size of your Premium SSD disk, use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-size <storage_size>
```

> [!NOTE]
> You might need to include other parameters with the previous command. The presence and values of these parameters depend on how you want to configure other features of the existing server.

The value you pass to the `--storage-size` parameter represents the size in GiB that you want to increase the disk to.

If you pass a value to `--storage-size` that's outside of the allowed range, you get the following error:

```output
The requested value for storage size does not fall between <current_storage_size> and 65536 GiB.
```

If you try to set `--storage-size` to a value smaller than the one currently assigned, you get the following error:

```output
Updating storage cannot be smaller than the original storage size <current_storage_size> GiB.
```

You can determine the current storage size of your server by using the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query storage.storageSizeGb
```

---

## Related content

- [Scale storage performance](how-to-scale-storage-performance.md).
- [Storage options](../extensions/concepts-storage.md).
- [Limits in Azure Database for PostgreSQL flexible server](../configure-maintain/concepts-limits.md).
