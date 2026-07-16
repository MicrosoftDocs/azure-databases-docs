---
title: Promote Read Replica to Standalone Server in Azure Database for PostgreSQL Flexible Server
description: This article describes how to promote a read replica so that it becomes an independent standalone server.
#customer intent: As a user, I want to promote a read replica to a standalone server, so that it becomes an independent primary server for its own workloads.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: how-to
---

# Promote read replica to standalone server in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to switch over a read replica of an Azure Database for PostgreSQL flexible server so that it becomes the new primary server of the replication set.

## Steps to promote replica to standalone server

### [Portal](#tab/portal-promote-replica-to-standalone-server)

Use the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to show its associated virtual endpoints.

1. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-read-replicas.png" alt-text="Screenshot showing the Replication page with read replicas." lightbox="./media/how-to-read-replicas/replication-with-read-replicas.png":::

1. Select the **Promote** icon next to the name of the endpoint of the read replica that you want to switch over to.

    :::image type="content" source="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png" alt-text="Screenshot showing the Switch over or Promote to standalone pane." lightbox="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png":::

1. In **Replica server to promote**, select **Promote to independent server and remove from replication. This action doesn't impact the primary server.** for **Action**. Select **Planned** or **Forced** for **Data sync**, depending on what suits your needs best. If you decide to use the **Planned** option, mark the **I understand that this read replica becomes an independent server and that this action can't be undone.** checkbox to acknowledge that the read replica is detached into its own standalone entity. If you decide to use the **Forced** option, mark the **I understand that this read replica becomes an independent server and that its data isn't synced first. This action can't be undone.** checkbox to also acknowledge the potential data loss. Finally, select **Promote**.

    :::image type="content" source="./media/how-to-read-replicas/promote-to-standalone.png" alt-text="Screenshot showing the Promote to standalone pane." lightbox="./media/how-to-read-replicas/promote-to-standalone.png":::

1. A notification informs you that the read replica is being promoted to a standalone server.

    :::image type="content" source="./media/how-to-read-replicas/notification-promoting-to-standalone.png" alt-text="Screenshot showing a notification informing that the read replica is being promoted to a standalone server." lightbox="./media/how-to-read-replicas/notification-promoting-to-standalone.png":::

1. When the process completes, a notification informs you that the read replica is successfully promoted to a standalone server.

    :::image type="content" source="./media/how-to-read-replicas/notification-promoted-to-standalone.png" alt-text="Screenshot showing a notification informing that the read replica promoted to a standalone server successfully." lightbox="./media/how-to-read-replicas/notification-promoted-to-standalone.png":::

### [CLI](#tab/cli-promote-replica-to-standalone-server)

You can switch a read replica to become the new primary server for your Azure PostgreSQL flexible server by using the [`az postgres flexible-server replica promote`](/cli/azure/postgres/flexible-server/replica#az-postgres-flexible-server-replica-promote) command.

To ensure the read replica synchronizes with all the changes on the primary server before the switch, set `--promote-option` to `planned`.

```azurecli-interactive
az postgres flexible-server replica promote \
  --resource-group <resource_group> \
  --name <server> \
  --promote-mode Standalone \
  --promote-option Planned
```

If you want the switch to finish faster and you're okay with losing changes that are already committed on the primary server but not yet synchronized to the read replica, set `--promote-option` to `forced`.

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
