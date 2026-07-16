---
title: Backup and Restore in Azure Database for PostgreSQL Flexible Server
description: Backup and restore in Azure Database for PostgreSQL flexible server keeps your data safe. Learn how automated backups and point-in-time recovery work.
#customer intent: As a user, I want to understand how automated backups work in Azure Database for PostgreSQL flexible server, so that I can rely on them for my business continuity strategy.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/05/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
ai-usage: ai-assisted
---

# Backup and restore in Azure Database for PostgreSQL flexible server

Backups are an essential part of any business continuity strategy. They help protect data from accidental corruption or deletion. 

Azure Database for PostgreSQL automatically performs regular backups of your server. You can then do a point-in-time recovery (PITR) within a retention period that you specify. The overall time to restore and recovery typically depends on the size of data and the amount of recovery to perform. 

## Backup overview

Azure Database for PostgreSQL takes snapshot backups of data files and stores them securely in zone-redundant storage or locally redundant storage, depending on the [region](../overview.md#azure-regions). The server also backs up transaction logs when the write-ahead log (WAL) file is ready to be archived. Use these backups to restore a server to any point in time within your configured backup retention period. 

The default backup retention period is seven days, but you can extend the period to a maximum of 35 days. All backups are encrypted through AES 256-bit encryption for data stored at rest.

You can't export these backup files or use them to create servers outside your Azure Database for PostgreSQL flexible server instance. For that purpose, you can use the PostgreSQL tools pg_dump and pg_restore/psql.

## Backup frequency

Backups on Azure Database for PostgreSQL flexible server instances are snapshot based. The first snapshot backup is scheduled immediately after a server is created. Snapshot backups are currently taken once daily. If you don't make any further modifications to any databases on the server after the last snapshot backup, the system temporarily suspends snapshot backups. As soon as you modify any database on the server, the system immediately takes a new snapshot to capture the latest changes. **The first snapshot is a full backup and consecutive snapshots are differential backups.**

Transaction log backups happen at varied frequencies, depending on the workload and when the WAL file is filled and ready to be archived. In general, the delay RPO (recovery point objective) can be up to five minutes.

## Backup redundancy options

Azure Database for PostgreSQL stores multiple copies of your backups to help protect your data from planned and unplanned events. These events can include transient hardware failures, network or power outages, and natural disasters. Backup redundancy helps ensure that your database meets its availability and durability targets, even if failures happen. 

Azure Database for PostgreSQL offers three options: 

- **Zone-redundant backup storage**: Azure Database for PostgreSQL automatically selects this option for regions that support availability zones. When you store backups in zone-redundant backup storage, the service keeps three copies of the data within the availability zone where your server is hosted. Additionally, the service replicates the data to another availability zone for added protection. 

  This option provides backup data availability across availability zones and restricts replication of data to within a country or region to meet data residency requirements. It provides at least 99.9999999999 percent (12 nines) durability of backup objects over a year.  

- **Locally redundant backup storage**: Azure Database for PostgreSQL automatically selects this option for regions that don't support availability zones yet. When you store backups in locally redundant backup storage, the service stores multiple copies of backups in the same datacenter. 

  This option helps protect your data against server rack and drive failures. It provides at least 99.999999999 percent (11 nines) durability of backup objects over a year. 
  
  By default, the service sets backup storage for servers with same-zone high availability (HA) or no high-availability configuration to locally redundant. 

- **Geo-redundant backup storage**: You can choose this option at the time of server creation. When you store backups in geo-redundant backup storage, in addition to three copies of data stored within the region where your server is hosted, the service replicates the data to a geo-paired region. 

  This option allows you to restore your server in a different region in the event of a disaster. It also provides at least 99.99999999999999 percent (16 nines) durability of backup objects over a year. 
  
  Geo-redundancy is supported for servers hosted in any of the [Azure paired regions](/azure/reliability/cross-region-replication-azure). 

## Moving from other backup storage options to geo-redundant backup storage 

You can configure geo-redundant storage for backup only during server creation. After a server is provisioned, you can't change the backup storage redundancy option.  

### Backup retention

The server retains backups based on the retention period that you set. You can select a retention period between 7 (default) and 35 days. Set the retention period during server creation or change it later. The server retains backups even for stopped servers.

The backup retention period determines the timeframe for retrieving a point-in-time restore (PITR) from the available backups. You can also consider the backup retention period as a recovery window from a restore perspective. 

The backup storage retains all backups required to perform a PITR within the backup retention period. For example, if you set the backup retention period to 7 days, the recovery window is the last 7 days. In this scenario, the backup storage retains all the data and logs that are required to restore and recover the server in the last 7 days. 

### Backup storage cost

Azure Database for PostgreSQL provides up to 100 percent of your provisioned server storage as backup storage at no extra cost. You pay for any extra backup storage that you use in gigabytes per month. 

For example, if you provision a server with 250 gibibytes (GiB) of storage, you get 250 GiB of backup storage capacity at no extra charge. If the daily backup usage is 25 GiB, you can have up to 10 days of free backup storage. You pay for backup storage consumption that exceeds 250 GiB as defined in the [pricing model](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/).

If you configure your server with geo-redundant backup, the backup data is also copied to the Azure paired region. So, your backup size is twice the size of the local backup copy. Billing is calculated as *((2 x local backup size) - provisioned storage size) x price @ gigabytes per month*. 

Use the [Backup Storage Used](../concepts-monitoring.md) metric in the Azure portal to monitor the backup storage that a server consumes. The Backup Storage Used metric represents the sum of storage consumed by all the retained database backups and log backups, based on the backup retention period set for the server. 

>[!Note]
> Irrespective of the database size, heavy transactional activity on the server generates more WAL files. The increase in files in turn increases the backup storage.

## Point-in-time recovery

In an Azure Database for PostgreSQL flexible server instance, performing a PITR creates a new server in the same region as your source server, but you can choose the availability zone. It's created with the source server's configuration for the pricing tier, compute generation, number of virtual cores, storage size, backup retention period, and backup redundancy option. 

The physical database files are first restored from the snapshot backups to the server's data location. The appropriate backup that was taken earlier than the desired point in time is automatically chosen and restored. A recovery process then starts by using WAL files to bring the database to a consistent state. 

For example, assume that the backups are performed at 11:00 PM every night. If the restore point is for August 15 at 10:00 AM, the daily backup of August 14 is restored. The database is recovered until 10:00 AM of August 15 by using the transaction log backup from August 14, 11:00 PM, to August 15, 10:00 AM. 

To restore your database server, see any of the following:
- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
- [Restore to full backup (fast restore)](how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).

> [!IMPORTANT]
> A restore operation in your Azure Database for PostgreSQL flexible server instance always creates a new database server with the name that you provide. It doesn't overwrite the existing database server.

PITR is useful in scenarios like these:

- A user accidentally deletes data, a table, or a database.
- An application accidentally overwrites good data with bad data because of an application defect. 
- You want to clone your server for test, development, or for data verification.

By using continuous backup of transaction logs, you can restore to the last transaction. You can choose between the following restore options:

-   **Latest restore point (now)**: This is the default option, which restores the server to the latest point in time. 

-   **Custom restore point**: This option allows you to choose any point in time within the retention period defined for this Azure Database for PostgreSQL flexible server instance. By default, the latest time in UTC is automatically selected. Automatic selection is useful if you want to restore to the last committed transaction for test purposes. You can optionally choose other days and times. 

-   **Fast restore point**: This option restores the server in the fastest time possible within the retention period defined for their Azure Database for PostgreSQL flexible server instance. Fastest restore is possible by directly choosing the timestamp from the list of backups. This restore operation provisions a server and simply restores the full snapshot backup. It doesn't require any recovery of logs, which makes it fast. Select a backup timestamp that's greater than the earliest restore point in time for a successful restore operation.

The time required to recover by using the latest and custom restore point options varies based on factors such as the volume of transaction logs to process since the last backup and the total number of databases being recovered simultaneously in the same region. The overall recovery time usually takes from few minutes up to a few hours.

If you configure your server within a virtual network, you can restore to the same virtual network or to a different virtual network. However, you can't restore to public access. Similarly, if you configured your server with public access, you can't restore to private virtual network access.

> [!IMPORTANT]
> You can restore deleted servers. If you delete the server, follow the guidance in [Restore a deleted server](how-to-restore-deleted-server.md) to recover. Use Azure resource lock to help prevent accidental deletion of your server.


## Geo-redundant backup and restore

To enable geo-redundant backup from the **Compute + storage** pane in the Azure portal, see [Create an Azure Database for PostgreSQL](../configure-maintain/../configure-maintain/quickstart-create-server.md). 

>[!IMPORTANT]
> You can configure geo-redundant backup only when you create the server. 

After you configure your server with geo-redundant backup, you can restore it to a [geo-paired region](/azure/reliability/cross-region-replication-azure). For more information, see the [supported regions](../overview.md#azure-regions) for geo-redundant backup.

When you configure the server with geo-redundant backup, the backup data and transaction logs are copied to the paired region asynchronously through storage replication. After you create a server, wait at least one hour before initiating a geo-restore. That wait period allows the first set of backup data to replicate to the paired region. 

Later, the transaction logs and the daily backups are asynchronously copied to the paired region. There might be up to one hour of delay in data transmission. So, you can expect up to one hour of RPO when you restore. You can restore only to the last available backup data that's available at the paired region. Currently, PITR of geo-redundant backups isn't available.

The estimated time to recover the server RTO (recovery time objective) depends on factors like the size of the database, the last database backup time, and the amount of WAL to process until the last received backup data. The overall recovery time usually takes from a few minutes up to a few hours.

During the geo-restore, you can change the server configurations that include virtual network settings and the ability to remove geo-redundant backup from the restored server. Changing other server configurations -such as compute, storage, or pricing tier (Burstable, General Purpose, or Memory Optimized)- isn't supported during geo-restore.

For more information, see the [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).

> [!IMPORTANT]
> When the primary region is down, you can't create geo-redundant servers in the respective geo-paired region, because storage can't be provisioned in the primary region. Before you can provision geo-redundant servers in the geo-paired region, you must wait for the primary region to be up. 
>
> With the primary region down, you can still geo-restore the source server to the geo-paired region. For more information, see the [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).
> Use geo-replicas as your disaster recovery (DR) strategy if you need to configure DR to any region, or if the primary region doesn't support geo-redundant backups.
> 
> Use virtual endpoints for your mission critical workloads, as they provide a stable connection point for applications, ensuring minimal disruption. If you have a virtual endpoint mapped to your primary server, remove the virtual endpoint from the primary server. Once removed, add the same virtual endpoint to the newly created server. This process ensures application connectivity remains consistent and minimizes downtime. For more information, see the [using virtual endpoints for consistent hostname during PITR](../read-replica/../read-replica/../read-replica/concepts-read-replicas-virtual-endpoints.md#use-virtual-endpoints-for-consistent-hostname-during-point-in-time-recovery-pitr-or-snapshot-restore).

## Restore and networking

### Point-in-time recovery

If you configure your source server with a *public access* network, you can only restore to public access. 

If you configure your source server with a *private access* virtual network, you can restore either to the same virtual network or to a different virtual network. You can't perform PITR across public and private access.

### Geo-restore

If you configure your source server with a *public access* network, you can only restore to public access. Also, you must apply firewall rules after the restore operation is complete.

If you configure your source server with a *private access* virtual network, you can only restore to a different virtual network, because virtual networks can't span regions. You can't perform geo-restore across public and private access.

## Post-restore tasks

After restoring the server, perform the following tasks to get your users and applications back up and running:

- If the new server replaces the original server, redirect clients and client applications to the new server. Change the server name of your connection string to point to the new server.

- The values of all [parameters](../parameters/concepts-parameters.md) on the original server aren't automatically applied to the new server. Ensure that you reconfigure all parameters on the new server according to the requirements of that new server.

- Ensure that appropriate server-level firewall rules, private endpoints, and virtual network rules are in place for user connections. These rules aren't copied from the original server.
  
- Scale up or scale down the restored server's compute as needed.

- Ensure that appropriate logins and database-level permissions are in place.

- Configure alerts as appropriate.
  
- If the source server from which you restored was configured with high availability, and you want to configure the restored server with high availability, follow [these steps](../high-availability/how-to-configure-high-availability.md).

- If the source server from which you restored was configured with read replicas, and you want to configure read replicas on the restored server, follow the instructions in [Create a read replica](../read-replica/how-to-create-read-replica.md).
 
## On-demand backups

Your Azure Database for PostgreSQL flexible server instance automatically generates storage volume snapshots of your entire database instance, covering all databases, as part of its scheduled backups. Additionally, you can create an on-demand backup whenever needed. This option is ideal for scenarios such as preparing for a potentially risky operation or performing periodic refreshes outside the usual backup schedule.

Take on-demand backups in addition to scheduled automatic backups. The backup retention window determines how long to keep these backups. You can delete on-demand backups at any time if they're no longer needed. To initiate an on-demand backup, select the database instance you wish to back up and specify a backup name. These backups are stored alongside automated backups, but only users can delete on-demand backups. The service manages and retains automated backups to meet backup retention requirements.

 For more information, see [Perform on-demand backups](how-to-perform-backups.md).

#### Limitations

- The Burstable server compute tier doesn't support the on-demand backup feature.
- The SSDv2 storage tier doesn't support the on-demand backup feature.
- You can take up to seven on-demand backups per flexible server instance. The backup retention window determines how long to keep these backups. 


## Long-term retention

Azure Backup and Azure Database for PostgreSQL services provide an enterprise-class long-term backup solution for Azure Database for PostgreSQL flexible server instances that retains backups for up to 10 years. You can use long-term retention (LTR) independently or alongside the automated backup solution offered by Azure Database for PostgreSQL, which offers retention of up to 35 days. Automated backups are physical backups suited for operational recoveries, especially when you want to restore from the latest backups. Long-term backups help you meet your compliance needs, are more granular, and are taken as logical backups using native pg_dump. In addition to long-term retention, the solution offers the following capabilities:

-	Customer-controlled scheduled and on-demand backups at the individual database level.
-	Central monitoring of all operations and jobs.
- Backups are stored in separate security and fault domains. If the source server or subscription is compromised, the backups remain safe in the Backup vault (in Azure Backup managed storage accounts).
- Using pg_dump provides greater flexibility in restoring data across different database versions.
-	Azure backup vaults support immutability and soft delete (preview) features, protecting your data.
-	LTR backup support for CMK-enabled servers.

#### Limitations and considerations

- Test your LTR backup and restore immediately after configuration to ensure they meet your business requirements.
- LTR restores are currently available only as **Restore as Files** to storage accounts, with **Restore as Server** capability planned for the future.
- LTR backs up all databases in flexible server instances, and you can't select individual databases for LTR configuration.
- LTR backup isn't supported on replicas, but you can perform it on primary servers.
- The maximum supported database size for Long-Term Retention (LTR) backups is 1 TiB.
- You can schedule LTR backups weekly, monthly, or yearly. The daily backup schedule isn't currently supported.
- LTR backups don't support tables containing a row with a BYTEA length exceeding 500 MB.
- When restoring roles for Microsoft Entra users, ensure that Microsoft Entra authentication is enabled and that you're signed in as a Microsoft Entra Admin to create additional users. Attempting to create Entra roles as a regular user results in errors.
  


For more information about performing a long term backup, see the [how-to guide](/azure/backup/backup-azure-database-postgresql-flex).

## Frequently asked questions

### Backup-related questions

* **How does Azure handle backup of my server?**
 
    By default, Azure Database for PostgreSQL enables automated backups of your entire server (encompassing all databases created) with a default retention period of seven days. The automated backups include a daily incremental snapshot of the database. The log (WAL) files are archived to Azure Blob Storage continuously.

* **Can I configure automated backups to retain data for the long term?**
  
    No. Currently, Azure Database for PostgreSQL supports a maximum of 35 days of retention. Use manual backups for a long-term retention requirement by using Azure Backup.

* **How do I manually back up my Azure Database for PostgreSQL flexible server instances?**
  
    You can manually take a physical snapshot by using the on-demand backup feature. You can also take logical backups by using the PostgreSQL tool [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html). For examples, see [Migrate your Azure Database for PostgreSQL database by using dump and restore](../howto-migrate-using-dump-and-restore.md). 
    
    
* **What are the backup windows for my server? Can I customize them?**
  
    Azure manages backup windows, and you can't customize them. The first full snapshot backup is scheduled immediately after a server is created. Subsequent snapshot backups are incremental and occur once a day.

* **Are my backups encrypted?**
  
    Yes. All Azure Database for PostgreSQL flexible server instance data, backups, and temporary files that are created during query execution are encrypted through  AES (Advanced Encryption Standard) 256-bit encryption. Storage encryption is always on and can't be disabled. 

* **Can I restore a single database or a few databases in a server?**
  
    Restoring a single database or a few databases or tables isn't directly supported. However, you can restore the entire server to a new server, and then drop tables or databases that you don't need on the new server.

* **Is my server available while a backup is in progress?**

    Yes. Backups are online operations that use snapshots. The snapshot operation takes only a few seconds and doesn't interfere with production workloads, to help ensure high availability of the server. 

* **When I'm setting up the maintenance window for the server, do I need to account for the backup window?**
  
    No. Backups are triggered internally as part of the managed service and have no bearing on the maintenance window.

* **Where are my automated backups stored, and how do I manage their retention?**
  
    Your Azure Database for PostgreSQL flexible server instance automatically creates server backups and stores them in:
    
    - Zone-redundant storage, in regions where multiple zones are supported.
    - Locally redundant storage, in regions that don't support multiple zones yet. 
    - The paired region, if you configure  geo-redundant backup.
    
    You can't export these backup files as they're stored in Microsoft-managed storage accounts. You have read-only access to restore these files but can't modify or delete them. The backup files are automatically deleted after the retention period.
    
    You can use backups to restore your server to a point in time only. The default backup retention period is seven days. You can optionally configure the backup retention up to 35 days. 

* **With geo-redundant backup, how often is the backup copied to the paired region?**  

    When you configure the server with geo-redundant backup, the backup data is stored in a geo-redundant storage account. The storage account copies data files to the paired region when the daily backup occurs at the primary server. WAL files are backed up when they're ready to be archived. 
    
    Backup data is asynchronously copied in a continuous manner to the paired region. You can expect up to one hour of delay in receiving backup data.

* **Can I do PITR at the remote region?**
  
    No. The data is recovered to the last available backup data at the remote region.

* **How are backups performed in a HA-enabled servers?**
  
    Data volumes in an Azure Database for PostgreSQL flexible server instance are backed up through managed disk incremental snapshots from the primary server. The WAL backup is performed from either the primary server or the standby server.

* **How can I validate that backups are performed on my server?**

    The best way to check backups is to perform periodic PITR and ensure that backups are valid and restorable. Backup operations or files aren't exposed to end users.

* **Where can I see the backup usage?**
  
    In the Azure portal, under **Monitoring**, select **Metrics**. In **Backup Storage Used**, you can monitor the total backup usage.

* **What happens to my backups if I delete my server?**
  
    If you delete a server, all backups that belong to the server are also deleted and can't be recovered. To help protect server resources from accidental deletion or unexpected changes after deployment, administrators can use management locks.

* **How are backups retained for stopped servers?**

    No new backups are performed for stopped servers. The service retains all older backups (within the retention window) at the time of stopping the server until the server is restarted. After that, backup retention for the active server is governed by its retention window.

* **How am I charged and billed for my backups?**
  
    Azure Database for PostgreSQL provides up to 100 percent of your provisioned server storage as backup storage at no extra cost. You pay for any additional backup storage you use, which is charged in gigabytes per month, as defined in the pricing model. 
    
    The backup retention period and backup redundancy option that you select, along with transactional activity on the server, directly affect the total backup storage and billing.

* **How am I billed for a stopped server?**
  
    While your server instance is stopped, no new backups are performed. You pay for provisioned storage and backup storage (backups stored within your specified retention window). 
    
    Free backup storage is limited to the size of your provisioned database. You pay for any excess backup data according to the backup price.

* **I configured my server with zone-redundant high availability. Do you take two backups, and will I be charged twice?**
  
    No. Irrespective of HA or non-HA servers, the service maintains only one set of backup copies. You pay only once.

### Restore-related questions

* **How do I restore my server?**

    Azure supports PITR for all servers. You can restore to the latest restore point or a custom restore point by using the Azure portal, the Azure CLI, and the API. 

    To restore your server from manual backups by using tools like `pg_dump`, you can first create an Azure Database for PostgreSQL flexible server instance and then restore your databases to the server by using [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html).

* **Can I restore to another availability zone within the same region?**
  
    Yes. If the region supports multiple availability zones, the backup is stored on a zone-redundant storage account so that you can restore to another zone. 

* **How long does a PITR take? Why is my restore taking so much time?**
  
    The data restore operation from a snapshot doesn't depend on the size of data. But the recovery process timing that applies the logs (transaction activities to replay) might vary, depending on the previous backup of the requested date and time and the number of logs to process. This condition applies to both restoring within the same zone and restoring data to a different zone. 
 
* **If I restore my HA-enabled server, is the restore server automatically configured with high availability?**
  
    No. The server is restored as a single-instance Azure Database for PostgreSQL flexible server instance. After the restore is complete, you can optionally configure the server with high availability.

* **I configured my server within a virtual network. Can I restore to another virtual network?**
  
    Yes. At the time of restore, choose a different virtual network to restore to.

* **Can I restore my public access server to a virtual network or vice versa?**

    No. Azure Database for PostgreSQL currently doesn't support restoring servers across public and private access.

* **How do I track my restore operation?**
  
    Currently, there's no way to track the restore operation. You can monitor the activity log to see if the operation is in progress or complete.

## Related content

- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
- [Restore to full backup (fast restore)](how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).
