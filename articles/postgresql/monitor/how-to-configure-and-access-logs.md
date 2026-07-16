---
title: Configure and Access Logs in Azure Database for PostgreSQL Flexible Server
description: This article describes the steps to configure and access logs in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to configure diagnostic settings for my Azure Database for PostgreSQL flexible server, so that I can stream logs to a Log Analytics workspace.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Configure and access logs in Azure Database for PostgreSQL flexible server

Every node in an Azure Database for PostgreSQL flexible server provides access to logs. You can send these logs to your own Log Analytics workspace. Use the logs to identify, troubleshoot, and fix configuration errors and performance issues.

## Steps to configure diagnostic settings

### [Portal](#tab/portal-enable-existing-server)

Use the [Azure portal](https://portal.azure.com/):

1. In the resource menu, under the **Monitoring** section, select **Diagnostic settings**. Select **Add diagnostic setting**.
   
   :::image type="content" source="media/how-to-configure-access-logs/diagnostic-settings-page-empty.png" alt-text="Screenshot showing the Diagnostic settings page with no entries." lightbox="media/how-to-configure-access-logs/diagnostic-settings-page-empty.png":::

1. In **Diagnostic setting name**, enter a name for the setting.

   :::image type="content" source="media/how-to-configure-access-logs/diagnostic-settings-name.png" alt-text="Screenshot showing the Diagnostic settings configuration page with the name of the setting." lightbox="media/how-to-configure-access-logs/diagnostic-settings-name.png":::

1. Under **Destination details**, select **Send to Log Analytics workspace**. From **Subscription**, choose the subscription that contains your Log Analytics workspace. On **Log Analytics workspace**, choose the workspace to which you want to stream logs or metrics. For **Destination table**, select **Resource specific** over **Azure diagnostics**. To learn more about the differences between the two, see [Resource logs in Azure Monitor](/azure/azure-monitor/platform/resource-logs?WT.mc_id=Portal-Microsoft_Azure_Monitoring&tabs=log-analytics#collection-mode). If you want to send the selected categories to another destination type, instead of or in addition to, select the desired options under **Destination details** and configure them accordingly.

   :::image type="content" source="media/how-to-configure-access-logs/diagnostic-settings-destination-details.png" alt-text="Screenshot showing the Diagnostic settings configuration page with a Log Analytics workspace selected." lightbox="media/how-to-configure-access-logs/diagnostic-settings-destination-details.png":::

1. To stream logs to the selected workspace, select the individual categories (PostgreSQL Server logs, PostgreSQL Sessions data, PostgreSQL Query Store Runtime, PostgreSQL Query Store Wait Statistics, PostgreSQL Autovacuum and schema statistics, PostgreSQL remaining transactions, PostgreSQL PgBouncer Logs, or PostgreSQL Query Store SQL Text), or select any of the two checkboxes from **Category groups** (audit or allLogs). Selecting either or both category groups is equivalent to selecting all individual categories. To learn more about each individual log category, see [Logs](./concepts-monitoring.md#logs). To stream metrics to the selected workspace, under **Metrics**, select **AllMetrics**.

   :::image type="content" source="media/how-to-configure-access-logs/diagnostic-settings-logs-metrics.png" alt-text="Screenshot showing the Diagnostic settings configuration page with all log categories and metrics selected." lightbox="media/how-to-configure-access-logs/diagnostic-settings-logs-metrics.png":::

1. Select **Save** to apply the changes. After you save the changes, close the page with all configuration details to return to the Diagnostic settings page.

   :::image type="content" source="media/how-to-configure-access-logs/diagnostic-settings-page-single-entry.png" alt-text="Screenshot showing the Diagnostic settings page with one entry." lightbox="media/how-to-configure-access-logs/diagnostic-settings-page-single-entry.png":::

    > [!IMPORTANT]
    > You can't select one category on more than one diagnostic setting for the same flexible server if the destination is the same for both. However, you can select the same category on different diagnostic settings for the same flexible server, as long as the destinations are different.
    
1. You can create up to five diagnostic settings for any given resource. When you reach that limit, the option to add a diagnostic setting is replaced with a message that indicates you reached the limit.

   :::image type="content" source="media/how-to-configure-access-logs/diagnostic-settings-page-full.png" alt-text="Screenshot showing the Diagnostic settings page with maximum allowed entries." lightbox="media/how-to-configure-access-logs/diagnostic-settings-page-full.png":::

### [CLI](#tab/cli-enable-new-server)

To see the different categories of logs and metrics that you can add to a diagnostic setting for your flexible server, use the [az monitor diagnostic-settings categories list](/cli/azure/monitor/diagnostic-settings/categories?view=azure-cli-latest#az-monitor-diagnostic-settings-categories-list) command.

```azurecli-interactive
az monitor diagnostic-settings categories list
  --resource-group <resource_group>
  --resource <server>
  --resource-namespace Microsoft.DBforPostgreSQL
  --resource-type flexibleServers
  --query "value[].{name:name,categoryType:categoryType}"
```

The output is similar to the following example:

```output
[
  {
    "categoryType": "Logs",
    "name": "PostgreSQLLogs"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLFlexSessions"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLFlexQueryStoreRuntime"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLFlexQueryStoreWaitStats"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLFlexTableStats"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLFlexDatabaseXacts"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLFlexPGBouncer"
  },
  {
    "categoryType": "Logs",
    "name": "PostgreSQLQueryStoreSqlText"
  },
  {
    "categoryType": "Metrics",
    "name": "AllMetrics"
  }
]
```

You can create a diagnostic setting on a flexible server to stream the `PostgreSQLFlexQueryStoreRuntime` and `PostgreSQLQueryStoreSqlText` log categories, and the `AllMetrics` metrics category to a Log Analytics workspace by using the [az monitor diagnostic-settings create](/cli/azure/monitor/diagnostic-settings?view=azure-cli-latest#az-monitor-diagnostic-settings-create) command. By using `--export-to-resource-specific`, you can control whether to use resource specific tables (`true`) or Azure diagnostics (`false`). To learn more about the differences between the two, see [Resource logs in Azure Monitor](/azure/azure-monitor/platform/resource-logs?WT.mc_id=Portal-Microsoft_Azure_Monitoring&tabs=log-analytics#collection-mode).

```azurecli-interactive
az monitor diagnostic-settings create
  --resource-group <resource_group>
  --resource <server>
  --resource-namespace Microsoft.DBforPostgreSQL
  --resource-type flexibleServers
  --name <diagnostic_setting>
  --workspace /subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.OperationalInsights/workspaces/<log_analytics_workspace>
  --export-to-resource-specific true
  --logs "[{category:PostgreSQLFlexQueryStoreRuntime,enabled:true},{category:PostgreSQLQueryStoreSqlText,enabled:true}]" --metrics "[{category:AllMetrics,enabled:true}]"
```

For more information about managing diagnostic settings from CLI, see the documentation for the [az monitor diagnostic-settings](/cli/azure/monitor/diagnostic-settings?view=azure-cli-latest) command group.

---

### Access resource logs

How you access the logs depends on which endpoint you choose. For Azure Storage, see the [logs storage account](/azure/azure-monitor/essentials/resource-logs#send-to-azure-storage) article. For Event Hubs, see the [stream Azure logs](/azure/azure-monitor/essentials/resource-logs#send-to-azure-event-hubs) article.

For Log Analytics workspaces, you send logs to the workspace you selected. If you configure the diagnostic setting to use resource specific tables, which is the recommended way, refer to [Azure Database for PostgreSQL resource logs] to see the mapping between category name of the log and its corresponding resource specific table. If, on the other hand, you configure the diagnostic settings to use Azure diagnostics as the destination table, all events from all categories land on the same AzureDiagnostics table.

To learn more about querying and alerting, see the [Overview of Log Analytics in Azure Monitor](/azure/azure-monitor/logs/log-analytics-overview?tabs=simple).

The following queries are some examples you can try to get started. You can also configure alerts based on queries.

#### All events in server log of one server in last day

If the destination of your diagnostic setting from which you're streaming the PostgreSQLLogs category is resource specific tables, use the following query:

```kusto
PGSQLServerLogs
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(1d)
```

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where LogicalServerName_s == "example-flexible-server"
| where Category == "PostgreSQLLogs"
| where TimeGenerated > ago(1d)
```

#### All remote connection attempts in last 6 hours to any server streaming logs to this workspace

If the destination of your diagnostic setting from which you're streaming the PostgreSQLLogs category is resource specific tables, use the following query:

```kusto
PGSQLServerLogs
| where Message contains "connection received" and Message !contains "host=127.0.0.1"
| where TimeGenerated > ago(6h)
```

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where Message contains "connection received" and Message !contains "host=127.0.0.1"
| where Category == "PostgreSQLLogs" and TimeGenerated > ago(6h)
```

#### Sessions collected from pg_stat_activity system view for one server in last 30 minutes

If the destination of your diagnostic setting from which you're streaming the PostgreSQLFlexSessions category is resource specific tables, use the following query:

```kusto
PGSQLPgStatActivitySessions
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(30m)
```

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where LogicalServerName_s == "example-flexible-server"
| where Category =='PostgreSQLFlexSessions'
| where TimeGenerated > ago(30m)
```

#### Query store runtime statistics for one server in last 2 days

If the destination of your diagnostic setting from which you're streaming the PostgreSQLFlexQueryStoreRuntime category is resource specific tables, use the following query:

```kusto
PGSQLQueryStoreRuntime
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(2d)
```

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where LogicalServerName_s == "example-flexible-server"
| where Category =='PostgreSQLFlexQueryStoreRuntime'
| where TimeGenerated > ago(2d)
```

#### Query store waits statistics for one server in last 3 days

If the destination of your diagnostic setting from which you're streaming the PostgreSQLFlexQueryStoreWaitStats category is resource specific tables, use the following query:

```kusto
PGSQLQueryStoreWaits
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(3d)

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where LogicalServerName_s == "example-flexible-server"
| where Category =='PostgreSQLFlexQueryStoreWaitStats'
| where TimeGenerated > ago(3d)
```

#### Query store query text for one server in last 3 days

If the destination of your diagnostic setting from which you're streaming the PostgreSQLQueryStoreSqlText category is resource specific tables, use the following query:

```kusto
PGSQLQueryStoreQueryText
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(3d)
```

> [!IMPORTANT]
> For multiple reasons, it's strongly discouraged to use Azure diagnostics destination table for any of the categories available. But it's specially important for the PostgreSQLQueryStoreSqlText category. To learn about the reasons why resource specific tables are far better than Azure diagnostics, refer to [collection modes in Log Analytics workspaces](/azure/azure-monitor/platform/resource-logs?tabs=log-analytics#collection-mode).

#### Autovacuum and schema statistics for one server in last 5 hours

If the destination of your diagnostic setting from which you're streaming the PostgreSQLFlexTableStats category is resource specific tables, use the following query:

```kusto
PGSQLAutovacuumStats
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(5h)
```

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where LogicalServerName_s == "example-flexible-server"
| where Category =='PostgreSQLFlexTableStats'
| where TimeGenerated > ago(1d)
```

#### Remaining transactions until emergency autovacuum or wraparound protection for each database in one server in last day

If the destination of your diagnostic setting from which you're streaming the PostgreSQLFlexDatabaseXacts category is resource specific tables, use the following query:

```kusto
PGSQLDbTransactionsStats
| where LogicalServerName == "example-flexible-server"
| where TimeGenerated > ago(1d)
```

If it's Azure diagnostics, use the following query:

```kusto
AzureDiagnostics
| where LogicalServerName_s == "example-flexible-server"
| where Category =='PostgreSQLFlexDatabaseXacts'
| where TimeGenerated > ago(1d)
```


For more advanced query examples, visit the queries hub of your Log Analytics workspace and filter by **Resource type** equals to **Azure Database for PostgreSQL Flexible Servers**.

   :::image type="content" source="media/how-to-configure-access-logs/log-analytics-queries-hub.png" alt-text="Screenshot showing the Queries hub filtered to show Azure Database for PostgreSQL flexible server queries in a Log Analytics workspace." lightbox="media/how-to-configure-access-logs/log-analytics-queries-hub.png":::


## Related content

- [Get started with log analytics queries](/azure/azure-monitor/logs/log-analytics-tutorial).
- [Overview of Azure event hubs](/azure/event-hubs/event-hubs-about).
