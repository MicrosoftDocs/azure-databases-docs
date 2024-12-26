---
title: Audit Logs
description: Describes the audit logs available in Azure Database for MySQL - Flexible Server.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Track database activity with Audit Logs in Azure Database for MySQL - Flexible Server

Azure Database for MySQL flexible server provides users with the ability to configure audit logs. Audit logs can be used to track database-level activity including connection, admin, DDL, and DML events. These types of logs are commonly used for compliance purposes.

## Configure audit logging

> [!IMPORTANT]  
> It is recommended to only log the event types and users required for your auditing purposes to ensure your server's performance isn't heavily affected and a minimum amount of data is collected.

By default, audit logs are disabled. To enable them, set the `audit_log_enabled` server parameter to *ON*. This can be configured using the Azure portal or Azure CLI.

Other parameters you can adjust to control audit logging behavior include:

- `audit_log_events`: controls the events to be logged. See below table for specific audit events.
- `audit_log_include_users`: MySQL users to be included for logging. The default value for this parameter is empty, which will include all the users for logging. This has higher priority over `audit_log_exclude_users`. Max length of the parameter is 512 characters. For example, wildcard value of `dev*` includes all the users with entries starting with keyword `dev` like "dev1,dev_user,dev_2". Another example for wildcard entry for including user is `*dev` in this example, all users ending with value "dev" like "stage_dev,prod_dev,user_dev" are included in the audit log entries. Additionally, the use of a question mark `(?)` as a wildcard character is permitted in patterns.
- `audit_log_exclude_users`: MySQL users to be excluded from logging. The Max length of the parameter is 512 characters. Wildcard entries for user are also accepted to exclude users in audit logs. For example, wildcard value of `stage*` excludes all the users with entries starting with keyword `stage` like "stage1,stage_user,stage_2". Another example for wildcard entry for excluding user is `*com` in this example, all users ending with value `com` will be excluded from the audit log entries. Additionally, the use of a question mark `(?)` as a wildcard character is permitted in patterns.

> [!NOTE]  
> `audit_log_include_users` has higher priority over `audit_log_exclude_users`. For example, if `audit_log_include_users` = `demouser` and `audit_log_exclude_users` = `demouser`, the user will be included in the audit logs because `audit_log_include_users` has higher priority.

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

## Access audit logs

Audit logs are integrated with Azure Monitor diagnostic settings. Once you've enabled audit logs on your flexible server, you can emit them to Azure Monitor logs, Azure Event Hubs, or Azure Storage. To learn more about diagnostic settings, see the [diagnostic logs documentation](/azure/azure-monitor/essentials/platform-logs-overview). To learn more about how to enable diagnostic settings in the Azure portal, see the [audit log portal article](tutorial-configure-audit.md#set-up-diagnostics).

> [!NOTE]  
> Premium Storage accounts aren't supported if you send the logs to Azure storage via diagnostics and settings.

The following sections describe the output of MySQL audit logs based on the event type. Depending on the output method, the fields included and the order in which they appear might vary.

### Connection

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

### General

Schema below applies to GENERAL, DML_SELECT, DML_NONSELECT, DML, DDL, DCL, and ADMIN event types.

> [!NOTE]  
> For `sql_text_s`, log will be truncated if it exceeds 2048 characters.

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

### Table access

> [!NOTE]  
> For `sql_text_s`, log will be truncated if it exceeds 2048 characters.

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

## Analyze logs in Azure Monitor Logs

Once your audit logs are piped to Azure Monitor Logs through Diagnostic Logs, you can perform further analysis of your audited events. Below are some sample queries to help you get started. Make sure to update the below with your server name.

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

## Related content

- [slow query logs](concepts-slow-query-logs.md)
- [auditing](tutorial-query-performance-insights.md)
