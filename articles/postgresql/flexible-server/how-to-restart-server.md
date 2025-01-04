---
title: Restart an instance of Azure Database for PostgreSQL flexible server
description: This article describes how to restart an instance of Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 01/04/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to restart an Azure Database for PostgreSQL flexible server instance, so that I can manage my server efficiently.
---

# Restart an instance of Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to restart an Azure Database for PostgreSQL flexible server instance.

## Restart a started server

### [Portal](#tab/portal-restart-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, select **Overview**.

3. The status of the server must be **Available**, for the **Restart** button to appear on the toolbar.

3. Select the **Restart** button.

    :::image type="content" source="./media/how-to-restart-server/restart-server.png" alt-text="Screenshot showing how to restart a stopped server." lightbox="./media/how-to-restart-server/restart-server.png":::

4. A notification informs you that the server is restarting. Also, the status of the server changes to **Restarting**.

    :::image type="content" source="./media/how-to-restart-server/restarting-server.png" alt-text="Screenshot showing a server which is restarting." lightbox="./media/how-to-restart-server/restarting-server.png":::

5. When the process completes, a notification informs you that the server is restarted. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-restart-server/restarted-server.png" alt-text="Screenshot showing a server which is restarted and shows its status as Available." lightbox="./media/how-to-restart-server/restarted-server.png":::

### [CLI](#tab/cli-restart-server)

You can restart a stopped server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

```azurecli-interactive
az postgres flexible-server restart --resource-group <resource_group> --name <server>
```

If you attempt to restart a server which isn't in `Available` state, you receive an error like this:

```output
Server will be automatically started after 7 days if you do not perform a manual start operation
(ServerIsNotReady) Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
Code: ServerIsNotReady
Message: Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
```

---

> [!NOTE]
> Once the server is restarted, all management operations are available for the Azure Database for PostgreSQL flexible server instance.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Start an instance of Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an instance of Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Enable, list, and download server logs in Azure Database for PostgreSQL - Flexible Server](how-to-server-logs-portal.md).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
