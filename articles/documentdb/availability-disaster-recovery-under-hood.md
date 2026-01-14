---
title: Availability and disaster recovery (DR) under the hood
description: Learn about Azure DocumentDB availability and disaster recovery internals.
author: abinav2307
ms.author: abramees
ms.topic: concept-article
ms.date: 01/02/2026
#Customer Intent: As a database adminstrator, I want to configure availability and cross-region replication, so that I can have appropirtiate in-region and cross-region disaster recovery plans in the event of outages on different levels.
---

# Availability (reliability) and disaster recovery (DR) in Azure DocumentDB: Behind the scenes

This article delves into the internals of [high availability (HA)](./high-availability.md) and [cross-region disaster recovery (DR)](./cross-region-replication.md) for Azure DocumentDB, outlining the design and capabilities of these features. It provides insights for effective in-region and cross-region strategy planning to ensure reliability and business continuity.

## Azure DocumentDB cluster anatomy

An **Azure DocumentDB** cluster is composed of one or more horizontally scaled physical shards (nodes). Each physical shard includes dedicated compute resources and remote premium SSD storage. The [compute and storage resources](./compute-storage.md) of a physical shard are exclusive to a single database and not shared across clusters or databases.

In clusters with multiple horizontally scaled shards, every shard has an identical compute and storage configuration. Regardless of the number of shards, all cluster resources are hosted within the same Azure region.

Azure DocumentDB uses *locally redundant storage* (LRS), ensuring all data is synchronously replicated three times within the cluster's physical location. Azure Storage transparently manages these replicas, verifies data integrity using cyclic redundancy checks (CRCs), and repairs any detected corruption using redundant data. Additionally, checksums are applied to network traffic to prevent data corruption during storage and retrieval.

:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster.png" alt-text="Diagram of the Azure DocumentDB cluster's components.":::
*Figure 1. Azure DocumentDB cluster components.*

Whether your application connects to a single shard or multishard cluster, it uses a single connection string and endpoint. This abstraction simplifies distributed database operations, making it as straightforward to connect to a multi-shard setup as to a standalone MongoDB database.

## In-region high availability (HA)
For production workloads, it is highly recommended to enable [**in-region high availability (HA)**](./high-availability.md) to meet modern reliability standards. While HA can be disabled for development or experimental clusters to reduce costs, it is critical for maintaining database availability in production.

HA can be toggled during cluster provisioning or at any time after the cluster is created. It is available in all Azure regions that support Azure DocumentDB, regardless of specific regional capabilities.

When HA is enabled, each primary physical shard in the cluster is paired with a standby shard. The standby shard mirrors the compute and storage configuration of its primary counterpart. This results in **six data replicas per shard**—three on the primary shard and three on the standby. In regions with [availability zones (AZs)](/azure/reliability/availability-zones-overview), primary and standby shards are deployed in separate zones.

Data is synchronously replicated between each primary and standby shard. Writes are acknowledged only after being successfully committed to both shards, ensuring strong consistency within the HA cluster. In other words, a standby physical shard is an always up-to-date full replica of its primary physical shard providing *strong consistency* within the highly available cluster.

:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster-with-ha.gif" alt-text="Diagram of high availability enablement in an Azure DocumentDB cluster.":::
*Figure 2. Azure DocumentDB cluster with and without in-region high availability (HA) enabled.*

In the event of a primary shard failure, the service automatically performs a *failover* to its standby shard. During failover, all read and write requests are redirected to the standby shard, which becomes the new primary. Write operations in progress during the failover are retried within the service to ensure continuity. A replacement shard is then created to re-establish synchronous replication, becoming the new standby.

## Cross-region replication: Regional disaster recovery (DR)

[Although rare](https://azure.status.microsoft/status/history/), regional outages can disrupt access to your database. Cross-region replication provides a robust disaster recovery (DR) strategy, ensuring access to your data even during large-scale disruptions.

With cross-region replication, you can create a replica cluster in a different Azure region. Each shard in the replica cluster asynchronously replicates data from its counterpart in the primary cluster. This replication model ensures *eventual consistency* while minimizing performance impact on the primary cluster.

Asynchronous replication avoids the need for each write operation to be immediately delivered to and confirmed by replicas before a "write complete" acknowledgment is sent back to the application. However, this means that some writes completed on the primary cluster may not yet be replicated to the replica cluster, resulting in replication lag. The extent of replication lag depends on the intensity of write operations on the primary cluster and the overall load on both the primary and replica clusters.

In this setup:

- The primary cluster in Region A handles all reads and writes.
- The replica cluster in Region B supports read-only access, enabling high-performance read operations closer to applications or users in that region.

Applications can perform OLTP queries on the primary cluster in region A and intense read operations such as OLAP/reporting queries can be pointed to the replica cluster in region B.

Applications can use a *dynamic global read-write connection string*, which always points to the cluster open for writes. During a regional outage, the replica cluster in Region B can be promoted to accept writes. The global connection string automatically updates to point to the promoted cluster, ensuring uninterrupted write operations.

:::image type="content" source="media/availability-and-dr-under-the-hood/mongodb-vcore-cluster-with-replica.gif" alt-text="Diagram of a cross-region replica promotion for disaster recovery purpose in Azure DocumentDB.":::
*Figure 3. Regional disaster recovery (DR) with an Azure DocumentDB cluster with cross-region replication enabled. Cluster in region B is promoted to become the new read-write cluster. Cluster in region A becomes a replica cluster.*

## Summary of in-region availability and cross-region DR capabilities

The following table summarizes primary considerations for enabling and managing in-region high availability and cross-region disaster recovery strategy.

|Scenario |Azure DocumentDB feature|No data loss|Protection from region-wide outages|Automatic failover|No connection string change|
|-----------------------|----------------------------------|--------------------|--------------------|--------------------|---------------------|
|Physical shard failure | In-region high availability (HA) | :heavy_check_mark: | :x:                | :heavy_check_mark: | :heavy_check_mark:  |
|Regional outage        | Cross-region replica cluster     | :x:                | :heavy_check_mark: | :x:                | :heavy_check_mark:† |

† When using the global read-write connection string.

## Related content

- [Learn about in-region high availability in Azure DocumentDB](./high-availability.md)
- [Learn about cross-region replication and cross-region disaster recovery](./cross-region-replication.md)
- [Learn about reliability in Azure DocumentDB](/azure/reliability/reliability-documentdb?context=/azure/documentdb/context/context)
