---
title: Enable and Download Server Logs
description: This article describes how to enable and download server logs for Azure Database for MySQL - Flexible Server by using the Azure portal.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---
# Enable and download server logs for Azure Database for MySQL - Flexible Server
You can use server logs to help monitor and troubleshoot an instance of Azure Database for MySQL Flexible Server, and to gain detailed insights into the activities that have run on your servers.
By default, the server logs feature in Azure Database for MySQL Flexible Server is disabled. However, after you enable the feature, an Azure Database for MySQL Flexible Server instance starts capturing events of the selected log type and writes them to a file. You can then use the Azure portal or the Azure CLI to download the files to assist with your troubleshooting efforts.
This article explains how to enable the server logs feature in Azure Database for MySQL Flexible Server and download server log files. It also provides information about how to disable the feature.

In this tutorial, you'll learn how to:
- Enable the server logs feature.
- Disable the server logs feature.
- Download server log files.

## Prerequisites

To complete this tutorial, you need an existing Azure Database for MySQL Flexible Server instance. If you need to create a new server, see [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md).

## Enable Server logs

To enable the server logs feature, perform the following steps.

1. In the [Azure portal](https://portal.azure.com), select your Azure Database for MySQL Flexible Server instance.

1. On the left pane, under **Monitoring**, select **Server logs**.

    :::image type="content" source="media/how-to-server-logs-portal/1-how-to-serverlog.png" alt-text="Screenshot showing Azure Database for MySQL Flexible Server Server Logs.":::

1. To enable server logs, under **Server logs**, select **Enable**.

    :::image type="content" source="media/how-to-server-logs-portal/2-how-to-serverlog.png" alt-text="Screenshot showing Enable Server Logs.":::

> [!NOTE]  
> You can also enable server logs in the Azure portal, on the [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md) pane for your server, by setting the value of the log_output parameter to FILE.
> For more information on the log_output parameter, in the MySQL documentation, see topic Server System Variables ([version 5.7](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_log_output) or [version 8.0](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_log_output)).

1. To enable the slow_query_log log, under **Select logs to enable**, select **slow_query_log**.

    :::image type="content" source="media/how-to-server-logs-portal/3-how-to-serverlog.png" alt-text="Screenshot showing select slow log - Server Logs.":::

To configure slow_logs on your Azure Database for MySQL Flexible Server instance, see [Tutorial: Query Performance Insight for Azure Database for MySQL - Flexible Server](tutorial-query-performance-insights.md)

## Download Server logs

To download server logs, perform the following steps.
> [!NOTE]  
> After enabling logs, the log files will be available to download after few minutes.

1. Under **Name**, select the log file you want to download, and then, under **Action**, select **Download**.

    :::image type="content" source="media/how-to-server-logs-portal/4-how-to-serverlog.png" alt-text="Screenshot showing Server Logs - Download." lightbox="media/how-to-server-logs-portal/4-how-to-serverlog.png":::

    For HA enabled Azure Database for MySQL Flexible Server instances, server logs for standby server can be identified by another four-letter identifier after the hostname of the server as shown below.

    :::image type="content" source="media/how-to-server-logs-portal/5-how-to-serverlog.png" alt-text="Screenshot showing server Logs - HA logs.":::

1. To download multiple log files at one time, under **Name**, select the files you want to download, and then above **Name**, select **Download**.

    :::image type="content" source="media/how-to-server-logs-portal/6-how-to-serverlog.png" alt-text="Screenshot showing server Logs - Download all.":::

## Disable Server Logs

1. From your Azure portal, select Server logs from Monitoring server pane.

1. For disabling Server logs to file, Uncheck Enable. (The setting will disable logging for all the log_types available)

    :::image type="content" source="media/how-to-server-logs-portal/7-how-to-serverlog.png" alt-text="Screenshot showing server Logs - Disable.":::

1. Select Save

    :::image type="content" source="media/how-to-server-logs-portal/8-how-to-serverlog.png" alt-text="Screenshot showing server Logs - Save.":::

## Related content

- [How to enable slow query logs](./tutorial-query-performance-insights.md#configure-slow-query-logs-by-using-the-azure-portal)
- [List and download Azure Database for MySQL - Flexible Server logs by using the Azure CLI](how-to-server-logs-cli.md)
