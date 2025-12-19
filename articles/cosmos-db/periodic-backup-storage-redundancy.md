---
title: Periodic backup storage redundancy
description: Learn how to configure Azure Storage-based data redundancy for periodic backup in Azure Cosmos DB accounts.
author: kanshiG
ms.author: govindk
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 03/21/2023
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Periodic backup storage redundancy in Azure Cosmos DB

By default, Azure Cosmos DB stores periodic mode backup data in geo-redundant [Azure Blob Storage](/azure/storage/common/storage-redundancy). The blob storage is then, by default, replicated to a [paired region](/azure/reliability/cross-region-replication-azure). You can update this default value using Azure PowerShell or Azure CLI and define an Azure policy to enforce a specific storage redundancy option. For more information, see [update backup storage redundancy](periodic-backup-update-storage-redundancy.md).

## Best practices

Change the default geo-redundant backup storage to ensure that your backup data stays within the same region where your Azure Cosmos DB account is provisioned. You can configure the geo-redundant backup to use either locally redundant or zone-redundant storage. Storage redundancy mechanisms store multiple copies of your backups so that it's protected from planned and unplanned events. These events can include transient hardware failure, network or power outages, or massive natural disasters.

## Redundancy options

You can configure storage redundancy for periodic backup mode at the time of account creation or update it for an existing account. You can use the following three data redundancy options in periodic backup mode:

- **Geo-redundant backup storage:** This option copies your data asynchronously across the paired region.

- **Zone-redundant backup storage:** This option copies your data synchronously across three Azure availability zones in the primary region. For more information, see [Zone-redundant storage.](/azure/storage/common/storage-redundancy#redundancy-in-the-primary-region)

- **Locally-redundant backup storage:** This option copies your data synchronously three times within a single physical location in the primary region. For more information, see [locally redundant storage.](/azure/storage/common/storage-redundancy#redundancy-in-the-primary-region)

> [!NOTE]
> Zone-redundant storage is currently available only in [specific regions](/azure/reliability/availability-zones-region-support). Depending on the region you select for a new account or the region you have for an existing account; the zone-redundant option will not be available.
>
> Updating backup storage redundancy will not have any impact on backup storage pricing.

## Next steps

> [!div class="nextstepaction"]
> [Update the redundancy of backup storage](periodic-backup-update-storage-redundancy.md)
