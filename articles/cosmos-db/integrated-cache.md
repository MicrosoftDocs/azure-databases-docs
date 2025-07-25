---
title: Azure Cosmos DB Integrated Cache
description: Learn how the Azure Cosmos DB integrated cache helps you ensure manageable costs and low latency as your request volume grows.
author: jcocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 6/30/2025
ms.author: jucocchi
---

# Azure Cosmos DB integrated cache - Overview
[!INCLUDE[NoSQL](includes/appliesto-nosql.md)]

The Azure Cosmos DB integrated cache is an in-memory cache that helps you ensure manageable costs and low latency as your request volume grows. The integrated cache is easy to set up and you don’t need to spend time writing custom code for cache invalidation or managing backend infrastructure.

The integrated cache uses the [dedicated gateway](dedicated-gateway.md) within your Azure Cosmos DB account. When provisioning your dedicated gateway, you can choose the number of nodes and the node size based on the number of cores and memory needed for your workload. Each dedicated gateway node has a separate integrated cache from the others.  

An integrated cache is automatically configured within the dedicated gateway. The integrated cache has two parts: 

* An item cache for point reads
* A query cache for queries

The integrated cache is a read-through, write-through cache with a Least Recently Used (LRU) eviction policy. The item cache and query caches share the same capacity within the integrated cache and the LRU eviction policy applies to both. Data is evicted from the cache strictly based on when it was least recently used, regardless of whether it's a point read or query. The cached data within each node depends on the data that was recently [written or read](integrated-cache.md#item-cache) through that specific node. If an item or query is cached on one node, it isn't necessarily cached on the others.

> [!NOTE]
> Do you have any feedback about the integrated cache? We want to hear it! Feel free to share feedback directly with the Azure Cosmos DB engineering team: cosmoscachefeedback@microsoft.com

## Workloads that benefit from the integrated cache

The main goal of the integrated cache is to reduce costs for read-heavy workloads. Low latency, while helpful, isn't the main benefit of the integrated cache because Azure Cosmos DB is already fast without caching.

Point reads and queries that hit the integrated cache have a Request Units (RU) charge of zero. Cache hits have a much lower per-operation cost than reads from the backend database.

Workloads that fit the following characteristics should evaluate if the integrated cache helps lower costs:

- Read-heavy workloads
- Many repeated point reads on large items
- Many repeated high RU queries
- Hot partition key for reads

The biggest factor in expected savings is the degree to which reads repeat themselves. If your workload consistently executes the same point reads or queries within a short period of time, it's a great candidate for the integrated cache. When using the integrated cache for repeated reads, you only use RUs for the first read. Subsequent reads routed through the same dedicated gateway node (within the `MaxIntegratedCacheStaleness` window and if the data hasn't been evicted) don't use throughput.

Some workloads shouldn't consider the integrated cache, including:

- Write-heavy workloads
- Rarely repeated point reads or queries
- Workloads reading the change feed

## Item cache

Item cache is used for point reads (key/value look ups based on the Item ID and partition key).

### Populating the item cache

- New writes, updates, and deletes are automatically populated in the item cache of the node that the request is routed through.
- Items from point read requests where the item isn’t already in the cache (cache miss) of the node the request is routed through are added to the item cache.
- Read requests for multiple items, such as `ReadMany`, populate the query cache as a set instead of the item cache as individual items.
- Requests that are part of a [transactional batch](./nosql/transactional-batch.md) or in [bulk mode](./nosql/how-to-migrate-from-bulk-executor-library.md#enable-bulk-support) don't populate the item cache.

### Item cache invalidation and eviction

Because each node has an independent cache, it's possible that items are invalidated or evicted in the cache of one node and not the others. Items in the cache of a given node are invalidated and evicted based on the following criteria:

- Item update or delete
- Least recently used (LRU)
- Cache retention time (in other words, the `MaxIntegratedCacheStaleness`)

## Query cache

The query cache is used to cache queries. The query cache transforms a query into a key/value lookup where the key is the query text and the value is the query results. The integrated cache doesn't have a query engine; it only stores the key/value lookup for each query. Query results are stored as a set, and the cache doesn't keep track of individual items. A given item can be stored in the query cache multiple times if it appears in the result set of multiple queries. Updates to the underlying items aren't reflected in query results unless the [max integrated cache staleness](#maxintegratedcachestaleness) for the query is reached and the query is served from the backend database.

### Populating the query cache

- If the cache doesn't have a result for that query (cache miss) on the node it was routed through, the query is sent to the backend. After the query is run, the cache stores the results for that query.
- Queries with the same shape but different parameters or request options that affect the results (for example, max item count) are stored as their own key/value pair.
- Read requests for multiple items, such as `ReadMany`, populate the query cache. `ReadMany` results are stored as a set, and requests with different inputs are stored as their own key/value pair.

### Query cache eviction

Query cache eviction is based on the node the request was routed through. It's possible that queries could be evicted or refreshed on one node and not the others.

- Least recently used (LRU)
- Cache retention time (in other words, the `MaxIntegratedCacheStaleness`)

### Working with the query cache

You don't need special code when working with the query cache, even if your queries have multiple pages of results. The best practices and code for query pagination are the same whether your query hits the integrated cache or is executed on the backend query engine.

The query cache automatically caches query continuation tokens where applicable. If you have a query with multiple pages of results, any pages that are stored in the integrated cache have an RU charge of zero. If subsequent pages of query results require backend execution, they have a continuation token from the previous page so they can avoid duplicating previous work.

> [!IMPORTANT]
> Integrated cache instances within different dedicated gateway nodes have independent caches from one another. If data is cached within one node, it's not necessarily cached in the others. Multiple pages of the same query aren't guaranteed to be routed to the same dedicated gateway node.

## Integrated cache consistency

The integrated cache supports read requests with session and eventual [consistency](consistency-levels.md) only. If a read has consistent prefix, bounded staleness, or strong consistency, it bypasses the integrated cache and is served from the backend. 

The easiest way to configure either session or eventual consistency for all reads is to [set it at the account-level](consistency-levels.md#configure-the-default-consistency-level). However, if you would only like some of your reads to have a specific consistency, you can also configure consistency at the [request-level](how-to-manage-consistency.md#override-the-default-consistency-level).

> [!NOTE]
> Write requests with other consistencies still populate the cache, but in order to read from the cache the request must have either session or eventual consistency.

### Session consistency

[Session consistency](consistency-levels.md#session-consistency) is the most widely used consistency level for both single region and globally distributed Azure Cosmos DB accounts. With session consistency, single client sessions can read their own writes. Any reads with session consistency that don't have a matching session token incur RU charges. This includes the first request for a given item or query when the client application is started or restarted, unless you explicitly pass a valid session token. Clients outside of the session performing writes see eventual consistency when they use the integrated cache.

## MaxIntegratedCacheStaleness

The `MaxIntegratedCacheStaleness` is the maximum acceptable staleness for cached point reads and queries, regardless of the selected consistency. The `MaxIntegratedCacheStaleness` is configurable at the request-level. For example, if you set a `MaxIntegratedCacheStaleness` of 2 hours, your request only returns cached data if the data is less than 2 hours old. To increase the likelihood of repeated reads utilizing the integrated cache, you should set the `MaxIntegratedCacheStaleness` as high as your business requirements allow.

The `MaxIntegratedCacheStaleness`, when configured on a request that ends up populating the cache, doesn't affect how long that request is cached. `MaxIntegratedCacheStaleness` enforces consistency when you try to read cached data. There's no global TTL or cache retention setting, so data is only evicted from the cache if either the integrated cache is full or a new read is run with a lower `MaxIntegratedCacheStaleness` than the age of the current cached entry.

This is an improvement from how most caches work and allows for the following other customizations:

- You can set different staleness requirements for each point read or query
- Different clients, even if they run the same point read or query, can configure different `MaxIntegratedCacheStaleness` values
- If you wanted to modify read consistency for cached data, changing `MaxIntegratedCacheStaleness` has an immediate effect on read consistency

> [!NOTE]
> The minimum `MaxIntegratedCacheStaleness` value is 0 and the maximum value is 10 years. When not explicitly configured, the `MaxIntegratedCacheStaleness` defaults to 5 minutes.

To better understand the `MaxIntegratedCacheStaleness` parameter, consider the following example:

| Time       | Request       | Response       |
| ---------- | ------------- | -------------- |
| t = 0 sec  | Run Query A with MaxIntegratedCacheStaleness = 30 seconds | Return results from backend database (normal RU charges) and populate cache     |
| t = 0 sec  | Run Query B with MaxIntegratedCacheStaleness = 60 seconds | Return results from backend database (normal RU charges) and populate cache     |
| t = 20 sec | Run Query A with MaxIntegratedCacheStaleness = 30 seconds | Return results from integrated cache (0 RU charge)           |
| t = 20 sec | Run Query B with MaxIntegratedCacheStaleness = 60 seconds | Return results from integrated cache (0 RU charge)           |
| t = 40 sec | Run Query A with MaxIntegratedCacheStaleness = 30 seconds | Return results from backend database (normal RU charges) and refresh cache |
| t = 40 sec | Run Query B with MaxIntegratedCacheStaleness = 60 seconds | Return results from integrated cache (0 RU charge)           |
| t = 50 sec | Run Query B with MaxIntegratedCacheStaleness = 20 seconds | Return results from backend database (normal RU charges) and refresh cache |

To learn how to configure `MaxIntegratedCacheStaleness`, see [Adjust MaxIntegratedCacheStaleness](how-to-configure-integrated-cache.md#adjust-maxintegratedcachestaleness).

## Bypass the integrated cache

The integrated cache has a limited storage capacity determined by the dedicated gateway SKU provisioned. By default, all requests from clients configured with the dedicated gateway connection string go through the integrated cache and take up cache space. You can control which items and queries are cached with the bypass integrated cache request option. This request option is useful for item writes or read requests that aren't expected to be frequently repeated.

Bypassing the integrated cache for items with infrequent access saves cache space for items with more repeats, increasing RU saving potential and reducing evictions. Requests that bypass the cache are still routed through the dedicated gateway. These requests are served from the backend and cost RUs.

To learn how to bypass the integrated cache, see [Bypass the integrated cache](how-to-configure-integrated-cache.md#bypass-the-integrated-cache).

## Metrics

It's helpful to monitor some key `DedicatedGateway` and `IntegratedCache` metrics for the integrated cache. To learn about these metrics, see [Supported metrics for Microsoft.DocumentDB/DatabaseAccounts](monitor-reference.md#supported-metrics-for-microsoftdocumentdbdatabaseaccounts).

All existing metrics are available, by default, from **Metrics** in the Azure portal (not Metrics classic):

   :::image type="content" source="./media/integrated-cache/integrated-cache-metrics.png" alt-text="Screenshot of the Azure portal that shows the location of integrated cache metrics.":::

Metrics are either an average, maximum, or sum across all dedicated gateway nodes. For example, if you provision a dedicated gateway cluster with five nodes, the metrics reflect the aggregated value across all five nodes. It isn't possible to determine the metric values for each individual node.

## Troubleshoot common issues

The following examples show how to debug some common scenarios:

### I can’t tell if my application is using the dedicated gateway

Check the `DedicatedGatewayRequests`. This metric includes all requests that use the dedicated gateway, regardless of whether they hit the integrated cache. If your application uses the standard gateway or direct mode with your original connection string, you don't see an error message, but the `DedicatedGatewayRequests` is zero. If your application uses direct mode with your dedicated gateway connection string, you might still see a few `DedicatedGatewayRequests`.

### I can’t tell if my requests are hitting the integrated cache

Check the `IntegratedCacheItemHitRate` and `IntegratedCacheQueryHitRate`. If both of these values are zero, then requests aren't hitting the integrated cache. Check that you're using the dedicated gateway connection string, [connecting with gateway mode](nosql/sdk-connection-modes.md), and [are using session or eventual consistency](consistency-levels.md#configure-the-default-consistency-level).

### I want to understand if my dedicated gateway is too small

Check the `IntegratedCacheItemHitRate` and `IntegratedCacheQueryHitRate`. High values (for example, preceding 0.7-0.8) are a good sign that the dedicated gateway is large enough.

If the `IntegratedCacheItemHitRate` or `IntegratedCacheQueryHitRate`is low, look at the `IntegratedCacheEvictedEntriesSize`. If the `IntegratedCacheEvictedEntriesSize` is high, it might mean that a larger dedicated gateway size would be beneficial. You can experiment by increasing the dedicated gateway size and comparing the new `IntegratedCacheItemHitRate` and `IntegratedCacheQueryHitRate`. If a larger dedicated gateway doesn't improve the `IntegratedCacheItemHitRate` or `IntegratedCacheQueryHitRate`, it's possible that reads simply don't repeat themselves enough for the integrated cache to be impactful.

### I want to understand if my dedicated gateway is too large

It's more difficult to measure if a dedicated gateway is too large than it is to measure if a dedicated gateway is too small. In general, you should start small and slowly increase the dedicated gateway size until the `IntegratedCacheItemHitRate` and `IntegratedCacheQueryHitRate` stop improving. In some cases, only one of the two cache hit metrics is important, not both. For example, if your workload is primarily queries, rather than point reads, the `IntegratedCacheQueryHitRate` is much more important than the `IntegratedCacheItemHitRate`.

If most data is evicted from the cache due to exceeding the `MaxIntegratedCacheStaleness`, rather than LRU, your cache might be larger than required. If `IntegratedCacheItemExpirationCount` and `IntegratedCacheQueryExpirationCount` combined are nearly as large as `IntegratedCacheEvictedEntriesSize`, you can experiment with a smaller dedicated gateway size and compare performance.

### I want to understand if I need to add more dedicated gateway nodes

In some cases, if latency is unexpectedly high, you might need more dedicated gateway nodes rather than bigger nodes. Check the `DedicatedGatewayCPUUsage` and `DedicatedGatewayMemoryUsage` to determine if adding more dedicated gateway nodes would reduce latency. It's good to keep in mind that since all instances of the integrated cache are independent from one another, adding more dedicated gateway nodes won't reduce the `IntegratedCacheEvictedEntriesSize`. However, adding more nodes improves the request volume that your dedicated gateway cluster can handle.

## Next steps

- [Azure Cosmos DB integrated cache frequently asked questions](integrated-cache-faq.md)
- [How to configure the Azure Cosmos DB integrated cache](how-to-configure-integrated-cache.md)
- [Azure Cosmos DB dedicated gateway - Overview](dedicated-gateway.md)
- Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
   - If all you know is the number of vCores and servers in your existing database cluster, see [Convert the number of vCores or vCPUs in your nonrelational database to Azure Cosmos DB RU/s](convert-vcore-to-request-unit.md)
   - If you know typical request rates for your current database workload, see [Estimate RU/s using the Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md)
