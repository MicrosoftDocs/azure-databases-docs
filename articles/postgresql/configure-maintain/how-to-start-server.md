---
title: Start compute of a server
description: This article describes how to start the compute of an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 06/09/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
#customer intent: As a user, I want to learn how to start the compute of an Azure Database for PostgreSQL.
---

# Start compute of a server

This article provides step-by-step instructions to start the compute of an Azure Database for PostgreSQL flexible server.

## Steps to start compute of a server

### [Portal](#tab/portal-start-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-start-server/overview.png" alt-text="Screenshot showing how to select the Overview page." lightbox="./media/how-to-start-server/overview.png":::

1. The status of the server must be **Stopped**, for the **Start** button to appear on the toolbar.

    :::image type="content" source="./media/how-to-start-server/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server ." lightbox="./media/how-to-start-server/server-status.png":::

1. Select the **Start** button.

    :::image type="content" source="./media/how-to-start-server/start-server.png" alt-text="Screenshot showing how to start a stopped server." lightbox="./media/how-to-start-server/start-server.png":::

1. A notification informs you that the server is starting. Also, the status of the server changes to **Starting**.

    :::image type="content" source="./media/how-to-start-server/starting-server-notification.png" alt-text="Screenshot showing the notification seen when a server initiates a start operation." lightbox="./media/how-to-start-server/starting-server-notification.png":::

1. When the process completes, a notification informs you that the server is started. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-start-server/started-server-notification.png" alt-text="Screenshot showing the notification seen when a server completes a successful start operation." lightbox="./media/how-to-start-server/started-server-notification.png":::

### [CLI](#tab/cli-start-server)

You can start the compute of a stopped server via the [az postgres flexible-server start](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-start) command.

```azurecli-interactive
az postgres flexible-server start \
  --resource-group <resource_group> \
  --name <server>
```

If you attempt to start the compute of a server which isn't in `Stopped` state and isn't processing any other operation, you receive an error like this:

```output
(ServerIsNotStopped) Start Server can only be performed on Stopped servers. Seever Name = <server>, Current Server State = Updating
Code: ServerIsNotStopped
Message: Start Server can only be performed on Stopped servers. Server Name = <server>, Current Server State = Updating
```

If you attempt to start the compute of a server which is processing any other operation, you receive an error like this:

```output
(SeverBusyWithOtherOperation) Cannot perform 'Start' server operation because server '<server>' is busy processing other operation.
Code: SeverBusyWithOtherOperation
Message: Cannot perform 'Start' server operation because server '<server>' is busy processing other operation.
```

---

> [!NOTE]
> Starting a server depends on the available capacity in the region. During capacity outages, the server start operation is not guaranteed to succeed. Once the server is started, all management operations are available for the Azure Database for PostgreSQL flexible server.

## Related content

- [Stop compute of a server](how-to-stop-server.md).
- [Restart PostgreSQL engine](how-to-restart-server.md).
- [Configure high availability](../high-availability/how-to-configure-high-availability.md).
