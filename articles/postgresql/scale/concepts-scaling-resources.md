---
title: Scaling Resources
description: This article describes the resource scaling in an Azure Database for PostgreSQL flexible server instance.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Scaling resources in Azure Database for PostgreSQL

An Azure Database for PostgreSQL flexible server instance supports both vertical and horizontal scaling options.

## Vertical scaling

You can scale your instance vertically by adding more resources to your Azure Database for PostgreSQL flexible server instance. You can increase or decrease the number of CPUs and memory assigned to it.

The network throughput of your instance depends on the values you choose for CPU and memory.

After you create an Azure Database for PostgreSQL flexible server instance, you can independently scale:

- Compute tier and SKU.
- Storage tier and size.
- Backup retention period.

You can scale the compute tier up or down between Burstable, General Purpose, and Memory Optimized to adjust to the needs of your workload. In each of these tiers, you can choose from a wide selection of preconfigured hardware of different generations with varying numbers of CPUs and amounts of installed memory. You can select the option that supports your resource requirements while keeping your operational costs reduced and adjusted to your needs.

You can scale the number of vCores and installed memory up or down. You can also configure the storage tier up or down to accommodate the throughput and IOPS requirements that your workload demands. You can only increase the storage size. Depending on your requirements, you can increase or decrease the backup retention period between 7 to 35 days.

You can scale these resources by using multiple interfaces. For instance, you can use the [Azure portal](../configure-maintain/quickstart-create-server.md) or [Azure CLI](../configure-maintain/quickstart-create-server.md).

> [!NOTE]  
> After you increase the size of the storage assigned to your instance, you can't shrink it to a smaller size.

## Horizontal scaling

Azure Database for PostgreSQL elastic clusters allows you to horizontally scale out your database to support data workloads that extend beyond the capabilities of a single database instance. Elastic clusters also enable the potential to execute parallel operations simultaneously across all nodes in a cluster, significantly increasing throughput and unlocking ultra-low latency. Elastic clusters offer two table sharding models: row-based sharding and schema-based sharding.

:::image type="content" source="media/concepts-scaling-resources/elastic-clusters.png" alt-text="Diagram of Elastic cluster five-node configuration." lightbox="media/concepts-scaling-resources/elastic-clusters.png":::

## Read replica scaling

Another approach to scaling your instance horizontally is by creating [read replicas](../read-replica/concepts-read-replicas.md). Read replicas let you scale your read workloads onto separate Azure Database for PostgreSQL flexible server instances. They don't affect the performance and availability of the primary instance.

In a horizontally scaled setup, you can also scale the primary instance and the read replicas vertically.

When you change the number of vCores or the compute tier, the instance restarts so that the new hardware assigned begins running your server workload. During this time, the system switches over to the new server type. No new connections can be established, and all uncommitted transactions are rolled back.

The overall time it takes to restart your server depends on the crash recovery process and database activity at the time of the restart. Restart typically takes a minute or less, but it can be several minutes. Timing depends on the transactional activity when the restart was initiated.

If your application is sensitive to loss of in-flight transactions that might occur during compute scaling, implement a transaction [retry pattern](../single-server/concepts-connectivity.md#handling-transient-errors).

Scaling the storage doesn't require a server restart in most cases. For more information, see [storage options in Azure Database for PostgreSQL](concepts-scaling-resources.md).

Backup retention period changes are an online operation.

To improve the restart time, perform scale operations during off-peak hours. That approach reduces the time needed to restart the database server.

## Near-zero downtime scaling

Near-zero downtime scaling is a feature designed to minimize downtime when you modify storage and compute tiers. If you modify the number of vCores or change the compute tier, the server restarts to apply the new configuration. During this transition to the new server, no new connections can be established.

Typically, this process could take anywhere between 2 to 10 minutes with regular scaling. With the near-zero downtime scaling feature, this duration is reduced to less than 30 seconds. This reduction in downtime during scaling resources improves the overall availability of your database instance.

### How it works

When you update your Azure Database for PostgreSQL flexible server instance in scaling scenarios, the service creates a new virtual machine for your server with the updated configuration. Then it synchronizes with the virtual machine that's currently running your instance, and then switches to the new virtual machine with a brief interruption. Then a background process eliminates the old virtual machine.

This process enables seamless updates with minimal downtime and is automatically triggered when you change storage or compute tiers. You don't need to take any action to use this capability. This capability is supported for both HA and non-HA Azure Database for PostgreSQL flexible server instances.

For horizontally scaled configurations, consisting of a primary server and one or more read replicas, scaling operations must follow a specific sequence to ensure data consistency and minimize downtime. For details about that sequence, see [scaling with read replicas](../read-replica/concepts-read-replicas.md#scale).

> [!NOTE]  
> Near-zero downtime scaling is the _default_ type of operation. When the following [limitations](#considerations-and-limitations) are encountered, the system switches to regular scaling, which involves more downtime compared to the near-zero downtime scaling.

### Precise downtime expectations

- **Downtime duration**: In most cases, the downtime ranges from 10 to 30 seconds.
- **Other considerations**: After a scaling event, there's an inherent DNS `Time-To-Live` (TTL) period of approximately 30 seconds. The scaling process doesn't directly control this period. It's a standard part of DNS behavior. From an application perspective, the total downtime experienced during scaling could be in the range of 40 to 60 seconds.

#### Considerations and limitations

- For near-zero downtime scaling to work, allow all [inbound and outbound connections between the IP addresses in the delegated subnet, when you use virtual network integrated networking](../network/concepts-networking-private.md#virtual-network-concepts). If you don't permit these connections, the near-zero downtime scaling process doesn't work, and scaling occurs through the standard scaling workflow.
- Near-zero downtime scaling doesn't work if there are regional capacity constraints or quota limits on your subscription.
- Near-zero downtime scaling doesn't work for a replica server, because it's only supported on the primary server. For replica servers, the scaling operation automatically goes through the regular process.
- Near-zero downtime scaling doesn't work if a [virtual network-injected server](../network/concepts-networking-private.md#virtual-network-concepts) doesn't have sufficient usable IP addresses in the delegated subnet. If you have a standalone server, one extra IP address is necessary. For an instance with high-availability enabled, two extra IP addresses are required.
- Logical replication slots aren't preserved during a near-zero downtime failover event. To maintain logical replication slots and ensure data consistency after a scale operation, use the [pg_failover_slot](https://github.com/EnterpriseDB/pg_failover_slots) extension. For more information, see [enabling the pg_failover_slots extension in an instance of flexible server](../extensions/concepts-extensions-considerations.md#pg_failover_slots).
- Near-zero downtime scaling doesn't work with [unlogged tables](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-UNLOGGED). If you use unlogged tables for any of your data, you lose all the data in those tables after the near-zero downtime scaling.
- Near-zero doesn't work if you scale the compute of your server from or to a compute size of 1 or 2 vCores of the Burstable tier.

## Related content

- [Manage Azure Database for PostgreSQL](../configure-maintain/how-to-manage-server-portal.md)
