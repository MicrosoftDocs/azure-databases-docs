---
title: High Availability and Failover Concepts in Azure HorizonDB
description: Learn about high availability architecture, zone redundancy, failover processes, and recovery behavior in Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: high-availability
ms.topic: concept-article
ai-usage: ai-assisted
---

# High availability and failover in Azure HorizonDB (preview)

For mission-critical workloads, minimizing downtime and preventing data loss are essential requirements. Azure HorizonDB addresses these requirements through a high availability architecture that takes advantage of its disaggregated compute and storage design. Unlike traditional PostgreSQL deployments that rely on streaming replication between independent servers, Azure HorizonDB uses a shared, zone-resilient storage layer that all compute replicas access directly. This approach fundamentally changes how failover works - eliminating the need for WAL catch-up, reducing failover time, and guaranteeing that committed transactions are never lost.

This article explains the HA architecture, how failover works, and what to expect during both planned and unplanned failover events.

## High availability architecture

Azure HorizonDB achieves high availability by combining two core design principles:

- **Zone-redundant compute replicas** deployed across different availability zones within the same Azure region.
- **Shared zone-resilient storage** that decouples data durability from individual compute instances.

When HA is enabled, an Azure HorizonDB cluster runs at least two compute replicas: one **primary** (read-write) and one or more **standby** replicas (read-only). Each replica is placed in a separate availability zone, so a failure in one zone doesn't affect replicas in other zones.

### How storage supports high availability

Unlike traditional PostgreSQL replication, Azure HorizonDB doesn't stream WAL from the primary to standby replicas for data durability. Instead, the architecture relies on a shared storage layer:

- The **WAL service** accepts write-ahead log records from the primary compute replica and persists them durably across zones before acknowledging the transaction.
- The **data storage fleet** asynchronously applies WAL records to reconstruct page state, with each data shard replicated across multiple availability zones for resilience.
- Azure Blob storage provides the underlying durability layer for both data and WAL archival.

Because all replicas share the same underlying storage, standby replicas don't need to replay a full WAL stream to stay current. Each replica maintains its own local NVMe cache for hot pages, and reads the latest committed data directly from the shared storage layer. This shared-storage model eliminates replication lag for committed data and enables fast failover without log rewinding.

### Zone redundancy by default

All layers of the Azure HorizonDB storage stack are zone resilient by default, including WAL storage, data storage, and blob storage. You don't need to configure zone redundancy for the storage layer separately. Zone redundancy for compute replicas requires enabling HA and provisioning at least two replicas.

## Failover process

Failover is the process of promoting a standby replica to become the new primary when the current primary becomes unavailable. Azure HorizonDB supports both automatic and planned failover.

### Automatic failover (unplanned)

Automatic failover occurs when the primary compute replica becomes unavailable due to an unexpected event, such as:

- Hardware failure in the availability zone hosting the primary
- Network partitions affecting the primary replica
- Operating system or process-level failures on the primary

When the service detects that the primary is unavailable, it initiates the following sequence:

1. **Detection** - The monitoring service identifies the primary replica as unhealthy.
1. **Promotion** - A standby replica in a healthy availability zone is selected and promoted to primary.
1. **Endpoint update** - The read-write endpoint is updated to point to the newly promoted primary.
1. **Client reconnection** - Client connections to the previous primary are dropped. Applications reconnect through the read-write endpoint, which now routes to the new primary.

Because all replicas share the same durable storage, the promoted standby doesn't need to replay a full WAL backlog. It only needs to apply any WAL records that haven't yet been replayed to its local cache, which significantly reduces failover time compared to traditional streaming replication.

### Planned failover

The service initiates planned failover during maintenance operations, such as:

- Minor version upgrades
- Security patches
- Compute scaling operations

During a planned failover, the service follows a controlled sequence:

1. **Drain** - Active transactions on the primary complete. The service might temporarily hold new connections.
1. **Checkpoint** - The primary performs a final checkpoint to ensure all recent changes are persisted.
1. **Promotion** - The service promotes a standby Hyper-V Replica to primary.
1. **Endpoint update** - The read-write endpoint switches to the new primary.

Planned failovers typically complete faster than unplanned failovers because the primary flushes its state before the switch.

## Recovery behavior

After a failover completes, the promoted standby Replica takes over as the new primary and begins serving read-write traffic. Because all Replicas share the same durable storage layer, recovery is faster than in traditional PostgreSQL deployments where a standby must replay a full WAL stream before it can accept connections.

### Recovery time

The recovery time for a failover depends on:

- **WAL replay on the promoted replica** - The standby must apply any WAL changes that aren't yet reflected in its local cache. Because the storage layer is shared, this is typically a small amount of data.
- **Endpoint propagation** - DNS and endpoint updates to redirect traffic to the new primary.
- **Client reconnection** - Applications must detect the dropped connection and reconnect.

In most cases, failover completes within seconds to a few minutes. Applications should implement connection retry logic to handle brief interruptions during failover.

### Data durability during failover

Azure HorizonDB guarantees that committed transactions aren't lost during failover. The WAL service persists every committed transaction durably across zones before acknowledging it to the client. Because all replicas read from the same durable storage, the promoted standby has access to every committed write.

Transactions that are in progress but not yet committed at the time of failover are rolled back, consistent with standard PostgreSQL ACID behavior.

## High availability compared to compute replicas

The following table compares compute replicas without HA to zone-redundant HA:

| Capability | Compute replicas (without HA) | Zone-redundant HA |
| --- | --- | --- |
| Read scale-out | Yes | Yes |
| Zone redundancy | Not guaranteed | Replicas placed in separate zones |
| Automatic failover | No | Yes |
| Endpoint redirection | Manual | Automatic |
| Minimum replicas required | 1 | 2 |

Compute replicas serve as both read scale-out targets and failover candidates. Enabling HA ensures that at least two replicas exist in separate zones and that automatic failover is activated.

## Application considerations

To get the most out of high availability in Azure HorizonDB, consider the following application-level practices:

- **Implement connection retry logic** - Use exponential backoff with retry on transient connection errors. Most PostgreSQL client libraries and frameworks support automatic retry configuration.
- **Use the service endpoints** - Always connect through the read-write or read-only endpoints rather than directly to specific replicas. The endpoints automatically route to the correct replica after a failover.
- **Avoid long-running transactions** - Long transactions delay planned failover completion and increase the risk of rollback during unplanned failover.
- **Don't store state in temporary tablespaces** - Temporary objects don't persist across failover events. Avoid creating user schema objects in temporary tablespaces.

## Limitations

During the public preview, the following HA-related limitations apply:

| Limitation | Details |
| --- | --- |
| Cross-region failover | Not yet available. HA operates within a single Azure region. |
| Configurable maintenance windows | Planned maintenance runs on a system-managed schedule. Custom maintenance windows aren't yet supported. |

## Related content

- [Overview of business continuity in Azure HorizonDB (preview)](../backup-restore/concepts-business-continuity.md)
- [Configure high availability in Azure HorizonDB (preview)](how-to-configure-high-availability.md)
- [High Availability (HA) health status monitoring in Azure HorizonDB](how-to-monitor-high-availability.md)
- [Backups in Azure HorizonDB (preview)](../backup-restore/concepts-backup-restore.md)
