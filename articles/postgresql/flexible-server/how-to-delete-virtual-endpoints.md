---
title: Delete virtual endpoints
description: This article describes how to delete virtual endpoints for an Azure Database for PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Delete virtual endpoints

This article provides step-by-step instructions to delete virtual endpoints associated to an Azure Database for PostgreSQL flexible server instance.

## Steps to delete virtual endpoints

### [Portal](#tab/portal-delete-virtual-endpoints)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server instance for which you want to delete its associated virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-virtual-endpoints.png" alt-text="Screenshot showing the Replication page with virtual endpoints created." lightbox="./media/how-to-read-replicas/replication-with-virtual-endpoints.png":::

3.  In the **Virtual endpoints** section, select the ellipsis to the right of the pencil icon, then select **Delete**.

    :::image type="content" source="./media/how-to-read-replicas/delete-virtual-endpoints.png" alt-text="Screenshot showing the location of the Delete virtual endpoints button in the Replication page." lightbox="./media/how-to-read-replicas/delete-virtual-endpoints.png":::

4. A dialog box asks for confirmation to proceed with the deletion of the virtual endpoints. Select **Delete** to proceed.

    :::image type="content" source="./media/how-to-read-replicas/delete-virtual-endpoints-confirmation.png" alt-text="Screenshot showing the Delete confirmation dialog." lightbox="./media/how-to-read-replicas/delete-virtual-endpoints-confirmation.png":::

5. A notification informs you that the virtual endpoints are being deleted.

    :::image type="content" source="./media/how-to-read-replicas/notification-deleting-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints are being deleted." lightbox="./media/how-to-read-replicas/notification-deleting-virtual-endpoints.png":::

6. When the process completes, a notification informs you that the virtual endpoints were successfully deleted.

    :::image type="content" source="./media/how-to-read-replicas/notification-deleted-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints were deleted successfully." lightbox="./media/how-to-read-replicas/notification-deleted-virtual-endpoints.png":::

### [CLI](#tab/cli-delete-virtual-endpoints)

You can delete the existing virtual endpoints of your Azure PostgreSQL flexible server instance via the [`az postgres flexible-server virtual-endpoint delete`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-delete) command. 

```azurecli-interactive
az postgres flexible-server virtual-endpoint delete \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <virtual_endpoints_base_name>
```
---

## Related content

- [Read replicas](concepts-read-replicas.md).
- [Create virtual endpoints](how-to-create-virtual-endpoints.md).
- [Update virtual endpoints](how-to-update-virtual-endpoints.md).
- [Show virtual endpoints](how-to-show-virtual-endpoints.md).
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md).
