---
title: Configure Storage Autogrow
description: This article describes how you can configure storage autogrow in an Azure Database for PostgreSQL flexible server instance.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
# customer intent: As a user, I want to learn how to configure storage autogrow in an Azure Database for PostgreSQL flexible server instance.
---

# Configure storage autogrow

This article describes how you can configure Azure Database for PostgreSQL server storage to grow without affecting the workload.

For servers with more than 1 TiB of provisioned storage, the storage autogrow mechanism activates when the available space is less than 10% of the total capacity or when the available space is less than 64 GiB. The smaller of the two is the value that determines when autogrow activates. Conversely, for servers with storage under 1 TiB, this threshold is adjusted to 20% of the total capacity or when the available space is less than 64 GiB. Again, picking the smaller of the two values.

As an illustration, take a server with a storage capacity of 2 TiB (greater than 1 TiB). In this case, the autogrow limit is set at 64 GiB. This choice is made because 64 GiB is the smaller value when compared to 10% of 2 TiB, which is roughly 204.8 GiB. In contrast, for a server with a storage size of 128 GiB (less than 1 TiB), the autogrow feature activates when there's only 25.8 GiB of space left. This activation is based on the 20% threshold of the total allocated storage (128 GiB), which is smaller than 64 GiB.

> [!NOTE]
> Azure Database for PostgreSQL only supports the storage autogrow feature on storage type Premium SSD.
>
> Storage always doubles in size for premium disk SSD, and that doubles the storage cost.
>
> Only premium SSD V2 supports more granular disk size increase.

## Steps to enable storage autogrow for existing servers

### [Portal](#tab/portal-enable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

1. In the resource menu, under the **Settings** section, select **Compute + storage**.

    :::image type="content" source="media/how-to-auto-grow-storage/compute-storage-disabled.png" alt-text="Screenshot the Compute + storage page." lightbox="media/how-to-auto-grow-storage/compute-storage-disabled.png":::

1. In the **Storage** section, enable the **Storage autogrow** checkbox.

    :::image type="content" source="media/how-to-auto-grow-storage/enable-autogrow-existing-server.png" alt-text="Screenshot showing how to enable storage autogrow on an existing Azure Database for flexible server instance." lightbox="media/how-to-auto-grow-storage/enable-autogrow-existing-server.png":::

1. Select **Save** to apply the changes.

    :::image type="content" source="media/how-to-auto-grow-storage/enable-autogrow-existing-server-save.png" alt-text="Screenshot showing how to save changes after enabling storage autogrow on an existing Azure Database for flexible server instance." lightbox="media/how-to-auto-grow-storage/enable-autogrow-existing-server-save.png":::

1. A deployment initiates and, when it completes, a notification shows that autogrow is successfully enabled.

    :::image type="content" source="media/how-to-auto-grow-storage/notification-autogrow-existing-server.png" alt-text="Screenshot showing notification that confirms that autogrow is enabled." lightbox="media/how-to-auto-grow-storage/notification-autogrow-existing-server.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable storage autogrow in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-auto-grow enabled
```

---

## Steps to disable storage autogrow for existing servers

### [Portal](#tab/portal-disable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

1. In the resource menu, under the **Settings** section, select **Compute + storage**.

    :::image type="content" source="media/how-to-auto-grow-storage/compute-storage-enabled.png" alt-text="Screenshot the Compute + storage page." lightbox="media/how-to-auto-grow-storage/compute-storage-enabled.png":::

1. In the **Storage** section, enable the **Storage autogrow** checkbox.

    :::image type="content" source="media/how-to-auto-grow-storage/disable-autogrow-existing-server.png" alt-text="Screenshot showing how to disable storage autogrow on an existing Azure Database for flexible server instance." lightbox="media/how-to-auto-grow-storage/disable-autogrow-existing-server.png":::

1. Select **Save** to apply the changes.

    :::image type="content" source="media/how-to-auto-grow-storage/disable-autogrow-existing-server-save.png" alt-text="Screenshot showing how to save changes after disabling storage autogrow on an existing Azure Database for flexible server instance." lightbox="media/how-to-auto-grow-storage/disable-autogrow-existing-server-save.png":::

1. A deployment initiates and, when it completes, a notification shows that autogrow is successfully enabled.

    :::image type="content" source="media/how-to-auto-grow-storage/notification-autogrow-existing-server.png" alt-text="Screenshot showing notification that confirms that autogrow is enabled." lightbox="media/how-to-auto-grow-storage/notification-autogrow-existing-server.png":::

### [CLI](#tab/cli-disable-existing-server)

You can enable storage autogrow in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --storage-auto-grow disabled
```

---

## Steps to enable storage autogrow during server provisioning

### [Portal](#tab/portal-enable-new-server)

Using the [Azure portal](https://portal.azure.com/):

1. During provisioning of a new Azure Database for PostgreSQL flexible server instance, in the **Compute + storage** section, select **Configure server**.

    :::image type="content" source="media/how-to-auto-grow-storage/create-server-storage-auto-grow.png" alt-text="Screenshot showing how to configure server compute and storage during provisioning of a new Azure Database for flexible server instance." lightbox="media/how-to-auto-grow-storage/create-server-storage-auto-grow.png":::

1. In the **Storage** section, enable the **Storage autogrow** checkbox.

    :::image type="content" source="media/how-to-auto-grow-storage/server-provisioning-storage-auto-grow.png" alt-text="Screenshot showing how to enable storage autogrow during provisioning of a new Azure Database for flexible server instance." lightbox="media/how-to-auto-grow-storage/server-provisioning-storage-auto-grow.png":::

### [CLI](#tab/cli-enable-new-server)

You can enable storage autogrow while provisioning a new server via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --storage-auto-grow disabled ...
```

> [!NOTE]
> The previous command needs to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

---

## Limitations and considerations

- Autogrow activates when available space is less than 10% of total provisioned storage or 64 GiB, whichever is greater.

- The autogrow feature only supports scaling up. It doesn't reduce storage size automatically.

## Frequently asked questions (FAQ)

**Q. Does autogrow work with high WAL usage?  

A.No, it doesn't trigger in that case.

**Q. Does autogrow cause downtime?**  
A. No, it relies on online disk scaling.

## Related content

- [Scale storage performance](how-to-scale-storage-performance.md)
- [Storage options](../extension-module/concepts-storage.md)
- [Limits in Azure Database for PostgreSQL](../configure-maintain/concepts-limits.md)
