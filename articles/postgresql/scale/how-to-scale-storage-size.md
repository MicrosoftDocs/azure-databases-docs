---
title: Scale storage size
description: This article describes how to scale the storage size of an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to scale the storage size of an Azure Database for PostgreSQL.
---

# Scale storage size

This article provides step-by-step instructions to increase the size allocated to the storage of an Azure Database for PostgreSQL flexible server.

To configure your server so that the storage grows automatically when it's running out of available space, see [storage autogrow](how-to-auto-grow-storage.md).

Whether you use the manual or automatic approach, you're only allowed to increase the size of the storage assigned to your Azure Database for PostgreSQL flexible server. Decreasing the size of the storage isn't supported.

If your server is using [Premium SSD disk](/azure/virtual-machines/disks-types#premium-ssds), you can also use a performance tier higher than the original baseline to meet higher demand. The baseline performance tier is set based on the provisioned disk size. For more information, see [Performance tiers for managed disks](/azure/virtual-machines/disks-change-performance).

If your server is using [Premium SSD v2 disk](/azure/virtual-machines/disks-types#premium-ssd-v2), you can also adjust, independently, the IOPS and throughput of your disk. For more information, see [Premium SSD v2 performance](/azure/virtual-machines/disks-types#premium-ssd-v2-performance).

To configure the performance related aspects of storage, see [scale storage performance](how-to-scale-storage-performance.md).

## Steps to scale storage size (Premium SSD)

### [Portal](#tab/portal-scale-storage-size-ssd)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd.png":::

3. If you want to increase the size of the disk allocated to your server, expand the **Storage size** drop-down and select the required size. Smallest size that can be assigned to a disk is 32 GiB. Each value in the list is double of the previous one. The first value shown in the list corresponds to current disk size. Values smaller than current size aren't shown, because it isn't supported to reduce the size of the disk assigned to a server.

    :::image type="content" source="./media/how-to-scale-storage/storage-size-ssd.png" alt-text="Screenshot showing where to select a different storage size for Premium SSD disks." lightbox="./media/how-to-scale-storage/storage-size-ssd.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-size-ssd.png" alt-text="Screenshot showing the Save button enabled after changing disk size for a Premium SSD disk." lightbox="./media/how-to-scale-storage/save-size-ssd.png":::

5. If you grow the disk from any size between 32 GiB and 4 TiB, to any other size in the same range, the operation is performed without causing any server downtime. It's also the case if you grow the disk from any size between 8 TiB and 32 TiB. In all those cases, the operation is performed while the server is online. However, if you increase the size of disk from any value lower or equal to 4096 GiB, to any size higher than 4096 GiB, a server restart is required. In that case, you're required to confirm that you understand the consequences of performing the operation.

    :::image type="content" source="./media/how-to-scale-storage/confirmation-ssd.png" alt-text="Screenshot showing the confirmation dialog displayed when a Premium SSD disk is grown from a size smaller to 4 TiB to a size larger than 4 TiB." lightbox="./media/how-to-scale-storage/confirmation-ssd.png":::

> [!IMPORTANT]
> Setting the size of the disk from the Azure portal to any size higher than 4 TiB, disables disk caching.

6. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-ssd.png" alt-text="Screenshot showing a deployment is in progress to scale the size of a Premium SSD disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-ssd.png":::

7. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-ssd.png" alt-text="Screenshot showing that the deployment to scale the size of the Premium SSD disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-ssd.png":::

### [CLI](#tab/cli-scale-storage-size-ssd)

You can initiate the scaling of your storage, to increase the size of your Premium SSD disk, via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-size <storage_size>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The value passed to the `--storage-size` parameter represents the size in GiB to which you want to increase the disk.

If you pass an incorrect value to `--storage-size`, you get the following error with the list of allowed values:

```output
Incorrect value for --storage-size : Allowed values(in GiB) : [32, 64, 128, 256, 512, 1024, 2048, 4095, 4096, 8192, 16384, 32767]
```

If you pass try to set `--storage-size` to a value smaller than the one currently assigned, you get the following error:

```output
Updating storage cannot be smaller than the original storage size <current_storage_size> GiB.
```

You can determine the current storage size of your server via the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query storage.storageSizeGb
```

> [!IMPORTANT]
> Setting the size of the disk from the CLI to any size equal or higher than 4 TiB, disables disk caching.
> If the current size of the disk is lower or equal to 4,096 GiB and you increase its size to any value higher than 4096 GiB, a server restart is required.

---

## Steps to scale storage size (Premium SSD v2)

### [Portal](#tab/portal-scale-storage-size-ssd-v2)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-storage/compute-storage-ssd-v2.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-storage/compute-storage-ssd-v2.png":::

3. If you want to increase the size of the disk allocated to your server, type the desired new size in the **Storage size (in GiB)**. Smallest size that can be assigned to a disk is 32 GiB. The value shown in the text box before you modify it corresponds to current disk size. You can't set it to a value smaller than current size, because it isn't supported to reduce the size of the disk assigned to a server.

    :::image type="content" source="./media/how-to-scale-storage/storage-size-ssd-v2.png" alt-text="Screenshot showing where to set a different storage size for Premium SSD v2 disks." lightbox="./media/how-to-scale-storage/storage-size-ssd-v2.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-scale-storage/save-size-ssd-v2.png" alt-text="Screenshot showing the Save button enabled after changing disk size for a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/save-size-ssd-v2.png":::

   > [!IMPORTANT]
   > Premium SSD v2 disks don't support host caching. For more information, see [Premium SSD v2 limitations](/azure/virtual-machines/disks-types##premium-ssd-v2-limitations).
   >
   > The operation to increase the size of Premium SSD v2 disks always requires a server restart, regardless of what's the current size and what's the target size to which you're growing it.

6. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-storage/deployment-progress-notification-ssd-v2.png" alt-text="Screenshot showing a deployment is in progress to scale the size of a Premium SSD v2 disk." lightbox="./media/how-to-scale-storage/deployment-progress-notification-ssd-v2.png":::

7. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-storage/deployment-succeeded-notification-ssd-v2.png" alt-text="Screenshot showing that the deployment to scale the size of the Premium SSD v2 disk succeeded." lightbox="./media/how-to-scale-storage/deployment-succeeded-notification-ssd-v2.png":::

### [CLI](#tab/cli-scale-storage-size-ssd-v2)

You can initiate the scaling of your storage, to increase the size of your Premium SSD disk, via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-size <storage_size>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The value passed to the `--storage-size` parameter represents the size in GiB to which you want to increase the disk.

If you pass a value to `--storage-size` which is outside of the allowed range of values, you get the following error:

```output
The requested value for storage size does not fall between <current_storage_size> and 65536 GiB.
```

If you pass try to set `--storage-size` to a value smaller than the one currently assigned, you get the following error:

```output
Updating storage cannot be smaller than the original storage size <current_storage_size> GiB.
```

You can determine the current storage size of your server via the [az postgres flexible-server show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-show) command.

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
