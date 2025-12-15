---
title: Premium SSD v2
description: This article describes the Premium SSD v2 storage option for an Azure Database for PostgreSQL flexible server instance.
author: kabharati  
ms.author: kabharati
ms.reviewer: maghan
ms.custom: references_regions
ms.date: 01/16/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Premium SSD v2 storage option in Azure Database for PostgreSQL 

## Premium SSD v2 (preview)

Premium SSD v2 offers higher performance than Premium SSD, while also being less costly, as a general rule. You can individually tweak the performance (capacity, throughput, and IOPS (input/output operations per second)) of Premium SSD v2 at any time. The ability to do these adjustments allow workloads to be cost-efficient, while meeting shifting performance needs. For example, a transaction-intensive database might need to cope with a large amount of IOPS for a couple of exceptionally high-demand days. Or a gaming application might demand higher throughput during peak hours only. Hence, for most general-purpose workloads, Premium SSD v2 can provide the best price for performance. You can now deploy Azure Database for PostgreSQL flexible server instances with Premium SSD v2 disk in all supported regions.

> [!NOTE]  
> Premium SSD v2 is currently in preview for Azure Database for PostgreSQL flexible server instances.

### Differences between Premium SSD and Premium SSD v2

Unlike Premium SSD, Premium SSD v2 doesn't have dedicated sizes. You can set a Premium SSD v2 disk to any size you prefer, and make granular adjustments as per your workload requirements. Those granular increments can go in steps of 1 GiB. Premium SSD v2 doesn't support host caching, but still provide lower latency than Premium SSD. Premium SSD v2 capacities range from 1 GiB to 64 TiBs.


#### Premium SSD v2 - IOPS

Azure Database for PostgreSQL server offers a baseline IOPS of 3000 for disks up to 399 GiB, and 12000 IOPS for disks over 400 GiB at no extra cost. To achieve 80,000 IOPS on a disk, it must be at least 160 GiB. Increasing IOPS beyond the free tier results in extra charges.

#### Premium SSD v2 - Throughput

Azure Database for PostgreSQL offers a baseline throughput of 125 MB/s for disks up to 399 GiB, and 500 MB/s for disks over 400 GiB at no extra cost. Increasing throughput beyond the free tier results in extra charges.

> [!NOTE]  
> Premium SSD v2 is currently in preview for Azure Database for PostgreSQL flexible server instances.

The storage that you provision is the amount of storage capacity available to your Azure Database for PostgreSQL flexible server instance. This storage is used for database files, temporary files, transaction logs, and PostgreSQL server logs. The total amount of storage that you provision also defines the I/O capacity available to your server.

The following table provides an overview of premium SSD v2 disk capacities and performance maximums to help you decide which want you should use.

| SSD v2 disk size | Maximum available IOPS | Maximum available throughput (MB/s) |
| :--- | :--- | :--- |
| 1 GiB-64 TiBs | 3,000-80,000 (Increases by 500 IOPS per GiB) | 125-1,200 (increases by 0.25 MB/s per set IOPS) |

Your virtual machine type also has IOPS limits. Although you can select any storage size, independently from the server type, you might not be able to use all IOPS that the storage provides, especially when you choose a server with a few vCores.
To learn more, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md).

> [!NOTE]  
> Regardless of the type of storage you assign to your instance, storage can only be scaled up, not down.

You can monitor your I/O consumption in the [Azure portal](https://portal.azure.com/), or by using [Azure CLI commands](/cli/azure/monitor/metrics). The relevant metrics to monitor are [storage limit, storage percentage, storage used, and I/O percentage](concepts-monitoring.md).



> [!IMPORTANT]  
> The selected compute size determines the minimum and maximum IOPS.
## Premium SSD v2 - Features

In preview, the following features are now supported for Azure Database for PostgreSQL flexible server instances using Premium SSD v2 in Canada Central and East Asia regions.
- _High availability_ 
- _Read Replica_, 
- _Geo Redundant Backups_
- _Geo DR_
- _Major Version Upgrade_,
- _Virtual endpoints__


#### Premium SSD v2 - Limitations

-  Customer Managed Keys, On-demand backups, Long Term Backups, Online Disk scaling, and storage autogrow features aren't supported for Premium SSD v2.
  
- Online migration from Premium SSD (PV1) to Premium SSD v2 (PV2) isn't supported. As an alternative, if you want to migrate across the different storage types, you can perform a [point-in-time-restore](concepts-backup-restore.md#point-in-time-recovery) of your existing server to a new one with Premium SSD v2 storage type.

- Premium SSD v2 can be provisioned using General Purpose and Memory Optimized compute tiers only. Creating new Burstable compute tier with Premium SSD v2 isn't supported.

- You can adjust disk performance settings (IOPS or throughput) up to four times within a 24-hour period. For newly created disks, the limit is three adjustments during the first 24 hours.

-  During preview, restoring a deleted server (Tombstone recovery) may lead to up to 24 hours of data loss. To avoid accidental deletions, we recommend enabling resource lock.

-  If you create a new server using point-in-time restore (PITR) and immediately perform an operation that requires a full backup, the following error may occur. This error occurs because Premium SSD v2 disks don't support creating a snapshot while the disk is still hydrating. Wait until hydration finishes before retrying the operation.

    _Error message: Unable to create a snapshot from the disk because the disk is still being hydrated. Retry after some time._

-  Azure Storage allows only three instant snapshots per hour. If you run more than three full-backup operations on large datasets within an hour, the operation may fail. Wait an hour or stagger operations to avoid this error.

    _Error message**: Snapshot Limit Reached. You reached the snapshot limit for this disk. Wait until the current background copy process completes before creating new snapshots._
  
     **Examples include**:
           - Compute scaling, enabling HA, and performing failover and failback within one hour.
            - Major version upgrades, adding HA, failover, creating in-region replicas within one hour.        
                         
              

Learn how to [scale up or down IOPS](how-to-scale-compute-storage-portal.md).


## Related content

- [Manage Azure Database for PostgreSQL using the Azure portal](how-to-manage-server-portal.md).
- [Limits in Azure Database for PostgreSQL](concepts-limits.md).
