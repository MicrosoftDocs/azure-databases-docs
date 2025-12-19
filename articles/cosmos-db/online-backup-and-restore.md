---
title: Online Backup and On-Demand Data Restore
description: Learn how to use automatic backup and on-demand data restore, and learn about the difference between continuous and periodic backup modes.
author: kanshiG
ms.service: azure-cosmos-db
ms.custom: build-2023
ms.topic: how-to
ms.date: 07/21/2025
ms.author: govindk
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Online backup and on-demand data restore in Azure Cosmos DB

Azure Cosmos DB automatically takes backups of your data at regular intervals. The automatic backups are taken without affecting the performance or availability of the database operations. All the backups are stored separately in a storage service. The automatic backups are helpful in scenarios when you accidentally delete or update your Azure Cosmos DB account, database, or container and later require the data recovery. Azure Cosmos DB backups are encrypted with Microsoft-managed service keys. These backups are transferred over a secure non-public network, which means that backup data remains encrypted while transferred over the wire and at rest. Backups of an account in a given region are uploaded to storage accounts in the same region.

## Backup modes

There are two backup modes:

* **Continuous backup mode**: This mode has two tiers. One tier includes 7-day retention and the second includes 30-day retention. Continuous backup allows you to restore to any point in time within either 7 or 30 days, either into a [new account](restore-account-continuous-backup.md) or [existing account](restore-in-account-continuous-backup-resource-model.md). You can choose this appropriate tier when creating an Azure Cosmos DB account. For more information about the tiers, see [Continuous backup with point-in-time restore in](continuous-backup-restore-introduction.md). To enable continuous backup, see the appropriate articles using [Azure portal](provision-account-continuous-backup.md#provision-portal), [PowerShell](provision-account-continuous-backup.md#provision-powershell), [CLI](provision-account-continuous-backup.md#provision-cli), or [Azure Resource Manager](provision-account-continuous-backup.md#provision-arm-template). You can also [migrate the accounts from periodic to continuous mode](migrate-continuous-backup.md).

* **Periodic backup mode**: This mode is the default backup mode for all existing accounts. In this mode, backup is taken at a periodic interval and the data is restored by creating a request with the support team. In this mode, you configure a backup interval and retention for your account. The maximum retention period extends to a month. The minimum backup interval can be one hour. To learn more, see [Periodic backup and restore](periodic-backup-restore-introduction.md).

  > [!NOTE]
  > If you configure a new account with continuous backup, you can do self-service restore via Azure portal, PowerShell, or CLI. If your account is configured in continuous mode, you can’t switch it back to periodic mode.

For Azure Synapse Link-enabled accounts, analytical store data isn't included in the backups and restores. When Azure Synapse Link is enabled, Azure Cosmos DB continues to automatically take backups of your data in the transactional store at a scheduled backup interval. Within an analytical store, automatic backup and restore of your data isn't supported at this time.

## Immutability of Cosmos DB backups

Cosmos DB backups are completely managed by the platform. Actions like restore, update backup retention, or redundancy change are controlled via permission model managed by database account administrator. Cosmos DB backups aren't exposed to any human actors, customers, or any other module for listing, deletion, or disabling of backups. The backups are encrypted and stored in storage accounts secured by rotating certificate-based access. These backups are only accessed by restore module to restore specific backup nondestructively when a customer initiates a restore. These actions are logged and audited regularly. For customers who chose [customer managed keys](how-to-setup-customer-managed-keys.md), their data and backup have protection through envelope encryption.

Backups kept under retention policy are:  

* Not alterable (no modifications are permitted to the backups)
* Not allowed to be re-encrypted
* Not allowed to be deleted
* Not allowed to be disabled

## Frequently asked questions

### Can I restore from an account A in subscription S1 to account B in a subscription S2?

No. You can only restore between accounts within the same subscription.

### Can I restore into an account that has fewer partitions or low provisioned throughput than the source account?

No. You can't restore into an account with lower RU/s or fewer partitions.

### Is periodic backup mode supported for Azure Synapse Link-enabled accounts?

Yes. However, analytical store data isn't included in backups and restores. When Azure Synapse Link is enabled on a database account, Azure Cosmos DB automatically backs up your data in the transactional store at the scheduled backup interval.

### Is periodic backup mode supported for analytical store-enabled containers?

Yes, but only for the regular transactional data. Within an analytical store, backup and restore of your data isn't supported at this time.

## Next steps

* [Periodic backup and restore in Azure Cosmos DB](periodic-backup-restore-introduction.md)
* [Continuous backup with point-in-time restore in Azure Cosmos DB](continuous-backup-restore-introduction.md)
* Enable continuous backup using [Azure portal](provision-account-continuous-backup.md#provision-portal), [PowerShell](provision-account-continuous-backup.md#provision-powershell), [CLI](provision-account-continuous-backup.md#provision-cli), or [Azure Resource Manager](provision-account-continuous-backup.md#provision-arm-template)
* Restore continuous backup into a new account using [Azure portal](restore-account-continuous-backup.md#restore-account-portal), [PowerShell](restore-account-continuous-backup.md#restore-account-powershell), [CLI](restore-account-continuous-backup.md#restore-account-cli), or [Azure Resource Manager](restore-account-continuous-backup.md#restore-arm-template)
* [Migrate to an account from periodic backup to continuous backup](migrate-continuous-backup.md)
* [Manage permissions to restore an Azure Cosmos DB account](continuous-backup-restore-permissions.md)
* [Resource model for the Azure Cosmos DB point-in-time restore feature](continuous-backup-restore-resource-model.md)
