---
title: Compute Options
description: This article describes the compute options in an Azure Database for PostgreSQL flexible server instance.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 01/13/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.custom:
  - ignite-2023
---

# Compute options in Azure Database for PostgreSQL

You can create an Azure Database for PostgreSQL flexible server instance in one of three pricing tiers: Burstable, General Purpose, and Memory Optimized. The pricing tier is calculated based on the compute, memory, and storage you provision. A server can have one or many databases.

| Resource/Tier | Burstable | General Purpose | Memory Optimized |
| --- | --- | --- | --- |
| VM-series | B-series | Ddsv6-series,<br />Dadsv6-series,<br />Ddsv5-series,<br />Dadsv5-series,<br />Ddsv4-series,<br />Dsv3-series | Edsv6-series,<br />Eadsv6-series,<br />Edsv5-series,<br />Eadsv5-series,<br />Edsv4-series,<br />Esv3-series |
| vCores | 1, 2, 4, 8, 12, 16, 20 | 2, 4, 8, 16, 32, 48, 64, 96, 128 (v6), 192 (v6) | 2, 4, 8, 16, 20 (v4/v5/v6), 32, 48, 64, 96 , 128 (v6), 192 (v6) |
| Memory per vCore | Variable | 4 GiB | 6.75 GiB to 9.5 GiB |
| Storage size | 32 GiB to 64 TiB | 32 GiB to 64 TiB | 32 GiB to 64 TiB |
| Automated Database backup retention period | 7 to 35 days | 7 to 35 days | 7 to 35 days |
| Long term Database backup retention period | up to 10 years | up to 10 years | up to 10 years |

To choose a pricing tier, use the following table as a starting point:

| Pricing tier | Target workloads |
| --- | --- |
| **Burstable** | Designed for workloads that do not require full CPU performance continuously. Uses a CPU credit model: credits accumulate when usage is below baseline and are consumed when usage exceeds it. When credits are exhausted, the VM is restricted to baseline CPU, which under sustained load can cause severe performance degradation, connection timeouts, and delays or transient failures in management operations until credits rebuild. Best suited for web servers, proof-of-concept environments, small databases, and development builds. Not recommended for production workloads. |
| **General Purpose** | Provides a balance between CPU and memory with scalable I/O throughput, making it suitable for most production workloads. Examples include servers for hosting web and mobile apps and other enterprise applications. |
| **Memory Optimized** | Suitable for high-performance database workloads that require in-memory performance for faster transaction processing and higher concurrency. Examples include servers for processing real-time data and high-performance transactional or analytical apps. |
After you create a server for the compute tier, you can change the number of vCores (up or down) and the storage size (up) in seconds. You also can independently adjust the backup retention period up or down. For more information, see the [Scaling resources in Azure Database for PostgreSQL](../scale/concepts-scaling-resources.md) page.

## Compute tiers, vCores, and server types

You can select compute resources based on the tier, vCores, and memory size. vCores represent the logical CPU of the underlying hardware.

> [!IMPORTANT]  
> Burstable compute is for workloads that stay idle or below baseline most of the time. If CPU runs near or above baseline for long periods, credits deplete and the server might become unreachable.  
>
> For these workloads, it's recommended to:  
> - Monitor **CPU Credits Remaining** in Azure Monitor and set alerts for low credits.  
> - Avoid restarts or scaling when credits are near zero; allow time to rebuild.  
> - If credits deplete often, move to a larger Burstable size or switch tiers.

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
| D2ads_v6 | 2 | 8 GiB | 4000 | 90 MiB/sec |
| D2ds_v6 | 2 | 8 GiB | 4167 | 124 MiB/sec |
| D4s_v3 / D4ds_v4 | 4 | 16 GiB | 6,400 | 96 MiB/sec |
| D4ds_v5 / D4ads_v5 | 4 | 16 GiB | 6,400 | 145 MiB/sec |
| D4ads_v6 | 4 | 16 GiB | 7600 | 180 MiB/sec |
| D4ds_v6 | 4 | 16 GiB | 8333 | 248 MiB/sec |
| D8s_v3 / D8ds_v4 | 8 | 32 GiB | 12,800 | 192 MiB/sec |
| D8ds_v5 / D8ads_v5 | 8 | 32 GiB | 12,800 | 290 MiB/sec |
| D8ads_v6 | 8 | 32 GiB | 15200 | 360 MiB/sec |
| D8ds_v6 | 8 | 32 GiB | 16667 | 496 MiB/sec |
| D16s_v3 / D16ds_v4 | 16 | 64 GiB | 25,600 | 384 MiB/sec |
| D16ds_v5 / D16ds_v5 | 16 | 64 GiB | 25,600 | 600 MiB/sec |
| D16ads_v6 | 16 | 64 GiB | 30400 | 720 MiB/sec |
| D16ds_v6 | 16 | 64 GiB | 33333 | 992 MiB/sec |
| D32s_v3 / D32ds_v4 | 32 | 128 GiB | 51,200 | 768 MiB/sec |
| D32ds_v5 / D32ads_v5 | 32 | 128 GiB | 51,200 | 865 MiB/sec |
| D32ads_v6 | 32 | 128 GiB | 57600 | 1200 MiB/sec |
| D32ds_v6 | 32 | 128 GiB | 66667 | 1200 MiB/sec |
| D48s_v3 / D48ds_v4 | 48 | 192 GiB | 76,800 | 1152 MiB/sec |
| D48ds_v5 / D48ads_v5 | 48 | 192 GiB | 76,800 | 1200 MiB/sec |
| D48ads_v6 | 48 | 192 GiB | 80000 | 1200 MiB/sec |
| D48ds_v6 | 48 | 192 GiB | 80000 | 1200 MiB/sec |
| D64s_v3 / D64ds_v4 / D64ds_v5/ D64ads_v5 | 64 | 256 GiB | 80,000 | 1200 MiB/sec |
| D64ads_v6 | 64 | 256 GiB | 80000 | 1200 MiB/sec |
| D64ds_v6 | 64 | 256 GiB | 80000 | 1200 MiB/sec |
| D96ds_v5 / D96ads_v5 | 96 | 384 GiB | 80,000 | 1200 MiB/sec |
| D96ads_v6 | 96 | 384 GiB | 80000 | 1200 MiB/sec |
| D96ds_v6 | 96 | 384 GiB | 80000 | 1200 MiB/sec |
| D128ds_v6 | 128 | 512 GiB | 80000 | 1200 MiB/sec |
| D192ds_v6 | 192 | 768 GiB | 80000 | 1200 MiB/sec |
| **Memory Optimized** | | | | |
| E2s_v3 / E2ds_v4 | 2 | 16 GiB | 3,200 | 48 MiB/sec |
| E2ds_v5 / E2ads_v5 | 2 | 16 GiB | 3,200 | 85 MiB/sec |
| E2ads_v6 | 2 | 16 GiB | 4000 | 90 MiB/sec |
| E2ds_v6 | 2 | 16 GiB | 4167 | 124 MiB/sec |
| E4s_v3 / E4ds_v4 | 4 | 32 GiB | 6,400 | 96 MiB/sec |
| E4ds_v5 / E4ads_v5 | 4 | 32 GiB | 6,400 | 145 MiB/sec |
| E4ads_v6 | 4 | 32 GiB | 7600 | 180 MiB/sec |
| E4ds_v6 | 4 | 32 GiB | 8333 | 248 MiB/sec |
| E8s_v3 / E8ds_v4 | 8 | 64 GiB | 12,800 | 192 MiB/sec |
| E8ds_v5 / E8ads_v5 | 8 | 64 GiB | 12,800 | 290 MiB/sec |
| E8ads_v6 | 8 | 64 GiB | 15200 | 360 MiB/sec |
| E8ds_v6 | 8 | 64 GiB | 16667 | 496 MiB/sec |
| E16s_v3 / E16ds_v4 | 16 | 128 GiB | 25,600 | 384 MiB/sec |
| E16ds_v5 / E16ds_v5 | 16 | 128 GiB | 25,600 | 600 MiB/sec |
| E16ads_v6 | 16 | 128 GiB | 30400 | 720 MiB/sec |
| E16ds_v6 | 16 | 128 GiB | 33333 | 992 MiB/sec |
| E20ds_v4 | 20 | 160 GiB | 32000 | 480 MiB/sec |
| E20ds_v5 / E20ads_v5 | 20 | 160 GiB | 32,000 | 750 MiB/sec |
| E20ads_v6 | 20 | 160 GiB | 38000 | 900 MiB/sec |
| E20ds_v6 | 20 | 160 GiB | 41667 | 1200 MiB/sec |
| E32s_v3 / E32ds_v4 | 32 | 256 GiB | 51,200 | 768 MiB/sec |
| E32ds_v5 / D32ads_v5 | 32 | 256 GiB | 51,200 | 865 MiB/sec |
| E32ads_v6 | 32 | 256 GiB | 57600 | 1200 MiB/sec |
| E32ds_v6 | 32 | 256 GiB | 66667 | 1200 MiB/sec |
| E48s_v3 / E48ds_v4 / E48ds_v5 / E48ads_v5 | 48 | 384 GiB | 76,800 | 1152 MiB/sec |
| E48ds_v5 / E48ads_v5 | 48 | 384 GiB | 76,800 | 1200 MiB/sec |
| E48ads_v6 | 48 | 384 GiB | 80000 | 1200 MiB/sec |
| E48ds_v6 | 48 | 384 GiB | 80000 | 1200 MiB/sec |
| E64s_v3 / E64ds_v4 | 64 | 432 GiB | 80000 | 1200 MiB/sec |
| E64ds_v5 / E64ads_v4 | 64 | 512 GiB | 80000 | 1200 MiB/sec |
| E64ads_v6 | 64 | 512 GiB | 80000 | 1200 MiB/sec |
| E64ds_v6 | 64 | 512 GiB | 80000 | 1200 MiB/sec |
| E96ds_v5 /E96ads_v5 | 96 | 672 GiB | 80000 | 1200 MiB/sec |
| E96ads_v6 | 96 | 672 GiB | 80000 | 1200 MiB/sec |
| E96ds_v6 | 96 | 768 GiB | 80000 | 1200 MiB/sec |
| E128ds_v6 | 128 | 1024 GiB | 80000 | 1200 MiB/sec |
| E192ds_v6 | 192 | 1832 GiB | 80000 | 1200 MiB/sec |
| > [!IMPORTANT] |
> Minimum and maximum IOPS are also determined by the storage tier so choose a storage tier and instance type that can scale as per your workload requirements.

[!INCLUDE [pricing](includes/compute-storage-pricing.md)]

## Related content

- [Manage Azure Database for PostgreSQL](../configure-maintain/how-to-manage-server-portal.md)
- [Limits in Azure Database for PostgreSQL](../configure-maintain/concepts-limits.md)
