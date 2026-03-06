---
title: Global Secondary Indexes (preview)
description: Global secondary indexes can be used to avoid cross-partition queries on a source container in Azure Cosmos DB.
author: jcocchi
ms.author: jucocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom:
  - build-2023
  - devx-track-azurecli
  - build-2025
ms.topic: concept-article
ms.date: 01/28/2026
appliesto:
  - ✅ NoSQL
---

# Azure Cosmos DB for NoSQL global secondary indexes (preview)

> [!IMPORTANT]
> Azure Cosmos DB for NoSQL global secondary indexes are currently in preview. For more information, see the [supplemental terms of use for Microsoft Azure previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Global secondary indexes (GSIs) improve query efficiency by storing data with a different partition key than the source container. GSIs are read-only containers that are automatically synchronized with the source container. Each GSI has its own partition key, indexing policy, throughput (RU) limit, and data model.

## Use cases

Applications often need to query data using properties other than the partition key. These queries must be executed across all partitions, even if some partitions don't contain data that matches the filter criteria. As a result, queries that don't include the partition key consume more RUs and have higher latency.

With a global secondary index, you can:

- Store data with a different partition key to convert cross-partition queries on the source container into single partition queries.
- Add GSIs to existing containers to keep queries efficient as application needs change.
- Isolate a subset of your workload, such as creating vector or full text search indexes in the GSI without impacting transactional operations on the source container.

## Global secondary index benefits

Azure Cosmos DB global secondary indexes offer the following benefits:

- Automatic Syncing: Index containers are automatically synced with the source container, eliminating the need for custom logic in client applications.
- Eventual Consistency: Index containers are eventually consistent with the source container without impacting write latency in the source.
- Performance Isolation: Index containers have their own storage and RU limits, providing performance isolation.
- Optimized Read Performance: Fine-tuned data model, partition key, and indexing policy for optimized read performance with support for queries using the rich NoSQL query syntax.
- Improved Write Performance: Clients only need to write to the source container, improving write performance compared to a multi-container-write strategy.
- Read-Only Containers: Writes to the index container are asynchronous and managed automatically. Client applications don't need to write directly to the index container.
- Multiple Indexes: You can create multiple index containers for the same source container.

## Defining global secondary indexes

Creating a global secondary index is similar to creating a new container, with added properties to specify the source container and a query defining the GSI data model. Many customizations for containers also apply to GSIs, including custom indexing, vector, and full text search policies. GSI containers must use autoscale throughput, which helps them respond to spikes in traffic without getting throttled or falling behind from updates in the source container.

The query that defines a GSI must adhere to the following constraints. Once the GSI is created, you can query it using the full Azure Cosmos DB for NoSQL query syntax.
 - The SELECT statement can project properties from any level of the JSON tree, or use SELECT * to include all properties. Projected properties are flattened to the top level in the GSI.
 - Property aliasing (AS) isn't supported in the definition query.
 - Queries can’t include a WHERE clause or other clauses such as JOIN, DISTINCT, GROUP BY, ORDER BY, TOP, OFFSET LIMIT, or EXISTS.
 - System functions and user-defined functions (UDFs) aren't supported.

Each item in the GSI has a one-to-one mapping to an item in the source container. To maintain this mapping, the `id` field in GSI items is auto populated and the source item `id` value is represented as `_id`. When using `SELECT *`, the source `id` is automatically included as `_id` in GSI items. When projecting specific properties, you must explicitly include `id` if needed.

For example, a valid query is: `SELECT c.id, c.name.first, c.emailAddress FROM c`. In the GSI, `_id`, `first` and `emailAddress` appear as top-level properties, even though `name.first` was nested in the source. This query defines the data model of the GSI, determining which properties are included for each item. The source container and definition query can't be changed once created.
 
 [Learn how to create global secondary indexes.](how-to-configure-global-secondary-indexes.md#create-a-global-secondary-index)

> [!TIP]
> If a projected property doesn't exist in all source items, the GSI uses null values for missing properties. If you choose a partition key that does not exist in all items, you can hit the 20 GB logical partition size limit. Set up alerts to [monitor if storage for a logical partition key is approaching 20 GB](./how-to-alert-on-logical-partition-key-storage-size.md).

## Syncing global secondary indexes

Global secondary indexes are automatically kept in sync with changes to data in source containers using [change feed](change-feed.md). When a GSI is defined for a source container, a change feed job is created and managed for you. Changes are asynchronously reflected to data in index containers and don't affect writes to the source container. Index containers are eventually consistent with the source container regardless of the [consistency level](consistency-levels.md) set for the account.

Change feed reads consume RUs from the source container, and writes to the GSI consume RUs from the GSI container. RUs provisioned on both containers determine how quickly data is hydrated and synced.

### Global secondary indexes in multi-region accounts

For Azure Cosmos DB accounts with a single region, change feed reads from the source container and writes to the GSI occur in that region. In a multi-region account with a single write region, change feed reads and GSI writes occur in the write region. In an account with multiple write regions, change feed reads and GSI writes occur in one of the write regions. If there's a failover for your account, change feed reads and GSI writes occur in the new write region.

## Querying global secondary indexes

Querying global secondary indexes is similar to querying any other container. You can use the full, rich Azure Cosmos DB for NoSQL query syntax to perform queries on GSIs including vector, full text search, and hybrid search queries. Similar to other containers, you should [tune the indexing policy](./how-to-manage-indexing-policy.md) on GSIs based on your query patterns.

Since GSIs can have a different partition key than the source, would-be cross-partition queries on the source can become single-partition queries on the GSI. Single partition queries improve latency and reduce RU consumption.

## Best practices

**Choose your partition key**
- GSI partition keys follow the same design principles as any container. Learn best practices for [choosing a partition key](./partitioning.md#choose-a-partition-key).
- Avoid uneven distribution caused by null values by selecting a partition key that exists in all or nearly all source items.
- Use [hierarchical partition keys](./hierarchical-partition-keys.md) with the final level as a high cardinality property like `id`. GSIs are uniquely positioned for hierarchical partition keys ending with `id` because the system automatically maintains writes and `id` generation. This optimizes partition keys that could cause logical partitions to approach the 20 GB storage limit without sacrificing any write or read patterns.

**Design projections based on queries**
- Only project properties you need for your data access patterns. Avoid projecting rarely accessed properties to minimize storage and RU consumption.
- Test your GSI definition query thoroughly before creating it. The definition can't be changed once created.
- Use `SELECT *` only if you need all properties. Selective projections are more efficient.

**Optimize for performance**
- [Tune the indexing policy](./how-to-manage-indexing-policy.md) on GSIs based on your query patterns, just as you would on any container.
- Remember that RUs are consumed separately: reads are from the source container during change feed processing, and writes are to the GSI during synchronization. Provision throughput on both containers appropriately.
- Use autoscale throughput on GSIs to handle synchronization spikes without throttling.

## Monitoring

Monitor GSI health and performance through the **Global Secondary Index Propagation Latency in Seconds** metric in the Azure portal **Metrics** section. This metric tracks the lag between source and GSIs during initial build and ongoing synchronization. For more details, see [supported metrics for Microsoft.DocumentDB/DatabaseAccounts](monitor-reference.md#supported-metrics-for-microsoftdocumentdbdatabaseaccounts).

:::image type="content" source="./media/global-secondary-indexes/global-secondary-index-catchup-gap.png" alt-text="Screenshot of the Global Secondary Index Propagation Latency in Seconds metric in the Metrics page of the Azure portal." :::

### Troubleshooting common issues

#### I want to understand the lag between my source container and GSIs

The propagation latency metric shows the average difference in seconds between source and GSI data. To view lag for an individual GSI, select **Apply splitting** and then **GlobalSecondaryIndexName** from the values list.

#### I want to know when my GSI is ready to query

There are two status types to differentiate between propagation latency when building the GSI for the first time and latency for active GSIs. Use the **Global Secondary Index Propagation Latency in Seconds** metric and select **Apply splitting**. Select the **GlobalSecondaryIndexStatus** value to view latency for global secondary indexes in the **Active**  or **InitialBuildAfterCreate** status. You can use this metric and status to configure [alerts](./create-alerts.md) should the latency go above a certain threshold.

#### I want to know if my GSI has enough throughput

The RUs provisioned on source and GSI affect the rate of changes propagated. Check the **Normalized RU Consumption** metric, if it's too high the container may benefit from increasing the maximum RUs.

## Next steps

> [!div class="nextstepaction"]
> [Data modeling and partitioning](model-partition-example.md)
> [Learn how to configure global secondary indexes](how-to-configure-global-secondary-indexes.md)
