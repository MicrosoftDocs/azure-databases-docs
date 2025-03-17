---
title: Configure and access logs
description: How to access database logs.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Configure and access logs in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server logs are available on every node of a flexible server. You can ship logs to a storage server, or to an analytics service. The logs can be used to identify, troubleshoot, and repair configuration errors and suboptimal performance.

## Configure diagnostic settings

You can enable diagnostic settings for your Azure Database for PostgreSQL flexible server instance using the Azure portal, CLI, REST API, and PowerShell. The log category to select is **PostgreSQLLogs**.

To enable resource logs using the Azure portal:

1. In the portal, go to *Diagnostic Settings* in the navigation menu of your Azure Database for PostgreSQL flexible server instance.
   
2. Select *Add Diagnostic Setting*.
   :::image type="content" source="media/howto-logging/diagnostic-settings.png" alt-text="Add diagnostic settings button":::

3. Name this setting. 

4. Select your preferred endpoint (Log Analytics workspace, Storage account, Event hub). 

5. Select the log type from the list of categories (Server Logs, Sessions data, Query Store Runtime / Wait Statistics etc.)
   :::image type="content" source="media/howto-logging/diagnostic-setting-log-category.png" alt-text="Screenshot of choosing log categories.":::

7. Save your setting.

To enable resource logs using PowerShell, CLI, or REST API, visit the [diagnostic settings](/azure/azure-monitor/essentials/diagnostic-settings) article.

### Access resource logs

The way you access the logs depends on which endpoint you choose. For Azure Storage, see the [logs storage account](/azure/azure-monitor/essentials/resource-logs#send-to-azure-storage) article. For Event Hubs, see the [stream Azure logs](/azure/azure-monitor/essentials/resource-logs#send-to-azure-event-hubs) article.

For Azure Monitor Logs, logs are sent to the workspace you selected. The Azure Database for PostgreSQL flexible server logs use the **AzureDiagnostics** collection mode, so they can be queried from the AzureDiagnostics table. The fields in the table are described below. Learn more about querying and alerting in the [Azure Monitor Logs query](/azure/azure-monitor/logs/log-query-overview) overview.

The following are queries you can try to get started. You can configure alerts based on queries.

Search for all Azure Database for PostgreSQL flexible server logs for a particular server in the last day.

```kusto
AzureDiagnostics
| where Resource == "myservername"
| where Category == "PostgreSQLLogs"
| where TimeGenerated > ago(1d) 
```
Search for all non-localhost connection attempts. Below query will show results over the last 6 hours for any Azure Database for PostgreSQL flexible server logging in this workspace.

```kusto
AzureDiagnostics
| where Message contains "connection received" and Message !contains "host=127.0.0.1"
| where Category == "PostgreSQLLogs" and TimeGenerated > ago(6h)
```

Search for Azure Database for PostgreSQL flexible server Sessions collected from `pg_stat_activity` system view for a particular server in the last day.

```kusto
AzureDiagnostics
| where Resource == "myservername"
| where Category =='PostgreSQLFlexSessions'
| where TimeGenerated > ago(1d) 
```

Search for Azure Database for PostgreSQL flexible server Query Store Runtime statistics collected from `query_store.qs_view` for a particular server in the last day. It requires Query Store to be enabled.

```kusto
AzureDiagnostics
| where Resource == "myservername"
| where Category =='PostgreSQLFlexQueryStoreRuntime'
| where TimeGenerated > ago(1d) 
```

Search for Azure Database for PostgreSQL flexible server Query Store Wait Statistics collected from `query_store.pgms_wait_sampling_view` for a particular server in the last day. It requires Query Store Wait Sampling to be enabled.

```kusto
AzureDiagnostics
| where Resource == "myservername"
| where Category =='PostgreSQLFlexQueryStoreWaitStats'
| where TimeGenerated > ago(1d) 
```

Search for Azure Database for PostgreSQL flexible server Autovacuum and Schema statistics for each database in a particular server within the last day.

```kusto
AzureDiagnostics
| where Resource == "myservername"
| where Category =='PostgreSQLFlexTableStats'
| where TimeGenerated > ago(1d) 
```

Search for Azure Database for PostgreSQL flexible server remaining transactions and multixacts till emergency autovacuum or wraparound protection for each database in a particular server within the last day.

```kusto
AzureDiagnostics
| where Resource == "myservername"
| where Category =='PostgreSQLFlexDatabaseXacts'
| where TimeGenerated > ago(1d) 
```

## Related content

- [Get started with log analytics queries](/azure/azure-monitor/logs/log-analytics-tutorial).
- [Overview of Azure event hubs](/azure/event-hubs/event-hubs-about).
