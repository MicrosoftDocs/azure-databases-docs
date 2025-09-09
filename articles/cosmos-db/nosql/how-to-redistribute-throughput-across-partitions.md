---
title: Redistribute throughput across partitions
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to redistribute throughput across partitions in Azure Cosmos DB for NoSQL to optimize performance. Discover steps and best practices.
author: tarabhatiamsft
ms.author: tarabhatia
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 09/09/2025
zone_pivot_groups: azure-scripting-languages
applies-to:
  - ✅ NoSQL
---

# Redistribute throughput across partitions

By default, Azure Cosmos DB spreads provisioned throughput evenly across all physical partitions. However, if your workload is skewed—such as when certain partitions consistently need more throughput due to hot keys or uneven traffic—you can redistribute throughput to optimize performance. This feature is available for databases and containers using provisioned throughput (manual or autoscale), and can be managed using Azure Cosmos DB PowerShell or Azure CLI commands.

For example, if you partition data by `StoreId` in a retail application, some stores could have higher activity than others. If you notice frequent rate limiting (429 errors) for those busy stores, redistributing throughput allows you to allocate more resources to the hot partitions, improving performance without increasing overall throughput.

## Prerequisites

- An existing Azure Cosmos DB account

::: zone pivot="azure-cli"

- Latest version of Azure CLI

  - `cosmosdb-preview` extension installed
  
    ```azurecli-interactive
    az extension add --name cosmosdb-preview
    ```

::: zone-end

::: zone pivot="azure-powershell"

- Latest version of Azure PowerShell

  - `Az.CosmosDB` module with prerelease features enabled
  
    ```azurepowershell-interactive
    $parameters = @{
        Name = "Az.CosmosDB"
        AllowPrerelease = $true
        Force = $true
    }
    Install-Module @parameters
    ```

::: zone-end

## Identify hot partitions using Azure Monitor metrics

To identify hot partitions in Azure Cosmos DB using Azure Monitor metrics, examine the normalized RU consumption for each physical partition to find the partitions with disproportionately high usage.

1. Sign in to the Azure portal (<https://portal.azure.com>).

1. Navigate to the **Insights** section for the Azure Cosmos DB account in the Azure portal.

1. Select **Throughput**.

1. Open **Normalized RU Consumption (%) By PartitionKeyRangeID**.

1. Filter to your specific database and container.

1. Review the chart for each `PartitionKeyRangeId`, which maps to a physical partition.

1. Identify any `PartitionKeyRangeId` that consistently shows higher normalized RU consumption than others. For example, if one value is always at 100 percent and others are at 30 percent or less, this pattern indicates a hot partition.

    :::image type="content" source="media/troubleshoot-request-rate-too-large/split-norm-utilization-by-pkrange-hot-partition.png" alt-text="Screenshot of the Normalized RU Consumption by PartitionKeyRangeId chart that shows one hot partition with higher usage.":::

## Identify hot partitions using diagnostic logs

Use the information from **CDBPartitionKeyRUConsumption** in the account's diagnostic logs to learn which logical partition keys and physical partitions consume the most RU/s at a second-level granularity.

1. Navigate to the **Diagnostic Logs** section for the Azure Cosmos DB account.

1. Find the physical partition (`PartitionKeyRangeId`) that consumes the most RU/s over time using this query.

    ```kusto
    CDBPartitionKeyRUConsumption 
    | where TimeGenerated >= ago(24hr)
    | where DatabaseName == "MyDB" and CollectionName == "MyCollection" // Replace with your database and collection name
    | where isnotempty(PartitionKey) and isnotempty(PartitionKeyRangeId)
    | summarize sum(RequestCharge) by bin(TimeGenerated, 1s), PartitionKeyRangeId
    | render timechart
    ```

1. For a physical partition, find the top 10 logical partition keys that consume the most RU/s each hour using this query.

    ```kusto
    CDBPartitionKeyRUConsumption 
    | where TimeGenerated >= ago(24hour)
    | where DatabaseName == "MyDB" and CollectionName == "MyCollection" // Replace with database and collection name
    | where isnotempty(PartitionKey) and isnotempty(PartitionKeyRangeId)
    | where PartitionKeyRangeId == 0 // Replace with your PartitionKeyRangeId
    | summarize sum(RequestCharge) by bin(TimeGenerated, 1hour), PartitionKey
    | order by sum_RequestCharge desc | take 10
    ```

> [!TIP]
> These sample queries use 24 hours for illustration, but it's best to use at least seven days of history to see usage patterns.

## Determine current throughput for each physical partition

To check the current RU/s for each physical partition, use the Azure Monitor metric **PhysicalPartitionThroughput** and split by **PhysicalPartitionId**. If throughput per partition was never changed, estimate the RU/s per partition by dividing the total RU/s by the number of physical partitions.

::: zone pivot="azure-cli"

#### [API for NoSQL](#tab/nosql)

Read the current RU/s on each physical partition by using [`az cosmosdb sql container retrieve-partition-throughput`](/cli/azure/cosmosdb/sql/container#az-cosmosdb-sql-container-retrieve-partition-throughput).

```azurecli-interactive
// Container with dedicated RU/s - some partitions
az cosmosdb sql container retrieve-partition-throughput \
    --resource-group '<resource-group-name>' \
    --account-name '<cosmos-account-name>' \
    --database-name '<cosmos-database-name>' \
    --name '<cosmos-container-name>' \
    --physical-partition-ids '<space separated list of physical partition ids>'

// Container with dedicated RU/s - all partitions
az cosmosdb sql container retrieve-partition-throughput \
    --resource-group '<resource-group-name>' \
    --account-name '<cosmos-account-name>' \
    --database-name '<cosmos-database-name>' \
    --name '<cosmos-container-name>'
    --all-partitions
```

#### [API for MongoDB](#tab/mongodb/azure-powershell)

Read the current RU/s on each physical partition by using [`az cosmosdb mongodb collection retrieve-partition-throughput`](/cli/azure/cosmosdb/sql/container#az-cosmosdb-mongodb-collection-retrieve-partition-throughput).

```azurecli-interactive
// Collection with dedicated RU/s - some partitions
az cosmosdb mongodb collection retrieve-partition-throughput \
    --resource-group '<resource-group-name>' \
    --account-name '<cosmos-account-name>' \
    --database-name '<cosmos-database-name>' \
    --name '<cosmos-collection-name>' \
    --physical-partition-ids '<space separated list of physical partition ids>'

// Collection with dedicated RU/s - all partitions
az cosmosdb mongodb collection retrieve-partition-throughput \
    --resource-group '<resource-group-name>' \
    --account-name '<cosmos-account-name>' \
    --database-name '<cosmos-database-name>' \
    --name '<cosmos-collection-name>'
    --all-partitions
```

---

::: zone-end

::: zone pivot="azure-powershell"

#### [API for NoSQL](#tab/nosql)

Use the `Get-AzCosmosDBSqlContainerPerPartitionThroughput` or `Get-AzCosmosDBSqlDatabasePerPartitionThroughput` command to read the current RU/s on each physical partition.

```azurepowershell-interactive
// Container with dedicated RU/s
$somePartitionsDedicatedRUContainer = Get-AzCosmosDBSqlContainerPerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -Name "<cosmos-container-name>" `
                    -PhysicalPartitionIds ("<PartitionId>", "<PartitionId">)

$allPartitionsDedicatedRUContainer = Get-AzCosmosDBSqlContainerPerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -Name "<cosmos-container-name>" `
                    -AllPartitions

// Database with shared RU/s
$somePartitionsSharedThroughputDatabase = Get-AzCosmosDBSqlDatabasePerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -PhysicalPartitionIds ("<PartitionId>", "<PartitionId">)

$allPartitionsSharedThroughputDatabase = Get-AzCosmosDBSqlDatabasePerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -AllPartitions
```

#### [API for MongoDB](#tab/mongodb/azure-powershell)

Use the `Get-AzCosmosDBMongoDBCollectionPerPartitionThroughput` command to read the current RU/s on each physical partition.

```azurepowershell-interactive
// Container with dedicated RU/s
$somePartitionsDedicatedRUContainer = Get-AzCosmosDBMongoDBCollectionPerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -Name "<cosmos-collection-name>" `
                    -PhysicalPartitionIds ("<PartitionId>", "<PartitionId">, ...)

$allPartitionsDedicatedRUContainer = Get-AzCosmosDBMongoDBCollectionPerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -Name "<cosmos-collection-name>" `
                    -AllPartitions

// Database with shared RU/s
$somePartitionsSharedThroughputDatabase = Get-AzCosmosDBMongoDBDatabasePerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -PhysicalPartitionIds ("<PartitionId>", "<PartitionId">)

$allPartitionsSharedThroughputDatabase = Get-AzCosmosDBMongoDBDatabasePerPartitionThroughput `
                    -ResourceGroupName "<resource-group-name>" `
                    -AccountName "<cosmos-account-name>" `
                    -DatabaseName "<cosmos-database-name>" `
                    -AllPartitions

```

---

> [!NOTE]
> For more information on finding the number of partitions, see [best practices for scaling provisioned throughput (RU/s)](../scaling-provisioned-throughput-best-practices.md#step-1-find-the-current-number-of-physical-partitions).

::: zone-end
