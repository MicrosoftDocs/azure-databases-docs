---
title: Backup and restore in Azure HorizonDB Cluster
description: Learn about the concepts of backup and restore with Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 4/22/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
ms.custom:
  - build-2026
---

# Backup and restore in Azure HorizonDB

Backups form an essential part of any business continuity strategy. They help protect data from accidental corruption or deletion. 

Azure HorizonDB uses highly scalable storage and compute performance tiers. HorizonDB Backups are snapshot-based and complete nearly instantaneously, with no impact on database performance or service availability during backup operations. Transaction log backups are stored in Azure Storage and retained for the configured backup retention period.This enables point-in-time restore (PITR) within the specified retention window.

 Restore time primarily depends on the volume of transaction logs that must be replayed to reach the selected recovery point.

## Backup overview

Storage and compute separation enables HorizonDB to offload backup and restore operations to the storage layer, eliminating resource consumption on compute replicas. As a result, backups do not impact the performance of either primary or secondary compute replicas.

Backup and restore operations for HorizonDB databases are fast regardless of data size, because they use storage snapshots. 

## Point-in-time restore (PITR)

HorizonDB services restores a database to any point in time within the configured retention period using the following process:

1. Restores the most recent snapshot prior to the selected restore time.
2. Applies transaction logs from that snapshot forward to the desired restore point to ensure transactional consistency.

For example, if the latest snapshot is at 6 PM and the target restore time is 9 PM, the service restores the 6 PM snapshot and applies transaction logs generated between 6 PM and 9 PM.

Because restore operations are based on snapshots and log replay rather than full data movement, restore time is not dependent on database size. As a result, restoring a HorizonDB database within the same region typically completes in minutes, even for large multi-terabyte databases.

## Backup retention

The default backup retention period is 7 days. You can specify a backup retention period from 1–35 days. All backups are encrypted through AES 256-bit encryption for data stored at rest.

These backup files can't be exported or used to create servers outside your Azure HorizonDB flexible server instance. For that purpose, you can use the PostgreSQL tools pg_dump and pg_restore/psql.

## Backup frequency

Backups in Azure HorizonDB are snapshot-based. The first snapshot is taken immediately after the server is created. Subsequent snapshots are taken multiple times a day to enable faster recovery.

Transaction log backups occur at variable intervals based on workload activity. Logs are captured when the write-ahead log (WAL) is ready to be archived. This ensures a transactionally consistent database state and enables point-in-time restore within the configured retention period, with no data loss at the selected restore point (RPO = 0).




#### Monitor backup storage consumption

In Azure HorizonDB, automated backups store incremental changes to data pages along with transaction log backups, both retained for the duration of the configured retention window.


You can use the Backup Storage Used metric in the Azure portal to monitor the backup storage that a server consumes. The Backup Storage Used metric represents the sum of storage consumed by all the retained database backups and log backups, based on the backup retention period set for the server. 

You can use the Backup Storage Used metrics in the Azure portal to monitor the backup storage that a server consumes.In HorizonDB, Azure Monitor metrics report the following consumption information:

1. Data backup storage size (snapshot backup size).
2. Data storage size (allocated database size).
3. Log backup storage size (transaction log backup size).

To view backup and data storage metrics in the Azure portal, follow these steps:

Go to the HorizonDB cluster for which you want to monitor backup and data storage metrics.
In the Monitoring section, select the Metrics page.
From the Metric dropdown list, select the Data backup storage, Data storage size, and Log backup storage metrics with an appropriate aggregation rule.
<< Image here>>

## Reduce backup storage consumption

Backup storage consumption for a HorizonDB cluster depends on the retention period and workload type. Consider some of the following tuning techniques to reduce your backup storage consumption for a HorizonDB cluster:

Reduce the backup retention period to the minimum for your needs.
Avoid doing large write operations, such as vaccum and reindex, more frequently than you need to. 
For large data-load operations, consider using data compression when appropriate.

### Backup storage cost

Azure HorizonDB backup storage cost depends on the workload type.

Write-heavy workloads are more likely to change data pages frequently, which results in larger storage snapshots. Such workloads also generate more transaction logs, contributing to the overall backup costs. Backup storage is charged based on gigabytes consumed per month. The backup storage amount equal to the database size is provided at no extra charge. For pricing details, see the Azure SQL Database pricing page.

For HorizonDB, billable backup storage is calculated as follows:

Total billable backup storage size = ( Changes to Data pages + log backup storage size)

Data storage size isn't included in the billable backup because it's already billed as allocated database storage.

Deleted HorizonDB databases incur backup costs to support recovery to a point in time before deletion. For a deleted HoirzonDB database, billable backup storage is calculated as follows:

Total billable backup storage size for deleted HorizonDB database = (data storage size + data backup size + log backup storage size) * (remaining backup retention period after deletion / configured backup retention period)

Data storage size is included in the formula because allocated database storage isn't billed separately for a deleted database. For a deleted database, data is stored after deletion to enable recovery during the configured backup retention period.

>[!Note]
> The data backup storage size metric only reflects billable backup storage consumed beyond the free allowance of one full database size. The data backup storage size metric only emits a value after backup storage consumption exceeds the free tier.

Billable backup storage for a deleted database reduces gradually over time after it's deleted. It becomes zero when backups are no longer retained, and then recovery is no longer possible. If it's a permanent deletion and you no longer need backups, you can optimize costs by reducing retention before deleting the database.

#### Monitor backup costs
To understand backup storage costs:

In the Azure portal, go to Cost Management + Billing.

Select Cost Management > Cost analysis.

For Scope, select the desired subscription.

Filter for the time period and service you're interested in by following these steps:

Add a filter for Service name.
Choose sql-database from the dropdown list.
Add another filter for Meter.
To monitor backup costs for point-in-time recovery, select Data Stored - Backup - RA from the dropdown list.
The following screenshot shows an example cost analysis.

<< Image>>

> [!Note]
> Irrespective of the database size, heavy transactional activity on the server generates more WAL files. The increase in files in turn increases the backup storage.

## Point-in-time recovery

In an Azure HorizonDB flexible server instance, performing a PITR creates a new server in the same region as your source server, but you can choose the availability zone. It's created with the source server's configuration for the pricing tier, compute generation, number of virtual cores, storage size, backup retention period, and backup redundancy option. 

The physical database files are first restored from the snapshot backups to the server's data location. The appropriate backup that was taken earlier than the desired point in time is automatically chosen and restored. A recovery process then starts by using WAL files to bring the database to a consistent state. 

For example, assume that the backups are performed at 11:00 PM every night. If the restore point is for August 15 at 10:00 AM, the daily backup of August 14 is restored. The database will be recovered until 10:00 AM of August 15 by using the transaction log backup from August 14, 11:00 PM, to August 15, 10:00 AM. 

To restore your database server, see any of the following:
- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
- [Restore to full backup (fast restore)](how-to-restore-full-backup.md).


> [!IMPORTANT]
> A restore operation in your Azure HorizonDB flexible server instance always creates a new database server with the name that you provide. It doesn't overwrite the existing database server.

PITR is useful in scenarios like these:

- A user accidentally deletes data, a table, or a database.
- An application accidentally overwrites good data with bad data because of an application defect. 
- You want to clone your server for test, development, or for data verification.

With continuous backup of transaction logs, you can restore to the last transaction. You can choose between the following restore options:

-   **Latest restore point (now)**: This is the default option, which allows you to restore the server to the latest point in time. 

-   **Custom restore point**: This option allows you to choose any point in time within the retention period defined for this Azure HorizonDB flexible server instance. By default, the latest time in UTC is automatically selected. Automatic selection is useful if you want to restore to the last committed transaction for test purposes. You can optionally choose other days and times. 

-   **Fast restore point**: This option allows users to restore the server in the fastest time possible within the retention period defined for their Azure HorizonDB flexible server instance. Fastest restore is possible by directly choosing the timestamp from the list of backups. This restore operation provisions a server and simply restores the full snapshot backup and doesn't require any recovery of logs, which makes it fast. We recommend you select a backup timestamp, which is greater than the earliest restore point in time for a successful restore operation.

The time required to recover using the latest and custom restore point options varies based on factors such as the volume of transaction logs to process since the last backup and the total number of databases being recovered simultaneously in the same region The overall recovery time usually takes from few minutes up to a few hours.

If you configure your server within a virtual network, you can restore to the same virtual network or to a different virtual network. However, you can't restore to public access. Similarly, if you configured your server with public access, you can't restore to private virtual network access.


## Related content

- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
- [Restore to full backup (fast restore)](how-to-restore-full-backup.md).

