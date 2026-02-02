---
title: Query a Container
description: Learn how to query containers in Azure Cosmos DB by using both in-partition and cross-partition queries.
author: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 07/09/2025
ms.author: mjbrown
appliesto:
  - ✅ NoSQL
---

# Query an Azure Cosmos DB container

This article explains how to query data (such as a collection, graph, or table) within a container in Azure Cosmos DB. In particular, it covers how in-partition and cross-partition queries work in Azure Cosmos DB.

## In-partition query

When you query data from containers, if the query has a partition key filter specified, Azure Cosmos DB automatically optimizes the query. It routes the query to the [physical partitions](partitioning.md#physical-partitions) corresponding to the partition key values specified in the filter.

For example, consider the following query with an equality filter on `DeviceId`. If we run this query on a container partitioned on `DeviceId`, this query filters to a single physical partition.

```sql
SELECT * FROM c WHERE c.DeviceId = 'XMS-0001'
```

As with the earlier example, this query also filters to a single partition. Adding the filter on `Location` doesn't change the following query:

```sql
SELECT * FROM c WHERE c.DeviceId = 'XMS-0001' AND c.Location = 'Seattle'
```

Here's a query that has a range filter on the partition key and won't be scoped to a single physical partition. In order to be an in-partition query, the query must have an equality filter that includes the partition key:

```sql
SELECT * FROM c WHERE c.DeviceId > 'XMS-0001'
```

## Cross-partition query

The following query doesn't have a filter on the partition key (`DeviceId`). Therefore, it must fan out to all physical partitions where it's run against each partition's index:

```sql
SELECT * FROM c WHERE c.Location = 'Seattle`
```

Each physical partition has its own index. Therefore, when you run a cross-partition query on a container, you're effectively running one query *per* physical partition. Azure Cosmos DB automatically aggregates results across different physical partitions.

The indexes in different physical partitions are independent from one another. There's no default global index in Azure Cosmos DB.

### Optimize cross-partition queries with global secondary indexes

[Global secondary indexes (preview)](global-secondary-indexes.md) provide an alternative approach to avoid cross-partition queries without changing your container's partition key. A global secondary index creates a separate, automatically synchronized container with a different partition key optimized for specific query patterns.

For example, if your container is partitioned by `DeviceId` but you frequently query by `Location`, you could create a global secondary index partitioned by `Location`. The query that was previously a cross-partition query can now be executed as an in-partition query against the global secondary index:

```sql
SELECT * FROM c WHERE c.Location = 'Seattle'
```

## Parallel cross-partition query

The Azure Cosmos DB SDKs 1.9.0 and later support parallel query execution options. Parallel cross-partition queries allow you to perform low latency, cross-partition queries.

You can manage parallel query execution by tuning the following parameters:

- `MaxConcurrency`: Sets the maximum number of simultaneous network connections to the container's partitions. If you set this property to *-1*, the SDK manages the degree of parallelism. If the `MaxConcurrency` is set to *0*, there's a single network connection to the container's partitions.

- `MaxBufferedItemCount`: Trades query latency versus client-side memory utilization. If this option is omitted or to set to *-1*, the SDK manages the number of items buffered during parallel query execution.

Because of the Azure Cosmos DB's ability to parallelize cross-partition queries, query latency generally scales well as the system adds [physical partitions](partitioning.md#physical-partitions). However, the Request Units (RUs) charge increases significantly as the total number of physical partitions increases.

When you run a cross-partition query, you're essentially doing a separate query per individual physical partition. While cross-partition queries use the index, if available, they still aren't nearly as efficient as in-partition queries.

## Useful example

Here's an analogy to better explain cross-partition queries:

Imagine you're a delivery driver who has to deliver packages to different apartment complexes. Each apartment complex has a list on the premises that has all of the residents' unit numbers. We can compare each apartment complex to a physical partition and each list to the physical partition's index.

We can compare in-partition and cross-partition queries using this example:

### In-partition query (example)

If the delivery driver knows the correct apartment complex (physical partition), then they can immediately drive to the correct building. The driver can check the apartment complex's list of the residents' unit numbers (the index) and quickly deliver the appropriate packages. In this case, the driver doesn't waste any time or effort driving to an apartment complex to check and see if any package recipients live there.

### Cross-partition query (fan-out)

If the delivery driver doesn't know the correct apartment complex (physical partition), they need to drive to every single apartment building and check the list with all of the residents' unit numbers (the index). Once the driver arrives at each apartment complex, they're still able to use the list of the addresses of each resident. However, they need to check every apartment complex's list, whether any package recipients live there or not. This example is how cross-partition queries work. While they can use the index (meaning, they don't need to knock on every door), they must separately check the index for every physical partition.

### Cross-partition query (scoped to only a few physical partitions)

If the delivery driver knows that all package recipients live within a certain few apartment complexes, they don't need to drive to every single one. While driving to a few apartment complexes still requires more work than visiting just a single building, the delivery driver still saves significant time and effort. If a query has the partition key in its filter with the `IN` keyword, it only checks the relevant physical partition's indexes for data.

## Avoid cross-partition queries

For most containers, having some cross-partition queries is inevitable, which is okay! Nearly all query operations are supported across partitions, both for logical partition keys and physical partitions. Azure Cosmos DB also has many optimizations in the query engine and client SDKs to parallelize query execution across physical partitions.

For most read-heavy scenarios, we recommend selecting the most common property in your query filters. You should also make sure your partition key adheres to other [partition key selection best practices](partitioning.md#choose-a-partition-key).

Avoiding cross-partition queries typically only matters with large containers. You're charged for a minimum of about 2.5 RUs each time you check a physical partition's index for results even if no items in the physical partition match the query's filter. As such, if you have only one (or just a few) physical partitions, cross-partition queries don't consume significantly more RUs than in-partition queries.

The number of physical partitions is tied to the number of provisioned RUs. Each physical partition allows for up to 10,000 provisioned RUs and can store up to 50 GB of data. Azure Cosmos DB automatically manages physical partitions for you. The number of physical partitions in your container is dependent on your provisioned throughput and consumed storage.

You should try to avoid cross-partition queries if your workload meets the following criteria:

- You plan to have over 30,000 RUs provisioned
- You plan to store over 100 GB of data

Consider using [global secondary indexes (preview)](global-secondary-indexes.md) to avoid cross-partition queries. Global secondary indexes allow you to create additional containers with different partition keys, automatically synchronized with your source container. This approach can eliminate cross-partition queries for specific query patterns without requiring changes to your existing application logic or partition key.

## Next steps

- [Partitioning and horizontal scaling in Azure Cosmos DB](partitioning.md)
- [Create a synthetic partition key](synthetic-partition-keys.md)
- [Global secondary indexes in Azure Cosmos DB](global-secondary-indexes.md)
