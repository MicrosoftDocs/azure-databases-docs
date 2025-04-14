---
title: Promote replica to standalone server
description: This article describes how to promote a read replica so that it becomes an independent standalone server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 04/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Promote replica to standalone server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to swicth over a read replica of an Azure Database for PostgreSQL flexible server so that it becomes the new primary server of the replication set.

## Steps to promote replica to standalone server

### [Portal](#tab/portal-promote-replica-to-standalone-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server for which you want to show its associated virtual endpoints.

2. In the resource menu, under the **Settings** section, select **Replication**.

    :::image type="content" source="./media/how-to-read-replicas/replication-with-read-replicas.png" alt-text="Screenshot showing the Replication page with read replicas." lightbox="./media/how-to-read-replicas/replication-with-read-replicas.png":::

3. Select the **Promote** icon to the side of the name of the endpoint of the read replica to which you want to switch over.

    :::image type="content" source="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png" alt-text="Screenshot showing the Switch over or Promote to standalone pane." lightbox="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png":::

4. If the server doesn't have the virtual endpoints created, or if the read replica which you're trying to switch over to primary isn't the reader virtual endpoint's target server, an attempt to switch over a read replica to primary fails. That's what the warning displayed in the dialog reminds you. 

    :::image type="content" source="./media/how-to-read-replicas/warning-switch-over-without-virtual-endpoints.png" alt-text="Screenshot showing the Switch over or Promote to standalone pane when there aren't virtual endpoints or aren't correctly configured to support the switch over operation." lightbox="./media/how-to-read-replicas/warning-switch-over-without-virtual-endpoints.png":::

5. In **Replica server to promote**, select **Promote to primary server** for **Action**. And select **Planned** or **Forced** for **Data sync**, depending on what suits your needs best. if you decide to use the **Forced** option, you have to mark the **I understand that any data changes that have not been replicated from the primary server will be lost. The read replica lag time is the approximate period of data loss.** checkbox to acknowledge the potential data loss. Finally, select **Promote**.

    :::image type="content" source="./media/how-to-read-replicas/promoting.png" alt-text="Screenshot showing the Switch over or Promote to standalone pane." lightbox="./media/how-to-read-replicas/switch-over-or-promote-to-standalone.png":::

6. A notification informs you that the read replica is being switched over to primary.

    :::image type="content" source="./media/how-to-read-replicas/notification-switching-over-to-primary.png" alt-text="Screenshot showing a notification informing that the read replica is being switched over to primary." lightbox="./media/how-to-read-replicas/notification-switching-over-to-primary.png":::

7. When the process completes, a notification informs you that the read replica successfully switched over to primary.

    :::image type="content" source="./media/how-to-read-replicas/notification-switched-over-to-primary.png" alt-text="Screenshot showing a notification informing that the read replica switched over to primary successfully." lightbox="./media/how-to-read-replicas/notification-switched-over-to-primary.png":::

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

## Related content

- [Read replicas](concepts-read-replicas.md).
