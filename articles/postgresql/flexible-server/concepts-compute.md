---
title: Compute options
description: This article describes the compute options in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 05/01/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - ignite-2023
---

# Compute options in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You can create an Azure Database for PostgreSQL flexible server instance in one of three pricing tiers: Burstable, General Purpose, and Memory Optimized. The pricing tier is calculated based on the compute, memory, and storage you provision. A server can have one or many databases.

| Resource/Tier | Burstable | General Purpose | Memory Optimized |
| :--- | :--- | :--- | :--- |
| VM-series | B-series | Ddsv5-series,<br />Dadsv5-series,<br />Ddsv4-series,<br />Dsv3-series | Edsv5-series,<br />Eadsv5-series,<br />Edsv4-series,<br />Esv3-series |
| vCores | 1, 2, 4, 8, 12, 16, 20 | 2, 4, 8, 16, 32, 48, 64, 96 | 2, 4, 8, 16, 20 (v4/v5), 32, 48, 64, 96 |
| Memory per vCore | Variable | 4 GiB | 6.75 GiB to 8 GiB |
| Storage size | 32 GiB to 64 TiB | 32 GiB to 64 TiB | 32 GiB to 64 TiB |
| Automated Database backup retention period | 7 to 35 days | 7 to 35 days | 7 to 35 days |
| Long term Database backup retention period | up to 10 years | up to 10 years | up to 10 years |

To choose a pricing tier, use the following table as a starting point:

| Pricing tier | Target workloads |
| :--- | :--- |
| Burstable | Workloads that don't need the full CPU continuously. B-series VMs utilize a CPU credit model to track how much CPU is consumed. The virtual machine accumulates CPU credits when a workload is operating below the base CPU performance threshold and uses credits when running above the base CPU performance threshold until all of its credits are consumed. Upon consuming all the CPU credits, a B-series virtual machine is throttled back to its base CPU performance until it accumulates the credits to burst again. B series VMs are ideal for web servers, proof of concepts, small databases, and development build environments. Burstable SKU is usually not recommended for production use.
| General Purpose | D-series VMs provide a solid balance between CPU capabilities and memory size with scalable I/O throughput which makes them suitable for most production workloads. Examples include servers for hosting web and mobile apps and other enterprise applications. |
| Memory Optimized | E- Series VMs that are suitable for high-performance database workloads that require in-memory performance for faster transaction processing and higher concurrency. Examples include servers for processing real-time data and high-performance transactional or analytical apps. |

After you create a server for the compute tier, you can change the number of vCores (up or down) and the storage size (up) in seconds. You also can independently adjust the backup retention period up or down. For more information, see the [Scaling resources in Azure Database for PostgreSQL flexible server](concepts-scaling-resources.md) page.

## Compute tiers, vCores, and server types

You can select compute resources based on the tier, vCores, and memory size. vCores represent the logical CPU of the underlying hardware.

The detailed specifications of the available server types are as follows:

| SKU name | vCores | Memory size | Maximum supported IOPS | Maximum supported I/O bandwidth |
| --- | --- | --- | --- | --- |
| **Burstable** | | | | |
| B1ms | 1 | 2 GiB | 640 | 10 MiB/sec |
| B2s | 2 | 4 GiB | 1,280 | 15 MiB/sec |
| B2ms | 2 | 8 GiB | 1,920 | 22.5 MiB/sec |
| B4ms | 4 | 16 GiB | 2,880 | 35 MiB/sec |
| B8ms | 8 | 32 GiB | 4,320 | 50 MiB/sec |
| B12ms | 12 | 48 GiB | 4,320 | 50 MiB/sec |
| B16ms | 16 | 64 GiB | 4,320 | 50 MiB/sec |
| B20ms | 20 | 80 GiB | 4,320 | 50 MiB/sec |
| **General Purpose** | | | | |
| D2s_v3 / D2ds_v4 | 2 | 8 GiB | 3,200 | 48 MiB/sec |
| D2ds_v5 / D2ads_v5 | 2 | 8 GiB | 3,750 | 85 MiB/sec |
| D4s_v3 / D4ds_v4 | 4 | 16 GiB | 6,400 | 96 MiB/sec |
| D4ds_v5 / D4ads_v5 | 4 | 16 GiB | 6,400 | 145 MiB/sec |
| D8s_v3 / D8ds_v4 | 8 | 32 GiB | 12,800 | 192 MiB/sec |
| D8ds_v5 / D8ads_v5 | 8 | 32 GiB | 12,800 | 290 MiB/sec |
| D16s_v3 / D16ds_v4 | 16 | 64 GiB | 25,600 | 384 MiB/sec |
| D16ds_v5 / D16ds_v5 | 16 | 64 GiB | 25,600 | 600 MiB/sec |
| D32s_v3 / D32ds_v4 | 32 | 128 GiB | 51,200 | 768 MiB/sec |
| D32ds_v5 / D32ads_v5 | 32 | 128 GiB | 51,200 | 865 MiB/sec |
| D48s_v3 / D48ds_v4 | 48 | 192 GiB | 76,800 | 1152 MiB/sec |
| D48ds_v5 / D48ads_v5 | 48 | 192 GiB | 76,800 | 1200 MiB/sec |
| D64s_v3 / D64ds_v4 / D64ds_v5/ D64ads_v5 | 64 | 256 GiB | 80,000 | 1200 MiB/sec |
| D96ds_v5 / D96ads_v5 | 96 | 384 GiB | 80,000 | 1200 MiB/sec |
| **Memory Optimized** | | | | |
| E2s_v3 / E2ds_v4 | 2 | 16 GiB | 3,200 | 48 MiB/sec |
| E2ds_v5 / E2ads_v5 | 2 | 16 GiB | 3,200 | 85 MiB/sec |
| E4s_v3 / E4ds_v4 | 4 | 32 GiB | 6,400 | 96 MiB/sec |
| E4ds_v5 / E4ads_v5 | 4 | 32 GiB | 6,400 | 145 MiB/sec |
| E8s_v3 / E8ds_v4 | 8 | 64 GiB | 12,800 | 192 MiB/sec |
| E8ds_v5 / E8ads_v5 | 8 | 64 GiB | 12,800 | 290 MiB/sec |
| E16s_v3 / E16ds_v4 | 16 | 128 GiB | 25,600 | 384 MiB/sec |
| E16ds_v5 / E16ds_v5 | 16 | 128 GiB | 25,600 | 600 MiB/sec |
| E20ds_v4 | 20 | 160 GiB | 32,000 | 480 MiB/sec |
| E20ds_v5 / E20ads_v5 | 20 | 160 GiB | 32,000 | 750 MiB/sec |
| E32s_v3 / E32ds_v4 | 32 | 256 GiB | 51,200 | 768 MiB/sec |
| E32ds_v5 / D32ads_v5 | 32 | 256 GiB | 51,200 | 865 MiB/sec |
| E48s_v3 / E48ds_v4 / E48ds_v5 / E48ads_v5 | 48 | 384 GiB | 76,800 | 1152 MiB/sec |
| E48ds_v5 / E48ads_v5 | 48 | 384 GiB | 76,800 | 1200 MiB/sec |
| E64s_v3 / E64ds_v4 | 64 | 432 GiB | 80,000 | 1200 MiB/sec |
| E64ds_v5 / E64ads_v4 | 64 | 512 GiB | 80,000 | 1200 MiB/sec |
| E96ds_v5 /E96ads_v5 | 96 | 672 GiB | 80,000 | 1200 MiB/sec |
> [!IMPORTANT]  
> Minimum and maximum IOPS are also determined by the storage tier so please choose a storage tier and instance type that can scale as per your workload requirements.

[!INCLUDE [pricing](includes/compute-storage-pricing.md)]

## Related content

- [Manage Azure Database for PostgreSQL flexible server](how-to-manage-server-portal.md)
- [Limits in Azure Database for PostgreSQL flexible server](concepts-limits.md)
