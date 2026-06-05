---
title: Compute Replicas in Azure HorizonDB
description: Learn about compute replicas in Azure HorizonDB, scaling up vCores and memory, and scaling out reads by adding replicas.
author: denzilribeiro
ms.author: denzilr
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: configuration
ms.topic: concept-article
---

# Compute replicas for Azure HorizonDB (Preview)

A compute replica is where the PostgreSQL relational engine runs and where language, query, and transaction processing occur. An Azure HorizonDB cluster contains one or more compute replicas:

- **Primary replica** - The single read-write replica that handles all write operations and can also serve read queries.
- **Standby replicas** - One or more read-only replicas that serve read traffic and act as failover candidates.

Azure HorizonDB supports two dimensions of compute scaling: scaling up (vertical) and scaling out (horizontal read scale-out).

## How compute replicas work

Each compute replica runs a stateless PostgreSQL engine that connects to the shared storage layer. The replica processes queries, manages transactions, and maintains a local NVMe SSD cache for frequently accessed data pages. Compute replicas are provisioned with 8 GB of memory per vCore. As you increase the vCore count, memory scales proportionally. You can scale compute resources without affecting storage, and vice versa.

### Local SSD cache

Every compute replica, whether primary or standby, includes a local NVMe SSD cache. This cache stores hot pages locally to reduce round trips to the remote storage layer, delivering lower read latencies for frequently accessed data. Because the cache is local, each replica maintains its own cache contents independent of other replicas.

### Offloaded tasks

Compute replicas offload durability and high availability tasks to the storage layer. This offloading frees CPU, disk, and network resources on the compute replica to run application workloads. The following tasks are handled by the storage layer instead of the compute replica:

| Task | PostgreSQL process | Resource savings |
| --- | --- | --- |
| WAL sending to replicas | walsender | Disk IO, Network IO |
| WAL archiving to blob storage | Archiver | Disk IO, Network IO |
| Dirty page writing | background writer | Disk IO |
| Checkpointing | checkpointer | Disk IO |
| Backups | pg_dump, pg_basebackup, pg_backup_start, pg_backup_stop | Disk IO |
| Full page writes | Backends doing WAL writing | Disk IO |
| PostgreSQL WAL recovery | startup recovering | Disk IO |
| PostgreSQL read replica redo | startup recovering | Disk IO |

## Scale up

Scaling up increases the vCores and memory allocated to each compute replica in the cluster. Scale up when your workload requires more processing power, memory per query for complex queries, large joins, or high connection counts, or needs more resources on your primary replica.

### When to scale up

Consider scaling up when you observe:

- Sustained high CPU utilization across replicas.
- Memory pressure causing excessive page evictions from the shared buffer pool.
- Query performance degradation due to insufficient compute resources.
- Workloads with large, complex queries that benefit from more memory and CPU per node.

### How scale up works

When you initiate a scale up operation, Azure HorizonDB restarts the compute replicas with the new vCore and memory configuration. During this restart:

- The database becomes temporarily unavailable.
- Existing connections are dropped.
- The service applies the new compute configuration and brings the server back online automatically.

## Scale out reads

Scaling out adds more standby replicas to the Azure HorizonDB cluster. Use scale out to distribute read traffic across multiple replicas, improving read throughput and reducing load on the primary replica. An Azure HorizonDB cluster supports up to 15 readable replicas in addition to the primary.

### When to scale out

Consider scaling out when you observe:

- Your application has read-heavy workloads.
- Your reads can tolerate a milliseconds delay for data visibility on a compute replica.
- You need to isolate reporting or analytics workloads from transactional write traffic.
- You want to improve availability by adding failover candidates across availability zones.

### How scale out works

When you add a standby or read replica to an Azure HorizonDB cluster:

1. A new compute replica is provisioned distributed across availability zones.
1. The replica connects to the shared storage layer. No data copying or replication setup is required because all replicas share the same underlying storage.
1. The replica begins serving read queries through the read-only endpoint.

Because the storage is shared, provisioning a new replica is fast. There's no need to stream an initial data snapshot or WAL as in traditional PostgreSQL streaming replication.

### Scale out considerations

- Adding a replica doesn't require downtime for the existing cluster. The new replica is provisioned and comes online without affecting the primary or other standby replicas.
- Removing a replica reduces the read capacity. If the cluster has only one standby replica, removing it disables high availability.
- All replicas in a cluster share the same vCore and memory configuration. You can't provision individual replicas with different compute tiers.
- Standby replicas serve read-only queries. Write operations must go through the primary replica via the read-write endpoint.

### Read-only endpoint

Azure HorizonDB provides a dedicated read-only endpoint that automatically load balances connections across all standby replicas. Applications that separate read and write traffic can direct read queries to this endpoint to distribute load without any application-level routing logic. The read-write endpoint always routes to the primary replica. Use it for all write operations and for reads that require the latest committed data.

## Relationship to high availability

Standby replicas serve a dual purpose: they handle read traffic and act as failover candidates. To enable zone-redundant high availability, you need at least two replicas (one primary and one standby) placed in separate availability zones. Adding more replicas increases both read capacity and failover options.

For more information about failover behavior, see [High availability in Azure HorizonDB (Preview)](../high-availability/concepts-high-availability-failover.md).

## Related content

- [Scale compute in Azure HorizonDB (Preview)](how-to-scale-compute.md)
- [Add or remove a replica in Azure HorizonDB (Preview)](how-to-add-remove-replica.md)
- [High availability in Azure HorizonDB (Preview)](../high-availability/concepts-high-availability-failover.md)
- [What is Azure HorizonDB (Preview)?](../overview.md)
