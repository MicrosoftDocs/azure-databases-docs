---
title: Query Performance Insight in Azure HorizonDB
description: This article describes the Query Performance Insight feature in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
---

# Query Performance Insight in Azure HorizonDB

Query Performance Insight provides intelligent query analysis for databases in an Azure HorizonDB instance. It helps identify the top resource consuming and long-running queries in your workload. This helps you find the queries to optimize to improve overall workload performance and efficiently use the resource that you're paying for. Query Performance Insight helps you spend less time troubleshooting database performance by providing:

> [!div class="checklist"]
> * Identify what your long running queries, and how they change over time.
> * Determine the wait types affecting those queries.
> * Details on top database queries by Calls (execution count), by data-usage, by IOPS and by Temporary file usage (potential tuning candidates for performance improvements).
> * The ability to drill down into details of a query, to view the Query ID and history of resource utilization.
> * Deeper insight into overall databases resource consumption.

## Prerequisites

1. **[Query store in Azure HorizonDB](concepts-query-store.md)** is enabled on your database. If Query Store isn't running, the Azure portal prompts you to enable it. To enable Query Store, refer [here](concepts-query-store.md#enable-query-store).

> [!NOTE]  
> **Query Store** is currently **disabled**. Query Performance Insight depends on Query Store data. You need to enable it by setting the dynamic server parameter `pg_qs.query_capture_mode` to either **ALL** or **TOP**.

1. **[Query store in Azure HorizonDB](concepts-query-store.md)** is enabled on your database. If Query Store Wait Sampling isn't running, the Azure portal prompts you to enable it. To enable Query Store Wait Sampling, refer [here](concepts-query-store.md#enable-query-store-wait-sampling).

> [!NOTE]  
> **Query Store Wait Sampling** is currently **disabled**. Query Performance Insight depends on Query Store wait sampling data. You need to enable it by setting the dynamic server parameter `pgms_wait_sampling.query_capture_mode` to **ALL**.

1. **[Configure and access logs in Azure HorizonDB](how-to-configure-and-access-logs.md)** is configured for storing 3 log categories including - Azure HorizonDB instance Sessions logs, Azure HorizonDB instance Query Store and Runtime, and Azure HorizonDB instance Query Store Wait Statistics. To configure log analytics, refer [Log analytics workspace](how-to-configure-and-access-logs.md#configure-diagnostic-settings).

> [!NOTE]  
> The **Query Store data isn't being transmitted to the log analytics workspace**. The logs (Sessions data / Query Store Runtime / Query Store Wait Statistics) aren't being sent to the log analytics workspace, which is necessary to use Query Performance Insight. To configure the diagnostic settings for an Azure HorizonDB instance and send the data to a log analytics workspace, please refer to [Configure and access logs in Azure HorizonDB](how-to-configure-and-access-logs.md).

## Permissions

You need the following [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) permissions assigned to Azure Database for your PostgreSQL flexible server instance so that you can use Query Performance Insight:

- Microsoft.DBforPostgreSQL/flexibleServers/configurations/read
- Microsoft.DBforPostgreSQL/flexibleServers/providers/Microsoft.Insights/diagnosticSettings/read
- Microsoft.DBforPostgreSQL/flexibleServers/read
- Microsoft.Insights/Components/read
- Microsoft.Insights/DiagnosticSettings/read
- Microsoft.Insights/DiagnosticSettingsCategories/read
- Microsoft.Insights/Logs/AzureDiagnostics/read
- Microsoft.Insights/Logs/read

<a id="using-query-performance-insight"></a>

## Use Query Performance Insight

The Query Performance Insight view in the Azure portal surfaces visualizations on key information from Query Store. Query Performance Insight is easy to use:

1. Open the Azure portal and find an Azure HorizonDB instance that you want to examine.
1. From the left-side menu, open **Intelligent Performance** > **Query Performance Insight**.
1. Select a **time range** for investigating queries.
1. On the first tab, review the list of **Long Running Queries**.
1. Use sliders or zoom to change the observed interval.
   :::image type="content" source="media/concepts-query-performance-insight/1-long-running-queries.png" alt-text="Screenshot of using sliders to change the observed interval." lightbox="media/concepts-query-performance-insight/1-long-running-queries.png" :::

1. Optionally, you can select the **custom** to specify a time range.

> [!NOTE]  
> For an Azure HorizonDB instance to render the information in Query Performance Insight, **Query Store needs to capture a couple hours of data**. If the database has no activity or if Query Store was not active during a certain period, the charts will be empty when Query Performance Insight displays that time range. You can enable Query Store at any time if it's not running. For more information, see [Best practices for query store in Azure HorizonDB](concepts-query-store-best-practices.md).

1. To **view details** of a specific query, select the `QueryId Snapshot` dropdown list.
   :::image type="content" source="media/concepts-query-performance-insight/2-individual-query-details.png" alt-text="Screenshot of viewing details of a specific query." lightbox="media/concepts-query-performance-insight/2-individual-query-details.png" :::

1. To get the **Query Text** of a specific query, connect to the `azure_sys` database on the server and query `query_store.query_texts_view` with the `QueryId`.
   :::image type="content" source="media/concepts-query-performance-insight/3-view-query-text.png" alt-text="Screenshot of getting query text of a specific query." lightbox="media/concepts-query-performance-insight/3-view-query-text.png" :::

1. On the Consecutive tabs, you can find other query insights including:
   > [!div class="checklist"]
   > * Wait Statistics
   > * Top Queries by Calls
   > * Top Queries by Data-Usage
   > * Top Queries by IOPS
   > * Top Queries by Temporary Files

## Considerations

- Query Performance Insight isn't available for [read replicas](../read-replica/concepts-read-replicas.md).
- For Query Performance Insight to function, data must exist in the Query Store. Query Store is an opt-in feature, so it isn't enabled by default on a server. Query store is enabled or disabled globally for all databases on a given server and can't be turned on or off per database.
- Enabling Query Store on the Burstable pricing tier might negatively impact performance; therefore, we don't recommend enabling it on that tier.

## Related content

- [Monitor metrics in Azure HorizonDB](concepts-monitoring.md)
