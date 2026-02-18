---
title: Building Resilient Applications
titleSuffix: Azure Managed Instance for Apache Cassandra
description: Learn about best practices for high availability and disaster recovery for Azure Managed Instance for Apache Cassandra.
author: TheovanKraay
ms.author: thvankra
ms.reviewer: sidandrews
ms.date: 06/04/2025
ms.service: azure-managed-instance-apache-cassandra
ms.topic: best-practice
keywords: azure high availability disaster recovery cassandra resiliency
#customer intent: As a networking engineer, I want to understand how to plan high availablity and disaster recovery for Azure Managed Instance for Apache Cassandra.
---

# Best practices for high availability and disaster recovery

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service allows configurations to be overridden, depending on the needs of each workload, which allows maximum flexibility and control where needed.

Apache Cassandra is a great choice for building highly resilient applications due to its distributed nature and peer-to-peer architecture. Any node in the database can provide the same functionality as any other node. This design contributes to Cassandra's robustness and resilience. This article provides tips on how to optimize high availability and how to approach disaster recover.

## Recovery point objective and recovery time objective

As long as you have the following elements, recovery point objective (RPO) and recovery time objective (RTO) are both usually low, close to zero:

- A [multiple region deployment](create-multi-region-cluster.md) with cross-region replication and a [replication factor](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html#replication-strategy) of 3.
- Enabled availability zones. Configure this option when you create a cluster in the [Azure portal](create-cluster-portal.md) or by using [Azure CLI](create-cluster-cli.md).
- Configured application-level failover using load balancing policy in the [client driver](https://cassandra.apache.org/doc/stable/cassandra/getting-started/drivers.html) or load balancing-level failover using Azure Traffic Manager or Azure Front Door.

RTO is *how long you're down in an outage*. It's low because the cluster is resilient across both zones and regions. Also, Apache Cassandra itself is a highly fault tolerant, peer-to-peer system, where all nodes can write by default.

RPO is *how much data can you lose in an outage*. It's low because data is synchronized between all nodes and data centers. Data loss in an outage would be minimal.

> [!NOTE]  
> It's not possible to achieve both RTO=0 *and* RPO=0 per the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem). Evaluate the trade-off between consistency and availability or optimal performance.
>
> This balance looks different for each application. For example, if your application is read heavy, it might be better to cope with increased latency of cross-region writes to avoid data loss, which favors consistency. If the application is write heavy with tight latency requirements, the risk of losing some of the most recent writes in a major regional outage might be acceptable, which favors availability.

## Availability zones

Cassandra's peer-to-peer architecture brings fault tolerance from the ground up. Azure Managed Instance for Apache Cassandra provides support for [availability zones](/azure/reliability/availability-zones-region-support) in selected regions. This support enhances resiliency at the infrastructure level. For a replication factor of 3, availability zone support ensures that each replica is in a different availability zone. This approach prevents a zone outage from affecting your database or application. We recommend enabling availability zones where possible.

## Multi-region redundancy

Cassandra's architecture, coupled with Azure availability zones support, gives you a level of fault tolerance and resiliency. Also consider the impact of regional outages for your applications. To safeguard against region level outages, we highly recommend deploying [multiple region clusters](create-multi-region-cluster.md). Although they're rare, the potential impact is severe.

For business continuity, it isn't sufficient to use a multiple region database. Other parts of your application also need to be distributed or with adequate mechanisms to fail over. If your users are spread across many geo locations, a multiple region data center deployment for your database has the added benefit of reducing latency. All nodes in all data centers across the cluster can serve both reads and writes from the region that is closest to them. 

If the application is configured to be *active-active*, consider how the [CAP theorem](https://cassandra.apache.org/doc/latest/cassandra/architecture/guarantees.html#what-is-cap) applies to the consistency of your data between replicas (nodes) and the trade-offs required to delivery high availability.

In CAP theorem terms, Cassandra is by default an Available Partition-tolerant (AP) database system, with highly [tunable consistency](https://cassandra.apache.org/doc/4.1/cassandra/architecture/dynamo.html#tunable-consistency). For most use cases, we recommend using LOCAL_QUORUM for reads.

- In active-passive for writes, there's a trade-off between reliability and performance. For reliability, we recommend QUORUM_EACH but for most users LOCAL_QUORUM or QUORUM is a good compromise. If there's a regional outage, some writes might be lost in LOCAL_QUORUM.
- If an application runs in parallel, prefer QUORUM_EACH writes for most cases to ensure consistency between the two data centers.
- If your goal is to favor consistency, or lower RPO, rather than latency or availability, or lower RTO, your consistency settings and replication factor should reflect this goal.

  In general, the number of quorum nodes required for a read plus the number of quorum nodes required for a write should be greater than the replication factor. For example, if you have a replication factor of 3, and quorum_one on reads (one node), you should do quorum_all on writes (three nodes), so that the total of 4 is greater than the replication factor of 3.

> [!NOTE]  
> The control plane operator for Azure Managed Instance for Apache Cassandra is only deployed in a single region. The region is the one selected when you deploy the first data center. In the unlikely event of a total region outage, we commit to a 3 hour recovery time for failing over the control plane to another region.
> 
> Because data centers should still continue to function, this issue doesn't affect the [availability SLA](https://azure.microsoft.com/support/legal/sla/managed-instance-apache-cassandra/v1_0/) for the service. During this period, it might not be possible to make changes to the database configuration from the Azure portal or resource provider tools.

## Replication

We recommend auditing `keyspaces` and their replication settings from time to time to ensure that the required replication between data centers is configured. In the early stages of development, we recommend that you do simple tests using `cqlsh`. For example, insert a value while connected to one data center and read it from the other.

In particular, when you set up a second data center where an existing data center already has data, determine that you replicated all the data and that the system is ready. We recommend that you monitor replication progress through our [DBA commands with `nodetool netstats`](dba-commands.md#run-a-nodetool-command). An alternate approach would be to count the rows in each table. Keep in mind that with big data sizes, due to the distributed nature of Cassandra, this approach can give only a rough estimate.

## Balancing the cost of disaster recovery

If your application is *active-passive*, we still generally recommend that you deploy the same capacity in each region. This approach helps your application fail over instantly to a *hot standby* data center in a secondary region. If a regional outage occurs, this approach ensures no performance degradation. Most Cassandra [client drivers](https://cassandra.apache.org/doc/stable/cassandra/getting-started/drivers.html) provide options to initiate application level failover. By default, they assume regional outage means that the application is also down, so failover should happen at the load balancer level.

To reduce the cost of provisioning a second data center, you might prefer to deploy a smaller SKU and fewer nodes in your secondary region. When an outage occurs, [turnkey vertical and horizontal scaling](create-cluster-portal.md#scale-a-datacenter) makes scaling up easier in Azure Managed Instance for Apache Cassandra. While your applications fail over to your secondary region, you can manually [scale out](create-cluster-portal.md#horizontal-scale) and [scale up](create-cluster-portal.md#vertical-scale) the nodes in your secondary data center. Your secondary data center acts as a lower cost warm standby. Taking this approach needs to be balanced against the time required to restore your system to full capacity if an outage occurs. It's important to test and practice what happens when a region is lost.

> [!NOTE]  
> Scaling up nodes is much faster than scaling out. Keep this fact in mind when you consider the balance between vertical and horizontal scale, and the number of nodes to deploy in your cluster.

## Backup schedules

Backups are automatic in Azure Managed Instance for Apache Cassandra. You can pick your own schedule for the daily backups. We recommend choosing times with less load. Though backups are configured to only consume idle CPU, they can in some circumstances trigger [compactions](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/compaction/overview.html) in Cassandra, which can lead to an increase in CPU usage. Compactions can happen anytime with Cassandra. They depend on workload and chosen compaction strategy.

> [!IMPORTANT]  
> The intent of backups is purely to mitigate accidental data loss or data corruption. We do **not** recommend backups as a disaster recovery strategy.
>
> Backups aren't geo-redundant. Even if they were, it can take a long time to recover a database from backups. Therefore, we strongly recommend multiple region deployments, coupled with enabling availability zones where possible, to mitigate against disaster scenarios, and to be able to recover effectively from them. This approach is particularly important in the rare scenarios where the failed region can't be recovered. Without multi-region replication, all data might be lost.

:::image type="content" source="media/resilient-applications/backup.png" border="true" alt-text="Screenshot of backup schedule configuration page." lightbox="media/resilient-applications/backup.png":::

## Next step

> [!div class="nextstepaction"]
> [Create a cluster using Azure Portal](create-cluster-portal.md)
