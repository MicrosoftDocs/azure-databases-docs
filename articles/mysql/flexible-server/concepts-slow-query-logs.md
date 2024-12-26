---
title: Slow Query Logs
description: Describes the slow query logs available in Azure Database for MySQL - Flexible Server.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Slow query logs in Azure Database for MySQL - Flexible Server

In Azure Database for MySQL Flexible Server, the slow query log is available to users to configure and access. Slow query logs are disabled by default and can be enabled to assist with identifying performance bottlenecks during troubleshooting.

For more information about the MySQL slow query log, see the [slow query log section](https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html) in the MySQL engine documentation.

## Configure slow query logging

By default, the slow query log is disabled. To enable logs, set the `slow_query_log` server parameter to *ON*. This can be configured using the Azure portal or Azure CLI.

Other parameters you can adjust to control slow query logging behavior include:

- **long_query_time**: log a query if it takes longer than `long_query_time` (in seconds) to complete. The default is 10 seconds. Server parameter `long_query_time` applies globally to all newly established connections in MySQL. However, it doesn't affect threads that are already connected. It's recommended to reconnect to Azure Database for MySQL Flexible Server from the application, or restarting the server will help clear out threads with older values of "long_query_time" and apply the updated parameter value.
- **log_slow_admin_statements**: determines if administrative statements (ex. `ALTER_TABLE`, `ANALYZE_TABLE`) are logged.
- **log_queries_not_using_indexes**: determines if queries that don't use indexes are logged.
- **log_throttle_queries_not_using_indexes**: limits the number of non-indexed queries that can be written to the slow query log. This parameter takes effect when `log_queries_not_using_indexes` is set to *ON*

> [!IMPORTANT]  
> If your tables are not indexed, setting the `log_queries_not_using_indexes` and `log_throttle_queries_not_using_indexes` parameters to **ON** might affect MySQL performance since all queries running against these non-indexed tables will be written to the slow query log.

See the MySQL [slow query log documentation](https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html) for full descriptions of the slow query log parameters.

## Access slow query logs

Slow query logs are integrated with Azure Monitor diagnostic settings. Once you've enabled slow query logs on your Azure Database for MySQL Flexible Server instance, you can emit them to Azure Monitor logs, Event Hubs, or Azure Storage. To learn more about diagnostic settings, see the [diagnostic logs documentation](/azure/azure-monitor/essentials/platform-logs-overview). To learn more about how to enable diagnostic settings in the Azure portal, see the [slow query log portal article](tutorial-query-performance-insights.md#set-up-diagnostics).

> [!NOTE]  
> Premium Storage accounts are not supported if you are sending the logs to Azure storage via diagnostics and settings.

The following table describes the output of the slow query log. Depending on the output method, the fields included and the order in which they appear might vary.

| **Property** | **Description** |
| --- | --- |
| `TenantId` | Your tenant ID |
| `SourceSystem` | `Azure` |
| `TimeGenerated` [UTC] | Time stamp when the log was recorded in UTC |
| `Type` | Type of the log. Always `AzureDiagnostics` |
| `SubscriptionId` | GUID for the subscription that the server belongs to |
| `ResourceGroup` | Name of the resource group the server belongs to |
| `ResourceProvider` | Name of the resource provider. Always `MICROSOFT.DBFORMYSQL` |
| `ResourceType` | `Servers` |
| `ResourceId` | Resource URI |
| `Resource` | Name of the server |
| `Category` | `MySqlSlowLogs` |
| `OperationName` | `LogEvent` |
| `Logical_server_name_s` | Name of the server |
| `start_time_t` [UTC] | Time the query began |
| `query_time_s` | Total time in seconds the query took to execute |
| `lock_time_s` | Total time in seconds the query was locked |
| `user_host_s` | Username |
| `rows_sent_s` | Number of rows sent |
| `rows_examined_s` | Number of rows examined |
| `last_insert_id_s` | [last_insert_id](https://dev.mysql.com/doc/refman/5.7/en/information-functions.html#function_last-insert-id) |
| `insert_id_s` | Insert ID |
| `sql_text_s` | Full query |
| `server_id_s` | The server's ID |
| `thread_id_s` | Thread ID |
| `\_ResourceId` | Resource URI |

> [!NOTE]  
> For `sql_text_s`, log will be truncated if it exceeds 2048 characters.

## Analyze logs in Azure Monitor Logs

Once your slow query logs are piped to Azure Monitor Logs through Diagnostic Logs, you can perform further analysis of your slow queries. Below are some sample queries to help you get started. Make sure to update the below with your server name.

- Queries longer than 10 seconds on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>'
    | where Category == 'MySqlSlowLogs'
    | project TimeGenerated, Resource , event_class_s, start_time_t , query_time_d, sql_text_s
    | where query_time_d > 10
    ```

- List top 5 longest queries on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>'
    | where Category == 'MySqlSlowLogs'
    | project TimeGenerated, Resource , event_class_s, start_time_t , query_time_d, sql_text_s
    | order by query_time_d desc
    | take 5
    ```

- Summarize slow queries by minimum, maximum, average, and standard deviation query time on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>'
    | where Category == 'MySqlSlowLogs'
    | project TimeGenerated, Resource , event_class_s, start_time_t , query_time_d, sql_text_s
    | summarize count(), min(query_time_d), max(query_time_d), avg(query_time_d), stdev(query_time_d), percentile(query_time_d, 95) by Resource
    ```

- Graph the slow query distribution on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>'
    | where Category == 'MySqlSlowLogs'
    | project TimeGenerated, Resource , event_class_s, start_time_t , query_time_d, sql_text_s
    | summarize count() by Resource , bin(TimeGenerated, 5m)
    | render timechart
    ```

- Display queries longer than 10 seconds across all Azure Database for MySQL Flexible Server instances with Diagnostic Logs enabled

    ```kusto
    AzureDiagnostics
    | where Category == 'MySqlSlowLogs'
    | project TimeGenerated, Resource , event_class_s, start_time_t , query_time_d, sql_text_s
    | where query_time_d > 10
    ```

## Related content

- [audit logs](concepts-audit-logs.md)
- [Tutorial: Query Performance Insight for Azure Database for MySQL - Flexible Server](tutorial-query-performance-insights.md)
- [How to configure slow query logs from the Azure CLI](scripts/sample-cli-slow-query-logs.md)
