---
title: High availability (HA) and cross-region replication best practices
description: Learn about best practices for high availability (HA) and cross-region replication in Azure DocumentDB.
author: niklarin
ms.author: nlarin
ms.topic: concept-article
ms.date: 09/09/2025
#Customer Intent: As a database adminstrator, I want to understand what is the optimal use of high availability and cross-region replication in Azure DocumentDB in differenct cases.
---

# Best practices for high availability (HA) and cross-region replication in Azure DocumentDB

Ensuring high availability and enabling cross-region replication are essential for mission-critical applications using Azure DocumentDB. This document outlines best practices for configuring and managing [high availability (HA)](./high-availability.md) and [cross-region replication](./cross-region-replication.md). Follow guidance in this document to achieve optimal performance, resilience, and disaster recovery capabilities in Azure DocumentDB.

## High availability (HA) best practices

### Use HA for production clusters
Enabling high availability (HA) is crucial for production clusters and any clusters that are sensitive to downtime. In a production environment, unexpected node failures can cause significant disruptions. HA ensures that your cluster remains available and operational with zero data loss even when one of its physical shards (nodes) becomes unavailable.

### Use HA to achieve 99.99% SLA
Azure DocumentDB offers a **99.99% monthly availability SLA** for clusters with high availability enabled. To meet this SLA, ensure that HA is activated for all critical workloads that require continuous uptime.

### Enable HA for automatic failover
Clusters with high availability enabled automatically recover from physical shard failures without manual intervention. When a node failure occurs, the system promotes a standby physical shard to replace the failed primary node. The automatic failover process retains the same connection string, so that the failover process is seamless and transparent to applications. This feature is critical for applications that require continuous uptime and consistent data access.

### Disable HA for non-production clusters
For non-production clusters or those clusters that aren't sensitive to downtime, high availability can be disabled to reduce costs. These environments may tolerate occasional downtime without impacting business operations. Carefully assess the risk and cost trade-offs before disabling HA on any cluster.

### Use HA with availability zones
In regions where **availability zones** are supported, enabling HA ensures that each primary-standby physical shard pair is provisioned in different availability zones. Zone redundancy provides extra resilience by protecting your cluster from data center-level failures within a region.

## Cross-region replication best practices

### Use cross-region replication for disaster recovery
Use cross-region replication when a copy of cluster data needs to be stored in another Azure region for disaster recovery (DR) purposes. Cross-region replication ensures that your data is available even in the event of a regional outage. Azure DocumentDB supports active-passive replication configuration to facilitate cross-region disaster recovery. Active-passive replication keeps one cluster as the primary one in read-write mode and maintains a read-only replica cluster in another Azure region. 

If there's a rare regional outage, replica cluster can be promoted to become the new read-write cluster with minimal interruption. This capability ensures that your data remains safe and accessible even if an entire region experiences an outage.

### Configure replication with minimal impact on performance
When configuring cross-region replication, consider network latency and write latency impact on your applications. Choose regions for the primary read-write and replica clusters that are geographically close to your users and ensure that your applications are optimized for eventual consistency.

### Read scaling
Use cross-region replication to offload massive read operations from the primary cluster to a replica cluster. Offloading read operations to a replica cluster prevents overloading the primary cluster and ensures that the system can handle high read volumes efficiently.

### Combined HA and DR strategy
Combine high availability (HA) for in-region availability with cross-region replication for disaster recovery (DR) and global read scalability. The combination of two provides 99.995% SLA. This approach delivers the best balance between local resilience and global redundancy, ensuring continuous availability and optimal performance for your applications.

## Summary of best practices
| Scenario                                 | Recommendation                                        |
|------------------------------------------|-------------------------------------------------------|
| Production clusters                      | [Enable high availability](./how-to-scale-cluster.md#enable-or-disable-high-availability)                              |
| Clusters requiring 99.99% SLA            | [Enable high availability](./how-to-scale-cluster.md#enable-or-disable-high-availability)                              |
| Clusters requiring 99.995% SLA           | [Enable high availability](./how-to-scale-cluster.md#enable-or-disable-high-availability) and [create a replica cluster](./how-to-cluster-replica.md#enable-cross-region-or-same-region-replication) |
| Non-production clusters                  | [Disable high availability](./how-to-scale-cluster.md#enable-or-disable-high-availability) to reduce costs             |
| Automatic failover requirement           | [Enable high availability](./how-to-scale-cluster.md#enable-or-disable-high-availability)                              |
| Cross-region disaster recovery (DR)      | [Create a replica cluster](./how-to-cluster-replica.md#enable-cross-region-or-same-region-replication)                              |
| Read scalability across multiple regions | [Create a replica cluster](./how-to-cluster-replica.md#enable-cross-region-or-same-region-replication)                              |

By following these best practices, you can ensure that your Azure DocumentDB clusters remain highly available and resilient against failures and regional outages.

## Related content

- [Get insights into how high availability and cross-region replication work](./availability-disaster-recovery-under-hood.md)
- [Learn more about high availability](./high-availability.md)
- [Learn about cross-region replication](./cross-region-replication.md)

> [!div class="nextstepaction"]
> [Migration options for Azure DocumentDB](./migration-options.md)
