---
title: What Is Azure HorizonDB?
description: Learn about Azure HorizonDB, a fully managed, AI-ready database service built on PostgreSQL engineered for performance and scale.
author: denzilribeiro
ms.author: denzilr
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: overview
---

# What is Azure HorizonDB (Preview)?

Azure HorizonDB is a cloud native fully managed, AI-ready database service built on PostgreSQL. It combines a disaggregated compute and storage architecture with a database-as-a-log design to deliver predictable performance, enterprise-grade security, high availability, and seamless scalability for mission-critical workloads.

Azure HorizonDB empowers developers to build intelligent, AI-powered applications through native support for vector embeddings and integration with Azure AI Foundry Tools, while retaining full PostgreSQL compatibility so existing applications can easily migrate to Azure HorizonDB.

## Azure HorizonDB use cases

Azure HorizonDB is a cloud native scalable alternative to self-managed PostgreSQL and is designed for mission-critical workloads not limited to but including:

- **Transactional workloads (OLTP)** - High-throughput, low-latency transaction processing with predictable performance for line-of-business applications, e-commerce platforms, and SaaS backends.
- **AI and intelligent applications** - Native vector search and embedding support lets you build retrieval-augmented generation (RAG) pipelines, recommendation engines, and semantic search directly within the database layer. AI model management and AI pipelines further simplify building intelligent applications within the database.
- **Massive read scale-out** - Applications that can benefit from read scale-out with shared zone resilient data.
- **Hybrid applications** - Integration with Azure ecosystem, mirror transactional data to Fabric One lake integrating with other analytical data.

## Architecture of Azure HorizonDB

Azure HorizonDB is built on two foundational architectural principles: separation of compute and storage, and a database-as-a-log design.

:::image type="content" source="media/overview/horizon-db-architecture.png" alt-text="Diagram showing the Azure HorizonDB architecture." lightbox="media/overview/horizon-db-architecture.png":::

### Disaggregated compute and storage

The architecture fully separates the compute layer from the storage layer:

- **Compute layer** - Compute on Azure HorizonDB is stateless. Compute resources (vCores and memory) can be independently scaled without affecting storage, and vice versa. You can horizontally scale out reads by adding replicas to the HorizonDB cluster.
- **Storage layer** - Storage layer uses two purpose-built storage fleets: one dedicated for WAL, another to data; both have durability backed by Azure storage. All storage is zone resilient by default. Storage scales automatically as data grows, independent of the provisioned compute tier.

The separation of compute and storage provides several benefits:

- Scale compute and storage independently based on workload demands.
- Quick provisioning of read replicas since they share the same underlying storage and no data replication is needed.
- Faster failover for high availability since the shared durable WAL storage and no log rewinding is needed.

### Database-as-a-log architecture

Azure HorizonDB adopts the database-as-a-log architecture where only WAL (Write ahead log) is the written from compute to the storage layer. Data pages aren't written from the compute replicas to the storage layer. WAL is the authoritative source of truth through the system.
- All writes (Write ahead Log) are appended to a durable log service before being acknowledged to the client. The WAL Service is optimized for semantics of a transaction log and optimized for low latency.
- Filtered WAL is sent to only the storage nodes that the changes belong to.
- Storage nodes reconstruct page state by applying the WAL, eliminating traditional checkpoint I/O bottlenecks.
- This approach reduces write amplification and delivers consistent, predictable write latency regardless of database size.

The combination of these two principles enables Azure HorizonDB to deliver high throughput, low latency, and efficient resource utilization while maintaining full ACID guarantees.

## Cluster

A provisioned Azure HorizonDB resource is a cluster. An Azure HorizonDB cluster has:
- One or more compute replicas, one is a writable primary, the rest being readable standby replicas.
- A single copy of the data in zone resilient storage shared by all replicas in the cluster.
- A read-write endpoint that always points to the primary replica.
- A read-only endpoint that load balances connections to all readable replicas.

## Compute replicas

An Azure HorizonDB compute replica can be either the primary (writeable) or a standby replica that is a readable, while also being a candidate for failover. Compute replica is where the PostgreSQL relational engine lives and where the language, query, and transaction processing occur. All interactions with the Azure HorizonDB cluster happen through the compute replicas. In order to have zonal resilience, you need atleast two replicas on the cluster. You can add or remove replicas to the Azure HorizonDB cluster as your workload needs it.

Compute replicas come with 8 GB of memory per core provisioned. Compute replicas also have a local SSD cache. This cache is a low latency NVMe cache that caches hot pages and minimizes the need to fetch data from the remote storage layer. The cache is present on all replicas, the primary, and the standby.

Compute replicas are used efficiently as they offload durability and high availability related tasks to the storage layer. This offloading gives more CPU, disk, and network to run business logic of applications on the database. The following tasks are offloaded from the Compute replicas to storage layer.

| Task | PostgreSQL process | Resource savings |
| --- | --- | --- |
| WAL sending from replicas | walsender | Disk IO, Network IO |
| WAL archiving to blob storage | Archiver | Disk IO, Network IO |
| Dirty Page Writing | background writer | Disk IO |
| Checkpointing | checkpointer | Disk IO |
| Backups | pg_dump, pg_basebackup, pg_backup_start, pg_backup_stop | Disk IO |
| Full page writes | Backends doing WAL writing | Disk IO |
| PostgreSQL WAL recovery | startup recovering | Disk IO |
| PostgreSQL read replica redo | startup recovering | Disk IO |

## Storage

Azure HorizonDB runs two storage fleets backed by Azure blob storage. All layers of the storage stack are zone resilient by default.

#### WAL storage

WAL Service is a purpose-built service that accepts WAL from the primary compute replica and is optimized for low latency and WAL writing patterns. When a data change (insert/update/delete) is made on the primary replica, WAL is written to the WAL service and the transaction is acknowledged. WAL is then applied asynchronously to respective shards of data on the data storage fleet to apply the latest changes. In addition, WAL is sent to secondary compute replicas to redo any changes to pages that are in memory on the replicas. WAL is then archived to Azure blob storage and kept for the short term retention time configured.

#### Data storage

The data storage fleet is a cache for all the data in the database that serves data to all compute replicas in the Azure HorizonDB cluster. Storage is allocated dynamically as the database grows without the need to configure storage size or IOPS. Data from postgres relations are sharded across the multiple storage nodes in the fleet to provide improved scalability. There are multiple copies of at the same shard of data stored across zones for resiliency. As WAL is replayed on the storage fleet, dirty pages from the storage fleet are then written to Azure Blob storage.

#### Azure Blob storage

Azure Blob storage provides durability for database data also serves as the data store for WAL archival. Data is stored on zone-redundant storage accounts. Database backups are implemented as snapshots of the blobs.

<a id="pricing"></a>

## Price

Azure HorizonDB currently charges for:
- Provisioned Compute in core hours,
- Used database storage (GB/month), and
- Used backup storage for the short term retention period.

For more pricing details, view the [pricing page](https://azure.microsoft.com/pricing/details/https://azure.microsoft.com/en-us/products/horizondb).

## Limitations

Azure HorizonDB is currently in **preview**. The following features aren't yet available we're actively working on these features.

| Feature | Status | Notes |
| --- | --- | --- |
| Configurable backup retention | Not yet available | Currently backup retention is seven days. We're working on enabling 1-35 days backup retention |
| Cross region read replicas | Not yet available | Cross-region replication for disaster recovery isn't yet supported. |
| Customer-managed keys (CMK) for encryption | Not available | Encryption at rest currently uses service-managed keys only. |
| Configurable maintenance windows | Not yet available | Currently upgrades occur on a system managed maintenance window. Ability to configure custom maintenance windows isn't yet available |
| Connection Pooling (PgBouncer) | Not yet available | An external connection pooler can be used while we're working connection pooling to the service. |
| Long-term retention (LTR) | Not available | Currently backup retention is seven days. |
| Index Tuning | Not yet available | Index tuning is coming soon. |
| Virtual network injection | Not available | Currently we support private link. Virtual network integration isn't yet supported |

> [!NOTE]  
> This list reflects the current state of the service and is subject to change as new capabilities are released. Check the [release notes](release-notes/release-notes.md) for the latest updates.

## Azure regions

Azure HorizonDB is currently available in the following Azure regions:

| Geography | Regions |
| --- | --- |
| Americas |  Central US, West US 2, West US 3 |
| Europe | Sweden Central |
| Asia Pacific | Australia East |

> [!NOTE]  
> Region availability is subject to change and we'll be adding more regions soon. Some regions might have restrictions on new deployments. For the latest region availability, see the Azure portal or contact Azure support.

## Feedback and support

If you have questions or suggestions about Azure HorizonDB, you can get help and support through the following channels:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/forums/597976-azure-database-for-postgresql).

## Related content

- [Create an Azure HorizonDB cluster](configure-maintain/quickstart-create-cluster.md)
- [Backups in Azure HorizonDB (Preview)](backup-restore/concepts-backup-restore.md)
- [What is the PostgreSQL extension for Visual Studio Code?](development/vs-code-extension/vs-code-overview.md)
