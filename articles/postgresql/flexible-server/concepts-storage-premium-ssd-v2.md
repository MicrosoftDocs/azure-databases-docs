---
title: Storage options
description: This article describes the storage options in Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.custom: references_regions
ms.date: 01/16/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Storage options in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You can create an Azure Database for PostgreSQL flexible server instance using [Azure managed disks](/azure/virtual-machines/managed-disks-overview), which are block-level storage volumes managed by Azure and used with Azure Virtual Machines. Managed disks are like a physical disk in an on-premises server, but they're virtualized. With managed disks, all you have to do is specify the disk size, the disk type, and provision the disk. Once you provision the disk, Azure handles the rest. Azure Database for PostgreSQL flexible server supports premium solid-state drives (Premium SSD) and premium solid-state drives version 2 (Premium SSD v2), and the pricing is calculated based on the compute, memory, and storage tier you provision.


## Premium SSD v2 (preview)

Premium SSD v2 offers higher performance than Premium SSD, while also being less costly, as a general rule. You can individually tweak the performance (capacity, throughput, and input/output operations per second, referred to as IOPS) of Premium SSD v2 at any time. The ability to do these adjustments allow workloads to be cost-efficient, while meeting shifting performance needs. For example, a transaction-intensive database might need to cope with a large amount of IOPS for a couple of exceptionally high-demand days. Or a gaming application might demand higher throughput during peak hours only. Hence, for most general-purpose workloads, Premium SSD v2 can provide the best price for performance. You can now deploy Azure Database for PostgreSQL flexible server instances with Premium SSD v2 disk in all supported regions.

> [!NOTE]  
> Premium SSD v2 is currently in preview for Azure Database for PostgreSQL flexible server.

### Differences between Premium SSD and Premium SSD v2

Unlike Premium SSD, Premium SSD v2 doesn't have dedicated sizes. You can set a Premium SSD v2 disk to any size you prefer, and make granular adjustments as per your workload requirements. Those granular increments can go in steps of 1 GiB. Premium SSD v2 doesn't support host caching, but still provide lower latency than Premium SSD. Premium SSD v2 capacities range from 1 GiB to 64 TiBs.

The following table provides a comparison of different aspect of the types of disk supported by Azure Database for PostgreSQL flexible server, to help you decide which one suits your needs better.

#### Premium SSD v2 - IOPS

Azure Database for PostgreSQL flexible server offers a baseline IOPS of 3000 for disks up to 399 GiB, and 12000 IOPS for disks over 400 GiB at no extra cost. To achieve 80,000 IOPS on a disk, it must be at least 160 GiB. Increasing IOPS beyond the free tier results in extra charges.

#### Premium SSD v2 - Throughput

Azure Database for PostgreSQL flexible server offers a baseline throughput of 125 MB/s for disks up to 399 GiB, and 500 MB/s for disks over 400 GiB at no extra cost. Increasing throughput beyond the free tier results in extra charges.

> [!NOTE]  
> Premium SSD v2 is currently in preview for Azure Database for PostgreSQL flexible server.


## Premium SSD v2 - High availability

High availability is now supported for Azure Database for PostgreSQL flexible server deployments using Premium SSD v2. You can configure both zone-redundant and same-zone high availability options using this storage tier. This capability is initially available in the following regions.

*Canada Central, Central US, East Asia,  East US 2*


#### Enable premium SSD v2 high availability preview

High availability is an opt-in feature that can be enabled at the subscription level using the following steps. As this is a preview feature, it is recommended for use only with non-production workloads.

1. In the **Search** bar, type **Preview features** and select it from the results.

 
 :::image type="content" source="./media/concepts-storage/preview-feature.png" alt-text="Screenshot of the preview page." lightbox="./media/concepts-storage/preview-feature.png":::

  
2. Use the **Filter by name** field, search for **Premium SSD v2 High Availability** and Select the **Subscription** 

 
   :::image type="content" source="./media/concepts-storage/registration.png" alt-text="Screenshot of the SSD v2 registration page." lightbox="./media/concepts-storage/registration.png":::

4.  Select the feature and click **Register**.

 
5. Validate that the **State** changed to **Registered**.


   :::image type="content" source="./media/concepts-storage/registration-validation.png" alt-text="Screenshot of the  registration validation page." lightbox="./media/concepts-storage/registration-validation.png":::



#### Premium SSD v2 - Limitations during preview

- [Read replicas](concepts-read-replicas.md), [geographically redundant backups](concepts-geo-disaster-recovery.md), [data encryption with customer managed keys](concepts-data-encryption.md), [Major Version Upgrade](concepts-major-version-upgrade.md), [Long Term Retention](concepts-backup-restore.md) or [storage autogrow](#limitations-and-considerations-of-storage-autogrow) features aren't supported for Premium SSD v2.

- Online migration from Premium SSD (PV1) to Premium SSD v2 (PV2) isn't supported. As an alternative, if you want to migrate across the different storage types, you can perform a [point-in-time-restore](concepts-backup-restore.md#point-in-time-recovery) of your existing server to a new one with a different storage type.

- Premium SSD v2 High availability can only be configured for servers created on or after July 1, 2025. Currently, SSD v2 High availability is supported in Canada Central, Central US,  East Asia, and East US 2 regions.
  
-  Premium SSD v2 High availability can only be configured for servers created with PG version 16.
  
- Premium SSD V2 can only be enabled in the following regions:
   *Australia East, Brazil South, Canada Central, Central India, Central US, East Asia, East US, East US 2, France Central, Germany West Central, Israel Central, Japan East, Korea Central, Norway East, Poland Central, South Central US, Southeast Asia, Switzerland North, UAE North, West Central US, West Europe, and West US 2*.  

- Point-in-time restore (PITR) from Premium SSD v2 to Premium SSD (v1) is currently not supported when the AFEC flag is enabled for accessing the High Availability (HA) preview feature.
  
- Premium SSD v2 can be provisioned using General Purpose and Memory Optimized compute tiers only. Creating new Burstable compute tier with Premium SSD v2 is not supported.
  
The storage that you provision is the amount of storage capacity available to your Azure Database for PostgreSQL flexible server instance. This storage is used for database files, temporary files, transaction logs, and PostgreSQL server logs. The total amount of storage that you provision also defines the I/O capacity available to your server.

The following table provides an overview of premium SSD v2 disk capacities and performance maximums to help you decide which want you should use.

| SSD v2 disk size | Maximum available IOPS | Maximum available throughput (MB/s) |
| :--- | :--- | :--- |
| 1 GiB-64 TiBs | 3,000-80,000 (Increases by 500 IOPS per GiB) | 125-1,200 (increases by 0.25 MB/s per set IOPS) |

Your virtual machine type also has IOPS limits. Although you can select any storage size, independently from the server type, you might not be able to use all IOPS that the storage provides, especially when you choose a server with a few vCores.
To learn more, see [compute options in Azure Database for PostgreSQL flexible server](concepts-compute.md).

> [!NOTE]  
> Regardless of the type of storage you assign to your instance, storage can only be scaled up, not down.

You can monitor your I/O consumption in the [Azure portal](https://portal.azure.com/), or by using [Azure CLI commands](/cli/azure/monitor/metrics). The relevant metrics to monitor are [storage limit, storage percentage, storage used, and I/O percentage](concepts-monitoring.md).



> [!IMPORTANT]  
> The selected compute size determines the minimum and maximum IOPS.

Learn how to [scale up or down IOPS](how-to-scale-compute-storage-portal.md).

[!INCLUDE [pricing](includes/compute-storage-princing.md)]

## Related content

- [Manage Azure Database for PostgreSQL flexible server](how-to-manage-server-portal.md).
- [Limits in Azure Database for PostgreSQL flexible server](concepts-limits.md).
