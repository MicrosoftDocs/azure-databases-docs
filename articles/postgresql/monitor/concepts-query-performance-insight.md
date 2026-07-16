---
title: Query Performance Insight in Azure Database for PostgreSQL Flexible Server
description: This article describes the Query Performance Insight feature in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to identify the top resource-consuming queries in my Azure Database for PostgreSQL flexible server, so that I can optimize them to improve workload performance.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Query Performance Insight in Azure Database for PostgreSQL flexible server

Query Performance Insight provides intelligent query analysis for databases in an Azure Database for PostgreSQL flexible server. It helps you identify the top resource-consuming and long-running queries in your workload. This information helps you find the queries to optimize to improve overall workload performance and efficiently use the resource that you're paying for. Query Performance Insight helps you spend less time troubleshooting database performance by providing:

>[!div class="checklist"]
> * Identification of your long running queries, and how they change over time.
> * Determination of the wait types affecting those queries.
> * Details on top database queries by calls (execution count), by data-usage, by IOPS, and by temporary file usage (potential tuning candidates for performance improvements).
> * The ability to drill down into details of a query, to view the query ID and history of resource utilization.
> * Deeper insight into overall databases resource consumption.

## Prerequisites

- **[Query store](concepts-query-store.md)** is enabled on your database. If query store isn't running, the Azure portal prompts you to enable it. To enable query store, see [Enable query store](concepts-query-store.md#enable-query-store).

> [!NOTE]
> **Query store** is currently **disabled**. Query Performance Insight depends on query store data. You need to enable it by setting the dynamic parameter `pg_qs.query_capture_mode` to either **ALL** or **TOP**.

- **[Query store wait sampling](concepts-query-store.md)** is enabled on your database. If query store wait sampling isn't running, the Azure portal prompts you to enable it. To enable query store wait sampling, see [Enable query store wait sampling](concepts-query-store.md#enable-query-store-wait-sampling).

> [!NOTE]
> **Query store wait sampling** is currently **disabled**. Query Performance Insight depends on query store wait sampling data. You need to enable it by setting the dynamic parameter `pgms_wait_sampling.query_capture_mode` to **ALL**.

- **[Log Analytics workspace](how-to-configure-and-access-logs.md)** is configured for storing three log categories including - PostgreSQL Sessions data, PostgreSQL query store Runtime, and PostgreSQL query store Wait Statistics. To configure log analytics, see [Configure and access logs](how-to-configure-and-access-logs.md).

> [!NOTE]
> **Query store data isn't transmitted to the log analytics workspace**. The logs (Sessions data, Query Store Runtime, and Query Store Wait Statistics) aren't sent to the log analytics workspace, which is necessary to use Query Performance Insight. To configure the diagnostic settings for an Azure Database for PostgreSQL flexible server and send the data to a log analytics workspace, see [Configure and access logs in Azure Database for PostgreSQL](how-to-configure-and-access-logs.md).

## Permissions

To use Query Performance Insight with Azure Database for PostgreSQL flexible server, you need the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) permissions assigned to your PostgreSQL flexible server:

  - Microsoft.DBforPostgreSQL/flexibleServers/configurations/read
  - Microsoft.DBforPostgreSQL/flexibleServers/providers/Microsoft.Insights/diagnosticSettings/read
  - Microsoft.DBforPostgreSQL/flexibleServers/read
  - Microsoft.Insights/Components/read
  - Microsoft.Insights/DiagnosticSettings/read
  - Microsoft.Insights/DiagnosticSettingsCategories/read
  - Microsoft.Insights/Logs/AzureDiagnostics/read
  - Microsoft.Insights/Logs/read

## Using Query Performance Insight

The Query Performance Insight view in the Azure portal provides visualizations on key information from query store. Query Performance Insight is easy to use:

1. Open the Azure portal and find an Azure Database for PostgreSQL flexible server that you want to examine.

1. From the left-side menu, open **Intelligent Performance** > **Query Performance Insight**.

1. Select a **time range** for investigating queries.

1. On the first tab, review the list of **Long Running Queries**.

1. Use sliders or zoom to change the observed interval.

    :::image type="content" source="./media/concepts-query-performance-insight/1-long-running-queries.png" alt-text="Screenshot showing the use of sliders to change the observed interval." lightbox="./media/concepts-query-performance-insight/1-long-running-queries.png":::

1. Optionally, select **custom** to specify a time range.

1. To **view details** of a specific query, select the `QueryId Snapshot` dropdown.

    :::image type="content" source="./media/concepts-query-performance-insight/2-individual-query-details.png" alt-text="Screenshot showing details of a specific query." lightbox="./media/concepts-query-performance-insight/2-individual-query-details.png":::

1. To get the **Query Text** of a specific query, connect to the `azure_sys` database on the server and query `query_store.query_texts_view` with the `QueryId`.

    :::image type="content" source="./media/concepts-query-performance-insight/3-view-query-text.png" alt-text="Screenshot showing how to get query text of a specific query." lightbox="./media/concepts-query-performance-insight/3-view-query-text.png":::

1. On the consecutive tabs, you can find other query insights, including:

    >[!div class="checklist"]
    > * Wait Statistics
    > * Top Queries by Calls
    > * Top Queries by Data-Usage
    > * Top Queries by IOPS
    > * Top Queries by Temporary Files

> [!NOTE]
> For an Azure Database for PostgreSQL flexible server to render the information in Query Performance Insight, **Query store needs to capture a couple hours of data**. If the database has no activity or if query store wasn't active during a certain period, the charts are empty when Query Performance Insight displays that time range. You can enable query store at any time if it's not running. For more information, see [Best practices with query store](concepts-query-store-best-practices.md).

## Considerations

* Query Performance Insight isn't available for [read replicas](../read-replica/concepts-read-replicas.md).
* For Query Performance Insight to work, the query store must have data. Since query store is an opt-in feature, it's not enabled by default on a server. You enable or disable query store globally for all databases on a server. You can't turn it on or off for individual databases.
* Enabling query store on the Burstable pricing tier might negatively affect performance. Don't enable it on that tier.

## Related content

- [Monitor metrics in Azure Database for PostgreSQL](concepts-monitoring.md).
