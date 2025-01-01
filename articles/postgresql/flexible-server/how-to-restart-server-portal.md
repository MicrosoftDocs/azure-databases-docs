---
title: Restart - Azure portal
description: This article describes how to perform restart operations in Azure Database for PostgreSQL - Flexible Server through the Azure portal.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Restart Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step procedure to perform restart of the Azure Database for PostgreSQL flexible server instance. This operation is useful to apply any static parameter changes that requires database server restart. The procedure is same for servers configured with zone redundant high availability. 

> [!IMPORTANT]
> When configured with high availability, both the primary and the standby servers are restarted at the same time.

## Pre-requisites

To complete this how-to guide, you need:

-   An Azure Database for PostgreSQL flexible server instance.

## Restart your flexible server

Follow these steps to restart your Azure Database for PostgreSQL flexible server instance.

1.  In the [Azure portal](https://portal.azure.com/), choose your Azure Database for PostgreSQL flexible server instance that you want to restart.

2.  Click **Overview** from the left panel and click **Restart**.
   
     :::image type="content" source="./media/how-to-restart-server-portal/restart-base-page.png" alt-text="Restart selection.":::

3.  A pop-up confirmation message appears.

4.  Click **Yes** if you want to continue.
   
     :::image type="content" source="./media/how-to-restart-server-portal/restart-pop-up.png" alt-text="Restart confirm.":::
 
6.  A notification is shown that the restart operation has been
    initiated.

> [!NOTE]
> Using custom RBAC role to restart server please make sure that in addition to Microsoft.DBforPostgreSQL/flexibleServers/restart/action permission this role also has Microsoft.DBforPostgreSQL/flexibleServers/read permission granted to it.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Stop/Start an instance of Azure Database for PostgreSQL flexible server](how-to-stop-start-server-portal.md).
- [Enable, list and download server logs in Azure Database for PostgreSQL - Flexible Server](how-to-server-logs-portal.md).
- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
