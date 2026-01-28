---
title: Stop/start By Using the Azure Portal
description: This article describes how to stop/start operations in Azure Database for MySQL - Flexible Server by using the Azure portal.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Stop/Start an Azure Database for MySQL - Flexible Server instance

This article provides step-by-step procedure to perform Stop and Start of an Azure Database for MySQL Flexible Server instance.

## Prerequisites

To complete this how-to guide, you must have an Azure Database for MySQL Flexible Server instance.

## Stop a running server

1. In the [Azure portal](https://portal.azure.com/), choose your Azure Database for MySQL Flexible Server instance that you want to stop.

1. From the **Overview** page, select the **Stop** button in the toolbar.

    :::image type="content" source="media/how-to-stop-start-server-portal/stop-server.png" alt-text="Screenshot of Stop Flexible Server." lightbox="media/how-to-stop-start-server-portal/stop-server.png":::

1. Select **Yes** to confirm stopping your server.

    :::image type="content" source="media/how-to-stop-start-server-portal/confirm-stop.png" alt-text="Screenshot of Confirm stopping Flexible Server." lightbox="media/how-to-stop-start-server-portal/confirm-stop.png":::

> [!NOTE]  
> Once the server is stopped, the other management operations are not available for the Azure Database for MySQL Flexible Server instance.

## Automatic server start for stopped servers after 30 days

To mitigate potential disruptions resulting from servers inadvertently remaining inactive, our system is equipped with an automatic start feature. If a server remains stopped for a continuous period of 30 days, it will be automatically started.

Upon this automatic start, the server status will update to "Available," and billing for the server will commence accordingly.

Please be advised that it's not permissible to stop servers for a duration exceeding 30 days. If you foresee the need to stop your server beyond this period, it's advisable to create a backup of your server data by exporting the data and later you might want to delete the server instance to avoid unwarranted costs and enhance security. You can employ a community tool such as [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) for the purpose.

## Start a stopped server

1. In the [Azure portal](https://portal.azure.com/), choose your Azure Database for MySQL Flexible Server instance that you want to start.

1. From the **Overview** page, select the **Start** button in the toolbar.

    :::image type="content" source="media/how-to-stop-start-server-portal/start-server.png" alt-text="Screenshot of Start Flexible Server." lightbox="media/how-to-stop-start-server-portal/start-server.png":::

> [!NOTE]  
> Once the server is started, all management operations are now available for the Azure Database for MySQL Flexible Server instance.

## Related content

- [networking in Azure Database for MySQL Flexible Server](concepts-networking.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
