---
title: Premium SSD
description: This article describes the Premium ssd storage option in an Azure Database for PostgreSQL flexible server instance.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.custom: references_regions
ms.date: 01/16/2025
ms.service: azure-database-postgresql
ms.subservice: compute-storage
ms.topic: concept-article
---


# Premium SSD  storage option in Azure Database for PostgreSQL 

## Premium SSD

Azure Premium SSD deliver high-performance and low-latency disk support for virtual machines (VMs) with input/output (IO)-intensive workloads. Premium SSD units are suitable for mission-critical production applications.Capacity, IOPS, and throughput are guaranteed when a premium storage disk is provisioned. For example, if you create a P40 disk, Azure provisions 2,048-GB storage capacity, 7,500 IOPS, and 250-MB/s throughput for that disk. Your application can use all or part of the capacity and performance. Premium SSDs are designed to provide the single-digit millisecond latencies, target IOPS, and throughput described in the preceding table 99.9% of the time.

The maximum supported storage size is 32 TiB with Premium SSD, allowing you to scale up to 20,000 IOPS and 900 MB/s throughput. By switching to Premium SSD v2, you can scale up to 64 TiB with support for 80,000 IOPS and 1,200 MB/s throughput.
  
The storage that you provision is the amount of storage capacity available to your Azure Database for PostgreSQL flexible server instance. This storage is used for database files, temporary files, transaction logs, and PostgreSQL server logs. The total amount of storage that you provision also defines the I/O capacity available to your server.

Your virtual machine type also has IOPS limits. Although you can select any storage size, independently from the server type, you might not be able to use all IOPS that the storage provides, especially when you choose a server with a few vCores.To learn more, see [Compute options in Azure Database for PostgreSQL](concepts-compute.md).

> [!NOTE]  
> Regardless of the type of storage you assign to your instance, storage can only be scaled up, not down.

You can monitor your I/O consumption in the [Azure portal](https://portal.azure.com/), or by using [Azure CLI commands](/cli/azure/monitor/metrics). The relevant metrics to monitor are [storage limit, storage percentage, storage used, and I/O percentage](../monitor/concepts-monitoring.md).


## Storage autogrow (Premium SSD)

Storage autogrow can help ensure that your server always has enough free space available, and doesn't become read-only which happens when the storage usage reaches 95 percent, or when the available capacity is less than 5 GiB.  When you turn on storage autogrow, disk size increases without affecting the workload. Storage autogrow is only supported for Premium SSD storage tier.

For servers with more than 1 TiB of provisioned storage, the storage autogrow mechanism activates when the available space falls below 10% of the total capacity or 64 GiB, whichever of the two values are smaller. Conversely, for servers with storage under 1 TiB this threshold is adjusted to 20% of the available free space or 64 GiB, depending on which of these values is smaller.

As an illustrative example, let's consider a server with a storage capacity of 2 TiB (which is greater than 1 TiB). In this case, the autogrow limit is set at 64 GiB. This choice is made because 64 GiB is the smaller value when compared to 10% of 2 TiB, which is roughly 204.8 GiB. In contrast, for a server with a storage size of 128 GiB (which is smaller than 1 TiB), the autogrow feature activates when there's only 25.8 GiB of space left. This activation is based on the 20% threshold of the total allocated storage (128 GiB), which is smaller than 64 GiB.

The default behavior increases the disk size to the next premium SSD storage size. This increase is always double in both size and cost, regardless of whether you start the storage scaling operation manually or through storage autogrow. Enabling storage autogrow is valuable when you're managing unpredictable workloads, because it automatically detects low-storage conditions and scales up the storage accordingly.

The process of scaling storage is performed online, without causing any downtime, except when the disk size needs to cross the border of 4,096 GiB. This exception is a limitation of [Azure managed disks](/azure/virtual-machines/managed-disks-overview). In that case, the automatic storage scaling activity isn't triggered, even if storage autogrow setting is enabled for the server. In such cases, you need to scale your storage manually. In this scenario (reaching or crossing the 4,096 GiB boundary), manual scaling is an offline operation. We recommend scheduling this task to align with your business needs. All other operations can be performed online. Once the allocated disk size is 8,192 GiB or higher, storage autogrow triggers again automatically and every subsequent storage grow operation is performed online until the disk allocated reaches its maximum growing capacity, which is 32,768 GiB.

> [!NOTE]  
> Regardless of the type of storage you assign to your instance, storage can only be scaled up, not down.

## Limitations and considerations of storage autogrow

- Disk scaling operations are typically performed online, except in specific scenarios involving crossing the boundary of 4,096 GiB. These scenarios include reaching or crossing the limit of 4,096 GiB. For instance, scaling from 2,048 GiB to 8,192 GiB triggers an offline operation. In the Azure portal, moving to 4 TiB, which is represented as 4,095 GiB, keeps the operation online. However, if you explicitly specify 4 TB as 4,096 GiB, such as in Azure CLI, the scaling operation is completed in offline mode, since it reaches the limit of 4,096 GiB. Oflline scale operation usually takes anywhere between 2 to 10 minutes. With the [reduced downtime scaling feature](../scale/concepts-scaling-resources.md), this duration is reduced to less than 30 seconds. This reduction in downtime during scaling resources improves the overall availability of your database instance.

- Host Caching (ReadOnly and Read/Write) is supported on disk sizes less than 4,096 GIB or 4 Tib. Any disk that is provisioned up to 4,095 GiB can take advantage of Host Caching. Host caching isn't supported for disk sizes more than or equal to 4,096 GiB. For example, a P50 premium disk provisioned at 4,095 GiB can take advantage of Host caching and a P50 disk provisioned at 4,096 GiB can't take advantage of Host Caching. Customers moving from lower disk size to 4,096 GiB or higher lose the ability to use disk caching.

  This limitation is due to the underlying [Azure managed disks](/azure/virtual-machines/managed-disks-overview), which needs a manual disk scaling operation. You receive an informational message in the portal when you approach this limit.

- Storage autogrow isn't triggered when you have high WAL usage.

> [!NOTE]  
> Storage autogrow depends on online disk scaling, so it never causes downtime.

## IOPS scaling

Azure Database for PostgreSQL supports provisioning of extra IOPS. This feature enables you to provision more IOPS beyond the complimentary IOPS limit. Using this feature, you can increase or decrease the number of IOPS provisioned, to adjust them to your workload requirements at any time.

The compute size selected determines the minimum and maximum IOPS. To learn more about the minimum and maximum IOPS per compute size, see [compute size](concepts-compute.md).

> [!IMPORTANT]  
> The selected compute size determines the minimum and maximum IOPS.

Learn how to [scale up or down IOPS](../scale/how-to-scale-compute.md).

## Related content

- [Manage Azure Database for PostgreSQL using the Azure portal](../configure-maintain/how-to-manage-server-portal.md).
- [Limits in Azure Database for PostgreSQL](../configure-maintain/concepts-limits.md).
