---
title: Monitor Azure Database for MySQL - Flexible Server
description: Learn how to monitor Azure Database for MySQL - Flexible Server using Azure Monitor, including data collection, analysis, and alerting.
ms.date: 01/22/2025
ms.custom: horz-monitor
ms.topic: conceptual
author: markingmyname
ms.author: maghan
ms.service: azure-database-mysql
---
# Monitor Azure Database for MySQL - Flexible Server

[!INCLUDE [azmon-horz-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-intro.md)]
 
## Collect data with Azure Monitor 

This table describes how you can collect data to monitor your service, and what you can do with the data once collected:

|Data to collect|Description|How to collect and route the data|Where to view the data|Supported data|
|---------|---------|---------|---------|---------|
|Metric data|Metrics are numerical values that describe an aspect of a system at a particular point in time. Metrics can be aggregated using algorithms, compared to other metrics, and analyzed for trends over time.|- Collected automatically at regular intervals.</br> - You can route some platform metrics to a Log Analytics workspace to query with other data. Check the **DS export** setting for each metric to see if you can use a diagnostic setting to route the metric data.|[Metrics explorer](/azure/azure-monitor/essentials/metrics-getting-started)| [Azure Database for MySQL - Flexible Server metrics supported by Azure Monitor](monitor-mysql-flexible-server-reference.md#metrics)|
|Resource log data|Logs are recorded system events with a timestamp. Logs can contain different types of data, and be structured or free-form text. You can route resource log data to Log Analytics workspaces for querying and analysis.|[Create a diagnostic setting](/azure/azure-monitor/essentials/create-diagnostic-settings) to collect and route resource log data.| [Log Analytics](/azure/azure-monitor/learn/quick-create-workspace)|[Azure Database for MySQL - Flexible Server resource log data supported by Azure Monitor](monitor-mysql-flexible-server-reference.md#resource-logs)  |
|Activity log data|The Azure Monitor activity log provides insight into subscription-level events. The activity log includes information like when a resource is modified or a virtual machine is started.|- Collected automatically.</br> - [Create a diagnostic setting](/azure/azure-monitor/essentials/create-diagnostic-settings) to a Log Analytics workspace at no charge.|[Activity log](/azure/azure-monitor/essentials/activity-log)|  |

[!INCLUDE [azmon-horz-supported-data](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-supported-data.md)]

## Built in monitoring for Azure Database for MySQL - Flexible Server

### Server logs

In Azure Database for MySQL Flexible Server, users can configure and download server logs to assist with troubleshooting efforts. With this feature enabled, an Azure Database for MySQL Flexible Server instance starts capturing events of the selected log type and writes them to a file. You can then use the Azure portal and Azure CLI to download the files to work with them.

The server logs feature is disabled by default. For information about how to enable server logs, see [Enable and download server logs for Azure Database for MySQL - Flexible Server](how-to-server-logs-portal.md)

Server logs support enabling and downloading [slow query logs](concepts-slow-query-logs.md) and [error logs](concepts-error-logs.md).
To perform a historical analysis of your data, in the Azure portal, on the Diagnostics settings pane for your server, add a diagnostic setting to send the logs to the Log Analytics workspace, Azure Storage, or event hubs. For more information, see [Set up diagnostics](./tutorial-query-performance-insights.md#set-up-diagnostics).

When logging is enabled for an Azure Database for MySQL Flexible Server instance, logs are available up to seven days from their creation. If the total size of the available logs exceeds 7 GB, then the oldest files are deleted until space is available.
The 7-GB storage limit for server logs is available free of cost and can't be extended.
Logs are rotated every 24 hours or 500 MB, whichever comes first.

### Slow query logs in Azure Database for MySQL - Flexible Server

In Azure Database for MySQL Flexible Server, the slow query log is available to users to configure and access. Slow query logs are disabled by default and can be enabled to assist with identifying performance bottlenecks during troubleshooting.

For more information about the MySQL slow query log, see the [slow query log section](https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html) in the MySQL engine documentation.

#### Configure slow query logging

By default, the slow query log is disabled. To enable logs, set the `slow_query_log` server parameter to *ON*. This can be configured using the Azure portal or Azure CLI.

Other parameters you can adjust to control slow query logging behavior include:

- **long_query_time**: log a query if it takes longer than `long_query_time` (in seconds) to complete. The default is 10 seconds. Server parameter `long_query_time` applies globally to all newly established connections in MySQL. However, it doesn't affect threads that are already connected. It's recommended to reconnect to Azure Database for MySQL Flexible Server from the application, or restarting the server will help clear out threads with older values of "long_query_time" and apply the updated parameter value.
- **log_slow_admin_statements**: determines if administrative statements (ex. `ALTER_TABLE`, `ANALYZE_TABLE`) are logged.
- **log_queries_not_using_indexes**: determines if queries that don't use indexes are logged.
- **log_throttle_queries_not_using_indexes**: limits the number of non-indexed queries that can be written to the slow query log. This parameter takes effect when `log_queries_not_using_indexes` is set to *ON*

> [!IMPORTANT]  
> If your tables are not indexed, setting the `log_queries_not_using_indexes` and `log_throttle_queries_not_using_indexes` parameters to **ON** might affect MySQL performance since all queries running against these non-indexed tables will be written to the slow query log.

See the MySQL [slow query log documentation](https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html) for full descriptions of the slow query log parameters.

#### Access slow query logs

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

[!INCLUDE [azmon-horz-tools](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-tools.md)]

[!INCLUDE [azmon-horz-export-data](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-export-data.md)]

[!INCLUDE [azmon-horz-kusto](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-kusto.md)]

### Recommended Kusto queries for Azure Database for MySQL - Flexible Server

You can use slow query logs to find candidates for optimization. After your slow query logs are piped to Azure Monitor Logs through Diagnostic Logs, you can perform further analysis of your slow queries. Below are some sample queries to help you get started. Make sure to update the below with your server name.

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

[!INCLUDE [azmon-horz-alerts-part-one](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-alerts-part-one.md)]

### Recommended Azure Monitor alert rules for Azure Database for MySQL - Flexible Server

The following table lists common and recommended alert rules for Azure Database for MySQL - Flexible Server.

| Alert type | Condition | Examples  |
|:---|:---|:---|
| Metric | |  |
| Log search |  | |
| Activity Log | | |
| Service Health | | |
| Resource Health | | |

[!INCLUDE [azmon-horz-alerts-part-two](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-alerts-part-two.md)]

[!INCLUDE [azmon-horz-advisor](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-advisor.md)]

## Related content

- [Azure Database for MySQL - Flexible Server monitoring data reference](monitor-mysql-flexible-server-reference.md)
- [Monitoring Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource)
