---
title: Plan Azure Database for PostgreSQL Deployments for Operational Performance
description: Learn how to plan Azure Database for PostgreSQL deployments by aligning workload requirements with compute, storage, IOPS, throughput, latency, and monitoring needs.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: compute-storage
ms.topic: concept-article
---

# Plan Azure Database for PostgreSQL deployments for operational performance

Cloud computing dramatically reshaped the database hosting landscape. It gives teams access to scalability, resilience, global reach, and capabilities that were previously unobtainable. Instead of incurring considerable costs and overhead by planning for the largest possible workload (and carrying that cost from day one), teams can now optimize around the precise scale they need, when they need it, and adjust as their demands change. 

## Introduction

The flexibility to choose the appropriate balance of resources is especially valuable for PostgreSQL database deployments. PostgreSQL database workloads might start small, grow quickly, spike seasonally, shift from read-heavy to write-heavy, or evolve from transactional workloads into hybrid operational and analytical systems in real-time. Azure Database for PostgreSQL ensures your solutions hit your targets by offering a broad range of choices across compute, storage, availability, replication, security, backup, and operational management.

But with all this power comes responsibility, especially when planning your deployments. To achieve the best possible performance, your deployment decisions must match your overall workload's requirements.

A successful Azure Database for PostgreSQL deployment isn't just a question of choosing "the most cores and memory we need." Instead, maximum operational performance comes from understanding your application's behaviors, client's behaviors, compute, storage, and database growth characteristics, and how these all intersect and interact.

> **The best architecture is the one where these pieces are intentionally aligned.**

## Cloud performance planning is a shared responsibility

One of the major benefits of moving to a trusted cloud platform is the shared responsibility model. Microsoft provides the global infrastructure, managed services, hardware innovation, reliability, security, and operational engineering. Your teams bring the specific application context expertise: business criticality, workload behavior, data model design, network traffic profile, growth expectations, recovery objectives, and end-user experience requirements.

> **The strongest outcomes arise when these two forces are unified.**

Azure provides highly scalable Postgres infrastructure, but your team must bring insights to these areas:

- How many concurrent users are expected during normal and peak periods?
- Are the most important operations read-heavy, write-heavy, or mixed?
- Does demand spike during month-end, quarter-end, holidays, launches, or reporting windows?
- How fast is the dataset growing?
- Which operations are latency-sensitive?
- Which queries or jobs can tolerate longer runtimes?
- Is the workload primarily OLTP, OLAP, or hybrid?
- Are clients located near the database region, globally distributed, or concentrated in one geography?

Capture these details before deployment, not after a production incident. Cloud deployments make scaling easier, but the highest-performing and most cost-efficient designs still start with sound requirements gathering and proper planning. In most instances, these questions can be distilled down to the relationships across concurrent connections, maximum IOPS, and required throughput.

### Performance has multiple layers

Database performance is rarely determined by a single setting. Successful deployment experiences depend on several layers working together:

- **Application layer performance.**
<br />
   This layer includes application code, query patterns, index coverage, trigger usage, data partitioning, connection handling, caching, retry logic, pooling, ORM behavior, transaction design, and background job behavior.
- **Client and network layer performance.**
<br />
   This layer includes where clients are located, how they connect, whether requests cross regions and availability zones, network latency, TLS overhead, connection churn, and whether the application uses connection pooling efficiently.
- **Database platform performance.**
<br />
   This layer includes Postgres deployment configuration, compute size, memory, CPU, storage type, storage size, storage IOPS, storage throughput, high availability, replicas, and maintenance operations.

This article focuses primarily on the third layer: planning the Azure Postgres database deployment so that compute and storage choices support the required performance profile.

### Azure Database for PostgreSQL offers flexibility, but planning is essential

Azure Database for PostgreSQL Flexible Server provides a wide range of deployment options, including:

| Deployment&nbsp;area | Available choices |
| --- | --- |
| Compute | Compute tiers, virtual machine (VM) generations, General Purpose configurations, and Memory Optimized configurations. |
| Storage | Azure Premium SSD v1, Premium SSD v2, storage scaling, IOPS configuration, and throughput configuration. |
| Availability | High availability, backup and restore, and geo-redundant backups in supported configurations. |
| Replication | Read replicas and geo-replicas. |
| Security | Customer-managed keys and enterprise security integration. |

This flexibility is powerful because different workloads require different capabilities. A write-heavy transactional system doesn't need the same profile as a reporting-heavy system. A global SaaS application doesn't need the same design as an internal regional application. A database growing 5% per year doesn't need the same storage plan as one growing 200% month over month.

The planning goal is to identify your workload performance profile needs, and then implement the proper choices across both compute and storage options to deliver your end-to-end solutions successfully.

### Start with the workload profile

Before choosing compute or storage, define the workload. Useful planning dimensions include:

| Planning&nbsp;area | Questions to answer |
| --- | --- |
| Geography | Where are users, applications, replicas, and integrations located? |
| Concurrency | How many simultaneous connections and active queries are expected? |
| Data size | What is the current database size, and what is the expected growth rate? |
| Rate of change | How quickly does data grow month over month? How much write-ahead log (WAL) is generated? |
| Workload type | Is the system OLTP, OLAP, reporting-heavy, batch-heavy, or hybrid? |
| Read/write mix | What percentage of operations are reads and writes? |
| Peak behavior | Are there predictable business cycles, seasonal peaks, or batch windows? |
| Latency sensitivity | Which transactions are user-facing and latency-critical? |
| Throughput needs | Are there large data scans, exports, imports, or extract, transform, and load (ETL) processes? |
| Scaling expectations | Will the workload need temporary bursts or sustained higher performance? |

> **The goal isn't to predict the future perfectly. The goal is to avoid designing blindly.**

## Understand the three core storage performance concepts

Azure storage performance planning usually comes down to three related but distinct concepts: IOPS, throughput, and latency. These factors are key for application performance planning.

### IOPS

**IOPS** means input/output operations per second. It measures how many read or write operations the database can send to storage each second.

IOPS is especially important for OLTP workloads. These systems often perform many small, random reads and writes, such as inserts, updates, index lookups, point reads, and short transactions. A transactional workload with thousands of concurrent users might need high IOPS even if each individual operation is small.

Common IOPS-sensitive scenarios include:

- High-volume order processing
- User profile updates
- Inventory systems
- Event ingestion
- Payment or billing systems
- Highly concurrent SaaS applications

### Throughput

**Throughput**, sometimes called bandwidth, measures how much data can be read from or written to storage over time. It's expressed in MB/s.

Throughput matters when operations move large amounts of data. Analytical queries, backups, restores, batch jobs, index builds, table scans, and ETL workflows might need high throughput even if they don't require the highest IOPS.

Common throughput-sensitive scenarios include:

- Reporting queries over large tables
- Bulk imports or exports
- Data warehouse-style scans
- Backup and restore operations
- Large index creation or rebuild operations
- Batch processing

### Latency

**Latency** is the time it takes for a single I/O request to complete. Low latency is essential for user-facing database operations, especially where many small operations are chained together in a transaction.

A system can have high theoretical IOPS but still feel slow if latency is high. For Postgres workloads, storage latency can directly affect query response times, transaction commit behavior, checkpoint behavior, and overall application responsiveness.

> [!NOTE]  
> Premium SSD v1 disks are designed for single-digit millisecond latencies for most I/O operations, and notably, disk caching can further reduce read latency for disk configurations under 4 TB. Premium SSD v2 and Ultra Disk offer submillisecond latency.

### IOPS, throughput, and latency must be considered together

IOPS and throughput are connected. A workload issuing several small 8-KiB operations might drive high IOPS without high throughput. A workload issuing large multi MB operations might drive high throughput with lower IOPS.

A simple way to think about it:

> **IOPS x I/O size = Throughput**

For Postgres, the practical implication is that workload storage planning should be based on observed or estimated workload behavior, not database size alone. For example:

- A high-concurrency OLTP system might need more IOPS and lower latency.
- A reporting-heavy system might need more throughput.
- A hybrid system might need both, especially during peak cycles.
- A high-concurrency OLTP system might need more IOPS and lower latency.
- A reporting-heavy system might need more throughput.
- A hybrid system might need both, especially during peak cycles.

## Your deployment choices directly affect storage performance

A common mistake is setting your storage for a target performance number without fully considering whether your selected compute SKU can drive the same performance levels.

Azure storage performance has multiple considerations. These details include:

- The compute capability set (maximum compute IOPS and throughput limits).
- The storage generation (SSD v1, SSD v2, Ultra Disk).
- The storage disk size (SSD v1 disks under 4,096 GB include host caching, which allows for IOPS bursts above standard baselines).
- The storage IOPS capacity.
- The storage throughput capacity.

In practical terms: **your effective performance ceiling is your lowest relevant limit in the chain.**

If the storage configuration can provide 80,000 IOPS but the compute SKU can only drive 20,000 IOPS, the deployment doesn't deliver 80,000 IOPS. Conversely, if the VM generation supports high IOPS but the selected storage tier is capped lower, the storage tier becomes the limit.

> **Compute and storage planning should happen together.**

### Premium SSD v1: strong baseline performance with important caching behavior

Premium SSD v1 is a common choice for production Azure Postgres workloads that need predictable, provisioned performance. Azure Postgres SSD v1 storage supports up to **32 TB** space, **20,000 IOPS**, and **900 MB/s** throughput.

Premium SSD v1 works well for workloads that benefit from host caching. Azure Postgres supports host caching for SSD v1 disk sizes **less than 4,096 GB**. Any disk provisioned **up to 4,095 GB** can benefit from host caching. Once storage is provisioned at **4,096 GB or higher**, host caching isn't supported. **That boundary matters.** For Premium SSD v1 deployments under 4 TB, caching can improve read performance and reduce read latency. This caching creates excellent cost-to-performance efficiency for read-heavy or mixed workloads that fit below the caching threshold.

#### Why the 4-TB boundary matters

When a Premium SSD v1 deployment grows beyond the caching-supported range, the performance profile can change:

- Reads no longer benefit from host cache.
- More read operations come directly from the underlying disk.
- Reads count against disk IOPS and throughput limits.
- Latency-sensitive read workloads might see different behavior.
- A configuration that was previously efficient might need more provisioned IOPS, more throughput, compute scaling, query tuning, or a different storage option.

Crossing above 4 TB isn't bad, but you must *plan* for it.

If you expect a database to grow beyond 4 TB, consider the future state during architecture design. A design that performs well at 2 TB with caching might need a different performance plan at 5 TB without caching.

<a id="bursting-helps-with-spikes-but-doesnt-replace-sustained-capacity"></a>

#### Burst helps with spikes, but doesn't replace sustained capacity

Azure Postgres Premium SSD v1 storage allocations under 4-TB support bursts of host caching, which can help in scenarios such as:

- Startup activity
- Short batch jobs
- Traffic spikes
- End-of-month processing
- Temporary workload surges

While bursting is useful, use it carefully. Bursting can absorb temporary spikes, but it shouldn't be the foundation for sustained workload demand. If the workload frequently runs above baseline, it's better to provision a higher performance tier, adjust storage performance settings, scale compute, or redesign the workload pattern.

A good planning question is: *Is this a temporary spike, or is this the new normal?*

Temporary spikes might be good candidates for bursting. Handle sustained demand with deliberate capacity planning.

### Premium SSD v2 decouples capacity, IOPS, and throughput

Premium SSD v2 changes the planning model by decoupling disk size, IOPS, and throughput. Azure Database for PostgreSQL flexible server Premium SSD v2 supports:

- Capacity from **32 GB** to **64 TB**.
- Up to **80,000 IOPS**.
- Up to **1,200 MB/s** throughput.
- Granular capacity adjustments in 1-GB increments.
- Flexible IOPS and throughput configuration.
- Lower latency than Premium SSD v1.
- No host caching.

This change is a major shift. With Premium SSD v1, performance is more tightly coupled to disk size. With Premium SSD v2, you can configure performance more directly around workload need.

For example, a transaction-heavy database might need high IOPS without needing a large amount of storage. Azure Postgres provides baseline IOPS and throughput at no extra cost, with additional IOPS and throughput available for additional charges. Premium SSD v2 offers:

- Disks up to 399 GB receive a baseline of **3,000 IOPS** and **125 MB/s**.
- Disks 400 GB or larger receive a baseline of **12,000 IOPS** and **500 MB/s**.
- Disks can reach up to **80,000 IOPS** when sized to at least 160-GB available space.
- Throughput can scale up to **1,200 MB/s**.

Premium SSD v2 is often attractive when you need more precise control over cost and performance. Instead of scaling storage capacity just to unlock performance, you can provision performance more intentionally.

### Ultra Disk (Preview): the high-end Azure disk performance class

Ultra Disk is the highest-performance disk option. Azure Ultra Disk offers performance levels up to:

- **400,000 IOPS**
- **10,000 MB/s** throughput
- **64 TB** capacity
- Submillisecond latency design targets
- Independently configurable capacity, IOPS, and throughput

Ultra Disk storage is designed to power IO-intensive workloads for top-tier databases, SAP HANA, and transaction-heavy systems. This new storage offering provides top-of-the-line performance for your mission-critical workloads. However, your team must consider some key deployment capabilities, regional availability restrictions, and configuration options when planning a deployment:

- Storage autogrow isn't supported for servers using Ultra Disk
- Data encryption with customer managed keys isn't supported for servers with Ultra Disk
- Ultra Disks don't support disk caching

It's important to understand Ultra Disk capabilities as part of the broader Azure storage performance landscape. However, you must validate service availability and support for your specific Azure Postgres workload. Check with your Microsoft representative if the Ultra Disk Preview is available for your Azure Postgres deployment.

The practical takeaway: **Ultra Disk represents the upper end of Azure storage performance, but your end-to-end Postgres design must include comparably supported combinations for the selected compute SKU, region, and release level.**

### VM generation matters: V5 and V6 compute storage ceilings are different

Compute generation can materially affect storage performance. When you explore the highest end of Azure storage performance, avoid the misunderstanding that "large compute" automatically means "maximum storage." You must validate the selected compute SKU against the intended storage tier. Let's illustrate this point by considering two similarly sized compute generations, `Ddsv5` and `Ddsv6`:

The `Ddsv5`-series supports Premium Storage (with caching), Premium SSD v2, and Ultra Disk at the VM family level. However, the VM's aggregate remote storage limits still define the ceiling for what that VM can drive. `Ddsv5`-series provides storage performance ranging up to **80,000 IOPS** and **2,600 MB/s**.

The `Ddsv6`-series provides a higher storage envelope, ranging up to **400,000 IOPS** and **12,000 MB/s**. V6-series compute also offers higher scalability than prior generations, with up to 192 vCPU and 768-GiB memory.

That generational change is important for high-performance Postgres design. If your target architecture requires high storage performance, choosing a compute generation with a lower aggregate storage ceiling can prevent the deployment from using the full storage capability.

### Example: why end-to-end alignment matters

Consider a PostgreSQL workload with an aspirational storage target of 400,000 IOPS.

At the disk layer, Azure Ultra Disk supports up to 400,000 IOPS per disk. Premium SSD v2 supports up to 80,000 IOPS per disk, and higher aggregate designs might require multiple disks or platform-level abstraction depending on service support.

But storage capability alone isn't enough.

A V5-series configuration might have a storage ceiling that's lower than the target. As previously mentioned, V5-series SKUs support up to 260,000 IOPS for Premium SSD remote disk throughput. In this case, choosing the V5-series compute layer for this target becomes the limiting factor before a 400,000 IOPS target is reached.

By contrast, the Ddsv6-series documentation offers up to 400,000 IOPS and 12,000 MB/s. That makes V6-series and newer generations strategically important for designs that need to align compute and storage around the highest storage-performance classes.

The lesson is simple: **maximum database performance is an end-to-end property, not a storage-only property.**

### Plan for business cycles, not just steady state

Many systems don't have a single performance profile. They have several:

| | |
| --- | --- |
| Normal weekday traffic. | Peak business hours. |
| Month-end or quarter-end processing. | Holiday or seasonal demand. |
| Product launch events. | Reporting windows. |
| Maintenance windows. | Azure Batch ingestion periods. |
| Backup and restore scenarios. | Disaster recovery events. |

A database sized for average utilization might struggle during the moments that matter most. Conversely, a database sized permanently for a once-a-month peak might be unnecessarily expensive.

Azure's flexibility allows teams to make more nuanced choices. For example:

- Use Premium SSD v2 to adjust IOPS and throughput as workload needs evolve.
- Use read replicas to offload read-heavy workloads where appropriate.
- Scale compute for known peak periods.
- Tune queries, indexes, and connection pooling before scaling infrastructure.
- Use observability to identify whether the bottleneck is CPU, memory, IOPS, throughput, lock contention, connection pressure, or query design.

> **The best deployment isn't always the largest deployment. It's the design that matches the workload and can evolve safely.**

## Observability is part of the architecture

Performance planning shouldn't stop at deployment. Postgres workloads change over time. Data grows, query patterns shift, new features launch, customer traffic changes, and operational jobs accumulate.

| Monitoring&nbsp;area | Signals to review |
| --- | --- |
| Compute | CPU utilization and memory pressure. |
| Connections | Active connections, idle connections, and connection pool behavior. |
| Queries | Query duration, query plan changes, and index usage. |
| Storage | Storage percentage, read latency, write latency, IOPS utilization, and throughput statistics. |
| Maintenance | Table bloat, index bloat, WAL characteristics, backup schedules, and maintenance schedules. |
| Replication | Replica lag, where relevant. |

Azure Database for PostgreSQL documentation highlights monitoring I/O consumption through Azure portal or Azure CLI metrics, including storage limit, storage percentage, storage used, and I/O percentage.

These metrics help answer the most important operational question: **which layer is actually limiting performance?**

Without observability, teams might scale the wrong thing. A query plan problem might look like a storage problem. Connection storms might look like CPU pressure. A missing index might look like insufficient IOPS. A regional client placement issue might look like database latency.

> **Monitoring helps teams make targeted changes instead of expensive guesses.**

## Practical planning checklist

Before selecting the production Azure Database for PostgreSQL configuration, capture the following information.

| Category | Planning inputs |
| --- | --- |
| Workload type | OLTP, OLAP, hybrid, reporting, batch, and ingestion. |
| Read/write mix | Percentage reads, writes, random I/O, and sequential I/O. |
| Current performance | Baseline IOPS, throughput, latency, CPU, memory, and connections. |
| Peak performance | 90th percentile and 99th percentile workload requirements. |
| Data size | Current size, expected growth, large object usage, and index growth. |
| Growth rate | Month-over-month and year-over-year storage projections. |
| Concurrency | Active sessions, idle sessions, and connection pool behavior. |
| Business cycles | Daily, weekly, monthly, seasonal, and launch-driven peaks. |
| Availability | High availability, replicas, disaster recovery, backup, restore, recovery point objective (RPO), and recovery time objective (RTO). |
| Storage choice | Premium SSD, Premium SSD v2, supported regions, and supported features. |
| Caching impact | Whether Premium SSD v1 host caching applies below 4 TB. |
| Compute generation | Whether the selected SKU can drive the required IOPS and throughput. |
| Scaling model | Manual scaling, scheduled scaling, performance adjustment, and replicas. |
| Observability | Metrics, alerts, query insights, and workload review process. |

## Recommended design principles

Use the following principles when planning Azure Postgres deployments for operational performance.

- **Size for workload shape, not just data size.**
<br />
   A 500-GB database can need more IOPS than a 5-TB database if it's highly transactional and latency-sensitive. Size matters, but workload behavior matters more.
- **Validate compute and storage together.**
<br />
   Don't choose storage based only on disk limits. Confirm that the selected compute SKU can drive the required IOPS and throughput.
- **Treat the 4-TB Premium SSD caching boundary as a design milestone.**
<br />
   Premium SSD deployments under 4 TB can benefit from host caching. At 4,096 GB and above, host caching isn't supported. If growth will cross that threshold, plan the future performance model early.
- **Consider Premium SSD v2 for flexible performance tuning.**
<br />
   Premium SSD v2 allows more granular control of capacity, IOPS, and throughput. It can be a strong fit when performance needs don't map cleanly to fixed disk sizes.
- **Use bursting for bursts, not sustained demand.**
<br />
   Bursting can help with short-lived spikes, but frequent or sustained bursting usually means the baseline configuration should be revisited.
- **Match generation to ambition.**
<br />
   For high-end performance goals, newer compute generations such as v6-series can expose higher aggregate remote storage limits than earlier general-purpose generations. If the target is a 400,000-IOPS-class architecture, select the compute generation accordingly.
- **Measure before and after changes.**
<br />
   Scaling is easier in the cloud, but measurement is what makes scaling effective. Capture baseline, peak, and post-change metrics so performance decisions are evidence-based.

## Real-world benchmark: compare storage configurations under load

The principles outlined in this article aren't theoretical. To demonstrate how compute, storage, and workload interact in practice, this section summarizes `pgbench` benchmarks that compare storage configurations and compute tiers under controlled, measured conditions.

### Benchmark setup and methodology

The benchmarks use `pgbench`, the standard PostgreSQL benchmark tool, to simulate a transactional workload across five different storage and compute configurations. The test starts with 500 concurrent connections and ramps up to 750 concurrent connections after an initial period, maintaining this elevated connection load for the remainder of the test window. This ramp-up pattern simulates how many real applications increase load over time as traffic grows, and measures how the database responds to both the initial spike and sustained high concurrency.

All benchmarks run on Azure Database for PostgreSQL Flexible Server in the same region, within the same availability zone, using the same test database and workload profile. By isolating storage and compute as the variables, you ensure that performance differences reflect actual platform capabilities rather than network, application, or workload variation.

### Configuration details

Test five distinct configurations, varying both storage tier and compute size to illustrate key planning concepts.

| Configuration | Compute&nbsp;SKU | vCores | Memory | Max&nbsp;compute&nbsp;IOPS | Storage&nbsp;type | Capacity | IOPS | Throughput |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Config 1 | Standard_D16ds_v5 | 16 | 64 GB | 25,600 (40,000 burst) | Premium SSD (P50) | 4,095 GB | 7,500 | 250 MB/s |
| Config 2 | Standard_D16ds_v5 | 16 | 64 GB | 25,600 (40,000 burst) | Premium SSD (P50) | 4,096 GB | 7,500 | 250 MB/s |
| Config 3 | Standard_D16ds_v5 | 16 | 64 GB | 25,600 (40,000 burst) | Premium SSD (P80) | 32 TB | 20,000 | 900 MB/s |
| Config 4 | Standard_D16ds_v5 | 16 | 64 GB | 25,600 (40,000 burst) | Premium SSD v2 | 4,095 GB | 40,000 | 1,200 MB/s |
| Config 5 | Standard_D32ds_v5 | 32 | 128 GB | 51,200 | Premium SSD v2 | 4,095 GB | 60,000 | 1,200 MB/s |

**Key observations from the configuration design:**

- **Config 1 vs. Config 2:** These configurations differ only in storage size, 4,095 GB versus 4,096 GB. This comparison tests the host caching boundary for Premium SSD v1 disks.
- **Config 2 vs. Config 3:** Both configurations use SSD v1, but Config 3 scales to 32-TB capacity to unlock higher IOPS and throughput.
- **Config 3 vs. Config 4:** Both configurations use the same compute, but Config 4 demonstrates Premium SSD v2 flexible IOPS and throughput independent of capacity.
- **Config 4 vs. Config 5:** Config 5 doubles the compute SKU to demonstrate how higher-tier compute unlocks more storage performance headroom.

### Performance results

#### Configuration 1: 4,095-GB Premium SSD v1 with host caching

:::image type="content" source="media/concepts-optimal-performance/4095.png" alt-text="Screenshot of chart showing performance results for configuration 1 with 4,095-GB Premium SSD v1 storage and host caching." lightbox="media/concepts-optimal-performance/4095.png":::

Configuration 1 uses the 4,095-GB Premium SSD v1 size, which benefits from host caching on Premium SSD v1. During the workload, this configuration sustained:

- **Max IOPS:** 24,773, capped by 7,500 provisioned IOPS on Premium SSD v1, with caching amplifying effective performance.
- **Max read IOPS:** 21,330, benefiting from host cache for read-heavy operations.
- **Max write IOPS:** 7,610.

Host caching provides read amplification, so effective IOPS momentarily exceed the disk's 7,500 provisioned IOPS limit and reach compute storage limits.

#### Configuration 2: 4,096-GB Premium SSD v1 without host caching

:::image type="content" source="media/concepts-optimal-performance/4096.png" alt-text="Screenshot of chart showing performance results for configuration 2 with 4,096-GB Premium SSD v1 storage without host caching." lightbox="media/concepts-optimal-performance/4096.png":::

Configuration 2 uses the 4,096-GB Premium SSD v1 size, crossing the caching boundary and losing host caching benefits. The impact is visible:

- **Max IOPS:** Lower effective IOPS compared to Config 1 because of the loss of caching.
- **Max read IOPS:** Significantly reduced without host cache.
- **Max write IOPS:** 7,610, unchanged.

This configuration demonstrates the practical importance of the 4-TB caching boundary. Crossing from 4,095 GB to 4,096 GB changes the performance profile by removing cached reads. For growing databases that approach this threshold, plan ahead.

#### Configuration 3: 32-TB Premium SSD v1 with higher IOPS

:::image type="content" source="media/concepts-optimal-performance/20000.png" alt-text="Screenshot of chart showing performance results for configuration 3 with 32-TB Premium SSD v1 storage." lightbox="media/concepts-optimal-performance/20000.png":::

Configuration 3 addresses Premium SSD v1 upper IOPS and throughput limits by scaling to 32-TB capacity. This configuration achieved:

- **Max IOPS:** 20,000.
- **Max read IOPS:** Approximately 12,000.
- **Max write IOPS:** Approximately 5,000.

Increasing the underlying Premium SSD v1 storage capacity increases IOPS and throughput. You can still reach the upper limits of the compute storage range for intensive workloads.

#### Configuration 4: Premium SSD v2 with 40,000 IOPS

:::image type="content" source="media/concepts-optimal-performance/40000.png" alt-text="Screenshot of chart showing performance results for configuration 4 with Premium SSD v2 and 40,000 IOPS." lightbox="media/concepts-optimal-performance/40000.png":::

Configuration 4 demonstrates Premium SSD v2 flexible performance configuration, provisioning 40,000 IOPS and 1,200-MB/s throughput on 4,095 GB of capacity:

- **Max IOPS:** Higher effective utilization because of Premium SSD v2 latency and throughput capability.
- **Max read IOPS:** Improved performance compared to Premium SSD v1 configurations.
- **Max write IOPS:** Higher sustained write capacity.

Premium SSD v2 allows provisioning high IOPS without requiring large storage capacity, making it efficient for transaction-heavy workloads.

#### Configuration 5: Premium SSD v2 with 60,000 IOPS on D32ds_v5 compute

:::image type="content" source="media/concepts-optimal-performance/60000.png" alt-text="Screenshot of chart showing performance results for configuration 5 with Premium SSD v2, 60,000 IOPS, and D32ds_v5 compute." lightbox="media/concepts-optimal-performance/60000.png":::

Configuration 5 scales both storage performance, at 60,000 IOPS, and compute, with Standard_D32ds_v5 and 32 vCores. This configuration demonstrates the end-to-end alignment principle:

- **Max IOPS:** Significantly higher than all prior configurations.
- **Max read IOPS:** Strong improvement with extra compute headroom.
- **Max write IOPS:** Sustained higher write capacity.

By aligning both compute and storage to higher performance tiers, this configuration achieves the best throughput and lowest CPU pressure. The higher storage ceiling of D32ds_v5 allows the 60,000-IOPS Premium SSD v2 disk to be more fully used.

### Lessons from the benchmarks

These five configurations illustrate the key principles from this article:

- **The 4-TB caching boundary matters.**
<br />
   Config 1 vs. Config 2 shows that host caching provides measurable read performance amplification below 4 TB, while crossing into 4,096 GB removes that benefit.
- **Capacity isn't performance.**
<br />
   Config 3 provisioned 32 TB but didn't deliver the highest IOPS. Storage capacity alone doesn't determine transaction throughput.
- **Premium SSD v2 provides flexible performance tuning.**
<br />
   Config four demonstrated high IOPS on modest capacity, validating the decoupled model that Premium SSD v2 enables.
- **Compute and storage must be aligned.**
<br />
   Config five shows that maximizing storage performance requires sufficient compute headroom. The higher storage ceiling of D32ds_v5 was necessary to more fully use the 60,000-IOPS provision.

The benchmark results validate the core principle: maximum performance is an end-to-end property. No single layer, such as storage, compute, or networking, determines the outcome. Success requires intentional alignment across all layers, measured validation, and continuous observation as workloads evolve.

## Conclusion

Azure Postgres provides a powerful and flexible platform for building modern, cloud-hosted database solutions. The engineering across Azure Compute, storage, networking, high availability, replication, security, and observability enables some of the most performant and resilient Postgres architectures available.

> **Maximum performance doesn't happen by accident.**

Maximum operational performance requires understanding the application, the clients, the workload, the data growth profile, the read/write mix, and the business cycles that shape demand. It also requires aligning both compute and storage choices so that IOPS, throughput, and latency targets are achieved end-to-end.

Premium SSD v1 can provide strong predictable performance, especially when host caching applies to data below the 4-TB boundary. Premium SSD v2 adds more flexible performance configuration by decoupling capacity, IOPS, and throughput. Ultra Disk represents the highest Azure managed disk performance class, while newer compute generations provide substantially higher aggregate remote storage ceilings for high-end architectures.

The best Azure Postgres deployments combine platform capability with deliberate planning, continuous monitoring, and clear operational ownership. With the right requirements and the right architecture, teams can deliver world-class Postgres experiences that provide peak performance.

## Related content

- [Azure Premium Storage: design for high performance](/azure/virtual-machines/premium-storage-performance)
- [Azure disk bursting](/azure/virtual-machines/disk-bursting#burstable-virtual-machine-with-nonburstable-disks)
- [Ddv5 and Ddsv5-series VM sizes](/azure/virtual-machines/sizes/general-purpose/ddsv5-series?tabs=sizestorageremote#sizes-in-series)
- [Ddsv6-series VM sizes](/azure/virtual-machines/sizes/general-purpose/ddsv6-series?tabs=sizestorageremote#sizes-in-series)
- [Premium SSD  storage option in Azure Database for PostgreSQL](concepts-storage-premium-ssd.md)
- [Premium SSD v2 storage option in Azure Database for PostgreSQL](concepts-storage-premium-ssd-v2.md)
- [Azure managed disk types](/azure/virtual-machines/disks-types)
- [Monitor metrics in Azure Database for PostgreSQL](../monitor/concepts-monitoring.md)
