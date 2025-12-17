---
title: Cross-Region Replication Best Practices - Disaster Recovery
description: Learn how to configure Azure DocumentDB cross-region replication for disaster recovery and read scalability. Includes best practices for replica cluster promotion and connection strings.
author: abinav2307
ms.author: abramees
ms.topic: best-practice
ms.date: 11/05/2025
ms.custom:
  - sfi-image-nochange
#Customer Intent: As a database adminstrator, I want to configure cross-region replication, so that I can have disaster recovery plans in the event of a regional outage.
---

# Cross-region and same-region replication best practices in Azure DocumentDB

This article discusses cross-region disaster recovery (DR) for Azure DocumentDB. It also covers read capabilities of the replica clusters in the same or other Azure regions for read operations scalability.

The replication feature allows you to replicate data from a cluster to a read-only cluster in another or the same Azure region. Replicas are updated with asynchronous replication technology. You can have one cluster replica in another region of choice for the primary Azure DocumentDB cluster. In a rare case of region outage, you can promote cluster replica in another region to become the new read-write cluster for continuous operation of your MongoDB database. Applications might continue to use the same connection strings after cluster replica in another region is promoted to become the new primary cluster.

Replicas are new clusters that you manage similar to regular clusters. For each read replica, you're billed for the provisioned compute in vCores and storage in GiB/month. Compute and storage costs for replica clusters have the same structure as the regular clusters and prices of the Azure region where they're created.

## Disaster recovery using replica clusters

Cross-region replication is one of several important pillars in [the Azure business continuity and disaster recovery (BCDR) strategy](/azure/reliability/business-continuity-management-program). Cross-region replication asynchronously replicates the same applications and data across other Azure regions for disaster recovery protection. Not all Azure services automatically replicate data or automatically fall back from a failed region to cross-replicate to another enabled region. Azure DocumentDB provides an option to create a cluster replica in another region and have data written on the primary cluster replicated to that replica automatically. The fallback to the cluster replica if there's an outage in the primary region needs to be initiated manually.

When cross-region replication is enabled on an Azure DocumentDB cluster, each shard gets replicated to another region continuously. This replication maintains a replica of data in the selected region. Such a replica is ready to be used as a part of disaster recovery plan in a rare case of the primary region outage. Replication is asynchronous. Write operations on the primary cluster's shard don't wait for completed replication to the corresponding replica's shard before sending confirmation of a successful write. Asynchronous replication helps to avoid increased latencies for write operations on the primary cluster.  

## Continuous writes, read operations on cluster replicas, and connection strings

The global read-write connection string in Azure DocumentDB consistently directs writes to the active write-enabled cluster. When you initiate a replica cluster promotion, the replica cluster in Region B is switched to write mode, while the original primary cluster in Region A transitions to read-only. Before promotion, the global read-write connection string targets the primary cluster in Region A and then updates to point to Region B as it assumes write responsibilities. For applications using the global read-write connection string, write operations continue seamlessly throughout the promotion process, maintaining uninterrupted data flow.

Replica clusters are also available for reads. It helps offload intensive read operations from the primary cluster or deliver reduced latency for read operations to the clients that are located closer to the replication region. When cross-region replication is enabled, applications can use the replica cluster self connection string to perform reads from the cluster replica. The primary cluster is available for read and write operations using its own self connection string. 

:::image type="content" source="media/cross-region-replication/global-read-write-connection-string-in-azure-portal.png" alt-text="Screenshot of cluster connection strings in Azure DocumentDB including global read-write connection string and self connection string.":::

When you create a replica by enabling cross-region or same region replication, it doesn't inherit networking settings such as firewall rules of the primary cluster. These settings must be set up independently for the replica. The replica inherits the admin account from the primary cluster. User accounts need to be managed on the primary cluster. You can connect to the primary cluster and its replica cluster using the same user accounts.

## Replica cluster promotion

If a region outage occurs, you can perform disaster recovery operation by promoting your cluster replica in another region to become available for writes. During replica promotion operation, these steps are happening:

1. Writes on the replica in region B are enabled in addition to reads. The former replica becomes a new read-write cluster.
1. The promoted replica cluster in region B accepts writes using its connection string and the global read-write connection string.
1. The cluster in region A is set to read-only and keeps its connection string.

> [!IMPORTANT]
> Because replication is asynchronous, some data from cluster in region A might not be replicated to region B when cluster replica in region B is promoted. If so, promotion would result in the unreplicated data not present on both clusters.

## Authentication methods on replica clusters

Authentication methods are managed independently on the primary and replica clusters. Users and other security principals, such as managed identities, are always managed on the primary cluster and synchronized to the replica cluster.  

If the primary cluster has native DocumentDB authentication method disabled *at the time the replica cluster is created*, enabling native DocumentDB authentication on the replica isn't allowed. To enable native DocumentDB authentication on such a replica, it must first be promoted.

## Related content

- [Learn how to enable replication and promote replica cluster](./how-to-cluster-replica.md)
- [See replication limits and limitations](./limitations.md#cross-region-and-same-region-replication)
- To resolve an issue with cross-region replication, see [this troubleshooting guide](./troubleshoot-replication.md).
- [Learn about reliability in Azure DocumentDB](/azure/reliability/reliability-documentdb?context=/azure/documentdb/context/context)
