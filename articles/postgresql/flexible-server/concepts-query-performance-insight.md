---
title: Query Performance Insight
description: This article describes the Query Performance Insight feature in  Azure Database for PostgreSQL - Flexible Server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 09/29/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Query Performance Insight in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Query Performance Insight provides intelligent query analysis for Azure Database for PostgreSQL flexible server databases. It helps identify the top resource consuming and long-running queries in your workload. This helps you find the queries to optimize to improve overall workload performance and efficiently use the resource that you're paying for. Query Performance Insight helps you spend less time troubleshooting database performance by providing:

>[!div class="checklist"]
> * Identify what your long running queries, and how they change over time.
> * Determine the wait types affecting those queries.
> * Details on top database queries by Calls (execution count), by data-usage, by IOPS and by Temporary file usage (potential tuning candidates for performance improvements).
> * The ability to drill down into details of a query, to view the Query ID and history of resource utilization.
> * Deeper insight into overall databases resource consumption.

## Prerequisites

1. **[Query Store](concepts-query-store.md)** is enabled on your database. If Query Store isn't running, the Azure portal prompts you to enable it. To enable Query Store, refer [here](concepts-query-store.md#enable-query-store).

> [!NOTE]
> **Query Store** is currently **disabled**. Query Performance Insight depends on Query Store data. You need to enable it by setting the dynamic server parameter `pg_qs.query_capture_mode` to either **ALL** or **TOP**.

2. **[Query Store Wait Sampling](concepts-query-store.md)** is enabled on your database. If Query Store Wait Sampling isn't running, the Azure portal prompts you to enable it. To enable Query Store Wait Sampling, refer [here](concepts-query-store.md#enable-query-store-wait-sampling).

> [!NOTE]
> **Query Store Wait Sampling** is currently **disabled**. Query Performance Insight depends on Query Store wait sampling data. You need to enable it by setting the dynamic server parameter `pgms_wait_sampling.query_capture_mode` to **ALL**.

3. **[Log analytics workspace](howto-configure-and-access-logs.md)** is configured for storing 3 log categories including - Azure Database for PostgreSQL flexible server Sessions logs, Azure Database for PostgreSQL flexible server Query Store and Runtime, and Azure Database for PostgreSQL flexible server Query Store Wait Statistics. To configure log analytics, refer [Log analytics workspace](howto-configure-and-access-logs.md#configure-diagnostic-settings).

> [!NOTE]
> The **Query Store data isn't being transmitted to the log analytics workspace**. The Azure Database for PostgreSQL flexible server logs (Sessions data / Query Store Runtime / Query Store Wait Statistics) aren't being sent to the log analytics workspace, which is necessary to use Query Performance Insight. To configure the diagnostic settings for Azure Database for PostgreSQL flexible server and send the data to a log analytics workspace, please refer to [Configure and access logs in Azure Database for PostgreSQL - Flexible Server](how-to-configure-and-access-logs.md).

## Permissions

You need the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) permissions assigned to Azure Database for PostgreSQL flexible server so that you can use Query Performance Insight:
  - Microsoft.DBforPostgreSQL/flexibleServers/configurations/read
  - Microsoft.DBforPostgreSQL/flexibleServers/providers/Microsoft.Insights/diagnosticSettings/read
  - Microsoft.DBforPostgreSQL/flexibleServers/read
  - Microsoft.Insights/Components/read
  - Microsoft.Insights/DiagnosticSettings/read
  - Microsoft.Insights/DiagnosticSettingsCategories/read
  - Microsoft.Insights/Logs/AzureDiagnostics/read
  - Microsoft.Insights/Logs/read

## Using Query Performance Insight

The Query Performance Insight view in the Azure portal surfaces visualizations on key information from Query Store. Query Performance Insight is easy to use:

1. Open the Azure portal and find an Azure Database for PostgreSQL flexible server instance that you want to examine.
2. From the left-side menu, open **Intelligent Performance** > **Query Performance Insight**.
3. Select a **time range** for investigating queries.
4. On the first tab, review the list of **Long Running Queries**.
5. Use sliders or zoom to change the observed interval.
:::image type="content" source="./media/concepts-query-performance-insight/1-long-running-queries.png" alt-text="Screenshot of using sliders to change the observed interval.":::

6. Optionally, you can select the **custom** to specify a time range.

> [!NOTE]
> For Azure Database for PostgreSQL flexible server to render the information in Query Performance Insight, **Query Store needs to capture a couple hours of data**. If the database has no activity or if Query Store was not active during a certain period, the charts will be empty when Query Performance Insight displays that time range. You can enable Query Store at any time if it's not running. For more information, see [Best practices with Query Store](concepts-query-store-best-practices.md).

7. To **view details** of a specific query, click the `QueryId Snapshot` dropdown.
:::image type="content" source="./media/concepts-query-performance-insight/2-individual-query-details.png" alt-text="Screenshot of viewing details of a specific query.":::

8. To get the **Query Text** of a specific query, connect to the `azure_sys` database on the server and query `query_store.query_texts_view` with the `QueryId`.
:::image type="content" source="./media/concepts-query-performance-insight/3-view-query-text.png" alt-text="Screenshot of getting query text of a specific query.":::

9. On the Consecutive tabs, you can find other query insights including:
    >[!div class="checklist"]
    > * Wait Statistics
    > * Top Queries by Calls
    > * Top Queries by Data-Usage
    > * Top Queries by IOPS
    > * Top Queries by Temporary Files

## Considerations

* Query Performance Insight isn't available for [read replicas](concepts-read-replicas.md).
* For Query Performance Insight to function, data must exist in the Query Store. Query Store is an opt-in feature, so it isn't enabled by default on a server. Query store is enabled or disabled globally for all databases on a given server and can't be turned on or off per database.
* Enabling Query Store on the Burstable pricing tier may negatively impact performance; therefore, we don't recommend enabling it on that tier.


## Next steps

- Learn more about [monitoring and tuning](concepts-monitoring.md) in Azure Database for PostgreSQL flexible server.
