---
title: Availability and disaster recovery (DR) under the hood
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn about Azure Cosmos DB for MongoDB vCore availability and disaster recovery internals.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 12/01/2024
#Customer Intent: As a database adminstrator, I want to configure availability and cross-region replication, so that I can have appropirtiate in-region and cross-region disaster recovery plans in the event of outages on different levels.
---

# Availability (reliability) and disaster recovery (DR) in Azure Cosmos DB for MongoDB vCore - Under the hood

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

TODO: This article discusses cross-region disaster recovery (DR) for Azure Cosmos DB for MongoDB vCore. It also covers read capabilities of the cluster replicas in other regions for read operations scalability.

## Azure Cosmos DB for MongoDB vCore cluster anatomy
An Azure Cosmos DB for MongoDB vCore cluster can have one or multiple physical shards (nodes). Each physical shard consists of a compute node and remote premium SSD storage attached to it. All provisioned [compute cores and storage](./compute-storage.md) on a physical shard are dedicated to one database hosted on the cluster and aren't shared with any other cluster or database. When cluster has multiple physical shards, each of its shards has exactly the same compute and storage configuration. No matter how many physical shards are provisioned for a cluster, all cluster's compute and storage resources are always hosted in the same Azure region.

The remote premium SSD storage used in Azure Cosmos DB for MongoDB vCore is locally redundant. It means that all data written to the cluster's storage is synchronously replicate three times within the same physical location in the cluster's Azure region. Azure Storage service transparently maintains three synchronous replicas at all time on each Azure Cosmos DB for MongoDB vCore cluster node. Azure Storage regularly verifies the integrity of data stored using cyclic redundancy checks (CRCs). And detected data corruption is repaired using redundant data. Azure Storage also calculates checksums on all network traffic to detect corruption of data packets when storing or retrieving data.

:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster.png" alt-text="Diagram of the Azure Cosmos DB for MongoDB vCore cluster's components.":::
*Figure 1. Azure Cosmos DB for MongoDB vCore cluster components.*

Whether application connects to a single shard or multishard Azure Cosmos DB for MongoDB vCore cluster, it uses a single connection string and a single endpoint to connect to the database at all times. It allows you to abstract complexity of distributed MongoDB database and let application  connect to it as it would to any other non-distributed MongoDB one.

## In-region high availability (HA)
It is recommended to have [in-region high availability (HA)](./high-availability.md) always enabled on all production Azure Cosmos DB for MongoDB vCore clusters to ensure database availability consistent with typical modern requirements. Disabling high availability on development or experimental clusters allows you to reduce overall cost. High availability can be enabled and disabled on a cluster during cluster provisioning and at any time after the cluster is created. 

When high availability is enabled, a standby physical shard (node) is created for each primary physical shard in the cluster. Each standby physical shard has the same compute and storage configuration as its primary counterpart. It means that when high availability is enabled on a cluster, six replicas of data are maintained on each physical shard (node) - three on the primary physical shard and three on its standby shard.

Synchronous replication is established between each primary and standby physical shards. When your application performs a write on an Azure Cosmos DB for MongoDB vCore cluster with high availability enabled, data is written on the primary physical shard and its standby physical shard before write acknowledgment is sent back to the application. In other words, a standby physical shard is a full replica of its primary node at all times providing strong consistency within the highly availaable cluster. 

:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster-with-ha.gif" alt-text="Diagram of high availability enablement in an Azure Cosmos DB for MongoDB vCore cluster.":::
*Figure 2. Azure Cosmos DB for MongoDB vCore cluster with and without in-region high availability (HA) enabled.*

If anything happens with a primary physical shard and it is rendered unavailable, Azure Cosmos DB for MongoDB vCore service detects unavailability and performs *failover* to its standby physical shard. During failover all read and write requests for the primary physical shard are redirected to the corresponding standby physical shard. The former standby shard now becomes the new primary one thus preserving availability of the physical shard from application perspective. Write operations that could be in progress at the time of failover are retried inside the service to avoid unavailability. The old primary physical shard is discarded and replaced by a new one. Once the new physical shard is (re)created, it establishes synchronous replication with the new primary physical shard and takes over the role of standby.

## Cross-region replication - Regional disaster recovery (DR)

While Azure regional outages are becoming [less and less frequent](https://azure.status.microsoft/status/history/), an outage when the whole region is unavailable might occur. Keeping an up-to-date replica of your data in another region is a good strategy for disaster recovery (DR) during a regional outage. Having a cluster with a copy of your database that is up and running at all times in another region allows to virtually prevent database access interruption even in the case of large scale disasters that might impact your primary Azure region. This is a capability that cross-region replication provides in Azure Cosmos DB for MongoDB vCore.

You can create a replica cluster in another Azure region to prevent loss of database access in case of such a regional outage. Each physical shard of that cluster is going to have asynchronous replication established with its counterpart in the primary region. Asynchrounous replication provides eventual consistency and is typically used for cross-region scenarios to avoid performance impact on the primary (read-write) cluster. Without asynchronous replication primary clusters would need to wait for each write to be delivered to replicas and get confirmed by the replicas before confirmation can be sent back to the application. Asynchronous replication means replication lag. Replication lag depends on intensity of write operations on the primary cluster and overall load of the priamry and replica clusters.

With a replica in another Azure region, the primary cluster in region A accepts reads and writes and the replica cluster in region B can be open for reads (only). Applications can perform reads and writes to the primary cluster and intense read operations such as dashboards with 10s of thousands of users can be pointed to the replica cluster. Single self connection string is provided for each cluster for maxium control of the operations. Self connection strings are permanent and always point to the same physical cluster regardless of its role (RW or RO). To facilitate uninterrupted writes without the need to reconfigure applications a dynamic *global read-write connection string* is provided in addition to the two permanent self connextion strings. Global read-write connection string always points to the cluster that is open for writes at the moment. During replica promotion global read-write connection string is updated to point to the promoted replica cluster that is now open for writes.

:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster-with-replica.gif" alt-text="Diagram of a cross-region replica promotion for disaster recovery purpose in Azure Cosmos DB for MongoDB vCore.":::
*Figure 3. Regional disaster recovery (DR) with an Azure Cosmos DB for MongoDB vCore cluster with cross-region replication enabled. Cluster in region B is promoted to become the new read-write cluster. Cluster in region A becomes a replica cluster.*

## Summary of in-region availabilty and cross-region DR

The following table summarizes primary considerations for enabling and managing in-region high avialability and cross-region disaster recovery strategy.

|Scenario|Azure Cosmos DB for MongoDB vCore feature|No data loss|Protection from region-wide outages|Automatic|No connection string change|
|--------------------|-----------------------------|-------------------|-----------------------------------|------------|---------------|
|Node failure | In-region high availability (HA)| :heavy_check_mark: | :x: | :heavy_check_mark: | :heavy_check_mark: |
|Regional outage | Cross-region replica cluster| :x: | :heavy_check_mark: | :x: | :heavy_check_mark:† |

† When using global read-write connection string.

## Related content

- [Learn how to enable cross-region replication and promote replica cluster](./how-to-cluster-replica.md)
- [Learn about reliability in Azure Cosmos DB for MongoDB vCore](/azure/reliability/reliability-cosmos-mongodb)
