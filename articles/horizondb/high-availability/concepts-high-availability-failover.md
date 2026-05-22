---
title: High Availability and Failover Concepts in Azure HorizonDB
description: Learn about high availability architecture, zone redundancy, failover processes, and recovery behavior in Azure HorizonDB.
author: denzilribeiro
ms.author: denzilr
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: high-availability
ms.topic: concept-article
---

# High availability in Azure HorizonDB (preview)

For mission-critical workloads, minimizing downtime and preventing data loss are essential requirements. In Azure HorizonDB, High availability is achieved through a combination of **zone-resilient storage**, **distributed compute replicas**, and **automated failover mechanisms**. 

## Overview of high availability
Unlike traditional PostgreSQL deployments that rely on streaming replication between independent servers, Azure HorizonDB uses a cloud-native architecture that separates compute and storage. This architecture  changes how failover works by eliminating the need for rewind of WAL (write-ahead log) or post failover reinitialization of the primary, thereby reducing failover time.

### Compute replicas
High availability at the compute layer requires at least **2 compute replicas**. Compute replicas serve as both read scale-out targets and failover candidates.

A HorizonDB cluster consists of:
  - One **primary replica** (read/write)
  - One or more **readable HA replicas**

When you add a replica, the system automatically places it in a **different availability zone** when the region supports multiple zones. This placement provides **zone-level fault isolation** at the compute layer.

> [!IMPORTANT]
> To achieve high availability, you must provision at least one replica in addition to the primary

### Zone-redundant storage
Unlike traditional PostgreSQL replication, Azure HorizonDB doesn't stream WAL from the primary to standby replicas for data durability. Instead, the architecture relies on a shared storage layer:

- The zone redundant **WAL service** that is shared across all compute replicas.
- The zone redundant **data storage fleet**  that asynchronously applies WAL from the WAL service.
- Azure Blob storage that's zone-redundant and provides underlying durability for both data and WAL archival.

## Failover process

Failover is the process of promoting a standby replica to become the new primary when the current primary becomes unavailable. Azure HorizonDB supports both automatic and planned failover.

### Automatic failover (unplanned)
Automatic failover occurs when the primary compute replica becomes unavailable due to an unexpected event, such as:

- Hardware failure in the availability zone hosting the primary
- Network partitions affecting the primary replica
- Operating system or process-level failures on the primary

When the service detects that the primary is unavailable, it initiates the following sequence:

1. **Detection** - The platform detects failure based on replica health signals.
1. **Fencing** - Ring fence the primary so that no more writes occur.
1. **Promotion** - A standby replica in a healthy availability zone is selected and promoted to primary. If there are multiple replicas, then the one that's closest to the LSN of the primary replica is chosen as a failover target.
1. **Wait for Promotion** - wait until the database is writable.
1. **Endpoint update** - The read-write endpoint is updated to point to the newly promoted primary.
1. **Client reconnection** - Client connections to the previous primary are dropped. Applications reconnect through the read-write endpoint, which now routes to the new primary.


### Planned failover

A **planned failover** is a controlled operation initiated by the user or platform. A planned failover is used to test high availability. In addition, the service initiates planned failover during maintenance operations, such as:
- Minor version upgrades
- Security patches

During a planned failover, the service follows a controlled sequence:

1. **Replica choice** - User initiated planned failover can specify the replica to fail over to and that replica becomes the target for failover.
1. **Fencing** - Ring fence the primary so that no more writes occur.
1. **Promotion** - The service promotes a standby chosen to the new primary
1. **Endpoint update** - The read-write endpoint switches to the new primary.

Planned failovers typically complete faster than unplanned failovers as there's no detection required.

### Forced failover

A **forced failover** can be triggered by a user to immediately promote a replica to primary without waiting for a coordinated transition. A forced failover is similar in logic to an automatic failover but is initiated by a user.

### Data durability during failover

Azure HorizonDB guarantees that committed transactions aren't lost during failover. The WAL service persists every committed transaction durably across zones before acknowledging it to the client. Because all replicas read from the same durable storage, the promoted standby has access to every committed write.

Transactions that are in progress but not yet committed at the time of failover are rolled back, consistent with standard PostgreSQL ACID behavior.

## Application considerations

To get the most out of high availability in Azure HorizonDB, consider the following application-level practices:

- **Implement connection retry logic** - Use exponential backoff with retry on transient connection errors. Most PostgreSQL client libraries and frameworks support automatic retry configuration.
- **Use endpoints** - Always connect through the read-write or read-only endpoints rather than directly to specific replicas. The endpoints automatically route to the correct replica after a failover.
- **Avoid long-running transactions** - Long transactions delay planned failover completion and increase the risk of rollback during unplanned failover.
- **Don't store state in temporary tablespaces** - Temporary objects don't persist across failover events. Avoid creating user schema objects in temporary tablespaces.


## Related content

- [Overview of business continuity in Azure HorizonDB (preview)](../backup-restore/concepts-business-continuity.md)
- [Configure high availability in Azure HorizonDB (preview)](how-to-configure-high-availability.md)
- [Perform failover in Azure HorizonDB (preview)](how-to-perform-failover.md)
- [Backups in Azure HorizonDB (preview)](../backup-restore/concepts-backup-restore.md)
