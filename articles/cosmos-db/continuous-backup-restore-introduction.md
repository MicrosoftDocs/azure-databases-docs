---
title: Continuous Backup with Point-in-Time Restore
description: Learn how Azure Cosmos DB's point-in-time restore feature helps to recover data from an accidental write, delete operation, or to restore data into any region. Learn about pricing and current limitations.
author: kanshiG
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 12/04/2025
ms.author: govindk
ms.custom: references_regions, cosmos-db-video, build-2023
---

# Continuous backup with point-in-time restore in Azure Cosmos DB

[!INCLUDE[NoSQL, MongoDB, Gremlin, Table](includes/appliesto-nosql-mongodb-gremlin-table.md)]

Azure Cosmos DB's point-in-time restore feature helps in multiple scenarios including:

* Recovering from an accidental write or delete operation within a container.
* Restoring a deleted account, database, or container.
* Restoring into any region (where backups existed) at the restore point in time.

> [!VIDEO https://www.youtube.com/embed/m3lKJf47bQA?si=yVT3iGBLa40eQXdb]

Azure Cosmos DB performs data backup in the background without consuming any extra provisioned throughput (RUs) or affecting the performance and availability of your database. Continuous backups are taken in every region where the account exists. For example, an account can have a write region in West US and read regions in East US and East US 2. These replica regions can then be backed up to a remote Azure Storage account in each respective region. By default, each region stores the backup in locally redundant storage accounts. If the region has [availability zones](/azure/well-architected/reliability/regions-availability-zones) enabled, then the backup is stored in zone-redundant storage accounts.

:::image type="complex" source="media/continuous-backup-restore-introduction/continuous-backup-restore-blob-storage.png" lightbox="media/continuous-backup-restore-introduction/continuous-backup-restore-blob-storage.png" alt-text="Diagram illustrating how a container is backed up across multiple regions.":::
Diagram illustrating how a container with a write region in West US and read regions in East and East US 2 is backed up. The container is backed up to a remote Azure Blob Storage account in each respective write and read region.
:::image-end:::

The time window available for restore (also known as retention period) is the lower value of the following two options: 30-day and 7-day.

The selected option depends on the chosen tier of continuous backup. The point in time for restore can be any timestamp within the retention period no further back than the point when the resource was created. In strong consistency mode, backups taken in the write region are more up to date when compared to the read regions. Read regions can lag behind due to network or other transient issues. While doing restore, you can [get the latest restorable timestamp](get-latest-restore-timestamp.md) for a given resource in a specific region. Referring to latest restorable timestamp helps to confirm resource backups are up to the given timestamp, and can restore in that region.

Currently, you can restore an Azure Cosmos DB account (API for NoSQL or MongoDB, API for Table, API for Gremlin) contents at a specific point in time to another account. You can perform this restore operation via the [Azure portal](restore-account-continuous-backup.md#restore-account-portal), the [Azure CLI](restore-account-continuous-backup.md#restore-account-cli), [Azure PowerShell](restore-account-continuous-backup.md#restore-account-powershell), or [Azure Resource Manager templates](restore-account-continuous-backup.md#restore-arm-template).

## Backup storage redundancy

By default, Azure Cosmos DB stores continuous mode backup data in locally redundant storage blobs. For the regions that have zone redundancy configured, the backup is stored in zone-redundant storage blobs. In continuous backup mode, you can't update the backup storage redundancy.

## Different ways to restore
Continuous backup mode supports two ways to restore deleted containers and databases. They can be restored into a [new account](restore-account-continuous-backup.md) or into an [existing account](restore-account-continuous-backup.md). The choice between these two modes depends on the scenarios. In most cases, it's preferred to restore deleted containers and databases into an existing account. This avoids the cost of data transfer required when restoring to a new account. For scenarios where accidental data modification was done, restoring into a new account could be the preferred option.

## What is restored into a new account?

In a steady state, all mutations performed on the source account (which includes databases, containers, and items) are backed up asynchronously within 100 seconds. If the Azure Storage backup media is down or unavailable, the mutations are persisted locally until the media is available. Then the mutations are flushed out to prevent any loss in fidelity of operations that can be restored.

You can choose to restore any combination of provisioned throughput containers, shared throughput database, or the entire account. The restore action restores all data and its index properties into a new account. The restore process ensures that all the data restored in an account, database, or a container is guaranteed to be consistent up to the restore time specified. The duration of restore depends on the amount of data that needs to be restored. The newly restored database account’s consistency setting is same as the source database account’s consistency settings.

> [!NOTE]
> With the continuous backup mode, the backups are taken in every region where your Azure Cosmos DB account is available. Backups taken for each region account are *locally redundant* by default, and zone redundant if your account has [availability zone](/azure/architecture/reliability/architect) feature enabled for that region. The restore action always restores data into a new account.

## What isn't restored?

The following configurations aren't restored after the point-in-time recovery:

* A subset of containers under a shared throughput database can't be restored. The entire database can be restored as a whole.
* Firewall, [virtual network](how-to-configure-vnet-service-endpoint.md), data plane role-based access control, or private endpoint settings.
* All the regions from the source account.
* Stored procedures, triggers, UDFs.
* Role-based access control assignments.

You can add these configurations to the restored account after the restore is completed.

## Restorable timestamp for live accounts

To restore Azure Cosmos DB live accounts that aren't deleted, it's a best practice to always identify the [latest restorable timestamp](get-latest-restore-timestamp.md) for the container. You can then use this timestamp to restore the account to its latest version.

## Restore scenarios

The point-in-time-restore feature supports the following scenarios. Scenarios 1 through 3 demonstrate how to trigger a restore if the restore timestamp is known beforehand. However, there could be scenarios where you don't know the exact time of accidental deletion or corruption. Scenarios 4 and 5 demonstrate how to *discover* the restore timestamp using the new event feed APIs on the restorable database or containers.

:::image type="content" source="./media/continuous-backup-restore-introduction/restorable-account-scenario.png" alt-text="Diagram that shows life-cycle events with timestamps for a restorable account." lightbox="./media/continuous-backup-restore-introduction/restorable-account-scenario.png":::

- **Scenario 1 - Restore deleted account**: All the deleted accounts that you can restore are visible from the **Restore** pane. For example, if *Account A* is deleted at timestamp T3. In this case the timestamp just before T3, location, target account name, resource group, and target account name are sufficient to restore from the [Azure portal](restore-account-continuous-backup.md#restore-deleted-account), [PowerShell](restore-account-continuous-backup.md#trigger-restore-ps), or [CLI](restore-account-continuous-backup.md#trigger-restore-cli).  

   :::image type="content" source="./media/continuous-backup-restore-introduction/restorable-container-database-scenario.png" alt-text="Life-cycle events with timestamps for a restorable database and container." lightbox="./media/continuous-backup-restore-introduction/restorable-container-database-scenario.png":::

- **Scenario 2 - Restore data of an account in a particular region**: For example, if *Account A* exists in two regions *East US* and *West US* at timestamp T3. If you need a copy of account A in *West US*, you can do a point in time restore from the [Azure portal](restore-account-continuous-backup.md#restore-deleted-account), [PowerShell](restore-account-continuous-backup.md#trigger-restore-ps), or [CLI](restore-account-continuous-backup.md#trigger-restore-cli) with West US as the target location.

- **Scenario 3 - Recover from an accidental write or delete operation within a container with a known restore timestamp**: For example, if you know that the contents of *Container 1* within *Database 1* were modified accidentally at timestamp T3. You can do a point in time restore from the [Azure portal](restore-account-continuous-backup.md#restore-live-account), [PowerShell](restore-account-continuous-backup.md#trigger-restore-ps), or [CLI](restore-account-continuous-backup.md#trigger-restore-cli) into another account at timestamp T3 to recover the desired state of container.

- **Scenario 4 - Restore an account to a previous point in time before the accidental delete of the database**: In the [Azure portal](restore-account-continuous-backup.md#restore-live-account), you can use the event feed pane to determine when a database was deleted and find the restore time. Similarly, with [Azure CLI](restore-account-continuous-backup.md#trigger-restore-cli) and [PowerShell](restore-account-continuous-backup.md#trigger-restore-ps), you can discover the database deletion event by enumerating the database events feed and then trigger the restore command with the required parameters.

- **Scenario 5 - Restore an account to a previous point in time before the accidental delete or modification of the container properties**: In the [Azure portal](restore-account-continuous-backup.md#restore-live-account), you can use the event feed pane to determine when a container was created, modified, or deleted to find the restore time. Similarly, with [Azure CLI](restore-account-continuous-backup.md#trigger-restore-cli) and [PowerShell](restore-account-continuous-backup.md#trigger-restore-ps), you can discover all the container events by enumerating the container events feed and then trigger the restore command with required parameters.

## Permissions

Azure Cosmos DB allows you to isolate and restrict the restore permissions for continuous backup account to a specific role or a principal. To learn more, see [Manage permissions to restore an Azure Cosmos DB account](continuous-backup-restore-permissions.md).

## Understand multi-region write account restore

Writes that are performed in the [hub region](multi-region-writes.md#hub-region) are immediately confirmed and backed up asynchronously within 100 seconds. In multi-write accounts, any mutations performed on the satellite region are sent to the hub region for confirmation. The hub region checks to see if any [conflict resolution](conflict-resolution-policies.md#conflict-resolution-policies) is needed, assigns a [conflict-resolution timestamp](multi-region-writes.md#understanding-timestamps) after resolving the conflicts, and sends back the document to satellite region. The satellite region only backs up the documents after the confirmation is received from the hub. In short, the restore process only restores the documents confirmed by the hub region by the restore point of time.  

What happens for restore for multi-region write account?

- The mutations that are yet to be confirmed by the restore timestamp aren't restored. 
- The collections with custom conflict resolution policy are reset to last writer wins based on timestamp. 

> [!NOTE]
> Restoring from satellite region is slower compared to restore in the [hub region](multi-region-writes.md#hub-region) for multi-region account to resolve local [tentative writes](multi-region-writes.md#hub-region) as confirmed or take an action to roll them back.

To learn more about understanding timestamps in a multi-write enabled account, see [Understanding timestamps](multi-region-writes.md#understanding-timestamps).

Example scenario: Given a multi-write region account with two regions East US and West US, out of which East US is the hub region, consider the following sequence of events:

- T1: Client writes a document Doc1 to East US (Since East US is the hub region, the write is immediately confirmed)  

- T2: Client writes a document Doc2 to West US  

- T3: West US sends Doc2 to East US for confirmation  

- T4: East US received Doc2, confirms the document and sends of Doc2 back to West US

- T5: West US received confirmed Doc2

In this scenario, if the restore timestamp provided is T3 for hub region as source, only Doc1 gets restored. Doc2 hasn't been confirmed by hub by T3. Only if the restore timestamp is more than T4, the doc2 gets restored as restore at T4 in satellite contains only doc1 since doc2 isn't confirmed yet.

## <a id="continuous-backup-pricing"></a>Pricing

Azure Cosmos DB account with continuous 30-day backup has an extra monthly charge to *store the backup*. Both the 30-day and 7-day tier of continuous back incur charges to *restore your data*. The restore cost is added every time the restore operation is initiated. If you configure an account with continuous backup but don't restore the data, only backup storage cost is included in your bill.

The following example is based on the price for an Azure Cosmos DB account deployed in West US. The pricing and calculation can vary depending on the region you're using, see the [Azure Cosmos DB pricing page](https://azure.microsoft.com/pricing/details/cosmos-db/) for latest pricing information.

* All accounts enabled with continuous backup policy with 30-day incur a monthly charge for backup storage that is calculated as follows:

  $0.20/GB \* Data size in GB in account \* Number of regions

* Every restore API invocation incurs a one-time charge. The charge is a function of the amount of data restored:

  $0.15/GB \* Data size in GB

For example, if you have 1 TB of data in two regions:

* Backup storage cost is calculated as 1000 \* 0.20 \* 2 = $400 per month

* Restore cost is calculated as 1000 \* 0.15 = $150 per restore

> [!TIP]
> For more information about measuring the current data usage of your Azure Cosmos DB account, see [Explore Azure Monitor Azure Cosmos DB insights](insights-overview.md#view-utilization-and-performance-metrics-for-azure-cosmos-db). Continuous 7-day tier doesn't incur charges for backup of the data.

## Continuous 30-day tier vs 7-day tier

* Retention period for one tier is 30-day compared to 7-day for another tier.
* 30-day retention tier is charged for backup storage. Seven-day retention tier isn't charged.
* Restore is always charged in either tier

## Time to live

* The default restore process restores all the properties of a container including its TTL configuration by default. This can result in deletion of data if restore is done without disabling the TTL. To prevent deletion, pass a parameter to disable TTL in [PowerShell](./restore-account-continuous-backup.md#trigger-restore-ps) (-DisableTtl $true) or [cli](./restore-account-continuous-backup.md#trigger-restore-cli) (--disable-ttl True) while doing the restore.

## Customer-managed keys

See [How do customer-managed keys affect continuous backups](./how-to-setup-cmk.md#how-do-customer-managed-keys-affect-continuous-backups) to learn:

* How to configure your Azure Cosmos DB account when using customer-managed keys with continuous backups.
* How do customer-managed keys affect restores?

## Current limitations

Currently the point-in-time restore functionality has the following limitations:

* Azure Cosmos DB APIs for SQL, MongoDB, Gremlin, and Table supported for continuous backup. API for Cassandra isn't supported now.

* Currently, customers that disabled Synapse Link *(deprecated)* from containers can't migrate to continuous backup. And analytical store isn't included in backups. 

* The restored account is created in the same region where your source account exists. You can't restore an account into a region where the source account didn't exist.

* The restore window is only 30 days for continuous 30-day tier and seven days for continuous 7-day tier. These tiers can be switched, but the actual quantities (`7` or `30`) can't be changed. Furthermore, if you switch from 30-day tier to 7-day tier, there's the potential for data loss on days beyond the seventh.

* The backups aren't automatically geo-disaster resistant. Another region should be explicitly added for resiliency of the account and the backup.

* While a restore is in progress, don't modify or delete the Identity and Access Management (IAM) policies. These policies grant the permissions for the account to change any virtual network, firewall configuration.

* Azure Cosmos DB for MongoDB accounts with continuous backup don't support creating a [unique index](./mongodb/indexing.md#unique-indexes) for an existing collection. For such an account, unique indexes must be created along with their collection creation, which must and can only be done using the create collection [extension commands](./mongodb/custom-commands.md#create-collection).

* After restoring, it's possible that for certain collections the consistent index might be rebuilding. You can check the status of the rebuild operation via the [IndexTransformationProgress](how-to-manage-indexing-policy.md) property.

* Unique indexes in API for MongoDB can't be added, updated, or dropped when you create a continuous backup mode account. They also can't be modified when you migrate an account from periodic to continuous mode.

* Continuous mode restore might not restore throughput setting valid as of restore point.

## Next steps

* Enable continuous backup using the [Azure portal](provision-account-continuous-backup.md#provision-portal), [PowerShell](provision-account-continuous-backup.md#provision-powershell), [CLI](provision-account-continuous-backup.md#provision-cli), or [Azure Resource Manager](provision-account-continuous-backup.md#provision-arm-template)
* Restore continuous backup account using the [Azure portal](restore-account-continuous-backup.md#restore-account-portal), [PowerShell](restore-account-continuous-backup.md#restore-account-powershell), [CLI](restore-account-continuous-backup.md#restore-account-cli), or [Azure Resource Manager](restore-account-continuous-backup.md#restore-arm-template)
* [Get the latest restorable timestamp for continuous backup accounts](get-latest-restore-timestamp.md)
* [Migrate an account from periodic backup to continuous backup](migrate-continuous-backup.md)
* [Manage permissions to restore an Azure Cosmos DB account](continuous-backup-restore-permissions.md)
* [Resource model for the Azure Cosmos DB point-in-time restore](continuous-backup-restore-resource-model.md)
* [Understanding multi-region writes in Azure Cosmos DB](multi-region-writes.md)
* [Understanding timestamps in Cosmos DB](multi-region-writes.md#understanding-timestamps)
* [Global data distribution with Azure Cosmos DB - under the hood](global-dist-under-the-hood.md)
