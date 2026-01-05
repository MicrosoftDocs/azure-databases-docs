---
title: Promote read replica to standalone server
description: This article describes how to promote a read replica so that it becomes an independent standalone server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Promote read replica to standalone server

This article provides step-by-step instructions to switch over a read replica of an Azure Database for PostgreSQL flexible server so that it becomes the new primary server of the replication set.

## Steps to promote replica to standalone server

### [Portal](#tab/portal-promote-replica-to-standalone-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to show its associated virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-read-replicas.png" alt-text="Screenshot showing the Replication page with read replicas." lightbox="./media/how-to-read-replicas/replication-with-read-replicas.png":::

3. Select the **Promote** icon to the side of the name of the endpoint of the read replica to which you want to switch over.

    :::image type="content" source="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png" alt-text="Screenshot showing the Switch over or Promote to standalone pane." lightbox="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png":::

4. In **Replica server to promote**, select **Promote to independent server and remove from replication. This won't impact the primary server.** for **Action**. And select **Planned** or **Forced** for **Data sync**, depending on what suits your needs best. if you decide to use the **Planned** option, you have to mark the **I understand that this read replica will become an independent server and that this action can't be undone.** to acknowledge that the read replica will be detached into its own standalone entity. If you decide to use the **Forced** option, you have to mark the **I understand that this read replica will become an independent server and that its data won't be synced first. This action can't be undone.** checkbox to also acknowledge the potential data loss. Finally, select **Promote**.

    :::image type="content" source="./media/how-to-read-replicas/promote-to-standalone.png" alt-text="Screenshot showing the Promote to standalone pane." lightbox="./media/how-to-read-replicas/promote-to-standalone.png":::

6. A notification informs you that the read replica is being promoted to a standalone server.

    :::image type="content" source="./media/how-to-read-replicas/notification-promoting-to-standalone.png" alt-text="Screenshot showing a notification informing that the read replica is being promoted to a standalone server." lightbox="./media/how-to-read-replicas/notification-promoting-to-standalone.png":::

7. When the process completes, a notification informs you that the read replica successfully promoted to a standalone server.

    :::image type="content" source="./media/how-to-read-replicas/notification-promoted-to-standalone.png" alt-text="Screenshot showing a notification informing that the read replica promoted to a standalone server successfully." lightbox="./media/how-to-read-replicas/notification-promoted-to-standalone.png":::

### [CLI](#tab/cli-promote-replica-to-standalone-server)

You can switch over a read replica to become the new primary of your Azure PostgreSQL flexible server via the [`az postgres flexible-server replica promote`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-promote) command.

If you want to make sure that the read replica is first synchronized with all the changes existing on the primary server, before the switch over is initiated, then set `--promote-option` to `planned`:

```azurecli-interactive
az postgres flexible-server replica promote \
  --resource-group <resource_group> \
  --name <server> \
  --promote-mode Standalone \
  --promote-option Planned
```

If you prefer the switch over to complete faster, and can assume that the changes which are already committed on the primary server but not yet synchronized to the read replica will be lost, then set `--promote-option` to `forced`:

```azurecli-interactive
az postgres flexible-server replica promote \
  --resource-group <resource_group> \
  --name <server> \
  --promote-mode Standalone \
  --promote-option Forced
```
---

## Related content

- [Read replicas](concepts-read-replicas.md).
- [Switch over read replica to primary](how-to-switch-over-replica-to-primary.md).
- [Delete a read replica](how-to-delete-read-replica.md).
