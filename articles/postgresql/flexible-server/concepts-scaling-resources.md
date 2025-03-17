---
title: Scaling resources
description: This article describes the resource scaling in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.date: 02/14/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Scaling resources in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server supports both vertical and horizontal scaling options.

## Vertical scaling

You can scale your instance vertically, by adding more resources to your Azure Database for PostgreSQL flexible server instance. You can increase or decrease the number of CPUs and memory assigned to it.

Network throughput of your instance depends on the values you choose for CPU and memory.

After an Azure Database for PostgreSQL flexible server instance is created, you can independently scale:

- Compute tier and SKU.
- Storage tier and size.
- Backup retention period.

Compute tier can be scaled up or down between Burstable, General Purpose, and Memory Optimized, to adjust to the needs of your workload. In each of these tiers, there's an ample selection of preconfigured hardware of different generations and with more or less CPUs and more or less installed memory. Among that wide selection you can choose the one that supports your resource requirements at any time, while keeping your operational costs reduced and adjusted to your needs.

The number of vCores and installed memory can be scaled up or down. The storage tier can also be configured up or down to accommodate to the requirements of throughput and IOPS that your workload demands. The storage size can only be increased. Also, depending on your requirements you can increase or decrease the backup retention period between 7 to 35 days.

These resources can be scaled by using multiple interfaces. For instance, you can use [Azure portal](quickstart-create-server.md) or [Azure CLI](quickstart-create-server.md).

> [!NOTE]
> After you increase the size of the storage assigned to your instance, you can't shrink it to a smaller size.

## Horizontal scaling

You can scale your instance horizontally by creating [read replicas](concepts-read-replicas.md). Read replicas let you scale your read workloads onto separate Azure Database for PostgreSQL flexible server instances. They don't affect the performance and availability of the primary instance.

In a horizontally scaled setup, the primary instance and the read replicas can also be scaled vertically.

When you change the number of vCores or the compute tier, the instance is restarted so that the new hardware assigned begins running your server workload. During this time, the system switches over to the new server type. No new connections can be established, and all uncommitted transactions are rolled back.

The overall time it takes to restart your server depends on the crash recovery process and database activity at the time of the restart. Restart typically takes a minute or less, but it can be several minutes. Timing depends on the transactional activity when the restart was initiated.

If your application is sensitive to loss of in-flight transactions that might occur during compute scaling, we recommend implementing a transaction [retry pattern](../single-server/concepts-connectivity.md#handling-transient-errors).

Scaling the storage doesn't require a server restart in most cases. For more information, see [storage options in Azure Database for PostgreSQL flexible server](concepts-scaling-resources.md).

Backup retention period changes are an online operation.

To improve the restart time, we recommend that you perform scale operations during off-peak hours. That approach reduces the time needed to restart the database server.

## Near-zero downtime scaling

Near-zero downtime scaling is a feature designed to minimize downtime when you modify storage and compute tiers. If you modify the number of vCores or change the compute tier, the server undergoes a restart to apply the new configuration. During this transition to the new server, no new connections can be established.

Typically, this process could take anywhere between 2 to 10 minutes with regular scaling. With the near-zero downtime scaling feature, this duration is reduced to less than 30 seconds. This reduction in downtime during scaling resources improves the overall availability of your database instance.

### How it works

When you update your Azure Database for PostgreSQL flexible server instance in scaling scenarios, the service creates a new virtual machine for your server with the updated configuration. Then is synchronized with the virtual machine that's currently running your instance, and then switches to the new with a brief interruption. Then a background process eliminates the old virtual machine. All this process occurs at no extra cost to you.

This process allows for seamless updates, while minimizing downtime and ensuring cost-efficiency. This scaling process is triggered when changes are made to the storage and compute tiers. *No customer action is required* to use this capability.

For horizontally scaled configurations, consisting of a primary server and one or more read replicas, scaling operations must follow a specific sequence to ensure data consistency and minimize downtime. For details about that sequence, see [scaling with read replicas](concepts-read-replicas.md#scale).

> [!NOTE]
> Near-zero downtime scaling is the _default_ type of operation. When the following [limitations](#considerations-and-limitations) are encountered, the system switches to regular scaling, which involves more downtime compared to the near-zero downtime scaling.

### Precise downtime expectations

* **Downtime duration**: In most cases, the downtime ranges from 10 to 30 seconds.
* **Other considerations**: After a scaling event, there's an inherent DNS `Time-To-Live` (TTL) period of approximately 30 seconds. The scaling process doesn't directly control this period. It's a standard part of DNS behavior. From an application perspective, the total downtime experienced during scaling could be in the range of 40 to 60 seconds.

#### Considerations and limitations

- For near-zero downtime scaling to work, allow all [inbound and outbound connections between the IP addresses in the delegated subnet, when you use virtual network integrated networking](concepts-networking-private.md#virtual-network-concepts). If these connections aren't permitted, the near-zero downtime scaling process doesn't work, and scaling occurs through the standard scaling workflow.
- Near-zero downtime scaling doesn't work if there are regional capacity constraints or quota limits on your subscription.
- Near-zero downtime scaling doesn't work for a replica server, because it's only supported on the primary server. For replica servers, the scaling operation automatically goes through the regular process.
- Near-zero downtime scaling doesn't work if a [virtual network-injected server](concepts-networking-private.md#virtual-network-concepts) doesn't have sufficient usable IP addresses in the delegated subnet. If you have a standalone server, one extra IP address is necessary. For an instance with high-availability enabled, two extra IP addresses are required.
- Logical replication slots aren't preserved during a near-zero downtime failover event. To maintain logical replication slots and ensure data consistency after a scale operation, use the [pg_failover_slot](https://github.com/EnterpriseDB/pg_failover_slots) extension. For more information, see [enabling the pg_failover_slots extension in an instance of flexible server](../extensions/concepts-extensions-considerations.md#pg_failover_slots).
- Near-zero downtime scaling doesn't work with [unlogged tables](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-UNLOGGED). If you're using unlogged tables for any of your data will lose all the data in those tables after the near-zero downtime scaling.
- Near-zero downtime scaling is currently not supported for High Availability (HA) enabled servers.

## Related content

- [Manage Azure Database for PostgreSQL flexible server](how-to-manage-server-portal.md).
