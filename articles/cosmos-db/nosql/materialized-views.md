---
title: Materialized views (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Materialized views are read-only containers with a persistent copy of data from a source container. They can be used to implement the Global Secondary Index pattern on Azure Cosmos DB.
author: jcocchi
ms.author: jucocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.custom: build-2023, devx-track-azurecli
ms.topic: conceptual
ms.date: 3/4/2025
---

# Azure Cosmos DB for NoSQL materialized views (preview)

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

> [!IMPORTANT]
> Azure Cosmos DB for NoSQL materialized views are currently in preview. You can enable this feature by using the Azure portal and the feature can't be disabled. This preview is provided without a service-level agreement. At this time, we don't recommend that you use materialized views for production workloads. Certain features of this preview might not be supported or might have constrained capabilities. For more information, see the [supplemental terms of use for Microsoft Azure previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Materialized views are read-only containers that store a persistent copy of data from a source container. These views have their own settings, separate from the source container, such as partition key, indexing policy, Request Unit (RU) limit, and data model, which can be customized by selecting a subset of item properties. Materialized views are automatically kept in sync with the source container using change feed, managed by the materialized views builder. The materialized views builder is dedicated compute provisioned for your Azure Cosmos DB account to maintain views.

> [!WARNING]
> The materialized views feature can't be disabled on an account once enabled, however the materialized views builder and view containers themselves can be deprovisioned.

## Use cases

Applications often need to query data without specifying a partition key. These queries must be executed across all partitions, even if some partitions don't contain data that matches the filter criteria. As a result, queries that don't include the partition key consume more RUs and have higher latency. 

With a materialized view, you can:

- Maintain a copy of data with a different partition key, allowing cross-partition queries to be retargeted to the view for more efficient lookups.
- Provide a SQL-based predicate (without conditions) to populate only specific item properties.
- Create real-time views to handle event-based data, which is often stored in separate containers.

### Implement the Global Secondary Index pattern

Materialized views can act as a Global Secondary Index (GSI), enabling efficient querying on properties other than the partition key of the source container. By creating a materialized view with a different partition key, you can achieve a similar effect to a GSI. Once the materialized view is created, queries that would otherwise be cross-partition can be retargeted to the view container, leading to reduced RU consumption and reduced latency.

## Materialized views features

Azure Cosmos DB materialized views offer the following features:

- Automatic Syncing: Views are automatically synced with the source container, eliminating the need for custom logic in client applications.
- Eventual Consistency: Views are eventually consistent with the source container regardless of the [consistency level](../consistency-levels.md) set for the account.
- Performance Isolation: View containers have their own storage and RU limits, providing performance isolation.
- Optimized Read Performance: Fine-tuned data model, partition key, and indexing policy for optimized read performance.
- Improved Write Performance: Clients only need to write to the source container, improving write performance compared to a multi-container-write strategy.
- Read-Only Containers: Writes to the view are asynchronous and managed by the materialized view builder. Client applications can't write directly to views.
- Multiple Views: You can create multiple views for the same source container without extra overhead.

## Defining materialized views

Creating a materialized view is similar to creating a new container, with requirements to specify the source container and a query defining the view. Each item in the materialized view has a one-to-one mapping to an item in the source container. To maintain this mapping, the `id` field in materialized view items is auto populated. The value of `id` from the source collection is represented as `_id` in the view.

The query used to define a materialized view must adhere to the following constraints:
 - The SELECT statement allows projection of only one level of properties in the JSON tree, or it can be SELECT * to include all properties.
 - Aliasing property names using AS isn’t supported.
 - Queries can’t include a WHERE clause or other clauses such as JOIN, DISTINCT, GROUP BY, ORDER BY, TOP, OFFSET LIMIT, and EXISTS.
 - System functions and user-defined functions (UDFs) aren't supported.

 For example, a valid query could be: `SELECT c.userName, c.emailAddress FROM c`, which selects the `userName` and `emailAddress` properties from the source container `c`. This query defines the structure of the materialized view, determining which properties are included in the view. The materialized view source container and definition query can't be changed once created.
 
 [Learn how to create materialized views.](how-to-configure-materialized-views.md#create-a-materialized-view)
 
> [!NOTE]
> Once views are created, if you want to delete the source container, you must first delete all materialized views that are created for it.

## Provisioning the materialized views builder

The materialized views builder is a dedicated compute layer provisioned for your Azure Cosmos DB account that automatically maintains views defined for source containers. The builder reads from the [change feed](../change-feed.md) of the source container and writes changes to the materialized views according to the view definition, keeping them in sync. Updating views is asynchronous and doesn't affect writes to the source container. Updates to the views are eventually consistent with the source container regardless of the consistency level set for the account.

You must provision a materialized views builder for your Azure Cosmos DB account for views to begin populating. The amount of compute provisioned in the builder, including the SKU and the number of nodes, as well as the RUs provisioned on the view container, determine how quickly views are hydrated and synced. The builder can have up to five nodes by default and you can add or remove nodes at any time. Scaling up and down the number of nodes helps control the rate at which views are built.

The materialized views builder is available in the following sizes:

| **Sku Name** | **vCPU** | **Memory**  |
| ------------ | -------- | ----------- |
| **D2s**      | **2**    | **8 GB** |
| **D4s**      | **4**    | **16 GB** |
| **D8s**      | **8**    | **32 GB** |
| **D16s**     | **16**   | **64 GB** |

> [!TIP]
> Once created, you can add or remove builder nodes, but you can't modify the size of the nodes. To change the size of your materialized view builder nodes you can deprovision the builder and provision it again in a different size. Views don't need to be re-created and will catch up to the source once the builder is provisioned again.

### Materialized views builders in multi-region accounts

For Azure Cosmos DB accounts with a single region, the materialized views builder is provisioned in that region. In a multi-region account with a single write region, the builder is provisioned in the write region and reads change feed from there. In an account with multiple write regions, the builder is provisioned in one of the write regions and reads change feed from the same region it's provisioned in. 

[Learn how to provision the materialized views builder.](how-to-configure-materialized-views.md#create-a-materialized-view-builder)

> [!IMPORTANT]
> In the event of a failover for your account, the materialized views builder is deprovisioned and re-provisioned in the new write region.
> 
> Manual failovers (change write region operation) are graceful operations, and views are guaranteed to be consistent with the source. However, service managed failovers are not guaranteed to be graceful and can result in inconsistencies between the source and view containers. In such cases, it's recommended to re-build the view containers and fall back to executing cross-partition queries on the source container until the view is updated.
>
> Learn more about [service managed failover.](/azure/reliability/reliability-cosmos-db-nosql#service-managed-failover)

## Monitoring

You can monitor the lag in building views and the health of the materialized views builder through Metrics in the Azure portal. To learn about these metrics, see [Supported metrics for Microsoft.DocumentDB/DatabaseAccounts](../monitor-reference.md#supported-metrics-for-microsoftdocumentdbdatabaseaccounts).

:::image type="content" source="./media/materialized-views/materialized-views-metrics.png" alt-text="Screenshot of the Materialized Views Builder Average CPU Usage metric in the Azure portal." :::

### Troubleshooting common issues

#### I want to understand the lag between my source container and views

The **MaterializedViewCatchupGapInMinutes** metric shows the maximum difference in minutes between data in a source container and a view. While there can be multiple views created in a single account, this metric exposes the highest lag among all views. A high value indicates the builder needs more compute to keep up with the volume of changes to source containers. The RUs provisioned on source and view containers can also affect the rate at which changes are propagated to the view. Check the **Total Requests** metric and split by **StatusCode** to determine if there are throttled requests on these containers. Throttled requests have status code 429.

#### I want to understand if my materialized views builder has the right number of nodes

The **MaterializedViewsBuilderAverageCPUUsage** and **MaterializedViewsBuilderAverageMemoryUsage** metrics show the average CPU usage and memory consumption across all nodes in the builder. If these metrics are too high, add nodes to scale up the cluster. If these metrics show under-utilization of CPU and memory, remove nodes by scaling down the cluster. For optimal performance, CPU usage should be no higher than 70 percent.

## Limitations

There are a few limitations with the Azure Cosmos DB for NoSQL API materialized view feature while it is in preview:

- The materialized views feature can't be disabled on an account once enabled.
- Materialized views can't be enabled on accounts that have partition merge, analytical store, or continuous backups.
- Role-based access control isn't supported for materialized views.
- Containers that have hierarchical partitioning or end-to-end encryption aren't supported as source containers.
- Cross-tenant customer-managed key (CMK) encryption isn't supported on materialized views.
- Availability zones
  - Materialized views can't be enabled on an account that has availability zone-enabled regions.
  - Adding a new region with an availability zone isn't supported after materialized views are enabled on an account.
- Periodic backup and restore
  - Materialized views aren't automatically restored during the restore process. You must enable the materialized views feature on the restored account after the restore process is finished. Then, you can create the materialized views and builder again.

## Next steps

> [!div class="nextstepaction"]
> [Data modeling and partitioning](model-partition-example.md)
> [Learn how to configure materialized views](how-to-configure-materialized-views.md)
