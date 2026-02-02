---
title: Monitor by using Azure Monitor workbooks
description: This article describes how you can monitor an Azure Database for PostgreSQL flexible server instance by using Azure Monitor workbooks.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 12/09/2024
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Monitor Azure Database for PostgreSQL  by using Azure Monitor workbooks

Azure Database for PostgreSQL is integrated with Azure Monitor workbooks. Workbooks give you a flexible canvas for analyzing data and creating rich visual reports within the Azure portal. Workbooks allow you to tap into multiple data sources across Azure and combine them into unified interactive experiences. Workbook templates serve as curated reports designed for flexible reuse by various users and teams.

When you open a template, you create a transient workbook which is populated with the contents of the template. With this integration, the server links to workbooks and a few sample templates, which can help you monitor the service at scale. You can edit these templates, customize them to your requirements, and pin them to the dashboard to create a focused and organized view of Azure resources.

In this article, you learn about the various workbook templates available for your Azure Database for PostgreSQL flexible server instance.

An Azure Database for PostgreSQL flexible server instance has two available templates:

- **Overview**: Displays an instance summary and top-level metrics to help you visualize and understand the resource utilization on your server. This template displays the following views:

    * Server details
        * Server summary
        * Database availability
        * Database summary
    * Connection metrics
    * Performance metrics
    * Storage metrics

- **Enhanced metrics**: Displays a summary of enhanced metrics for your Azure Database for PostgreSQL flexible server instance, with more fine-grained database monitoring. To enable these metrics, enable the server parameters `metrics.collector_database_activity` and `metrics.autovacuum_diagnostics`. These parameters are dynamic and don't require a server restart. For more information, see [enhanced metrics](concepts-monitoring.md#enhanced-metrics) and [autovacuum metrics](concepts-monitoring.md#autovacuum-metrics). This template displays the following views:

    * Activity
    * Database
    * Autovacuum
    * Replication

You can also edit and customize these templates according to your requirements. For more information, see [Azure Workbooks](/azure/azure-monitor/visualize/workbooks-overview).

## Access the workbook templates

Using the [Azure portal](https://portal.azure.com).

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Monitoring**, select **Workbooks**.

    :::image type="content" source="./media/concepts-workbooks/monitor-workbooks.png" alt-text="Screenshot showing the Workbooks menu option under Monitoring." lightbox="media/concepts-workbooks/monitor-workbooks.png":::

3. Select the **Overview** or the **Enhanced Metrics** template.

    :::image type="content" source="./media/concepts-workbooks/overview-enhanced-metrics.png" alt-text="Screenshot showing the Overview and Enhanced Metrics templates on the Workbooks page." lightbox="media/concepts-workbooks/overview-enhanced-metrics.png":::

## Related content

- [Access control in Azure workbooks](/azure/azure-monitor/visualize/workbooks-overview#access-control)
- [Visualization options in Azure workbooks](/azure/azure-monitor/visualize/workbooks-visualizations)
- [Enhanced metrics](concepts-monitoring.md#enhanced-metrics)
- [Autovacuum metrics](concepts-monitoring.md#autovacuum-metrics)
