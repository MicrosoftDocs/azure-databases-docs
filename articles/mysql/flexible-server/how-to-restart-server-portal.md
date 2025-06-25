---
title: Restart Server - Azure Portal
description: This article describes how you can restart an Azure Database for MySQL - Flexible Server instance by using the Azure portal.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Restart an Azure Database for MySQL - Flexible Server instance by using the Azure portal

This article describes how you can restart an Azure Database for MySQL Flexible Server instance. You might need to restart your server for maintenance reasons, which causes a short outage as the server performs the operation.

The server restart will be blocked if the service is busy. For example, the service might be processing a previously requested operation such as scaling vCores.

The time required to complete a restart depends on the MySQL recovery process. To decrease the restart time, we recommend you minimize the amount of activity occurring on the server prior to the restart.

## Prerequisites

To complete this how-to guide, you need:

- An [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)

## Perform server restart

The following steps restart the Azure Database for MySQL Flexible Server instance:

1. In the Azure portal, select your Azure Database for MySQL Flexible Server instance.

1. In the toolbar of the server's **Overview** page, select **Restart**.

   :::image type="content" source="media/how-to-restart-server-portal/2-server.png" alt-text="Screenshot of Azure Database for MySQL - Overview - Restart button." lightbox="media/how-to-restart-server-portal/2-server.png":::

1. Select **Yes** to confirm restarting the server.

   :::image type="content" source="media/how-to-restart-server-portal/3-restart-confirm.png" alt-text="Screenshot of Azure Database for MySQL - Restart confirm." lightbox="media/how-to-restart-server-portal/3-restart-confirm.png":::

1. Observe that the server status changes to "Restarting".

   :::image type="content" source="media/how-to-restart-server-portal/4-restarting-status.png" alt-text="Screenshot of Azure Database for MySQL - Restart status." lightbox="media/how-to-restart-server-portal/4-restarting-status.png":::

1. Confirm server restart is successful.

   :::image type="content" source="media/how-to-restart-server-portal/5-restart-success.png" alt-text="Screenshot of Azure Database for MySQL - Restart success." lightbox="media/how-to-restart-server-portal/5-restart-success.png":::

## Next step

> [!div class="nextstepaction"]
> [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)