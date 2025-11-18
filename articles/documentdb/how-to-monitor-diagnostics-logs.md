---
title: Monitor diagnostic logs with Azure Monitor
description: Observe and query diagnostic logs from Azure DocumentDB using Azure Monitor Log Analytics.
author: sajeetharan
ms.author: sasinnat
ms.custom:
  - ignite-2023
  - devx-track-azurecli
ms.topic: how-to
ms.date: 10/31/2023
# CustomerIntent: As a operations engineer, I want to review diagnostic logs so that I troubleshoot issues as they occur.
---

# Monitor Azure DocumentDB diagnostics logs with Azure Monitor

Azure's diagnostic logs are essential to capture Azure resource logs for an Azure DocumentDB account. These logs furnish detailed and frequent insights into the operations for resources with the account.

> [!IMPORTANT]
> This feature is not available with compute tier `M30` or lower tiers, or free-tier SKUs.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

- An existing Log Analytics workspace or Azure Storage account.

## Create diagnostic settings

Platform metrics and activity logs are gathered automatically. To collect resource logs and route them externally from Azure Monitor, you must establish a diagnostic setting. To learn how, see [Create diagnostic settings in Azure Monitor](/azure/azure-monitor/essentials/create-diagnostic-settings?tabs=cli).

## Manage diagnostic settings

Sometimes you need to manage settings by finding or removing them. The `az monitor diagnostic-settings` command group includes subcommands for the management of diagnostic settings.

1. List all diagnostic settings associated with the API for cluster.

    ```azurecli
    az monitor diagnostic-settings list \
        --resource-group $resourceGroupName \
        --resource $clusterResourceId
    ```

1. Delete a specific setting using the associated resource and the name of the setting.

    ```azurecli
    az monitor diagnostic-settings delete \
        --resource-group $resourceGroupName \
        --name $diagnosticSettingName \
        --resource $clusterResourceId
    ```

## Use advanced diagnostics queries

Use these resource-specific queries to perform common troubleshooting research in an API for cluster.

> [!IMPORTANT]
> This section assumes that you are using a Log Analytics workspace with resource-specific logs.

1. Navigate to **Logs** section of the API for cluster. Observe the list of sample queries.

    :::image type="content" source="media/how-to-monitor-diagnostics-logs/sample-queries.png" lightbox="media/how-to-monitor-diagnostics-logs/sample-queries.png" alt-text="Screenshot of the diagnostic queries list of sample queries.":::

1. Run this query to **count the number of failed API for requests grouped by error code**.

    ```Kusto
    VCoreMongoRequests
    // Time range filter:  | where TimeGenerated between (StartTime .. EndTime)
    // Resource id filter: | where _ResourceId == "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group-name/providers/microsoft.documentdb/mongoclusters/my-cluster-name"
    | where ErrorCode != 0
    | summarize count() by bin(TimeGenerated, 5m), ErrorCode=tostring(ErrorCode)
    ```

1. Run this query to **get the API for requests `P99` runtime duration by operation name**.

    ```Kusto
    // Mongo requests P99 duration by operation 
    // Mongo requests P99 runtime duration by operation name. 
    VCoreMongoRequests
    // Time range filter:  | where TimeGenerated between (StartTime .. EndTime)
    // Resource id filter: | where _ResourceId == "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group-name/providers/microsoft.documentdb/mongoclusters/my-cluster-name"
    | summarize percentile(DurationMs, 99) by bin(TimeGenerated, 1h), OperationName
    ```

1. Run this query to **get the count of API for requests grouped by total runtime duration**.

    ```Kusto
    // Mongo requests binned by duration 
    // Count of Mongo requests binned by total runtime duration. 
    VCoreMongoRequests
    // Time range filter:  | where TimeGenerated between (StartTime .. EndTime)
    // Resource id filter: | where _ResourceId == "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group-name/providers/microsoft.documentdb/mongoclusters/my-cluster-name"
    | project TimeGenerated, DurationBin=tostring(bin(DurationMs, 5))
    | summarize count() by bin(TimeGenerated, 1m), tostring(DurationBin)
    ```

1. Run this query to **get the count of API for requests by user agent**.

    ```Kusto
    // Mongo requests by user agent 
    // Count of Mongo requests by user agent. 
    VCoreMongoRequests
    // Time range filter:  | where TimeGenerated between (StartTime .. EndTime)
    // Resource id filter: | where _ResourceId == "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/my-resource-group-name/providers/microsoft.documentdb/mongoclusters/my-cluster-name"
    | summarize count() by bin(TimeGenerated, 1h), UserAgent
    ```

## Related content

- Read more about [feature compatibility with MongoDB](compatibility-features.md).
- Review options for [migrating from MongoDB to Azure DocumentDB](migration-options.md)
- Get started by [creating an account](quickstart-portal.md).
