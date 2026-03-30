---
title: Backup and Restore
description: Learn about the concepts of backup and restore with Azure Database for MySQL.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 03/27/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ms.custom:
  - reliability-horizontal-2026
---

# Backup and restore in Azure Database for MySQL

Azure Database for MySQL Flexible Server automatically creates server backups and securely stores them in local redundant storage within the region. Use backups to restore your server to a point in time. Backup and restore are essential parts of any business continuity strategy because they protect your data from accidental corruption or deletion.

## Backup overview

Azure Database for MySQL Flexible Server supports two types of backups to provide enhanced flexibility for maintaining backups of business-critical data.

### Automated backup

Azure Database for MySQL Flexible Server takes snapshot backups of the data files and stores them in local redundant storage. The server also backs up transaction logs and stores them in local redundant storage. These backups allow you to restore a server to any point in time within your configured backup retention period. The default backup retention period is seven days. You can optionally configure the database backup from 1 to 35 days. All backups use AES 256-bit encryption for the data stored at rest.

### On-demand backup

In addition to the automated backups, Azure Database for MySQL Flexible Server enables you to trigger on-demand backups of the production workload and store them in alignment with the server's backup retention policy. Use these backups as the fastest restore point to perform a point-in-time restore and reduce restore times by up to 90%. The default backup retention period is seven days. You can optionally configure the database backup from 1 to 35 days. You can trigger a total of 50 on-demand backups from the portal. All backups use AES 256-bit encryption for the data stored at rest.

You can't export these backup files. You can only use the backups for restore operations in Azure Database for MySQL Flexible Server. You can also use [mysqldump](../concepts-migrate-dump-restore.md#dump-and-restore-using-mysqldump-utility) from a MySQL client to copy a database.

## Backup frequency

Backups on Flexible Servers use snapshots. The first snapshot backup is scheduled right after you create a server. The system takes snapshot backups once a day. Transaction log backups happen every five minutes.

If a scheduled backup fails, the backup service tries every 20 minutes to take a backup until it succeeds. Heavy transactional production loads on the server instance can cause these backup failures.

To increase the frequency of automated daily backups, increase the backup interval. This change is especially helpful when you expect large transactions, as it significantly reduces restore time by reducing the number of binlogs that need to be replayed during a point-in-time restore operation. In a typical point-in-time restore (PITR) process, the system first restores data from the nearest full snapshot (taken daily) and then replays binary logs (captured every five minutes) to reach the exact restore time. If the target restore time is far from the snapshot, a large number of binlogs need to be replayed, which can significantly increase the restore duration. This new feature optimizes the process by introducing more frequent snapshots, which reduces the number of binlogs that need to be replayed and minimizes overall restore time.

The feature also comes with a new snapshot backup trimming logic that helps manage backups more efficiently by keeping all snapshots from the last 24 hours and only one snapshot per day for older backups. This logic ensures maximum flexibility and coverage for recent point-in-time restore (PITR) operations. At the same time, it helps optimize backup costs by ensuring that increasing the snapshot frequency doesn't significantly increase overall backup storage cost even if you set the back interval to a value other than 24 hours.

To change the backup interval, go to **Settings > Compute + Storage** and set the **Backup Interval** field. The default interval is 24 hours, but you can change it to 12 or 6 hours.

:::image type="content" source="media/concepts-backup-restore/configure-backup-interval.png" alt-text="Screenshot of modify backup frequency." lightbox="media/concepts-backup-restore/configure-backup-interval.png":::

> [!NOTE]  
> - If the server experiences a high transaction load, which results in larger and faster-growing binlog files, the backup service performs multiple backups per day to ensure reliable and quicker restoration by using these backups.
> - For 5.7 servers, long-running or large transactions can prevent global instance level lock acquisition, which is required for a successful daily backup. In such scenarios, daily backups can fail. To resolve this issue, either terminate the long-running transaction or restart the server. To ensure smoother operations, upgrade your MySQL 5.7 servers to version 8.0 by using a [major version upgrade](how-to-upgrade.md).

## Backup redundancy options

Azure Database for MySQL Flexible Server stores multiple copies of your backups so that your data is protected from planned and unplanned events. These events include transient hardware failures, network or power outages, and massive natural disasters. Azure Database for MySQL Flexible Server provides the flexibility to choose between locally redundant, zone-redundant, or geo-redundant backup storage in the Basic, General Purpose, and Memory-Optimized tiers. By default, Azure Database for MySQL Flexible Server uses locally redundant backup storage for servers with same-zone high availability (HA) or no high availability configuration, and it uses zone redundant backup storage for servers with zone-redundant HA configuration.

Backup redundancy ensures that your database meets its availability and durability targets even in the face of failures. Azure Database for MySQL Flexible Server offers three options:

- **Locally redundant backup storage** : When you use locally redundant backup storage, the system stores multiple copies of backups in the same datacenter. This option protects your data against server rack and drive failures. It also provides at least 99.999999999% (11 9's) durability of Backups objects over a given year. By default, the backup storage for servers with same-zone high availability (HA) or no high availability configuration is set to locally redundant.

- **Zone-redundant backup storage** : When you use zone-redundant backup storage, the system stores multiple copies within the availability zone in which your server is hosted. It also replicates backups to another availability zone in the same region. Use this option for scenarios that require high availability or for restricting replication of data to within a country or region to meet data residency requirements. It provides at least 99.9999999999% (12 9's) durability of Backups objects over a given year. Select the Zone-Redundant High Availability option at server creation time to ensure zone-redundant backup storage. You can disable High Availability for a server after creation, but the backup storage remains zone-redundant.

- **Geo-redundant backup storage** : When you use geo-redundant backup storage, the system stores multiple copies within the region in which your server is hosted. It also replicates backups to its geo-paired region. This option provides better protection and the ability to restore your server in a different region in the event of a disaster. It provides at least 99.99999999999999% (16 9's) durability of Backups objects over a given year. You can enable the Geo-Redundancy option at server creation time to ensure geo-redundant backup storage. Additionally, you can move from locally redundant storage to geo-redundant storage after server creation. Geo redundancy is supported for servers hosted in any of the [Azure paired regions](overview.md#azure-regions).

> [!NOTE]  
> The zone-redundant high availability option to support zone redundancy is currently available as a create time operation only. Currently, for a zone-redundant high availability server, you can enable or disable geo-redundancy only at server creation time.

<a id="moving-from-other-backup-storage-options-to-geo-redundant-backup-storage"></a>

## Move from other backup storage options to geo-redundant backup storage

To move your existing backup storage to geo-redundant storage, use the following methods:

- **Move from locally redundant to geo-redundant backup storage** - To move your backup storage from locally redundant storage to geo-redundant storage, change the Compute + Storage server configuration from the Azure portal to enable geo-redundancy for the locally redundant source server. You can also restore same zone redundant HA servers as a geo-redundant server in a similar fashion as the underlying backup storage is locally redundant for the same.

- **Move from zone-redundant to geo-redundant backup storage** - Azure Database for MySQL Flexible Server doesn't support conversion from zone-redundant storage to geo-redundant storage through Compute + Storage settings change after the server is provisioned. To move your backup storage from zone-redundant storage to geo-redundant storage, you have two options: a) Use PITR (point-in-time restore) to restore the server with the desired configuration. b) Create a new server with the desired configuration and migrate the data by using [dump and restore](../concepts-migrate-dump-restore.md).

## Backup retention

The server backup retention period setting determines how long to keep backups. You can select a retention period from 1 to 35 days, and the default retention period is seven days. Set the retention period during server creation or later by updating the backup configuration in the Azure portal.

The backup retention period determines how far back in time a point-in-time restore operation can go, since it's based on available backups. You can also think of the backup retention period as a recovery window from a restore perspective. The backup storage retains all backups required to perform a point-in-time restore within the backup retention period. For example, if you set the backup retention period to seven days, the recovery window is the last seven days. In this scenario, the backup storage retains all backups required to restore the server in the last seven days. With a backup retention window of seven days, database snapshots and transaction log backups are stored for the last eight days (one day prior to the window).

## Backup storage cost

Azure Database for MySQL Flexible Server provides up to 100% of your provisioned server storage as backup storage at no extra cost. You pay for any additional backup storage you use in GB per month. For example, if you provision a server with 250 GB of storage, you get 250 GB of storage for server backups at no extra charge. If the daily backup usage is 25 GB, you can have up to 10 days of free backup storage. You pay for storage consumed for backups that exceed 250 GB according to the [pricing model](https://azure.microsoft.com/pricing/details/mysql/).

To monitor the backup storage consumed by a server, use the [Monitor Azure Database for MySQL - Flexible Server](concepts-monitoring.md) metric in Azure Monitor available in the Azure portal. The **Backup Storage** used metric represents the sum of storage consumed by all the database backups and log backups retained based on the backup retention period set for the server. Heavy transactional activity on the server can cause backup storage usage to increase regardless of the total database size. Backup storage used for a geo-redundant server is twice that of a locally redundant server.

Set the appropriate backup retention period to control the backup storage cost. You can select a retention period between 1 and 35 days.

> [!IMPORTANT]  
> The primary database server handles backups for a database server configured in a zone redundant high availability configuration. The primary server has minimal overhead when using snapshot backups.

## View available full backups

The **Backup and Restore** page in the Azure portal provides a complete list of the full backups available to you at any given point in time. This list includes automated backups as well as the on-demand backups. Use this page to view the completion timestamps for all available full backups within the server's retention period and to perform restore operations by using these full backups. The list of available backups includes all full backups within the retention period, a timestamp that shows the successful completion, a timestamp that indicates how long a backup is retained, and a restore action.

## Restore

In Azure Database for MySQL Flexible Server, restoring creates a new server from the original server's backups. Two types of restore are available:

- **Point-in-time restore**: Available with either backup redundancy option. It creates a new server in the same region as your original server.
- **Geo-restore**: Available only if you configured your server for geo-redundant storage. It restores your server to either a geo-paired region or any other Azure supported region where Flexible Server is available.

Several factors affect the estimated time for the recovery of the server:

- The size of the databases
- The number of transaction logs involved
- The amount of activity that needs to be replayed to recover to the restore point
- The network bandwidth if the restore is to a different region
- The number of concurrent restore requests being processed in the target region
- The presence of primary key in the tables in the database. For faster recovery, consider adding primary key for all the tables in your database.

> [!NOTE]  
> After restore, a High Availability-enabled server becomes non-HA (High Availability disabled) for both point-in-time restore and geo-restore.

## Point-in-time restore

In Azure Database for MySQL Flexible Server, when you perform a point-in-time restore, you create a new server from the Flexible Server backups in the same region as your source server. The new server has the original server's configuration for the compute tier, number of vCores, storage size, backup retention period, and backup redundancy option. The restored server also inherits tags and settings such as virtual network and firewall from the source server. You can change the restored server's compute and storage tier, configuration, and security settings after the restore is complete.

> [!NOTE]  
> Two server parameters reset to default values and aren't copied from the primary server after the restore operation:
> - `time_zone` - This value sets to the default value `SYSTEM`.
> - `event_scheduler` - For MySQL version 5.7 servers, the server parameter `event_scheduler` is automatically turned `OFF` when backup is initiated, and server parameter `event_scheduler` is turned back `ON` after the backup completes successfully. In MySQL version 8.0 for Azure Database for MySQL - Flexible Server, the `event_scheduler` remains unaffected during backups. To ensure smoother operations, upgrade your MySQL 5.7 servers to version 8.0 by using a [major version upgrade](how-to-upgrade.md).

Point-in-time restore is useful in multiple scenarios. Some common use cases include:
- A user accidentally deletes data in the database.
- A user drops an important table or database.
- A user application accidentally overwrites good data with bad data due to an application defect.

You can choose between the latest restore point, a custom restore point, and the fastest restore point (restore by using full backup) through [Point-in-time restore in Azure Database for MySQL - Flexible Server with the Azure portal](how-to-restore-server-portal.md).

- **Latest restore point**: Restore the server to the timestamp when the restore operation was triggered. This option is useful to quickly restore the server to the most updated state.
- **Custom restore point**: Choose any point in time within the retention period defined for this server. This option is useful to restore the server at the precise point in time to recover from a user error.
- **Fastest restore point**: Restore the server in the fastest time possible for a given day within the retention period defined for the server. Fastest restore is possible by choosing the restore point-in-time at which the full backup is completed. This restore operation simply restores the full snapshot backup and doesn't warrant restore or recovery of logs, which makes it fast. Select a full backup timestamp that's greater than the earliest restore point in time for a successful restore operation.

The estimated time of recovery depends on several factors, including the database sizes, the transaction log backup size, the compute size of the SKU, and the time of the restore. The transaction log recovery is the most time-consuming part of the restore process. If you choose the restore time closer to the snapshot backup schedule, the restore operations are faster since transaction log application is minimal. To estimate the accurate recovery time for your server, test it in your environment as it has many environment-specific variables.

> [!IMPORTANT]  
> If you restore an Azure Database for MySQL Flexible Server instance configured with zone redundant high availability, the restored server is configured in the same region and zone as your primary server, and deployed as a single server in a non-HA mode. For more information, see [zone redundant high availability](concepts-high-availability.md) for Flexible Server.

> [!IMPORTANT]  
> You can recover a deleted Azure Database for MySQL Flexible Server resource within five days from the time of server deletion. For a detailed guide on how to restore a deleted server, [refer documented steps](how-to-restore-dropped-server.md). To protect server resources post deployment from accidental deletion or unexpected changes, administrators can use [management locks](/azure/azure-resource-manager/management/lock-resources).

## Geo-restore

If you configure your server to use geo-redundant backups, you can restore it to its [geo-paired region](overview.md#azure-regions), or any other Azure supported region where Azure Database for MySQL Flexible Server is available (except `Brazil South`, `USGov Virginia`, and `West US 3`). The ability to restore a geo-redundant backup to any region is known as "Universal Geo-restore".

Geo-restore is the default recovery option when an incident in the region where the server is hosted makes your server unavailable. If a large-scale incident in a region results in unavailability of your database application, you can restore a server from the geo-redundant backups to a server in any other region. Geo-restore uses the most recent backup of the server. There's a delay between when a backup is taken and when it's replicated to a different region. This delay can be up to an hour, so if a disaster occurs, there can be up to one hour data loss.

You can also perform geo-restore on a stopped server by using Azure CLI. To learn more, see [Point-in-time restore in Azure Database for MySQL - Flexible Server with Azure CLI](how-to-restore-server-cli.md).

The estimated time of recovery depends on several factors, including the database sizes, the transaction log size, the network bandwidth, and the total number of databases recovering in the same region at the same time.

> [!NOTE]  
> If you're geo-restoring an Azure Database for MySQL Flexible Server instance configured with zone redundant high availability, the restored server is configured in the geo-paired region and the same zone as your primary server. It's deployed as a single Azure Database for MySQL Flexible Server instance in a non-HA mode. For more information, see [zone redundant high availability](concepts-high-availability.md) for Azure Database for MySQL Flexible Server.

> [!IMPORTANT]  
> When the primary region is down, you can't create geo-redundant servers in the respective geo-paired region because storage can't be provisioned in the primary region. You must wait for the primary region to be up to provision geo-redundant servers in the geo-paired region.  
> When the primary region is down, you can still geo-restore the source server to the geo-paired region by disabling the geo-redundancy option in the **Compute + Storage Configure Server** settings in the restore portal experience. Restore as a locally redundant server to ensure business continuity.

## Perform post-restore tasks

After a restore from either **latest restore point** or **custom restore point** recovery mechanism, perform the following tasks to get your users and applications back up and running:

- If the new server replaces the original server, redirect clients and client applications to the new server.
- Ensure appropriate server-level firewall and virtual network rules are in place for users to connect.
- Ensure appropriate logins and database level permissions are in place.
- Configure alerts, as appropriate.

## Long-term retention (preview)

> [!NOTE]  
> The preview feature - "Long-term retention" solution for protection of Azure Database for MySQL flexible servers by using Azure Backup is currently paused. Don't configure any new backups until further notice. All existing backup data is safe and available for restore.

Azure Backup and Azure Database for MySQL Flexible Server services built an enterprise-class long-term backup solution for Azure Database for MySQL Flexible Server instances that retains backups for up to 10 years. You can use long-term retention independently or in addition to the automated backup solution offered by Azure Database for MySQL Flexible Server, which offers retention of up to 35 days. Automated backups are snapshot backups suited for operational recoveries, especially when you want to restore from the latest backups. Long-term backups help you with your compliance needs and auditing needs. In addition to long-term retention, the solution offers the following capabilities:

- Customer-controlled scheduled and on-demand backups
- Manage and monitor all the backup-related operations and jobs across servers, resource groups, locations, subscriptions, and tenants from a single pane of glass called the Backup Center.
- Backups are stored in separate security and fault domains. If the source server or subscription is compromised, the backups remain safe in the Backup vault (in Azure Backup managed storage accounts).

### Limitations and considerations

- In preview, LTR restore is currently available as RestoreasFiles to storage accounts. RestoreasServer capability will be added in the future.
- Support for LTR creation and management through Azure CLI isn't currently supported.

For more information about performing a long-term backup, see the [how-to guide](/azure/backup/backup-azure-mysql-flexible-server).

## Frequently Asked Questions (FAQs)

### Backup-related questions

- **How do I back up my server?**

  By default, Azure Database for MySQL Flexible Server enables automated backups of your entire server (encompassing all databases created) with a default seven-day retention period. You can also trigger a manual backup by using the On-Demand backup feature. Another way to manually take a backup is by using community tools such as `mysqldump` as documented [here](../concepts-migrate-dump-restore.md#dump-and-restore-using-mysqldump-utility) or `mydumper` as documented [here](../concepts-migrate-mydumper-myloader.md#create-a-backup-using-mydumper). If you want to back up an Azure Database for MySQL Flexible Server instance to a Blob storage, see the tech community blog [Backup Azure Database for MySQL Flexible Server to a Blob Storage](https://techcommunity.microsoft.com/blog/adformysql/backup-azure-database-for-mysql-to-a-blob-storage/803830).

- **Can I configure automatic backups to be retained for long term?**

  No, currently Azure Database for MySQL Flexible Server only supports up to 35 days of automated backup retention. You can take manual backups and use them for long-term retention.

- **What are the backup windows for my server? Can I customize them?**

  The first snapshot backup is scheduled immediately after a server is created. Snapshot backups are taken once daily. Transaction log backups occur every five minutes. Azure manages backup windows and you can't customize them.

- **Are my backups encrypted?**

  All Azure Database for MySQL Flexible Server data, backups, and temporary files created during query execution are encrypted by using AES 256-bit encryption. The storage encryption is always on and can't be disabled.

- **Can I restore a single or a few databases?**

  Restoring a single or a few databases or tables isn't supported. If you want to restore specific databases, perform a point-in-time restore and then extract the tables or databases needed.

- **Is my server available during the backup window?**

  Yes. Backups are online operations and are snapshot-based. The snapshot operation only takes a few seconds and doesn't interfere with production workloads, ensuring high availability of the server.

- **When I set up the maintenance window for the server, do I need to account for the backup window?**

  No, backups are triggered internally as part of the managed service and have no bearing on the Managed Maintenance Window.
- **Where are my automated backups stored and how do I manage their retention?**

  Azure Database for MySQL Flexible Server automatically creates server backups and stores them in user-configured, locally redundant storage or in geo-redundant storage. You can't export these backup files. The default backup retention period is seven days. You can optionally configure the database backup from 1 to 35 days.
- **How can I validate my backups?**

  The best way to validate availability of successfully completed backups is to view the full-automated backups taken within the retention period in the Backup and Restore blade. If a backup fails, it isn't listed in the available backups list, and the backup service tries every 20 minutes to take a backup until a successful backup is taken. These backup failures are due to heavy transactional production loads on the server.

- **Where can I see the backup usage?**

  In the Azure portal, under the Monitoring tab - Metrics section, you can find the [Monitor Azure Database for MySQL - Flexible Server](concepts-monitoring.md) metric, which can help you monitor the total backup usage.

- **What happens to my backups if I delete my server?**

  If you delete the server, all backups that belong to the server are also deleted and can't be recovered. To protect server resources post deployment from accidental deletion or unexpected changes, administrators can use [management locks](/azure/azure-resource-manager/management/lock-resources).
- **What happens to my backups when I restore a server?**

  If you restore a server, the operation always results in a creation of a new server that is restored by using the original server's backups. The old backup from the original server isn't copied over to the newly restored server and it remains with the original server. However, for the newly created server the first snapshot backup is scheduled immediately after a server is created and the service ensures daily automated backups are taken and stored as per configured server retention period.
- **How am I charged and billed for my use of backups?**

  Azure Database for MySQL Flexible Server provides up to 100% of your provisioned server storage as backup storage at no added cost. Any extra backup storage used is charged in GB per month as per the [pricing model](https://azure.microsoft.com/pricing/details/mysql/server/). Backup storage billing is also governed by the backup retention period selected and backup redundancy option chosen, apart from the transactional activity on the server, which impacts the total backup storage used directly.

- **How are backups retained for stopped servers?**

  No new backups are performed for stopped servers. The service retains all older backups (within the retention window) at the time of stopping the server until the server is restarted. After the server restarts, backup retention for the active server is governed by its backup retention window.
- **How am I billed for backups for a stopped server?**

  While your server instance is stopped, you're charged for provisioned storage (including provisioned IOPS) and backup storage (backups stored within your specified retention window). Free backup storage is limited to the size of your provisioned database and only applies to active servers.

- **How is my backup data protected?**

  Azure Database for MySQL Flexible Server protects your backup data by blocking any operations that could lead to loss of recovery points for the duration of the configured retention period. Backups taken during the retention period can only be read for the purpose of restoration and are deleted after the retention period. Also, all backups in Azure Database for MySQL Flexible Server are encrypted by using AES 256-bit encryption for the data stored at rest.

- **How does a Point-In-Time Restore (PITR) operation affect IOPS usage?**

  During a PITR operation in Azure Database for MySQL - Flexible Server, the service creates a new server and copies data from the source server's storage to the new server's storage. This process increases IOPS usage on the source server. This increase in IOPS usage is a normal occurrence and doesn't indicate any problems with the source server or the PITR operation. When the PITR operation finishes, IOPS usage on the source server returns to its usual levels.

### Restore-related questions

- **How do I restore my server?**
  The Azure portal supports point-in-time restore for all servers, so you can restore to the latest or a custom restore point. To manually restore your server from the backups created by `mysqldump` or MyDumper, see [Restore your database using myLoader](../concepts-migrate-mydumper-myloader.md#restore-your-database-using-myloader).

- **Why is my restore taking so much time?**

  Several factors affect the estimated time for the recovery of the server:
  - The size of the databases. As part of the recovery process, the database hydrates from the last physical backup. Therefore, the time taken to recover is proportional to the size of the database.
  - The active portion of transaction activity that the process needs to replay to recover. Recovery can take longer depending on the added transaction activity from the last successful checkpoint.
  - The network bandwidth if the restore is to a different region.
  - The number of concurrent restore requests being processed in the target region.
  - The presence of primary keys in the tables in the database. For faster recovery, consider adding primary keys for all the tables in your database.

- **Does modifying session-level database variables affect restoration?**

  Modifying session-level variables and running DML statements in a MySQL client session can affect the point-in-time restore (PITR) operation. These modifications don't get recorded in the binary log that the backup and restore operation uses. For example, [foreign_key_checks](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_foreign_key_checks) is a session-level variable. If you disable it to run a DML statement that violates the foreign key constraint, the point-in-time restore (PITR) operation fails. The only workaround in this scenario is to select a point-in-time restore (PITR) time earlier than the time at which [foreign_key_checks](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_foreign_key_checks) were disabled. Don't modify any session variables for a successful point-in-time restore (PITR) operation.

## Related content

- [business continuity](concepts-business-continuity.md)
- [zone redundant high availability](concepts-high-availability.md)
- [backup and recovery](concepts-backup-restore.md)
