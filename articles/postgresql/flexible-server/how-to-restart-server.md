---
title: Restart a server
description: This article describes how to restart an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to restart an Azure Database for PostgreSQL flexible server.
---

# Restart a server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to restart an Azure Database for PostgreSQL flexible server.

## Steps to restart a server

### [Portal](#tab/portal-restart-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

3. The status of the server must be **Ready**, for the **Restart** button to appear on the toolbar.

    :::image type="content" source="./media/how-to-restart-server/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-restart-server/server-status.png":::

4. Select the **Restart** button.

    :::image type="content" source="./media/how-to-restart-server/restart-server.png" alt-text="Screenshot showing how to restart a started server." lightbox="./media/how-to-restart-server/restart-server.png":::

5. In the **Restart server** dialog, confirm or abort your decision to restart the server.

    :::image type="content" source="./media/how-to-restart-server/confirm-restart-server.png" alt-text="Screenshot showing the Restart server dialog to confirm or abort the operation." lightbox="./media/how-to-restart-server/confirm-restart-server.png":::

6. A notification informs you that the server is restarting. Also, the status of the server changes to **Restarting**.

    :::image type="content" source="./media/how-to-restart-server/restarting-server-status.png" alt-text="Screenshot showing a server which is restarting." lightbox="./media/how-to-restart-server/restarting-server-status.png":::

7. When the process completes, a notification informs you that the server is restarted.

    :::image type="content" source="./media/how-to-restart-server/restarted-server-notification.png" alt-text="Screenshot showing the notification seen when a server completes a successful restart operation." lightbox="./media/how-to-restart-server/restarted-server-notification.png":::

8. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-restart-server/restarted-server-status.png" alt-text="Screenshot showing a server which is started, highlighting its status as Ready." lightbox="./media/how-to-restart-server/restarted-server-status.png":::

### [CLI](#tab/cli-restart-server)

You can restart a started server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

```azurecli-interactive
az postgres flexible-server restart --resource-group <resource_group> --name <server>
```

If you attempt to restart a server which isn't in `Ready` state, you receive an error like this:

```output
Server will be automatically started after 7 days if you do not perform a manual start operation
(ServerIsNotReady) Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
Code: ServerIsNotReady
Message: Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
```

---

> [!NOTE]
> Once the server is restarted, all management operations are available for the Azure Database for PostgreSQL flexible server.

## Related content

- [Stop a server](how-to-stop-server.md).
- [Configure high availability](how-to-configure-high-availability.md).
- [Download PostgreSQL server logs and major version upgrade logs](how-to-configure-server-logs.md).
