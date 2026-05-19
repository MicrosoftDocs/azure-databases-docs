---
title: Backup and restore in Azure HorizonDB Cluster
description: Learn about the concepts of backup and restore with Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
ms.custom:
  - build-2026
---

# Backups in Azure HorizonDB
This article explains the automated backup feature in Azure HorizonDB.


## Backup overview

Azure HorizonDB provides highly scalable storage and compute performance tiers. Backup operations are snapshot-based and complete near instantaneously, with no impact on database performance or service availability. In addition to snapshots, WAL is continuously archived to Azure Storage when the write-ahead log (WAL) file is ready to be archived. These logs are retained according to the configured backup retention period, enabling point-in-time restore (PITR) within the specified retention window.

Storage and compute separation enables HorizonDB to offload backup and restore operations to the storage layer, eliminating resource consumption on compute replicas. As a result, backups do not impact the performance of either primary or secondary compute replicas.

Backup and restore operations for HorizonDB databases are fast regardless of data size, because they use storage snapshots. During restore operations, you have the option to specify a backup retention period for your Azure HorizonDB cluster. When you don't explicitly set this value, the restored cluster inherits the backup retention period from the source snapshot of the cluster. 



## Backup retention

The default backup retention period is 7 days. You can specify a backup retention period from 7–35 days. All backups are encrypted through AES 256-bit encryption for data stored at rest.

Backups in Azure HorizonDB are snapshot-based. The first snapshot is taken immediately after the server is created. Subsequent snapshots are taken multiple times a day to enable faster recovery.

Transaction log backups occur at variable intervals based on workload activity. Logs are captured when the write-ahead log (WAL) is ready to be archived. This ensures a transactional consistent database state and enables point-in-time restore within the configured retention period, with no data loss at the selected restore point, allowing for a recovery point objective (RPO) of zero.

These backup files can't be exported or used to create servers outside your Azure HorizonDB cluster. For that purpose, you can use the PostgreSQL tools pg_dump and pg_restore/psql.


## Backup metrics

In Azure HorizonDB, automated backups store incremental changes to data pages along with transaction log backups, both retained for the duration of the configured retention window.


You can use the Backup Storage Used metric in the Azure portal to monitor the backup storage that a server consumes. The Backup Storage Used metric represents the sum of storage consumed by all the retained database backups and log backups, based on the backup retention period set for the server. 

In HorizonDB, Azure Monitor metrics report the following consumption information:

- Data backup storage size (snapshot backup size).
- Data storage size (allocated database size).
- Log backup storage size (transaction log backup size).

To view backup and data storage metrics in the Azure portal, follow these steps:

1. Go to the HorizonDB cluster for which you want to monitor backup and data storage metrics.
2. In the Monitoring section, select the Metrics page.
3. From the Metric dropdown list, select the Data backup storage, Data storage size, and Log backup storage metrics with an appropriate aggregation rule.


## Backup storage cost

Azure HorizonDB backup storage cost depends on the workload type.

Write-heavy workloads are more likely to change data pages frequently, which results in larger storage snapshots. Such workloads also generate more transaction logs, contributing to the overall backup costs. Backup storage is charged based on gigabytes consumed per month. The backup storage amount equal to the database size is provided at no extra charge. For pricing details, see the Azure HorizonDB pricing page.

For HorizonDB, billable backup storage is calculated as follows:

*Total billable backup storage size = (Changes to Data pages + log backup storage size)*

Data storage size isn't included in the billable backup because it's already billed as allocated database storage.

Deleted HorizonDB databases incur backup costs to support recovery to a point in time before deletion. For a deleted HoirzonDB database, billable backup storage is calculated as follows:

*Total billable backup storage size for deleted HorizonDB database = (data storage size + data backup size + log backup storage size) * (remaining backup retention period after deletion / configured backup retention period)*

Data storage size is included in the formula because allocated database storage isn't billed separately for a deleted database. For a deleted database, data is stored after deletion to enable recovery during the configured backup retention period.

Billable backup storage for a deleted database reduces gradually over time after it's deleted. It becomes zero when backups are no longer retained, and then recovery is no longer possible. If it's a permanent deletion and you no longer need backups, you can optimize costs by reducing retention before deleting the database.

> [!Note]
> The data backup storage size metric only reflects billable backup storage consumed beyond the free allowance of HoirzonDB cluster. The data backup storage size metric only emits a value after backup storage consumption exceeds the free tier.

Backup storage consumption for a HorizonDB cluster depends on the retention period and workload type. Consider some of the following tuning techniques to reduce your backup storage consumption for a HorizonDB cluster:

Reduce the backup retention period to the minimum for your needs.
Avoid doing large write operations, such as vacuum and reindex, more frequently than you need to. 


## Backup limitations

- Geo-redundant backups are currently not supported.
- Maximum backup retention currently supported is 7 days. 
- Point-in-time restore is limited to timestamps that are at least 300 seconds earlier than the current time. Select a restore point that is at least 5 minutes in the past.


> [!Note]
> Irrespective of the database size, heavy transactional activity on the server generates more WAL files. The increase in files in turn increases the backup storage.


## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
