---
title: Global Secondary Indexes (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Global secondary indexes are read-only containers with a persistent copy of data from a source container. They can be used to optimize cross partition queries on a source container in Azure Cosmos DB.
author: jcocchi
ms.author: jucocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: build-2023, devx-track-azurecli
ms.topic: conceptual
ms.date: 3/24/2025
---

# Azure Cosmos DB for NoSQL global secondary indexes (preview)

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

> [!IMPORTANT]
> Azure Cosmos DB for NoSQL global secondary indexes are currently in preview. You can enable this feature by using the Azure portal and the feature can't be disabled. This preview is provided without a service-level agreement. At this time, we don't recommend that you use global secondary indexes for production workloads. Certain features of this preview might not be supported or might have constrained capabilities. For more information, see the [supplemental terms of use for Microsoft Azure previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Global secondary indexes are read-only containers that store a persistent copy of data from a source container. These index containers have their own settings, separate from the source container, such as partition key, indexing policy, Request Unit (RU) limit, and data model, which can be customized by selecting a subset of item properties. Global secondary indexes are automatically kept in sync with the source container using change feed, managed by the global secondary index builder. The global secondary index builder is dedicated compute provisioned for your Azure Cosmos DB account to maintain index containers.

> [!WARNING]
> The global secondary index feature can't be disabled on an account once enabled, however the global secondary index builder and index containers themselves can be deprovisioned.

## Use cases

Applications often need to query data without specifying a partition key. These queries must be executed across all partitions, even if some partitions don't contain data that matches the filter criteria. As a result, queries that don't include the partition key consume more RUs and have higher latency.

With a global secondary index, you can:

- Maintain a copy of data with a different partition key, allowing cross-partition queries to be re-targeted to the view for more efficient lookups.
- Provide a SQL-based predicate (without conditions) to populate only specific item properties.
- Create real-time indexes to handle event-based data, which is often stored in separate containers.

## Global secondary index features

Azure Cosmos DB global secondary indexes offer the following features:

- Automatic Syncing: Index containers are automatically synced with the source container, eliminating the need for custom logic in client applications.
- Eventual Consistency: Index containers are eventually consistent with the source container regardless of the [consistency level](../consistency-levels.md) set for the account.
- Performance Isolation: Index containers have their own storage and RU limits, providing performance isolation.
- Optimized Read Performance: Fine-tuned data model, partition key, and indexing policy for optimized read performance.
- Improved Write Performance: Clients only need to write to the source container, improving write performance compared to a multi-container-write strategy.
- Read-Only Containers: Writes to the index container are asynchronous and managed by the global secondary index builder. Client applications can't write directly to indexes.
- Multiple Indexes: You can create multiple index containers for the same source container without extra overhead.

## Defining global secondary indexes

Creating a global secondary index is similar to creating a new container, with requirements to specify the source container and a query defining the index. Each item in the global secondary index has a one-to-one mapping to an item in the source container. To maintain this mapping, the `id` field in global secondary index items is auto populated. The value of `id` from the source collection is represented as `_id` in the index.

The query used to define a global secondary index must adhere to the following constraints:
 - The SELECT statement allows projection of only one level of properties in the JSON tree, or it can be SELECT * to include all properties.
 - Aliasing property names using AS isn’t supported.
 - Queries can’t include a WHERE clause or other clauses such as JOIN, DISTINCT, GROUP BY, ORDER BY, TOP, OFFSET LIMIT, and EXISTS.
 - System functions and user-defined functions (UDFs) aren't supported.

 For example, a valid query could be: `SELECT c.userName, c.emailAddress FROM c`, which selects the `userName` and `emailAddress` properties from the source container `c`. This query defines the data model of the global secondary index, determining which properties are included in the index. The source container and definition query can't be changed once created.
 
 [Learn how to create global secondary indexes.](how-to-configure-global-secondary-indexes.md#create-a-global-secondary-index)
 
> [!NOTE]
> If you want to delete a source container, you must first delete all global secondary indexes that are created for it.

## Provisioning the global secondary index builder

The global secondary index builder is a dedicated compute layer provisioned for your Azure Cosmos DB account that automatically maintains indexes defined for source containers. The builder reads from the [change feed](../change-feed.md) of the source container and writes changes to the index containers according to the definition, keeping them in sync. Updating index containers is asynchronous and doesn't affect writes to the source container. Updates to the indexes are eventually consistent with the source container regardless of the consistency level set for the account.

You must provision a global secondary index builder for your Azure Cosmos DB account for indexes to begin populating. The amount of compute provisioned in the builder, including the SKU and the number of nodes, as well as the RUs provisioned on the index container, determine how quickly indexes are hydrated and synced. The builder can have up to five nodes by default and you can add or remove nodes at any time. Scaling up and down the number of nodes helps control the rate at which indexes are built.

The global secondary index builder is available in the following sizes:

| **Sku Name** | **vCPU** | **Memory**  |
| ------------ | -------- | ----------- |
| **D2s**      | **2**    | **8 GB** |
| **D4s**      | **4**    | **16 GB** |
| **D8s**      | **8**    | **32 GB** |
| **D16s**     | **16**   | **64 GB** |

> [!TIP]
> Once created, you can add or remove builder nodes, but you can't modify the size of the nodes. To change the size of your global secondary index builder nodes you can deprovision the builder and provision it again in a different size. Index containers don't need to be re-created and will catch up to the source once the builder is provisioned again.

### Global secondary index builders in multi-region accounts

For Azure Cosmos DB accounts with a single region, the global secondary index builder is provisioned in that region. In a multi-region account with a single write region, the builder is provisioned in the write region and reads change feed from there. In an account with multiple write regions, the builder is provisioned in one of the write regions and reads change feed from the same region it's provisioned in. 

[Learn how to provision the global secondary index builder.](how-to-configure-global-secondary-indexes.md#create-a-global-secondary-index-builder)

> [!IMPORTANT]
> In the event of a failover for your account, the global secondary index builder is deprovisioned and re-provisioned in the new write region.
> 
> Manual failovers (change write region operation) are graceful operations, and indexes are guaranteed to be consistent with the source. However, service managed failovers are not guaranteed to be graceful and can result in inconsistencies between the source and index containers. In such cases, it's recommended to re-build the index containers. It's a best practice for index container names to be loosely coupled so they can be changed out for the new index container. Alternately, fall back to executing cross-partition queries on the source container until the index is updated.  
>
> Learn more about [service managed failover.](/azure/reliability/reliability-cosmos-db-nosql#service-managed-failover)

## Monitoring

You can monitor the lag in building indexes and the health of the global secondary index builder through Metrics in the Azure portal. To learn about these metrics, see [Supported metrics for Microsoft.DocumentDB/DatabaseAccounts](../monitor-reference.md#supported-metrics-for-microsoftdocumentdbdatabaseaccounts).

:::image type="content" source="./media/materialized-views/materialized-views-metrics.png" alt-text="Screenshot of the Global Secondary Index Builder Average CPU Usage metric in the Azure portal." :::

> [!NOTE]
> The global secondary index metrics are prefixed with `MaterializedView`, which is the prior name of this feature. 

### Troubleshooting common issues

#### I want to understand the lag between my source container and indexes

The **MaterializedViewCatchupGapInMinutes** metric shows the maximum difference in minutes between data in a source container and an index. While there can be multiple indexes created in a single account, this metric exposes the highest lag among all indexes. A high value indicates the builder needs more compute to keep up with the volume of changes to source containers. The RUs provisioned on source and index containers can also affect the rate at which changes are propagated to the index. Check the **Total Requests** metric and split by **StatusCode** to determine if there are throttled requests on these containers. Throttled requests have status code 429.

#### I want to understand if my global secondary index builder has the right number of nodes

The **MaterializedViewsBuilderAverageCPUUsage** and **MaterializedViewsBuilderAverageMemoryUsage** metrics show the average CPU usage and memory consumption across all nodes in the builder. If these metrics are too high, add nodes to scale up the cluster. If these metrics show under-utilization of CPU and memory, remove nodes by scaling down the cluster. For optimal performance, CPU usage should be no higher than 70 percent.

## Limitations

There are a few limitations with the Azure Cosmos DB for NoSQL API global secondary index feature while it is in preview:

- The global secondary index feature can't be disabled on an account once enabled.
- Global secondary indexes can't be enabled on accounts that have partition merge, analytical store, or continuous backups.
- Role-based access control isn't supported for global secondary indexes.
- Containers that have hierarchical partitioning or end-to-end encryption aren't supported as source containers.
- Cross-tenant customer-managed key (CMK) encryption isn't supported on global secondary indexes.
- Availability zones
  - Global secondary indexes can't be enabled on an account that has availability zone-enabled regions.
  - Adding a new region with an availability zone isn't supported after global secondary indexes are enabled on an account.
- Periodic backup and restore
  - Global secondary indexes aren't automatically restored during the restore process. You must enable the global secondary index feature on the restored account after the restore process is finished. Then, you can create the global secondary indexes and builder again.

## Next steps

> [!div class="nextstepaction"]
> [Data modeling and partitioning](model-partition-example.md)
> [Learn how to configure global secondary indexes](how-to-configure-global-secondary-indexes.md)
