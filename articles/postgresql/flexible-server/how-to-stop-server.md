---
title: Stop a server
description: This article describes how to stop an instance of Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 01/04/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to stop an Azure Database for PostgreSQL flexible server instance, so that I can manage my server efficiently.
---

# Stop a server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to stop an Azure Database for PostgreSQL flexible server instance.

## Stop a started server

### [Portal](#tab/portal-stop-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, select **Overview**.

3. The status of the server must be **Available**, for the **Stop** button to appear on the toolbar.

3. Select the **Stop** button.

    :::image type="content" source="./media/how-to-stop-server/stop-server.png" alt-text="Screenshot showing how to stop a started server." lightbox="./media/how-to-stop-server/stop-server.png":::

4. In the **Stop server** dialog, confirm or abort your decision to stop the server.

    :::image type="content" source="./media/how-to-stop-server/confirm-stop-server.png" alt-text="Screenshot showing the Stop server dialog to confirm or abort the operation." lightbox="./media/how-to-stop-server/confirm-stop-server.png":::

5. A notification informs you that the server is stopping. Also, the status of the server changes to **Stopping**.

    :::image type="content" source="./media/how-to-stop-server/stopping-server.png" alt-text="Screenshot showing a server which is stopping." lightbox="./media/how-to-stop-server/stopping-server.png":::

6. When the process completes, a notification informs you that the server is stopped. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-stop-server/stopped-server.png" alt-text="Screenshot showing a server which is stopped and shows its status as Stopped." lightbox="./media/how-to-stop-server/stopped-server.png":::

### [CLI](#tab/cli-stop-server)

You can stop a started server via the [az postgres flexible-server stop](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-stop) command.

```azurecli-interactive
az postgres flexible-server stop --resource-group <resource_group> --name <server>
```

If you attempt to stop a server which isn't in `Available` state, you receive an error like this:

```output
Server will be automatically started after 7 days if you do not perform a manual start operation
(ServerIsNotReady) Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
Code: ServerIsNotReady
Message: Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
```

---

> [!NOTE]
> Once the server is stopped, other management operations aren't available for the Azure Database for PostgreSQL flexible server.
> While the Azure Database for PostgreSQL flexible server is in stopped state, it could be briefly restarted for scheduled monthly maintenance, and then returned to its stopped state. This procedure ensures that even instances in a stopped state, stay up to date with all necessary patches and updates.

## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Restart an Azure Database for PostgreSQL flexible server](how-to-restart-server.md).
- [Reset administrator password of an Azure Database for PostgreSQL flexible server](how-to-reset-admin-password.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
