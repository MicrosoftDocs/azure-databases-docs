---
title: Premium SSD v2
description: This article describes about Premium ssd v2 storage option for an Azure Database for PostgreSQL flexible server instance.
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

Premium SSD v2 offers higher performance than Premium SSD, while also being less costly, as a general rule. You can individually tweak the performance (capacity, throughput, and input/output operations per second, referred to as IOPS) of Premium SSD v2 at any time. The ability to do these adjustments allow workloads to be cost-efficient, while meeting shifting performance needs. For example, a transaction-intensive database might need to cope with a large amount of IOPS for a couple of exceptionally high-demand days. Or a gaming application might demand higher throughput during peak hours only. Hence, for most general-purpose workloads, Premium SSD v2 can provide the best price for performance. You can now deploy Azure Database for PostgreSQL flexible server instances with Premium SSD v2 disk in all supported regions.

> [!NOTE]  
> Premium SSD v2 is currently in preview for Azure Database for PostgreSQL flexible server instances.

### Differences between Premium SSD and Premium SSD v2

Unlike Premium SSD, Premium SSD v2 doesn't have dedicated sizes. You can set a Premium SSD v2 disk to any size you prefer, and make granular adjustments as per your workload requirements. Those granular increments can go in steps of 1 GiB. Premium SSD v2 doesn't support host caching, but still provide lower latency than Premium SSD. Premium SSD v2 capacities range from 1 GiB to 64 TiBs.

The following table provides a comparison of different aspect of the types of disk supported by Azure Database for PostgreSQL flexible server instances, to help you decide which one suits your needs better.

#### Premium SSD v2 - IOPS

Azure Database for PostgreSQL server offers a baseline IOPS of 3000 for disks up to 399 GiB, and 12000 IOPS for disks over 400 GiB at no extra cost. To achieve 80,000 IOPS on a disk, it must be at least 160 GiB. Increasing IOPS beyond the free tier results in extra charges.

#### Premium SSD v2 - Throughput

Azure Database for PostgreSQL offers a baseline throughput of 125 MB/s for disks up to 399 GiB, and 500 MB/s for disks over 400 GiB at no extra cost. Increasing throughput beyond the free tier results in extra charges.

> [!NOTE]  
> Premium SSD v2 is currently in preview for Azure Database for PostgreSQL flexible server instances.


## Premium SSD v2 - High availability

High availability is now supported for Azure Database for PostgreSQL flexible server instances using Premium SSD v2. You can configure both zone-redundant and same-zone high availability options using this storage tier. 


#### Premium SSD v2 - Limitations during preview

- [Geographically redundant backups](../backup-restore/concepts-geo-disaster-recovery.md), [data encryption with customer managed keys](../security/security-data-encryption.md), [Major Version Upgrade](concepts-major-version-upgrade.md), [Long Term Retention](../backup-restore/concepts-backup-restore.md) or storage auto grow  features aren't supported for Premium SSD v2.
  
- Please wait until your first backup becomes available before configuring in-region replicas, as this process depends on disk snapshots. This limitation does not apply to cross-region replicas, which use pg_basebackups instead.

- Online migration from Premium SSD (PV1) to Premium SSD v2 (PV2) isn't supported. As an alternative, if you want to migrate across the different storage types, you can perform a [point-in-time-restore](../backup-restore/concepts-backup-restore.md#point-in-time-recovery) of your existing server to a new one with a different storage type.

- Premium SSD V2 can only be enabled in the following regions:
   *Australia East, Brazil South, Canada Central, Central India, Central US, East Asia, East US, East US 2, France Central, Germany West Central, Israel Central, Japan East, Korea Central, Norway East, Poland Central, South Central US, Southeast Asia, Switzerland North, UAE North, West Central US, West Europe, and West US 2*.  

- Premium SSD v2 can be provisioned using General Purpose and Memory Optimized compute tiers only. Creating new Burstable compute tier with Premium SSD v2 is not supported.
  
The storage that you provision is the amount of storage capacity available to your Azure Database for PostgreSQL flexible server instance. This storage is used for database files, temporary files, transaction logs, and PostgreSQL server logs. The total amount of storage that you provision also defines the I/O capacity available to your server.

The following table provides an overview of premium SSD v2 disk capacities and performance maximums to help you decide which want you should use.

| SSD v2 disk size | Maximum available IOPS | Maximum available throughput (MB/s) |
| :--- | :--- | :--- |
| 1 GiB-64 TiBs | 3,000-80,000 (Increases by 500 IOPS per GiB) | 125-1,200 (increases by 0.25 MB/s per set IOPS) |

Your virtual machine type also has IOPS limits. Although you can select any storage size, independently from the server type, you might not be able to use all IOPS that the storage provides, especially when you choose a server with a few vCores.
To learn more, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md).

> [!NOTE]  
> Regardless of the type of storage you assign to your instance, storage can only be scaled up, not down.

You can monitor your I/O consumption in the [Azure portal](https://portal.azure.com/), or by using [Azure CLI commands](/cli/azure/monitor/metrics). The relevant metrics to monitor are [storage limit, storage percentage, storage used, and I/O percentage](../monitor/concepts-monitoring.md).



> [!IMPORTANT]  
> The selected compute size determines the minimum and maximum IOPS.

Learn how to [scale up or down IOPS](../scale/how-to-scale-compute.md).


## Related content

- [Manage Azure Database for PostgreSQL using the Azure portal](how-to-manage-server-portal.md).
- [Limits in Azure Database for PostgreSQL](concepts-limits.md).
