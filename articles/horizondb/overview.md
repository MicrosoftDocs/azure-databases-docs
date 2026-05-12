---
title: What is Azure HorizonDB?
description: Learn about Azure HorizonDB, a fully managed, AI-readydatabase service built on PostgreSQL engineered for performance and scale.
author: denzilribeiro
ms.author: denzilr
ms.reviewer: maghan
ms.date: 05/11/2026
ms.service: azure-database-postgresql
ms.topic: overview
ai-usage: ai-assisted
---

# What is Azure HorizonDB?

Azure HorizonDB is a cloud native fully managed, AI-ready database service built on PostgreSQL. It combines a disaggregated compute and storage architecture with a database-as-a-log design to deliver predictable performance, enterprise-grade security, high availability, and seamless scalability for mission-critical workloads.

Azure HorizonDB empowers developers to build intelligent, AI-powered applications through native support for vector embeddings and integration with Azure AI Foundry Tools, while retaining full PostgreSQL compatibility so existing applications.

## Azure HorizonDB use cases
Azure HorizonDB is a cloud native scalable alternative to self-managed PostgreSQL and is designed for mission-critical workloads not limited to but including :

- **Transactional workloads (OLTP)** - High-throughput, low-latency transaction processing with predictable performance for line-of-business applications, e-commerce platforms, and SaaS backends.
- **AI and intelligent applications** - Native vector search and embedding support let you build retrieval-augmented generation (RAG) pipelines, recommendation engines, and semantic search directly within the database layer. With AI model management and AI pipelines further simplify building intelligent applications within the database.
- **Massive read scale-out** - Applications that can benefit from read scale out with a single copy of zone resilient data within region without the overhead of PostgreSQL replication.
- **Hybrid applications** - Ability to integrate with Azure ecosystem, mirror transactional data to Fabric Onelake integrating with other analytical data.


## Architecture of Azure HorizonDB

Azure HorizonDB is built on two foundational architectural principles:  separation of compute and storage, and a database-as-a-log design.

:::image type="content" source="./media/overview/horizon-db-architecture.png" alt-text="Diagram showing the Azure HorizonDB architecture." lightbox="./media/overview/horizon-db-architecture.png":::

### Disaggregated compute and storage

The architecture fully separates the compute layer from the storage layer:

- **Compute layer** - Compute on Azure HorizonDB is stateless.You can independently scale compute resources (vCores and memory) without affecting storage, and vice versa. You can horizontally scale out reads by adding replicas to the HorizonDB cluster
- **Storage layer** - Storage layer consistes of purpose built storage fleets one for WAL, another for data both have durability backed by Azure storage. All storage is zone resilient by default. Storage scales automatically as data grows, independent of the provisioned compute tier. 

This separation provides several benefits:

- Scale compute and storage independently based on workload demands.
- Quick provisioning of read replicas since they attach to the same underlying storage.
- Faster failover during high availability events because the standby node attaches to existing durable storage.

### Database-as-a-log architecture

Azure HorizonDB adopts the database-as-a-log architecture where WAL is the only thing written from Compute to the storage subsytem and is the authoritative source of truth for all data changes:
- All writes (WAL) are appended to a durable log service before being acknowledged to the client. The WAL Service is optimized for semantics of a transaction log and optimized for low latency.
- Filtered WAL is sent to only the storage nodes that the changes belong to.
- Storage nodes reconstruct page state by applying the WAL, eliminating traditional checkpoint I/O bottlenecks.
- This approach reduces write amplification and delivers consistent, predictable write latency regardless of database size.

The combination of these two principles enables Azure HorizonDB to deliver high throughput, low latency, and efficient resource utilization while maintaining full ACID guarantees.

## Cluster
A provisioned HorizonDB resource is called a cluster. A HorizonDB cluster
- Has one ore more compute replicas, one is a writable, the rest are readable.
- Has a single copy of zone resilient storage accross all the replicas within region.
- Has a read-write endpoint that always points to the primary replica.
- Has a read-only endpoint that load balances connections to all readable replicas.

## Compute Replicas
A HorizonDB compute replica can be either the primary (writeable) or a secondary replica that is a readable  and also a candidate for failover. Compute replica is where the PostgreSQL relational engine lives and where the language, query and transaction processing occurs. All interations to the HorizonDB cluster happen through the compute replicas. In order to have zonal resilience, you need atleast 2 replicas on the cluster. You can add or remove replicas to the HorizonDB cluster as your workload needs it.


Compute replicas also have a local SSD cache. This cache is a very low latency cache that caches hot pages and minimizes the need to fetch data from the remove storage layer, and exists on all replicas primary and read replicas.

Compute replicas are used efficiently as they offload a lot of durability and high availability related work to the storage layer. This gives more CPU, disk and network to run business logic of applications on the database. Below are tasks that are offloaded from the Compute replicas to storage layer.

| Task | PostgreSQL process | Resource savings |
| --- | --- | --- |
| WAL sending from replicas | Walsender | Disk IO, Network IO |
| WAL archiving to blob storage | Archiver  | Disk IO, Network IO |
| Dirty Page Writing | background writer | Disk IO |
| Checkpointing  | checkpointer | Disk IO |
| Backups  | pg_dump, pg_basebackup, pg_backup_start, pg_backup_stop | Disk IO |
| Full page writes | Backends doing WAL writing | Disk IO |
| PostgreSQL WAL recovery | startup recovering  | Disk IO |
| PostgreSQL read replica redo | startup recovering | Disk IO |


## Storage
HorizonDB runs two storage fleets that are backed by Azure Blob storage. All layers of the storage stack are zone resilient by default.

#### WAL Storage
This is a purpose built service that accepts WAL from the primary compute replica and is optimized for low latency and WAL writing patterns. When a data change (insert/update/delete) is made on the primary replica, WAL is written to the the WAL service and the transaction is acknowledged. This WAL is then applied asynchronously to respective shards of data on the Data storage fleet as well as sent to secondary compute read replicas to redo any changes of pages that are in their shared buffers. WAL is then archived to Azure Blob storage and kept for the short term retention time configured.

#### Data Storage
The data storage fleet is a cache for all the data in the database that serves data to all compute replicas in the HorizonDB cluster. Storage is allocated dynamically as the database grows without the need to configure storage size or IOPS. Data from postgres relations are sharded accross the multiple storage nodes in the fleet to provide scalability for reads. There are multiple copies of a the same data stored accross zones for resiliency.

#### Azure Blob Storage
Azure Blob storage is the durability for data in the database as well as the data store for WAL archival. Backups of the database are snapshots of the blobs. 

## Pricing
HorizonDB currently charges for
- Provisioned Compute in core hours
- Used Storage
- Used Backup Storage for the short term retention period

## Limitations

Azure HorizonDB is currently in Public Preview. The following features aren't yet available and we are actively working on most of these.

| Feature | Status | Notes |
| --- | --- | --- |
| Cross region read replicas | Not available | Cross-region replication for disaster recovery isn't yet supported.|
| Configurable backup retention | Not yet available | Currentlly backup retention is 7 days. We are working on enabling 1-35 days backup retention |
| Long-term retention (LTR) | Not available | Currentlly backup retention is 7 days. |
| Customer-managed keys (CMK) for encryption | Not available | Encryption at rest currently uses service-managed keys only. |
| Virtual network injection | Not available | Currently we support private link, vnet integration isn't yet supported|
|Configurable maintenance windows | Not available | Currently upgrades will happen on system managed maintenance window. Ability to configure custom maintenance windows isn't yet available |


> [!NOTE]
> This list reflects the current state of the service and is subject to change as new capabilities are released. Check the [release notes](release-notes/release-notes.md) for the latest updates.

## Regions

Azure HorizonDB is currently available in the following Azure regions:

| Geography | Regions |
| --- | --- |
| Americas | Central US, West US 2, Canada Central |
| Europe | Sweden Central, Poland Central, Italy North |
| Asia Pacific | SAustralia East, Korea Central, Indonesia Central |

> [!NOTE]
> Region availability is subject to change. Some regions might have restrictions on new deployments. For the latest region availability, see the Azure portal or contact Azure support.

## Related content

- [Quickstart: Create an Azure HorizonDB server](configure-maintain/quickstart-create-server.md)
- [High availability in Azure HorizonDB](/azure/reliability/reliability-postgresql-flexible-server)
- [Backup and restore in Azure HorizonDB](backup-restore/concepts-backup-restore.md)
- [Networking overview](network/concepts-networking.md)
- [Migration service overview](migrate/migration-service/overview-migration-service-postgresql.md)
- [Release notes](release-notes/release-notes.md)
