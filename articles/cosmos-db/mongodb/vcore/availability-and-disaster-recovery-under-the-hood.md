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

If anything happens with a primary physical shard and it is rendered unavailable, Azure Cosmos DB for MongoDB vCore service detects unavailability and performs *failover* to standby physical shard. During failover all read and write requests are redirected to the corresponding standby physical shard. The former standby shard now becomes a new primary one thus preserving availability of the physical shard from application perspective. Write operations that could be in progress at the time of failover are retried inside the service to avoid unavailability. The old primary physical shard is discarded and replaced by a new one. Once the new physical shard is (re)created, it establishes synchronous replication with the new primary physical shard and takes over the role of standby.

## Cross-region replication - Regional disaster recovery (DR)



:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster-with-replica.gif" alt-text="Diagram of a cross-region replica promotion for disaster recovery purpose in Azure Cosmos DB for MongoDB vCore.":::
*Figure 3. Regional disaster recovery (DR) with an Azure Cosmos DB for MongoDB vCore cluster with cross-region replication enabled.*



## Related content

- [Learn how to enable cross-region replication and promote replica cluster](./how-to-cluster-replica.md)
- [Learn about reliability in Azure Cosmos DB for MongoDB vCore](/azure/reliability/reliability-cosmos-mongodb)
