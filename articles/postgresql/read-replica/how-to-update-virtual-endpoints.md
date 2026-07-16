---
title: Update virtual endpoints in Azure Database for PostgreSQL Flexible Server
description: This article describes how to update virtual endpoints for an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to update virtual endpoints for my Azure Database for PostgreSQL flexible server, so that I can redirect connections to the correct target server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: how-to
---

# Update virtual endpoints in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to update virtual endpoints associated with an Azure Database for PostgreSQL flexible server.

## Steps to update virtual endpoints

### [Portal](#tab/portal-update-virtual-endpoints)

Use the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to update its associated virtual endpoints.

1. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-virtual-endpoints.png" alt-text="Screenshot showing the Replication page with virtual endpoints created." lightbox="./media/how-to-read-replicas/replication-with-virtual-endpoints.png":::

1.  In the **Virtual endpoints** section, select the pencil icon. You can update one property of the existing virtual endpoints.

    :::image type="content" source="./media/how-to-read-replicas/update-virtual-endpoints.png" alt-text="Screenshot showing the location of the pencil icon in the Replication page." lightbox="./media/how-to-read-replicas/update-virtual-endpoints.png":::

1. The only property you can update for an existing pair of virtual endpoints is the **Target of the reader virtual endpoint**. However, you can only change this property if there's at least one read replica created. Otherwise, it refers to the primary server, just like the **Target of writer virtual endpoint** property. If the server doesn't have read replicas, you can't change any property, and you must select **Cancel**.

    :::image type="content" source="./media/how-to-read-replicas/update-virtual-endpoints-no-replicas.png" alt-text="Screenshot showing the update virtual endpoints dialog when there're no read replicas." lightbox="./media/how-to-read-replicas/update-virtual-endpoints-no-replicas.png":::

1. If the server has read replicas and you change the value of **Target of the reader virtual endpoint**, select **Save** to persist the changes.

    :::image type="content" source="./media/how-to-read-replicas/save-virtual-endpoints-update.png" alt-text="Screenshot showing the Save button to persist changes made to existing virtual endpoints." lightbox="./media/how-to-read-replicas/save-virtual-endpoints-update.png":::


1. A notification informs you that the virtual endpoints are being updated.

    :::image type="content" source="./media/how-to-read-replicas/notification-updating-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints are being updated." lightbox="./media/how-to-read-replicas/notification-updating-virtual-endpoints.png":::

1. When the process completes, a notification informs you that the virtual endpoints were successfully updated.

    :::image type="content" source="./media/how-to-read-replicas/notification-updated-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints were updated successfully." lightbox="./media/how-to-read-replicas/notification-updated-virtual-endpoints.png":::

### [CLI](#tab/cli-update-virtual-endpoints)

Use the [`az postgres flexible-server virtual-endpoint update`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-update) command to update the existing virtual endpoints of your Azure PostgreSQL flexible server.

```azurecli-interactive
az postgres flexible-server virtual-endpoint update \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <virtual_endpoints_base_name> \
  --endpoint-type ReadWrite
  --members <replica>
```
---

## Related content

- [Read replicas](concepts-read-replicas.md).
- [Show virtual endpoints](how-to-show-virtual-endpoints.md).
- [Delete virtual endpoints](how-to-delete-virtual-endpoints.md).
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md).
