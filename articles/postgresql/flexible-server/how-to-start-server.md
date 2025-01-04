---
title: Start an instance of Azure Database for PostgreSQL flexible server
description: This article describes how to start an instance of Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 01/04/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to start an Azure Database for PostgreSQL flexible server instance, so that I can manage my server efficiently.
---

# Start an instance of Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to start an Azure Database for PostgreSQL flexible server instance.

## Start a stopped server

### [Portal](#tab/portal-start/server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, select **Overview**.

3. The status of the server must be **Stopped**, for the **Start** button to appear on the toolbar.

3. Select the **Start** button.

    :::image type="content" source="./media/how-to-start-server/start-server.png" alt-text="Screenshot showing how to start a stopped server." lightbox="./media/how-to-start-server/start-server.png":::

4. A notification informs you that the server is starting. Also, the status of the server changes to **Starting**.

    :::image type="content" source="./media/how-to-start-server/starting-server.png" alt-text="Screenshot showing a server which is starting." lightbox="./media/how-to-start-server/starting-server.png":::

5. When the process completes, a notification informs you that the server is started. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-start-server/started-server.png" alt-text="Screenshot showing a server which is started and shows its status as Available." lightbox="./media/how-to-start-server/started-server.png":::

### [CLI](#tab/cli-start-server)

You can start a stopped server via the [az postgres flexible-server start](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-start) command.

```azurecli-interactive
az postgres flexible-server start --resource-group <resource_group> --name <server>
```

If you attempt to start a server which isn't in `Stopped` state, you receive an error like the following:

```output
(ServerIsNotStopped) Start Server can only be performed on Stopped servers. Seever Name = <server>, Current Server State = Updating
Code: ServerIsNotStopped
Message: Start Server can only be performed on Stopped servers. Server Name = <server>, Current Server State = Updating
```

---

> [!NOTE]
> Once the server is started, all management operations are available for the Azure Database for PostgreSQL flexible server instance.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Restart an instance of Azure Database for PostgreSQL flexible server](how-to-restart-server-portal.md).
- [Enable, list and download server logs in Azure Database for PostgreSQL - Flexible Server](how-to-server-logs-portal.md).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
