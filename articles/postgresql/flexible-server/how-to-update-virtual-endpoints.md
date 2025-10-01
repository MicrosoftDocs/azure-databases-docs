---
title: Update virtual endpoints
description: This article describes how to update virtual endpoints for an Azure Database for PostgreSQL flexible server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Update virtual endpoints

This article provides step-by-step instructions to update virtual endpoints associated to an Azure Database for PostgreSQL flexible server.

## Steps to update virtual endpoints

### [Portal](#tab/portal-update-virtual-endpoints)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to update its associated virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-virtual-endpoints.png" alt-text="Screenshot showing the Replication page with virtual endpoints created." lightbox="./media/how-to-read-replicas/replication-with-virtual-endpoints.png":::

3.  In the **Virtual endpoints** section, select the pencil icon, which lets you update one property of the existing virtual endpoints.

    :::image type="content" source="./media/how-to-read-replicas/update-virtual-endpoints.png" alt-text="Screenshot showing the location of the pencil icon in the Replication page." lightbox="./media/how-to-read-replicas/update-virtual-endpoints.png":::

4. The only property you can update of an existing pair of virtual endpoints is the **Target of the reader virtual endpoint**. However, it can only be changed if there's at least one read replica created. Otherwise, it will refer to the primary server, just like the **Target of writer virtual endpoint** property does. If the server doesn't have read replicas, you cannot change any property, and you must select **Cancel**.

    :::image type="content" source="./media/how-to-read-replicas/update-virtual-endpoints-no-replicas.png" alt-text="Screenshot showing the update virtual endpoints dialog when there're no read replicas." lightbox="./media/how-to-read-replicas/update-virtual-endpoints-no-replicas.png":::

5. If the server has read replicas and you change the value of **Target of the reader virtual endpoint**, select **Save** to persist the changes.

    :::image type="content" source="./media/how-to-read-replicas/save-virtual-endpoints-update.png" alt-text="Screenshot showing the Save button to persist changes made to existing virtual endpoints." lightbox="./media/how-to-read-replicas/save-virtual-endpoints-update.png":::


6. A notification informs you that the virtual endpoints are being updated.

    :::image type="content" source="./media/how-to-read-replicas/notification-updating-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints are being updated." lightbox="./media/how-to-read-replicas/notification-updating-virtual-endpoints.png":::

7. When the process completes, a notification informs you that the virtual endpoints were successfully updated.

    :::image type="content" source="./media/how-to-read-replicas/notification-updated-virtual-endpoints.png" alt-text="Screenshot showing a notification informing that the virtual endpoints were updated successfully." lightbox="./media/how-to-read-replicas/notification-updated-virtual-endpoints.png":::

### [CLI](#tab/cli-update-virtual-endpoints)

You can update the existing virtual endpoints of your Azure PostgreSQL flexible server via the [`az postgres flexible-server virtual-endpoint update`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-virtual-endpoint-update) command. 

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
