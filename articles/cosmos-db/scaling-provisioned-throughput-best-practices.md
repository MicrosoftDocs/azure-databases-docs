---
title: Best Practices for Scaling Provisioned Throughput
description: Learn about best practices for scaling manual and autoscale provisioned throughput for databases and containers.
author: deborahc
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.date: 07/23/2025
ms.author: dech
ms.topic: troubleshooting
ms.custom: sfi-image-nochange
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Best practices for scaling provisioned throughput

This article describes best practices and strategies for scaling the throughput of your database or container (collection, table, or graph). The concepts apply when you increase either the provisioned manual request units per second (RU/s) or the autoscale maximum RU/s of any resource for any of the Azure Cosmos DB APIs.

## Prerequisites

- If you're new to partitioning and scaling in Azure Cosmos DB, see [Partitioning and horizontal scaling in Azure Cosmos DB](partitioning.md).
- If you're planning to scale your RU/s due to 429 exceptions, review the guidance in [Diagnose and troubleshoot "Request rate too large" (429) exceptions](troubleshoot-request-rate-too-large.md). Before increasing RU/s, identify the root cause of the issue and whether increasing RU/s is the right solution.

## Background on scaling RU/s

When you send a request to increase the RU/s of your database or container, depending on your requested RU/s and your current physical partition layout, the scale-up operation either completes instantly or asynchronously (typically 4-6 hours). 
- **Instant scale-up**:
  - When your requested RU/s can be supported by the current physical partition layout, Azure Cosmos DB doesn’t need to split or add new partitions.
  - As a result, the operation completes immediately and the RU/s are available for use. 
- **Asynchronous scale-up**:
  - When the requested RU/s are higher than what can be supported by the physical partition layout, Azure Cosmos DB splits existing physical partitions. This occurs until the resource has the minimum number of partitions required to support the requested RU/s. 
  - As a result, the operation can take some time to complete, typically 4-6 hours. Each physical partition can support a maximum of 10,000 RU/s (applies to all APIs) of throughput and 50 GB of storage (applies to all APIs, except Cassandra, which has 30 GB of storage). 

  > [!NOTE]
  > If you perform a [change write region operation](how-to-manage-database-account.yml#change-write-region-for-your-azure-cosmos-db-account) or [add/remove a new region](how-to-manage-database-account.yml#add-remove-regions-from-your-database-account) while an asynchronous scale-up operation is in progress, the throughput scale-up operation pauses. It resumes automatically when the failover or add/remove region operation is complete.

- **Instant scale-down**:
  - For scale-down operation, Azure Cosmos DB doesn’t need to split or add new partitions.
  - As a result, the operation completes immediately and the RU/s are available for use.
  - Key result of this operation is that RUs per physical partition are reduced.

## How to scale-up RU/s without changing partition layout

### Step 1: Find the current number of physical partitions

Navigate to **Insights** > **Throughput** > **Normalized RU Consumption (%) By PartitionKeyRangeID**. Count the distinct number of PartitionKeyRangeIds.

:::image type="content" source="media/scaling-provisioned-throughput-best-practices/number-of-physical-partitions.png" alt-text="Screenshot showing the distinct number of PartitionKeyRangeIds in the Normalized RU Consumption by PartitionKeyRangeID chart.":::

> [!NOTE]
> The chart only shows a maximum of 50 PartitionKeyRangeIds. If your resource has more than 50, you can use the [Azure Cosmos DB REST API](/rest/api/cosmos-db/get-partition-key-ranges#example) to count the total number of partitions. 

Each PartitionKeyRangeId maps to one physical partition and is assigned to hold data for a range of possible hash values. 

Azure Cosmos DB distributes your data across logical and physical partitions based on your partition key to enable horizontal scaling. As data gets written, Azure Cosmos DB uses the hash of the partition key value to determine which logical and physical partition the data lives on.

### Step 2: Calculate the default maximum throughput

The highest RU/s you can scale to without triggering Azure Cosmos DB to split partitions is equal to `Current number of physical partitions * 10,000 RU/s`.

You can get this value from the Azure Cosmos DB resource provider. Perform a GET request on your [database](/rest/api/cosmos-db-resource-provider/database-accounts/update) or [container](/azure/templates/microsoft.documentdb/databaseaccounts/sqldatabases/containers) throughput setting objects and retrieve the `instantMaximumThroughput` property. This value is also available in the **Scale and Settings** page of your database or container in the portal.

#### Example

Suppose you have an existing container with five physical partitions and 30,000 RU/s of manual provisioned throughput. You can increase the RU/s to `5 * 10,000 RU/s = 50,000 RU/s` instantly. Similarly if we had a container with autoscale max RU/s of 30,000 RU/s (scales between 3000 - 30,000 RU/s), we could increase our max RU/s to 50,000 RU/s instantly (scales between 5000 - 50,000 RU/s).

> [!TIP]
> If you're scaling up RU/s to respond to request rate too large exceptions (429s), it's recommended to first increase RU/s to the highest RU/s that are supported by your current physical partition layout and assess if the new RU/s is sufficient before increasing further.

## How to ensure even data distribution during asynchronous scaling

### Background

When you increase the RU/s beyond the current number of `physical partitions * 10,000 RU/s`, Azure Cosmos DB splits existing partitions until the new number of partitions = `ROUNDUP(requested RU/s / 10,000 RU/s)`. During a split, parent partitions are split into two children partitions. 

For example, suppose you have a container with three physical partitions and 30,000 RU/s of manual provisioned throughput. If you increase the throughput to 45,000 RU/s, Azure Cosmos DB splits two of the existing physical partitions so that in total, there are `ROUNDUP(45,000 RU/s / 10,000 RU/s) = 5 physical partitions`. 

> [!NOTE]
> Applications can always ingest or query data during a split. The Azure Cosmos DB client SDKs and service automatically handle this scenario and ensure that requests are routed to the correct physical partition, so no other user action is required. 
 
If you have a workload that's evenly distributed with respect to storage and request volume—typically accomplished by partitioning by high cardinality fields like `/id`—it's recommended to set RU/s such that all partitions are split evenly when you scale-up.

To see why, let's take an example where you have an existing container with two physical partitions, 20,000 RU/s, and 80 GB of data.

Thanks to choosing a good partition key with high cardinality, the data is roughly evenly distributed in both physical partitions. Each physical partition is assigned roughly 50% of the keyspace, which is defined as the total range of possible hash values.

In addition, Azure Cosmos DB distributes RU/s evenly across all physical partitions. As a result, each physical partition has 10,000 RU/s and 50% (40 GB) of the total data. The following diagram shows our current state.

:::image type="content" source="media/scaling-provisioned-throughput-best-practices/diagram-1-baseline.png" alt-text="Diagram showing two PartitionKeyRangeIds, each with 10,000 RU per second, 40 GB, and 50% of the total keyspace.":::

Now, suppose you want to increase our RU/s from 20,000 RU/s to 30,000 RU/s. 
 
If you simply increase the RU/s to 30,000 RU/s, only one of the partitions is split. After the split, you have:
- One partition that contains 50% of the data (this partition wasn't split).
- Two partitions that contain 25% of the data each (these are the resulting child partitions from the parent that was split).

Because Azure Cosmos DB distributes RU/s evenly across all physical partitions, each physical partition still gets 10,000 RU/s. However, you now have a skew in storage and request distribution. 

In the following diagram, Partitions 3 and 4 (the children partitions of Partition 2) each have 10,000 RU/s to serve requests for 20 GB of data, while Partition 1 has 10,000 RU/s to serve requests for twice the amount of data (40 GB).

:::image type="content" source="media/scaling-provisioned-throughput-best-practices/diagram-2-uneven-partition-split.png" alt-text="Diagram showing there are 3 PartitionKeyRangeIds, each with 10,000 RU/s, after the split. One of the PartitionKeyRangeIds has 50% of the total keyspace, while two of the PartitionKeyRangeIds have 25% of the total keyspace.":::

To maintain an even storage distribution, you can first scale up your RU/s to ensure every partition splits. Then, you can lower your RU/s back down to the desired state.

So, if you start with two physical partitions, to guarantee that the partitions are even post-split, you need to set RU/s such that you end up with four physical partitions. To achieve this, first set `RU/s = 4 * 10,000 RU/s per partition = 40,000 RU/s`. Then, after the split completes, lower your RU/s to 30,000 RU/s. 

As a result, each physical partition gets `30,000 RU/s / 4 = 7500 RU/s` to serve requests for 20 GB of data. Overall, you maintain even storage and request distribution across partitions. 

:::image type="content" source="media/scaling-provisioned-throughput-best-practices/diagram-3-even-partition-split.png" alt-text="Diagram showing the RU/s have been lowered from 40,000 RU/s to 30,000 RU/s. There are 4 PartitionKeyRangeIds, each with 7500 RU/s and 25% of the total keyspace.":::

### General formula

#### Step 1: Increase your RU/s to guarantee that all partitions split evenly

In general, if you have a starting number of physical partitions `P`, and want to set a desired RU/s `S`:

Increase your RU/s to: `10,000 * P * (2 ^ (ROUNDUP(LOG_2 (S/(10,000 * P))))`. This gives the closest RU/s to the desired value that ensures all partitions are split evenly. 

> [!NOTE]
> When you increase the RU/s of a database or container, this can affect the minimum RU/s that you can lower to in the future. Typically, the minimum RU/s is equal to `MAX(400 RU/s, Current storage in GB * 1 RU/s, Highest RU/s ever provisioned / 100)`. For example, if the highest RU/s you've ever scaled to is 100,000 RU/s, the lowest RU/s you can set in the future is 1000 RU/s. Learn more about [minimum RU/s](concepts-limits.md#minimum-throughput-limits).

#### Step 2: Lower your RU/s to the desired RU/s

For example, suppose we have five physical partitions, 50,000 RU/s and want to scale to 150,000 RU/s. We should first set: `10,000 * 5 * (2 ^ (ROUND(LOG_2(150,000/(10,000 * 5)))) = 200,000 RU/s`, and then lower to 150,000 RU/s. 

When we scaled up to 200,000 RU/s, the lowest manual RU/s we can now set in the future is 2000 RU/s. The [lowest autoscale max RU/s](./autoscale-faq.yml#how-do-i-lower-the-maximum-ru-s-) we can set is 20,000 RU/s (scales between 2000 - 20,000 RU/s). Since our target RU/s is 150,000 RU/s, we aren't affected by the minimum RU/s.

## How to optimize RU/s for large data ingestion

When you plan to migrate or ingest a large amount of data into Azure Cosmos DB, it's recommended to set the RU/s of the container so that Azure Cosmos DB pre-provisions the physical partitions needed to store the total amount of data you plan to ingest upfront. Otherwise, during ingestion, Azure Cosmos DB might have to split partitions, which adds more time to the data ingestion. 

We can take advantage of the fact that during container creation, Azure Cosmos DB uses the heuristic formula of starting RU/s to calculate the number of physical partitions to start with. 

### Step 1: Review the choice of partition key

Follow [best practices](partitioning.md) for choosing a partition key to ensure you have even distribution of request volume and storage post-migration. 

### Step 2: Calculate the number of physical partitions you need 

`Number of physical partitions = Total data size in GB / Target data per physical partition in GB`

Each physical partition can hold a maximum of 50 GB of storage (30 GB for API for Cassandra). The value you should choose for the *Target data per physical partition in GB* depends on how fully packed you want the physical partitions to be and how much you expect storage to grow post-migration. 

For example, if you anticipate that storage will continue to grow, you could choose to set the value to 30 GB. Assuming you chose a good partition key that evenly distributes storage, each partition is ~60% full (30 GB out of 50 GB). As future data is written, it can be stored on the existing set of physical partitions, without requiring the service to immediately add more physical partitions.

In contrast, if you believe that storage will not grow significantly post-migration, you could choose to set the value higher, for example 45 GB. This means each partition is ~90% full (45 GB out of 50 GB). This minimizes the number of physical partitions your data is spread across, which means each physical partition can get a larger fraction of the total provisioned RU/s. 
 
### Step 3: Calculate the number of RU/s to start with for all partitions

`Starting RU/s for all partitions = Number of physical partitions * Initial throughput per physical partition`

Let's start with an example with an arbitrary number of target RU/s per physical partition.

- `Initial throughput per physical partition = 10,000 RU/s per physical partition` when using autoscale or shared throughput databases
- `Initial throughput per physical partition = 6000 RU/s per physical partition` when using manual throughput
 
### Example

Let's say you have 1 TB (1,000 GB) of data to ingest and you want to use manual throughput. Each physical partition in Azure Cosmos DB has a capacity of 50 GB. Let's assume you aim to pack partitions to be 80% full (40 GB), leaving room for future growth. 
 
This means that for 1 TB of data, you need `1000 GB / 40 GB = 25` physical partitions. To ensure you get 25 physical partitions, using manual throughput, you first provision `25 * 6000 RU/s = 150,000 RU/s`. Then, after the container is created, to help ingestion go faster, increase the RU/s to 250,000 RU/s before the ingestion begins (happens instantly because you already have 25 physical partitions). This allows each partition to get the maximum of 10,000 RU/s. 

If you're using autoscale throughput or a shared throughput database, to get 25 physical partitions, you'd first provision `25 * 10,000 RU/s = 250,000 RU/s`. Because you're already at the highest RU/s that can be supported with 25 physical partitions, you wouldn't further increase our provisioned RU/s before the ingestion.
 
In theory, with 250,000 RU/s and 1 TB of data, if we assume 1-kb documents and 10 RUs required for write, the ingestion can theoretically complete in: `1000 GB * (1,000,000 kb / 1 GB) * (1 document / 1 kb) * (10 RU / document) * (1 sec / 250,000 RU) * (1 hour / 3600 seconds) = 11.1 hours`. 

This calculation is an estimate assuming the client performing the ingestion can fully saturate the throughput and distribute writes across all physical partitions. As a best practice, it’s recommended to *shuffle* your data on the client-side. This ensures that each second, the client is writing to many distinct logical (and thus physical) partitions. 
 
Once the migration is over, you can lower the RU/s or enable autoscale as needed.

## Next steps

* [How to monitor normalized RU/s for an Azure Cosmos DB container or an account](monitor-normalized-request-units.md)
* [Diagnose and troubleshoot "Request rate too large" (429) exceptions](troubleshoot-request-rate-too-large.md)
* [Create Azure Cosmos DB containers and databases with autoscale throughput](provision-throughput-autoscale.md)
