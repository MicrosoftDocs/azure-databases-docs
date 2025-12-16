---
title: Periodic Backup and Restore Introduction
titleSuffix: Azure Cosmos DB
description: Learn about Azure Cosmos DB accounts with periodic backup retention and restoration capabilities at a specified interval.
author: kanshiG
ms.author: govindk
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 07/22/2025
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Periodic backup and restore in Azure Cosmos DB

Azure Cosmos DB automatically takes backups of your data at regular intervals. The automatic backups are taken without affecting the performance or availability of the database operations. All the backups are stored separately in a storage service, and those backups are globally replicated for resiliency against regional disasters. With Azure Cosmos DB, not only your data, but also the backups of your data are highly redundant and resilient to regional disasters.

## How Azure Cosmos DB performs data backup

The following steps show how Azure Cosmos DB performs data backup:

- Azure Cosmos DB automatically takes a full backup of your database every 4 hours. At any point of time, only the latest two backups are stored by default. If the default intervals aren't sufficient for your workloads, you can change the backup interval and the retention period from the Azure portal. You can change the backup configuration during or after the Azure Cosmos DB account is created. If the container or database is deleted, Azure Cosmos DB retains the existing snapshots of a given provisioned throughput container or shared throughput database for 30 days. If throughput is provisioned at the database level, the backup and restore process happens across the entire database scope.

- Azure Cosmos DB stores these backups in Azure Blob storage whereas the actual data resides locally within Azure Cosmos DB.

- To guarantee low latency, the snapshot of your backup is stored in Azure Blob storage in the same region as the current write region (or *one* of the write regions, in case you have a multi-region write configuration). For resiliency against regional disaster, each snapshot of the backup data in Azure Blob storage is again replicated to another region through geo-redundant storage (GRS). The region to which the backup is replicated is based on your source region and the regional pair associated with the source region. To learn more, see the list of [geo-redundant pairs of Azure regions](/azure/reliability/cross-region-replication-azure). You can't access this backup directly. Azure Cosmos DB team restores your backup when you request through a support request.

  The following image shows how an Azure Cosmos DB container with all the three primary physical partitions in West US. The container is backed up in a remote Azure Blob Storage account in West US and then replicated to East US:

  :::image type="content" source="./media/periodic-backup-restore-introduction/automatic-backup.png" alt-text="Diagram of periodic full backups taken of multiple Azure Cosmos DB entities in geo-redundant Azure Storage." lightbox="./media/periodic-backup-restore-introduction/automatic-backup.png":::

- The backups are taken without affecting the performance or availability of your application. Azure Cosmos DB performs data backup in the background without consuming any extra provisioned throughput (RUs) or affecting the performance and availability of your database.

With the periodic backup mode, the backups are taken only in the write region of your Azure Cosmos DB account. The restore action always restores data into a new account, which is located in the write region of the source account. 

## What is restored into a new account?

- You can choose to restore any combination of provisioned throughput containers, shared throughput database, or the entire account.
- The restore action restores all data and its index properties into a new account.
- The duration of restore depends on the amount of data that needs to be restored.
- The newly restored database account’s consistency setting is the same as the source database account’s consistency settings. 

## What isn't restored? 

The following configurations aren't restored after the point-in-time recovery:

- A subset of containers under a shared throughput database can't be restored. The entire database can be restored as a whole.
- Database account keys. The restored account is generated with new database account keys. 
- Firewall, virtual network, data plane RBAC, or private endpoint settings. 
- Regions. The restored account is only a single-region account, which is the write region of the source account. 
- Stored procedures, triggers, user-defined functions (UDF). 
- Role-based access control assignments. These need to be reassigned. 
- Documents that were deleted because of expired TTL. 
- Analytical data when synapse link is enabled. 
- Materialized views.

Some of these configurations can be added to the restored account after the restore is completed. 

## Azure Cosmos DB Backup with Azure Synapse Link

For Azure Synapse Link-enabled accounts, analytical store data isn't included in the backups and restores. When Azure Synapse Link is enabled, Azure Cosmos DB continues to automatically take backups of your data in the transactional store at a scheduled backup interval. Automatic backup and restore of your data in the analytical store isn't supported at this time.

## Understand the cost of backups

Two backups are provided free and extra backups are charged according to the region-based pricing for backup storage described in [Azure Cosmos DB pricing](https://azure.microsoft.com/pricing/details/cosmos-db/).

For example, consider a scenario where Backup Retention is configured to *240 hrs* (or *10 days*) and Backup Interval is configured to *24 hours*. This configuration implies that there are *10* copies of the backup data. If you have *1 TB* of data in an Azure West US region, the cost for backup storage in a given month would be: `0.12 * 1000 * 8`

## Required permissions to manage retention or restoration

Principals who are part of the role [CosmosdbBackupOperator](/azure/role-based-access-control/built-in-roles#cosmosbackupoperator), owner, or contributor are allowed to request a restore or change the retention period.

## Manually manage periodic backups in Azure Cosmos DB

With Azure Cosmos DB API for NoSQL accounts, you can also maintain your own backups by using one of the following approaches:

### Azure Data Factory

Use [Azure Data Factory](/azure/data-factory/connector-azure-cosmos-db) to move data periodically to a storage solution of your choice.

### Azure Cosmos DB change feed

Use the Azure Cosmos DB [change feed](change-feed.md) to read data periodically for full backups or for incremental changes, and store it in your own storage.

## Next step

> [!div class="nextstepaction"]
> [Periodic backup storage redundancy](periodic-backup-storage-redundancy.md)
