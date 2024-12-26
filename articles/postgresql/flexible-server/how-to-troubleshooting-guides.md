---
title: Troubleshooting guides - Azure portal
description: Learn how to use troubleshooting guides for Azure Database for PostgreSQL - Flexible Server from the Azure portal.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 06/25/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Use the troubleshooting guides in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this article, you learn how to use troubleshooting guides for Azure Database for PostgreSQL flexible server from the Azure portal. To learn more about troubleshooting guides, see the [overview](concepts-troubleshooting-guides.md).

## Prerequisites

To effectively troubleshoot a specific issue, you need to make sure that you have all the necessary data in place. 
Each troubleshooting guide requires a specific set of data, which is sourced from three separate features: [Diagnostic settings](how-to-configure-and-access-logs.md), [Query Store](concepts-query-store.md), and [Enhanced metrics](concepts-monitoring.md#enabling-enhanced-metrics).
All troubleshooting guides require logs to be sent to a Log Analytics workspace, but the specific category of logs to be captured may vary depending on the particular guide. 

Please, follow the steps described in [Configure and Access Logs - Azure Database for PostgreSQL - Flexible Server](howto-configure-and-access-logs.md) to configure diagnostic settings and send the logs to a Log Analytics workspace.

Query Store, and Enhanced metrics are configured via Server parameters. Please follow the steps described in the configure server parameters in Azure Database for PostgreSQL flexible server articles for [Azure portal](howto-configure-server-parameters-using-portal.md) or [Azure CLI](howto-configure-server-parameters-using-cli.md).

The table below provides information on the required log categories for each troubleshooting guide, as well as the necessary Query Store, Enhanced metrics and Server parameters prerequisites.

| Troubleshooting guide | Diagnostic settings log categories and metrics                                                                                                         | Query Store                                                                             | Enhanced metrics                    | Server parameters           |
|:----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-------------------------------------|-----------------------------|
| CPU                   | PostgreSQL Server Logs<br/>PostgreSQL Server Sessions data<br/>PostgreSQL Server Query Store Runtime<br/>AllMetrics                                    | pg_qs.query_capture_mode to TOP or ALL                                                  | metrics.collector_database_activity | N/A                         |
| Memory                | PostgreSQL Server Logs<br/>PostgreSQL Server Sessions data<br/>PostgreSQL Server Query Store Runtime                                                   | pg_qs.query_capture_mode to TOP or ALL                                                  | metrics.collector_database_activity | N/A                         |
| IOPS                  | PostgreSQL Server Query Store Runtime<br/>PostgreSQL Server Logs<br/>PostgreSQL Server Sessions data<br/>PostgreSQL Server Query Store Wait Statistics | pg_qs.query_capture_mode to TOP or ALL<br/>pgms_wait_sampling.query_capture_mode to ALL | metrics.collector_database_activity | track_io_timing to ON       |
| Temporary files       | PostgreSQL Server Sessions data<br/>PostgreSQL Server Query Store Runtime<br/>PostgreSQL Server Query Store Wait Statistics                            | pg_qs.query_capture_mode to TOP or ALL<br/>pgms_wait_sampling.query_capture_mode to ALL | metrics.collector_database_activity | N/A                         |
| Autovacuum monitoring | PostgreSQL Server Logs<br/>PostgreSQL Autovacuum and schema statistics<br/>PostgreSQL remaining transactions                                           | N/A                                                                                     | N/A                                 | log_autovacuum_min_duration |
| Autovacuum blockers   | PostgreSQL Server Sessions data<br/>PostgreSQL remaining transactions                                                                                  | N/A                                                                                     | N/A                                 | N/A                         |


> [!NOTE]
> Please note that if you have recently enabled diagnostic settings, query store, enhanced metrics or server parameters, it may take some time for the data to be populated. Additionally, if there has been no activity on the database within a certain time frame, the charts might appear empty. In such cases, try changing the time range to capture relevant data. Be patient and allow the system to collect and display the necessary data before proceeding with your troubleshooting efforts.

## Using the troubleshooting guides

To use the troubleshooting guides, follow these steps:

1. Open the Azure portal and find an Azure Database for PostgreSQL flexible server instance that you want to examine.

2. From the left-side menu, under the *Monitoring* section, select *Troubleshooting guides*.

3. Navigate to the top of the page where you will find a series of tabs, each representing one of the six problems you may wish to resolve. Click on the relevant tab.

   :::image type="content" source="./media/how-to-troubleshooting-guides/portal-blade-overview.png" alt-text="Screenshot of Troubleshooting guides - tabular view.":::

4. Select the period of time which you want to analyze.

    :::image type="content" source="./media/how-to-troubleshooting-guides/time-range.png" alt-text="Screenshot of time range picker.":::

5. Follow the step-by-step instructions provided by the guide. Pay close attention to the charts and data visualizations plotted within the troubleshooting steps, as they can help you identify any inaccuracies or anomalies. Use this information to effectively diagnose and resolve the problem at hand.

### Retrieving the text of queries collected by query store

Due to privacy considerations, certain information such as query text and usernames may not be displayed within the Azure portal. 
To retrieve the text of those queries collected by query store, you need to log in to your Azure Database for PostgreSQL flexible server instance. 
Using the PostgreSQL client of your choice, access the `azure_sys` database where query store data is stored. 
Once connected, query the `query_store.query_texts_view view` to retrieve the desired query text.

:::image type="content" source="./media/how-to-troubleshooting-guides/retrieve-query-text.png" alt-text="Screenshot of retrieving the Query Text.":::

### Retrieving the name of a user or role

For privacy reasons, the Azure portal displays the role ID from the PostgreSQL metadata (pg_catalog) rather than the actual username. 
To retrieve the username, you can query the `pg_roles` view or use the query shown below in your PostgreSQL client of choice, such as Azure Cloud Shell and the `psql` tool:

```sql
SELECT 'UserID'::regrole;
```

In the following example you would be retrieving the name of the user or role whose identifier is 24776.

```sql
SELECT '24776'::regrole;
```

:::image type="content" source="./media/how-to-troubleshooting-guides/retrieve-username.png" alt-text="Screenshot of retrieving the Username.":::

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Configure intelligent tuning for Azure Database for PostgreSQL - Flexible Server](how-to-enable-intelligent-performance-portal.md).
- [Troubleshooting guides for Azure Database for PostgreSQL - Flexible Server](concepts-troubleshooting-guides.md).
- [Autovacuum tuning in Azure Database for PostgreSQL - Flexible Server](how-to-autovacuum-tuning.md).
- [Troubleshoot high IOPS utilization in Azure Database for PostgreSQL - Flexible Server](how-to-high-io-utilization.md).
- [Best practices for uploading data in bulk in Azure Database for PostgreSQL - Flexible Server](how-to-bulk-load-data.md).
- [Troubleshoot high CPU utilization in Azure Database for PostgreSQL - Flexible Server](how-to-high-cpu-utilization.md).
- [Query Performance Insight in Azure Database for PostgreSQL - Flexible Server](concepts-query-performance-insight.md).
