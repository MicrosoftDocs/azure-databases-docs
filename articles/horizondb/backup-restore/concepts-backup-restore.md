---
title: Backup and Restore in Azure HorizonDB Cluster
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

# Backups in Azure HorizonDB (Preview)

This article explains the automated backup feature in Azure HorizonDB.

Azure HorizonDB provides fully managed, built-in backups to protect data and support reliable recovery. Backups are performed automatically, with no manual configuration, or ongoing management required, allowing you to focus on your application while HorizonDB continuously safeguards your data.

## Backup overview

Azure HorizonDB backup operations are snapshot-based and complete near instantaneously, with no impact on database performance or service availability. In addition to snapshots, the service continuously archives write-ahead logs (WAL) to Azure Blob storage as transactions are committed. WAL archiving captures and persists database changes in near real time and doesn't require manual configuration. The snapshot and archiving process are managed by the storage layer and runs independently of the compute layer, reducing resource overhead and maintaining consistent performance for active workloads.

WAL archiving runs continuously in the background and doesn't impact query execution or application availability. WAL files are retained according to the configured backup retention policy. WAL archiving, combined with periodic snapshots, supports point-in-time restore (PITR), allowing the database to be restored to a specific time within the retention window. This supports recovery from scenarios such as data corruption, unintended changes, or operational incidents.

Backup and restore operations for HorizonDB databases are fast regardless of data size, because they use storage snapshots. During restore operations, the restored cluster inherits the backup retention period from the source snapshot of the cluster.

## Backup retention

The default backup retention period currently is 7 days. All backups are encrypted through Advanced Encryption Standard (AES) 256-bit encryption for data stored at rest.

Backups in Azure HorizonDB are snapshot-based. The first snapshot is taken immediately after the server is created. Subsequent snapshots are taken multiple times a day to enable faster recovery.

## Backup metrics

In Azure HorizonDB, automated backups capture incremental changes to data pages and transaction logs, which are both retained for the configured backup retention period.

You can use the Backup Storage Used metric in the Azure portal to monitor the backup storage that a server consumes. The Backup Storage Used metric represents the sum of storage consumed by all the retained database backups and log backups, based on the backup retention period set for the server.

In HorizonDB, Azure Monitor metrics report the following consumption information:

- Data backup storage size (snapshot backup size).
- Data storage size (allocated database size).
- Log backup storage size (transaction log backup size).

To view backup and data storage metrics in the Azure portal, follow these steps:

1. Go to the HorizonDB cluster for which you want to monitor backup and data storage metrics.
1. In the Monitoring section, select the Metrics page.
1. From the Metric dropdown list, select the Data backup storage, Data storage size, and Log backup storage metrics with an appropriate aggregation rule.

## Backup storage cost

Azure HorizonDB backup storage cost depends on the workload type.

Write-heavy workloads are more likely to change data pages frequently, which results in larger storage snapshots. Such workloads also generate more transaction logs, contributing to the overall backup costs. Backup storage is charged based on gigabytes consumed per month. The backup storage amount equal to the database size is provided at no extra charge. For pricing details, see the Azure HorizonDB pricing page.

For HorizonDB, billable backup storage is calculated as follows:

``` *Total billable backup storage size = (Changes to Data pages + WAL archive size)*```

Data storage size is excluded from billable backup storage because it is already billed as allocated database storage.

Deleted HorizonDB databases incur backup costs to support recovery to a point in time before deletion. For a deleted HorizonDB database, billable backup storage is calculated as follows:

``` *Total billable backup storage size for deleted HorizonDB database = (data storage size + data backup size + WAL archive size) * (remaining backup retention period after deletion / configured backup retention period)*```

Data storage size is included in the formula because allocated database storage isn't billed separately for a deleted database. For a deleted database, data is stored after deletion to enable recovery during the configured backup retention period.

Billable backup storage for a deleted database decreases over time after deletion, based on the remaining retention period. It becomes zero when backups are no longer retained, and then recovery is no longer possible. If it's a permanent deletion and you no longer need backups, you can optimize costs by reducing retention before deleting the database.

## Backup limitations

- Geo-redundant backups are currently not supported.
- Maximum backup retention currently supported is 7 days.
- Currently point-in-time restore is limited to 5 minutes before current timestamp. Select a restore point that is at least 5 minutes in the past.

> [!NOTE]  
> Irrespective of the database size, heavy transactional activity on the server generates more WAL files. The increase in files in turn increases the backup storage.

## Related content

- [Restore in Azure HorizonDB (Preview)](how-to-restore-custom-restore-point.md)
