---
title: Monitor Azure Database for MySQL - Flexible Server
description: Learn how to monitor Azure Database for MySQL - Flexible Server using Azure Monitor, including data collection, analysis, and alerting.
author: markingmyname
ms.author: maghan
ms.date: 07/03/2025
ms.service: azure-database-mysql
ms.topic: concept-article
ms.custom:
  - horz-monitor
ai-usage: ai-assisted
---

# Monitor Azure Database for MySQL - Flexible Server

[!INCLUDE [azmon-horz-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-intro.md)]

Monitoring is essential for maintaining the health, performance, and security of your Azure Database for MySQL - Flexible Server instances. Azure Monitor provides a comprehensive solution for collecting, analyzing, and acting on telemetry from your MySQL servers. This article outlines the key monitoring capabilities available, including metrics, logs, alerting, and visualization tools, to help you proactively manage your database workloads.

## Collect data with Azure Monitor

This table describes how you can collect data to monitor your service, and what you can do with the data once collected:

| Data to collect | Description | How to collect and route the data | Where to view the data | Supported data |
| --- | --- | --- | --- | --- |
| Metric data | Metrics are numerical values that describe an aspect of a system at a particular point in time. Metrics can be aggregated using algorithms, compared to other metrics, and analyzed for trends over time. | - Collected automatically at regular intervals.<br />- You can route some platform metrics to a Log Analytics workspace to query with other data. Check the **DS export** setting for each metric to see if you can use a diagnostic setting to route the metric data. | [Metrics explorer](/azure/azure-monitor/essentials/metrics-getting-started) | [Azure Database for MySQL - Flexible Server metrics supported by Azure Monitor](concepts-monitor-mysql-reference.md#metrics) |
| Resource log data | Logs are recorded system events with a timestamp. Logs can contain different types of data, and be structured or free-form text. You can route resource log data to Log Analytics workspaces for querying and analysis. | [Create a diagnostic setting](/azure/azure-monitor/essentials/create-diagnostic-settings) to collect and route resource log data. | [Log Analytics](/azure/azure-monitor/learn/quick-create-workspace) | [Azure Database for MySQL - Flexible Server resource log data supported by Azure Monitor](concepts-monitor-mysql-reference.md#resource-logs) |
| Activity log data | The Azure Monitor activity log provides insight into subscription-level events. The activity log includes information like when a resource is modified or a virtual machine is started. | - Collected automatically.<br />- [Create a diagnostic setting](/azure/azure-monitor/essentials/create-diagnostic-settings) to a Log Analytics workspace at no charge. | [Activity log](/azure/azure-monitor/essentials/activity-log) | |

[!INCLUDE [azmon-horz-supported-data](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-supported-data.md)]

### Known Issues

Server metrics fail to generate when the server parameter for `character_set_server` is set to **UTF16**. This occurs because the metrics collection task relies on the C# MySQL connector, which has compatibility issues with UTF16. We recommend customers use an alternative character set and restart the server after updating the configuration to restore metrics functionality.

## Built in monitoring for Azure Database for MySQL - Flexible Server

Azure Database for MySQL - Flexible Server offers built-in resources for monitoring.

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

By default, the slow query log is disabled. To enable logs, set the `slow_query_log` server parameter to *ON*. This parameter can be configured using the Azure portal or Azure CLI.

Other parameters you can adjust to control slow query logging behavior include:

- **long_query_time**: log a query if it takes longer than `long_query_time` (in seconds) to complete. The default is 10 seconds. Server parameter `long_query_time` applies globally to all newly established connections in MySQL. However, it doesn't affect threads that are already connected. We recommended that you reconnect to Azure Database for MySQL Flexible Server from the application or restart the server to clear out threads with older values of `long_query_time` and apply the updated parameter value.
- **log_slow_admin_statements**: determines if administrative statements (ex. `ALTER_TABLE`, `ANALYZE_TABLE`) are logged.
- **log_queries_not_using_indexes**: determines if queries that don't use indexes are logged.
- **log_throttle_queries_not_using_indexes**: limits the number of nonindexed queries that can be written to the slow query log. This parameter takes effect when `log_queries_not_using_indexes` is set to *ON*

> [!IMPORTANT]  
> If your tables aren't indexed, setting the `log_queries_not_using_indexes` and `log_throttle_queries_not_using_indexes` parameters to **ON** might affect MySQL performance. All queries that run against these nonindexed tables are written to the slow query log.

See the MySQL [slow query log documentation](https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html) for full descriptions of the slow query log parameters.

#### Access slow query logs

Slow query logs are integrated with Azure Monitor diagnostic settings. After you enable slow query logs on your Azure Database for MySQL Flexible Server instance, you can emit them to Azure Monitor logs, Event Hubs, or Azure Storage. To learn more about diagnostic settings, see the [diagnostic logs documentation](/azure/azure-monitor/essentials/platform-logs-overview). To learn more about how to enable diagnostic settings in the Azure portal, see the [slow query log portal article](tutorial-query-performance-insights.md#set-up-diagnostics).

> [!NOTE]  
> Premium Storage accounts aren't supported if you're sending the logs to Azure storage via diagnostics and settings.

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
> For `sql_text_s`, log is truncated if it exceeds 2,048 characters.

### Track database activity with Audit Logs

Azure Database for MySQL flexible server provides users with the ability to configure audit logs. Audit logs can be used to track database-level activity including connection, admin, DDL, and DML events. These types of logs are commonly used for compliance purposes.

#### Configure audit logging

> [!IMPORTANT]  
> We recommend to only log the event types and users required for your auditing purposes. This approach helps to ensure your server's performance isn't heavily affected and a minimum amount of data is collected.

By default, audit logs are disabled. To enable them, set the `audit_log_enabled` server parameter to *ON*. Enable audit logs using the Azure portal or Azure CLI.

Other parameters you can adjust to control audit logging behavior include:

- `audit_log_events`: controls the events to be logged. See the following table for specific audit events.
- `audit_log_include_users`: MySQL users to be included for logging. The default value for this parameter is empty, which includes all the users for logging. This parameter has higher priority over `audit_log_exclude_users`. Max length of the parameter is 512 characters. For example, wildcard value of `dev*` includes all the users with entries starting with keyword `dev` like *dev1,dev_user,dev_2*. Another example for wildcard entry for including user is `*dev` in this example, all users ending with value "dev" like "stage_dev,prod_dev,user_dev" are included in the audit log entries. Additionally, the use of a question mark `(?)` as a wildcard character is permitted in patterns.
- `audit_log_exclude_users`: MySQL users to be excluded from logging. The Max length of the parameter is 512 characters. Wildcard entries for user are also accepted to exclude users in audit logs. For example, wildcard value of `stage*` excludes all the users with entries starting with keyword `stage` like *stage1,stage_user,stage_2*. Another example for wildcard entry for excluding user is `*com`. In this example, all users ending with value `com` are excluded from the audit log entries. Additionally, the use of a question mark `(?)` as a wildcard character is permitted in patterns.

> [!NOTE]  
> `audit_log_include_users` has higher priority over `audit_log_exclude_users`. For example, if `audit_log_include_users` = `demouser` and `audit_log_exclude_users` = `demouser`, the user is included in the audit logs because `audit_log_include_users` has higher priority.

| **Event** | **Description** |
| --- | --- |
| `CONNECTION` | - Connection initiation<br />- Connection termination |
| `CONNECTION_V2` | - Connection initiation (successful or unsuccessful attempt error code)<br />- Connection termination<br />|
| `DML_SELECT` | SELECT queries |
| `DML_NONSELECT` | INSERT/DELETE/UPDATE queries |
| `DML` | DML = DML_SELECT + DML_NONSELECT |
| `DDL` | Queries like "DROP DATABASE" |
| `DCL` | Queries like "GRANT PERMISSION" |
| `ADMIN` | Queries like "SHOW STATUS" |
| `GENERAL` | All in DML_SELECT, DML_NONSELECT, DML, DDL, DCL, and ADMIN |
| `TABLE_ACCESS` | - Table read statements, such as SELECT or INSERT INTO ... SELECT<br />- Table delete statements, such as DELETE or TRUNCATE TABLE<br />- Table insert statements, such as INSERT or REPLACE<br />- Table update statements, such as UPDATE |

#### Access audit logs

Audit logs are integrated with Azure Monitor diagnostic settings. After you enable audit logs on your flexible server, you can emit them to Azure Monitor logs, Azure Event Hubs, or Azure Storage. To learn more about diagnostic settings, see the [diagnostic logs documentation](/azure/azure-monitor/essentials/platform-logs-overview). To learn more about how to enable diagnostic settings in the Azure portal, see the [audit log portal article](tutorial-configure-audit.md#set-up-diagnostics).

> [!NOTE]  
> Premium Storage accounts aren't supported if you send the logs to Azure storage via diagnostics and settings.

Depending on the output method, the fields included and the order in which they appear might vary.

Connection:

| **Property** | **Description** |
| --- | --- |
| `TenantId` | Your tenant ID |
| `SourceSystem` | `Azure` |
| `TimeGenerated [UTC]` | Time stamp when the log was recorded in UTC |
| `Type` | Type of the log. Always `AzureDiagnostics` |
| `SubscriptionId` | GUID for the subscription that the server belongs to |
| `ResourceGroup` | Name of the resource group the server belongs to |
| `ResourceProvider` | Name of the resource provider. Always `MICROSOFT.DBFORMYSQL` |
| `ResourceType` | `Servers` |
| `ResourceId` | Resource URI |
| `Resource` | Name of the server in upper case |
| `Category` | `MySqlAuditLogs` |
| `OperationName` | `LogEvent` |
| `LogicalServerName_s` | Name of the server |
| `event_class_s` | `connection_log` |
| `event_subclass_s` | `CONNECT`, `DISCONNECT`, `CHANGE USER` |
| `connection_id_d` | Unique connection ID generated by MySQL |
| `host_s` | Blank |
| `ip_s` | IP address of client connecting to MySQL |
| `user_s` | Name of user executing the query |
| `db_s` | Name of database connected to |
| `\_ResourceId` | Resource URI |
| `status_d` | Connection [Error code](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html) entry for CONNECTIONS_V2 event. |

General:

The following Schema applies to GENERAL, DML_SELECT, DML_NONSELECT, DML, DDL, DCL, and ADMIN event types.

> [!NOTE]  
> For `sql_text_s`, log is truncated if it exceeds 2,048 characters.

| **Property** | **Description** |
| --- | --- |
| `TenantId` | Your tenant ID |
| `SourceSystem` | `Azure` |
| `TimeGenerated [UTC]` | Time stamp when the log was recorded in UTC |
| `Type` | Type of the log. Always `AzureDiagnostics` |
| `SubscriptionId` | GUID for the subscription that the server belongs to |
| `ResourceGroup` | Name of the resource group the server belongs to |
| `ResourceProvider` | Name of the resource provider. Always `MICROSOFT.DBFORMYSQL` |
| `ResourceType` | `Servers` |
| `ResourceId` | Resource URI |
| `Resource` | Name of the server in upper case |
| `Category` | `MySqlAuditLogs` |
| `OperationName` | `LogEvent` |
| `LogicalServerName_s` | Name of the server |
| `event_class_s` | `general_log` |
| `event_subclass_s` | `LOG`, `ERROR`, `RESULT` (only available for MySQL 5.6) |
| `event_time` | Query start time in UTC timestamp |
| `error_code_d` | Error code if query failed. `0` means no error |
| `thread_id_d` | ID of thread that executed the query |
| `host_s` | Blank |
| `ip_s` | IP address of client connecting to MySQL |
| `user_s` | Name of user executing the query |
| `sql_text_s` | Full query text |
| `\_ResourceId` | Resource URI |

Table access:

> [!NOTE]  
> For `sql_text_s`, log is truncated if it exceeds 2,048 characters.

| **Property** | **Description** |
| --- | --- |
| `TenantId` | Your tenant ID |
| `SourceSystem` | `Azure` |
| `TimeGenerated [UTC]` | Time stamp when the log was recorded in UTC |
| `Type` | Type of the log. Always `AzureDiagnostics` |
| `SubscriptionId` | GUID for the subscription that the server belongs to |
| `ResourceGroup` | Name of the resource group the server belongs to |
| `ResourceProvider` | Name of the resource provider. Always `MICROSOFT.DBFORMYSQL` |
| `ResourceType` | `Servers` |
| `ResourceId` | Resource URI |
| `Resource` | Name of the server in upper case |
| `Category` | `MySqlAuditLogs` |
| `OperationName` | `LogEvent` |
| `LogicalServerName_s` | Name of the server |
| `event_class_s` | `table_access_log` |
| `event_subclass_s` | `READ`, `INSERT`, `UPDATE`, or `DELETE` |
| `connection_id_d` | Unique connection ID generated by MySQL |
| `db_s` | Name of database accessed |
| `table_s` | Name of table accessed |
| `sql_text_s` | Full query text |
| `\_ResourceId` | Resource URI |

### Use Azure Monitor workbooks

Azure Database for MySQL flexible server is now integrated with Azure Monitor workbooks. With workbooks, you get a flexible canvas for analyzing data and creating rich visual reports within the Azure portal. Workbooks allow you to tap into multiple data sources across Azure and combine them into unified interactive experiences. Workbook templates serve as curated reports that multiple users and teams design for flexible reuse.

When you open a template, you create a transient workbook that's populated with the contents of the template. With this integration, the server links to workbooks and a few sample templates, which can help you monitor the service at scale. You can edit these templates, customize them to your requirements, and pin them to the dashboard to create a focused and organized view of Azure resources.

Azure Database for MySQL flexible server has three available templates:

- **Overview**: Displays an instance summary and top-level metrics to help you visualize and understand the resource utilization on your server. This template displays the following views:

  - Server Summary
  - Database Summary
  - Connection Metrics
  - Performance Metrics
  - Storage Metrics

- **Auditing**: Displays a summary and details of the auditing events that are collected for the server. This template displays the following views:

  - Administrative Actions on the service
  - Audit Summary
  - Audit Connection Events Summary
  - Audit Connection Events
  - Table Access Summary
  - Errors Identified

- **Query Performance Insight**: Displays a summary and details of query workload on the instance, long running query, slow query analysis, and connection metrics. This template displays the following views:

  - Query Load
  - Total Active Connections
  - Slow Query Trend (>10 seconds of query time)
  - Slow Query Details
  - List top five longest queries
  - Summarize slow queries by minimum, maximum, average, and standard deviation query time

You can also edit and customize these templates according to your requirements. For more information, see [Azure Workbooks](/azure/azure-monitor/visualize/workbooks-overview).

#### Access the workbook templates

To view the templates in the Azure portal, go to the **Monitoring** pane for Azure Database for MySQL flexible server, and then select **Workbooks**.

:::image type="content" source="media/concepts-monitor-mysql/monitor-workbooks-all.png" alt-text="Screenshot showing the 'Overview', 'Auditing', and 'Query Performance Insight' templates on the Workbooks pane." lightbox="media/concepts-monitor-mysql/monitor-workbooks-all.png":::

You can also display the list of templates by going to the **Public Templates** pane.

:::image type="content" source="media/concepts-monitor-mysql/monitor-workbooks-public.png" alt-text="Diagram that shows the 'Overview', 'Auditing', and 'Query Performance Insight' templates on the 'Public Templates' pane." lightbox="media/concepts-monitor-mysql/monitor-workbooks-public.png":::

[!INCLUDE [azmon-horz-tools](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-tools.md)]

[!INCLUDE [azmon-horz-export-data](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-export-data.md)]

[!INCLUDE [azmon-horz-kusto](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-kusto.md)]

### Recommended Kusto queries for Azure Database for MySQL - Flexible Server

You can use slow query logs to find candidates for optimization. After your slow query logs are piped to Azure Monitor Logs through Diagnostic Logs, you can perform further analysis of your slow queries. These sample queries can get you started. Make sure to update them with your server name.

- Queries longer than 10 seconds on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>'
    | where Category == 'MySqlSlowLogs'
    | project TimeGenerated, Resource , event_class_s, start_time_t , query_time_d, sql_text_s
    | where query_time_d > 10
    ```

- List top five longest queries on a particular server

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

For audit logs, after your audit logs are piped to Azure Monitor Logs through Diagnostic Logs, you can perform further analysis of your audited events. These sample queries can get you started. Make sure to update them with your server name.

- List GENERAL events on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>' //Server name must be in Upper case
    | where Category == 'MySqlAuditLogs' and event_class_s == "general_log"
    | project TimeGenerated, Resource, event_class_s, event_subclass_s, event_time_t, user_s , ip_s , sql_text_s
    | order by TimeGenerated asc nulls last
    ```

- List CONNECTION_V2 events on a particular server, `status_d` column denotes the client connection [error code](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html) faced by the client application while connecting.

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>' //Server name must be in Upper case
    | where Category == 'MySqlAuditLogs' and event_subclass_s == "CONNECT"
    | project TimeGenerated, Resource, event_class_s, event_subclass_s, user_s, ip_s, status_d
    | order by TimeGenerated asc nulls last
    ```

- List CONNECTION events on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>' //Server name must be in Upper case
    | where Category == 'MySqlAuditLogs' and event_class_s == "connection_log"
    | project TimeGenerated, Resource, event_class_s, event_subclass_s, event_time_t, user_s , ip_s , sql_text_s
    | order by TimeGenerated asc nulls last
    ```

- Summarize audited events on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>' //Server name must be in Upper case
    | where Category == 'MySqlAuditLogs'
    | project TimeGenerated, Resource, event_class_s, event_subclass_s, event_time_t, user_s , ip_s , sql_text_s
    | summarize count() by event_class_s, event_subclass_s, user_s, ip_s
    ```

- Graph the audit event type distribution on a particular server

    ```kusto
    AzureDiagnostics
    | where Resource  == '<your server name>' //Server name must be in Upper case
    | where Category == 'MySqlAuditLogs'
    | project TimeGenerated, Resource, event_class_s, event_subclass_s, event_time_t, user_s , ip_s , sql_text_s
    | summarize count() by Resource, bin(TimeGenerated, 5m)
    | render timechart
    ```

- List audited events across all Azure Database for MySQL Flexible Server instances with Diagnostic Logs enabled for audit logs

    ```kusto
    AzureDiagnostics
    | where Category == 'MySqlAuditLogs'
    | project TimeGenerated, Resource, event_class_s, event_subclass_s, event_time_t, user_s , ip_s , sql_text_s
    | order by TimeGenerated asc nulls last
    ```

[!INCLUDE [azmon-horz-alerts-part-one](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-alerts-part-one.md)]

### Recommended Azure Monitor alert rules for Azure Database for MySQL - Flexible Server

[!INCLUDE [azmon-horz-alerts-part-two](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-alerts-part-two.md)]

[!INCLUDE [azmon-horz-advisor](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/azmon-horz-advisor.md)]

## Related content

- [Azure Database for MySQL - Flexible Server monitoring data reference](concepts-monitor-mysql-reference.md)
- [Monitoring Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource)
