---
title: Configure storage autogrow
description: This article describes how you can configure storage autogrow in an Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 01/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure storage autogrow in an Azure Database for PostgreSQL flexible server.
---

# Configure storage autogrow

[!INCLUDE [applies-to-postgresql-Flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article describes how you can configure Azure Database for PostgreSQL server storage to grow without impacting the workload.

For servers with more than 1 TiB of provisioned storage, the storage autogrow mechanism activates when the available space is less than 10% of the total capacity or when the available space is less than 64 GiB. The smaller of the two is the value that determines when autogrow activates. Conversely, for servers with storage under 1 TiB, this threshold is adjusted to 20% of the available free space or 64 GiB. Again, picking the smaller of the two values.

As an illustration, take a server with a storage capacity of 2 TiB (greater than 1 TiB). In this case, the autogrow limit is set at 64 GiB. This choice is made because 64 GiB is the smaller value when compared to 10% of 2 TiB, which is roughly 204.8 GiB. In contrast, for a server with a storage size of 128 GiB (less than 1 TiB), the autogrow feature activates when there's only 25.8 GiB of space left. This activation is based on the 20% threshold of the total allocated storage (128 GiB), which is smaller than 64 GiB. 

> [!NOTE]  
> Storage always doubles in size for premium disk SSD, and that doubles the storage cost. Only premium SSD V2 supports more granular disk size increase.

## Enable storage autogrow for existing servers

### [Portal](#tab/portal-enable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Compute + storage**.

3. In the **Storage** section, enable the **Storage Auto-growth** checkbox.

4. Select **Save** to apply the changes.

    :::image type="content" source="./media/how-to-auto-grow-storage/enable-autogrow-existing-server.png" alt-text="Screenshot showing how to enable storage autogrow on an existing instance." lightbox="./media/how-to-auto-grow-storage/enable-autogrow-existing-server.png":::

5. A deployment initiates and, when it completes, a notification shows that auto grow is successfully enabled.

    :::image type="content" source="./media/how-to-auto-grow-storage/notification-autogrow-existing-server.png" alt-text="Screenshot showing notification that confirms that autogrow is enabled." lightbox="./media/how-to-auto-grow-storage/notification-autogrow-existing-server.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable storage autogrow in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --storage-auto-grow enabled
```
---

## Disable storage autogrow for existing servers

### [Portal](#tab/portal-disable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Compute + storage**.

3. In the **Storage** section, enable the **Storage Auto-growth** checkbox.

4. Select **Save** to apply the changes.

    :::image type="content" source="./media/how-to-auto-grow-storage/disable-autogrow-existing-server.png" alt-text="Screenshot showing how to disable storage autogrow on an existing instance." lightbox="./media/how-to-auto-grow-storage/disable-autogrow-existing-server.png":::

5. A deployment initiates and, when it completes, a notification shows that auto grow is successfully enabled.

    :::image type="content" source="./media/how-to-auto-grow-storage/notification-autogrow-existing-server.png" alt-text="Screenshot showing notification that confirms that autogrow is enabled." lightbox="./media/how-to-auto-grow-storage/notification-autogrow-existing-server.png":::

### [CLI](#tab/cli-disable-existing-server)

You can enable storage autogrow in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --storage-auto-grow disabled
```

---

## Enable storage autogrow during server provisioning

### [Portal](#tab/portal-enable-new-server)

Using the [Azure portal](https://portal.azure.com/):

1. During provisioning of a new instance of Azure Database for PostgreSQL Flexible Server, in the **Compute + storage** section, select **Configure server**.

    :::image type="content" source="./media/how-to-auto-grow-storage/create-server-storage-auto-grow.png" alt-text="Screenshot showing how to configure server compute and storage during provisioning of a new instance." lightbox="./media/how-to-auto-grow-storage/create-server-storage-auto-grow.png":::

3. In the **Storage** section, enable the **Storage Auto-growth** checkbox.

    :::image type="content" source="./media/how-to-auto-grow-storage/server-provisioning-storage-auto-grow.png" alt-text="Screenshot showing how to enable storage autogrow during provisioning of a new instance." lightbox="./media/how-to-auto-grow-storage/server-provisioning-storage-auto-grow.png":::

### [CLI](#tab/cli-enable-new-server)

You can enable storage autogrow while provisioning a new server via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

```azurecli-interactive
az postgres flexible-server create --resource-group <resource_group> --name <server> --storage-auto-grow disabled ...
```

> [!NOTE]
> The command provided above needs to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

---


## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Restart an Azure Database for PostgreSQL flexible server](how-to-restart-server.md).
- [Reset administrator password of an Azure Database for PostgreSQL flexible server](how-to-reset-admin-password.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
