---
title: Configure Storage Autogrow in Azure Database for PostgreSQL Flexible Server
description: This article describes how you can configure storage autogrow in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to enable storage autogrow on an existing Azure Database for PostgreSQL flexible server, so that my storage grows automatically without affecting the workload.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: scale-out
ms.topic: how-to
---

# Configure storage autogrow in Azure Database for PostgreSQL flexible server

This article describes how to configure Azure Database for PostgreSQL server storage to grow without affecting the workload.

For servers with more than 1 TiB of provisioned storage, the storage autogrow mechanism activates when the available space is less than 10% of the total capacity or when the available space is less than 64 GiB. The smaller of the two values determines when autogrow activates. Conversely, for servers with storage under 1 TiB, the autogrow threshold is adjusted to 20% of the total capacity or when the available space is less than 64 GiB. Again, the smaller of the two values is used.

As an illustration, take a server with a storage capacity of 2 TiB (greater than 1 TiB). In this case, the autogrow limit is set at 64 GiB. This choice is made because 64 GiB is the smaller value when compared to 10% of 2 TiB, which is roughly 204.8 GiB. In contrast, for a server with a storage size of 128 GiB (less than 1 TiB), the autogrow feature activates when there's only 25.8 GiB of space left. This activation is based on the 20% threshold of the total allocated storage (128 GiB), which is smaller than 64 GiB.

The process of scaling storage is performed online, without causing any downtime, except when the disk size needs to cross the border of 4,096 GiB. This exception is a limitation of Azure managed disks. In that case, the automatic storage scaling activity isn't triggered, even if the storage autogrow setting is enabled for the server. In such cases, you need to scale your storage manually. In this scenario (reaching or crossing the 4,096 GiB boundary), manual scaling is an offline operation. Schedule this task to align with your business needs. All other operations can be performed online. Once the allocated disk size is 8,192 GiB or higher, storage autogrow triggers again automatically and every subsequent storage grow operation is performed online until the disk allocated reaches its maximum growing capacity, which is 32,768 GiB.

> [!NOTE]
> Azure Database for PostgreSQL only supports the storage autogrow feature on storage type Premium SSD.
>
> Storage always doubles in size for premium disk SSD, and that doubling also doubles the storage cost.
>
> Only premium SSD V2 supports more granular disk size increase.

## Steps to enable storage autogrow for existing servers

### [Portal](#tab/portal-enable-existing-server)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Compute + storage**.

    :::image type="content" source="media/how-to-auto-grow-storage/compute-storage-disabled.png" alt-text="Screenshot the Compute + storage page." lightbox="media/how-to-auto-grow-storage/compute-storage-disabled.png":::

1. In the **Storage** section, select the **Storage autogrow** checkbox.

    :::image type="content" source="media/how-to-auto-grow-storage/enable-autogrow-existing-server.png" alt-text="Screenshot showing how to enable storage autogrow on an existing Azure Database for flexible server." lightbox="media/how-to-auto-grow-storage/enable-autogrow-existing-server.png":::

1. Select **Save** to apply the changes.

    :::image type="content" source="media/how-to-auto-grow-storage/enable-autogrow-existing-server-save.png" alt-text="Screenshot showing how to save changes after enabling storage autogrow on an existing Azure Database for flexible server." lightbox="media/how-to-auto-grow-storage/enable-autogrow-existing-server-save.png":::

1. A notification shows that a deployment is in progress.

   :::image type="content" source="./media/how-to-auto-grow-storage/deployment-progress-notification.png" alt-text="Screenshot showing a deployment is in progress to enable storage autogrow on an existing Azure Database for flexible server." lightbox="./media/how-to-auto-grow-storage/deployment-progress-notification.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

   :::image type="content" source="./media/how-to-auto-grow-storage/deployment-succeeded-notification.png" alt-text="Screenshot showing that the deployment to enable storage autogrow succeeded." lightbox="./media/how-to-auto-grow-storage/deployment-progress-notification.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable storage autogrow in an existing server by using the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-auto-grow enabled
```

---

## Steps to disable storage autogrow for existing servers

### [Portal](#tab/portal-disable-existing-server)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Compute + storage**.

    :::image type="content" source="media/how-to-auto-grow-storage/compute-storage-enabled.png" alt-text="Screenshot the Compute + storage page." lightbox="media/how-to-auto-grow-storage/compute-storage-enabled.png":::

1. In the **Storage** section, select the **Storage autogrow** checkbox.

    :::image type="content" source="media/how-to-auto-grow-storage/disable-autogrow-existing-server.png" alt-text="Screenshot showing how to disable storage autogrow on an existing Azure Database for flexible server." lightbox="media/how-to-auto-grow-storage/disable-autogrow-existing-server.png":::

1. Select **Save** to apply the changes.

    :::image type="content" source="media/how-to-auto-grow-storage/disable-autogrow-existing-server-save.png" alt-text="Screenshot showing how to save changes after disabling storage autogrow on an existing Azure Database for flexible server." lightbox="media/how-to-auto-grow-storage/disable-autogrow-existing-server-save.png":::

1. A notification shows that a deployment is in progress.

   :::image type="content" source="./media/how-to-auto-grow-storage/deployment-progress-notification.png" alt-text="Screenshot showing a deployment is in progress to disable storage autogrow on an existing Azure Database for flexible server." lightbox="./media/how-to-auto-grow-storage/deployment-progress-notification.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

   :::image type="content" source="./media/how-to-auto-grow-storage/deployment-succeeded-notification.png" alt-text="Screenshot showing that the deployment to disable storage autogrow succeeded." lightbox="./media/how-to-auto-grow-storage/deployment-progress-notification.png":::

### [CLI](#tab/cli-disable-existing-server)

Use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command to enable storage autogrow in an existing server.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-auto-grow disabled
```

---

## Steps to enable storage autogrow during server provisioning

### [Portal](#tab/portal-enable-new-server)

Use the [Azure portal](https://portal.azure.com/):

1. During provisioning of a new Azure Database for PostgreSQL flexible server, in the **Compute + storage** section, select **Configure server**.

    :::image type="content" source="media/how-to-auto-grow-storage/create-server-storage-auto-grow.png" alt-text="Screenshot showing how to configure server compute and storage during provisioning of a new Azure Database for flexible server." lightbox="media/how-to-auto-grow-storage/create-server-storage-auto-grow.png":::

1. In the **Storage** section, select the **Storage autogrow** checkbox.

    :::image type="content" source="media/how-to-auto-grow-storage/server-provisioning-storage-auto-grow.png" alt-text="Screenshot showing how to enable storage autogrow during provisioning of a new Azure Database for flexible server." lightbox="media/how-to-auto-grow-storage/server-provisioning-storage-auto-grow.png":::

### [CLI](#tab/cli-enable-new-server)

Use the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command to enable storage autogrow while provisioning a new server.

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --storage-auto-grow disabled ...
```

> [!NOTE]
> You need to provide other parameters to complete the previous command. The presence and values of these parameters vary depending on how you want to configure other features of the provisioned server.

---

## Limitations and considerations

- Autogrow activates when available space is less than 10% of total provisioned storage or 64 GiB, whichever is smaller.

- The autogrow feature only supports scaling up. It doesn't reduce storage size automatically.

## Frequently asked questions (FAQ)

**Q. Does autogrow work with high WAL usage?  

A. No, it doesn't trigger in that case.

**Q. Does autogrow cause downtime?**  
A. No, it relies on online disk scaling.

## Related content

- [Scale storage performance](how-to-scale-storage-performance.md)
- [Storage options](../extensions/concepts-storage.md)
- [Limits in Azure Database for PostgreSQL](../configure-maintain/concepts-limits.md)
