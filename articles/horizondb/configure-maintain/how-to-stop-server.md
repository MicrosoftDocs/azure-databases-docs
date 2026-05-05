---
title: Stop Compute of a Server in Azure HorizonDB
description: This article describes how to stop the compute of an Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
# customer intent: As a user, I want to learn how to stop the compute of an Azure HorizonDB.
---

# Stop compute of a server in Azure HorizonDB

This article provides step-by-step instructions to stop the compute of an Azure HorizonDB instance.

## Steps to stop a server

### [Portal](#tab/portal-stop-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB instance.

1. In the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-stop-server/overview.png" alt-text="Screenshot showing how to select the Overview page." lightbox="media/how-to-stop-server/overview.png":::

1. The status of the server must be **Ready**, for the **Stop** button to appear on the toolbar.

   :::image type="content" source="media/how-to-stop-server/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="media/how-to-stop-server/server-status.png":::

1. Select the **Stop** button.

   :::image type="content" source="media/how-to-stop-server/stop-server.png" alt-text="Screenshot showing how to stop a started server." lightbox="media/how-to-stop-server/stop-server.png":::

1. In the **Stop server** dialog, confirm or abort your decision to stop the server.

   :::image type="content" source="media/how-to-stop-server/confirm-stop-server.png" alt-text="Screenshot showing the Stop server dialog to confirm or abort the operation." lightbox="media/how-to-stop-server/confirm-stop-server.png":::

1. A notification informs you that the server is stopping.

   :::image type="content" source="media/how-to-stop-server/stopping-server-notification.png" alt-text="Screenshot showing the notification seen when a server initiates a stop operation." lightbox="media/how-to-stop-server/stopping-server-notification.png":::

1. Also, the status of the server changes to **Stopping**.

   :::image type="content" source="media/how-to-stop-server/stopping-server-status.png" alt-text="Screenshot showing a server which is stopping, highlighting its status as Stopping." lightbox="media/how-to-stop-server/stopping-server-status.png":::

1. When the process completes, a notification informs you that the server is stopped.

   :::image type="content" source="media/how-to-stop-server/stopped-server-notification.png" alt-text="Screenshot showing the notification seen when a server completes a successful stop operation." lightbox="media/how-to-stop-server/stopped-server-notification.png":::

1. Also, the status of the server changes to **Stopped**.

   :::image type="content" source="media/how-to-stop-server/stopped-server-status.png" alt-text="Screenshot showing a server which is stopped, highlighting its status as Stopped." lightbox="media/how-to-stop-server/stopped-server-status.png":::

### [CLI](#tab/cli-stop-server)

You can stop the compute of a started server via the [az postgres flexible-server stop](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-stop) command.

```azurecli-interactive
az postgres flexible-server stop \
  --resource-group <resource_group> \
  --name <server>
```

If you attempt to stop the compute of a server which isn't in `Ready` state, you receive an error like this:

```output
Server will be automatically started after 7 days if you do not perform a manual start operation
(ServerIsNotReady) Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = <non_started_server_state>
Code: ServerIsNotReady
Message: Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = <non_started_server_state>
```

---

> [!NOTE]  
> Once the server is stopped, other management operations aren't available for the Azure HorizonDB.
> While the Azure HorizonDB is in stopped state, it could be briefly restarted for scheduled monthly maintenance, and then returned to its stopped state. This procedure ensures that even instances in a stopped state, stay up to date with all necessary patches and updates.

## Related content

- [Start compute of a server in Azure HorizonDB](how-to-start-server.md)
- [Restart PostgreSQL engine in Azure HorizonDB](how-to-restart-server.md)
- [Configure high availability in Azure HorizonDB](../high-availability/how-to-configure-high-availability.md)
