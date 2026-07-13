---
title: Restart PostgreSQL engine in Azure Database for PostgreSQL Flexible Server
description: This article describes how to restart the PostgreSQL engine of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn how to restart the PostgreSQL engine of an Azure Database for PostgreSQL.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ai-usage: ai-assisted
---

# Restart PostgreSQL engine in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to restart the PostgreSQL engine hosted by an Azure Database for PostgreSQL flexible server.

> [!IMPORTANT]
> Restarting the PostgreSQL engine in an Azure Database for PostgreSQL flexible server doesn't restart the compute (virtual machine) that hosts it. It only restarts the database engine process.

## Steps to restart PostgreSQL engine

### [Portal](#tab/portal-restart-server)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-restart-server/overview.png" alt-text="Screenshot showing how to select the Overview page." lightbox="./media/how-to-restart-server/overview.png":::

1. The server status must be **Ready** for the **Restart** button to appear on the toolbar.

    :::image type="content" source="./media/how-to-restart-server/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-restart-server/server-status.png":::

1. Select the **Restart** button.

    :::image type="content" source="./media/how-to-restart-server/restart-server.png" alt-text="Screenshot showing how to restart a started server." lightbox="./media/how-to-restart-server/restart-server.png":::

1. In the **Restart server** dialog, confirm or cancel your decision to restart the server.

    :::image type="content" source="./media/how-to-restart-server/confirm-restart-server.png" alt-text="Screenshot showing the Restart server dialog to confirm or abort the operation." lightbox="./media/how-to-restart-server/confirm-restart-server.png":::

1. A notification informs you that the server is restarting. Also, the status of the server changes to **Restarting**.

    :::image type="content" source="./media/how-to-restart-server/restarting-server-notification.png" alt-text="Screenshot showing a server which is restarting." lightbox="./media/how-to-restart-server/restarting-server-notification.png":::

1. When the process completes, a notification informs you that the server is restarted. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-restart-server/restarted-server-notification.png" alt-text="Screenshot showing the notification seen when a server completes a successful restart operation." lightbox="./media/how-to-restart-server/restarted-server-notification.png":::

### [CLI](#tab/cli-restart-server)

Use the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command to restart the PostgreSQL engine hosted in a started server.

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server>
```

If you try to restart the PostgreSQL engine on a server that isn't in the `Ready` state, you get an error like this:

```output
(ServerIsNotReady) Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
Code: ServerIsNotReady
Message: Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
```

If you try to restart the compute of a server that's processing any other operation, you get an error like this:

```output
(SeverBusyWithOtherOperation) Cannot perform 'Restart' server operation because server '<server>' is busy processing other operation.
Code: SeverBusyWithOtherOperation
Message: Cannot perform 'Restart' server operation because server '<server>' is busy processing other operation.
```

---

> [!NOTE]
> After the server restarts, all management operations are available for the Azure Database for PostgreSQL flexible server.

## Related content

- [Start compute of a server](how-to-start-server.md).
- [Stop compute of a server](how-to-stop-server.md).
- [Configure high availability](../high-availability/how-to-configure-high-availability.md).
