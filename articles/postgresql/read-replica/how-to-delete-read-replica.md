---
title: Delete a read replica
description: This article describes how to delete a read replica of an Azure Database for PostgreSQL flexible server instance.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.topic: how-to
---

# Delete a read replica

This article provides step-by-step instructions to delete a read replica of an Azure Database for PostgreSQL flexible server instance.

## Steps to delete a read replica

### [Portal](#tab/portal-delete-read-replica)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server instance for which you want to delete a read replica.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-read-replicas.png" alt-text="Screenshot showing the Replication page." lightbox="./media/how-to-read-replicas/replication-with-read-replicas.png":::

3.  In the **Servers** section, select the ellipsis to the side of the replica that you want to delete, select **Delete**.

    :::image type="content" source="./media/how-to-read-replicas/delete-read-replica.png" alt-text="Screenshot showing the location of the Delete button in the Replication page." lightbox="./media/how-to-read-replicas/delete-read-replica.png":::

4.  In the **Delete \<server\>** dialog, mark the **I have read and understand that this server, as well as any databases it contains, will be deleted.** checkbox to acknowledge that you understand the effects of the action, and select **Delete**.

    :::image type="content" source="./media/how-to-read-replicas/confirm-and-delete-read-replica.png" alt-text="Screenshot showing the Delete server dialog." lightbox="./media/how-to-read-replicas/confirm-and-delete-read-replica.png":::

7. A notification informs you that the read replica is being deleted.

    :::image type="content" source="./media/how-to-read-replicas/notification-deleting-read-replica.png" alt-text="Screenshot showing a notification informing that the read replica is being deleted." lightbox="./media/how-to-read-replicas/notification-deleting-read-replica.png":::

8. When the process completes, a notification informs you that the read replica was successfully deleted.

    :::image type="content" source="./media/how-to-read-replicas/notification-deleted-read-replica.png" alt-text="Screenshot showing a notification informing that the read replica was deleted successfully." lightbox="./media/how-to-read-replicas/notification-deleted-read-replica.png":::

### [CLI](#tab/cli-delete-read-replica)

You can delete a read replica of your Azure PostgreSQL flexible server instance via the [`az postgres flexible-server delete`](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-delete) command. 

```azurecli-interactive
az postgres flexible-server delete \
  --resource-group <resource_group> \
  --name <server>
```
---

## Related content

- [Read replicas](concepts-read-replicas.md).
- [Create a read replica](how-to-create-read-replica.md).
