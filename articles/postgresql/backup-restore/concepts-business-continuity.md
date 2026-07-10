---
title: Overview of Business Continuity in Azure Database for PostgreSQL Flexible Server
description: Business continuity in Azure Database for PostgreSQL flexible server helps you meet RTO and RPO goals. Explore backup, high availability, and recovery options.
#customer intent: As a user, I want to understand the business continuity features in Azure Database for PostgreSQL flexible server so that I can protect my data during planned and unplanned downtime events.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/05/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
ai-usage: ai-assisted
---

# Overview of business continuity in Azure Database for PostgreSQL flexible server

**Business continuity** in Azure Database for PostgreSQL refers to the mechanisms, policies, and procedures that enable your business to continue operating in the face of disruption, particularly to its computing infrastructure. In most cases, Azure Database for PostgreSQL handles disruptive events that might happen in the cloud environment and keeps your applications and business processes running. However, some events can't be handled automatically, such as:

- A user accidentally deletes or updates a row in a table.
- An earthquake causes a power outage and temporarily disables an availability zone or a region.
- Database patching required to fix a bug or security issue.

Azure Database for PostgreSQL provides features that protect data and mitigate downtime for your mission-critical databases during planned and unplanned downtime events. Built on top of the Azure infrastructure that offers robust resiliency and availability, Azure Database for PostgreSQL has business continuity features that provide another fault protection, address recovery time requirements, and reduce data loss exposure. As you architect your applications, consider the downtime tolerance - the recovery time objective (RTO), and data loss exposure - the recovery point objective (RPO). For example, your business-critical database requires stricter uptime than a test database.

The following table illustrates the features that Azure Database for PostgreSQL offers.

| **Feature** | **Description** | **Considerations** |
| ---------- | ----------- | ------------ |
| **Automatic backups** | An Azure Database for PostgreSQL flexible server instance automatically performs daily backups of your database files and continuously backs up transaction logs. You can retain backups from 7 days up to 35 days. You can restore your database server to any point in time within your backup retention period. RTO depends on the size of the data to restore plus the time to perform log recovery. It can be from a few minutes up to 12 hours. For more details, see [Concepts - Backup and Restore](concepts-backup-restore.md). |Backup data remains within the region. |
| **Zone redundant high availability** | You can deploy an Azure Database for PostgreSQL flexible server instance with zone redundant high availability (HA) configuration where primary and standby servers are deployed in two different availability zones within a region. This HA configuration protects your databases from zone-level failures and also helps reduce application downtime during planned and unplanned downtime events. Data from the primary server is replicated to the standby replica in synchronous mode. In the event of any disruption to the primary server, the server is automatically failed over to the standby replica. RTO in most cases is expected to be less than 120 seconds. RPO is expected to be zero (no data loss). For more information, see [Concepts - High availability](/azure/reliability/reliability-postgresql-flexible-server). | Supported in general purpose and memory optimized compute tiers. Available only in regions where multiple zones are available. |
| **Same zone high availability** | You can deploy an Azure Database for PostgreSQL flexible server instance with same zone high availability (HA) configuration where primary and standby servers are deployed in the same availability zone in a region. This HA configuration protects your databases from node-level failures and also helps reduce application downtime during planned and unplanned downtime events. Data from the primary server is replicated to the standby replica in synchronous mode. In the event of any disruption to the primary server, the server is automatically failed over to the standby replica. RTO in most cases is expected to be less than 120 seconds. RPO is expected to be zero (no data loss). For more information, see [Concepts - High availability]/azure/reliability/reliability-postgresql-flexible-server. | Supported in general purpose and memory optimized compute tiers. |
| **Premium-managed disks** | Database files are stored in a highly durable and reliable premium-managed storage. This storage provides data redundancy with three copies of the replica stored within an availability zone with automatic data recovery capabilities. For more information, see [Managed disks documentation](/azure/virtual-machines/managed-disks-overview). | Data stored within an availability zone. |
| **Zone redundant backup** | Azure Database for PostgreSQL flexible server instance backups are automatically and securely stored in a zone redundant storage within a region, if the region supports availability zones. During a zone-level failure where your server is provisioned, and if your server isn't configured with zone redundancy, you can still restore your database by using the latest restore point in a different zone. For more information, see [Concepts - Backup and Restore](concepts-backup-restore.md).| Only applicable in regions where multiple zones are available.|
| **Geo redundant backup** | Azure Database for PostgreSQL flexible server instance backups are copied to a remote region. This feature helps with disaster recovery situation in the event the primary server region is down. | This feature is currently enabled in selected regions. It takes a longer RTO and a higher RPO depending on the size of the data to restore and amount of recovery to perform.  |
| **Read Replica** | You can deploy cross region read replicas to protect your databases from region-level failures. Read replicas are updated asynchronously by using PostgreSQL's physical replication technology, and might lag the primary. For more information, see [Concepts - Read Replicas](../read-replica/concepts-read-replicas.md).| Supported in general purpose and memory optimized compute tiers. |


The following table compares RTO and RPO in a **typical workload** scenario:

| **Capability** | **Burstable** | **Production SKU (General Purpose/Memory Optimized)** |
| :------------: | :-------: | :------------------: |
| Point in Time Restore from backup | Any restore point within the retention period <br/> RTO - Varies <br/>RPO < 5 Minutes| Any restore point within the retention period <br/> RTO - Varies <br/>RPO < 5 Minutes |
| Geo-restore from geo-replicated backups | RTO - Varies <br/>RPO < 1 h  | RTO - Varies <br/>RPO < 1 h |
| Read replicas | Not Applicable | RTO - Minutes* <br/>RPO - Typically ranging from 30 secs to 5 Minutes* |
| High Availability | Not Applicable | RTO < 120 secs <br/> RPO = 0 |


## Planned downtime events

The following table describes some common planned maintenance scenarios. These events typically cause a few minutes of downtime, but they don't cause data loss.

| **Scenario** | **Process** |
| ------------------- | ----------- | 
| <b>Compute scaling (User-initiated)| During the compute scaling operation, the process allows active checkpoints to complete, drains client connections, cancels any uncommitted transactions, detaches storage, and then shuts down. The process provisions a new Azure Database for PostgreSQL flexible server instance with the same database server name but with the scaled compute configuration. The process attaches the storage to the new server and starts the database, which performs recovery if necessary before accepting client connections. |
| <b>Scaling up storage (User-initiated) | When you initiate a scaling up storage operation, the process allows active checkpoints to complete, drains client connections, and cancels any uncommitted transactions. After that, the process shuts down the server. The process scales the storage to the desired size and then attaches it to the new server. The process performs recovery if needed before accepting client connections. Note that scaling down of the storage size isn't supported. |
| <b>New software deployment (Azure-initiated) | The service automatically rolls out new features or bug fixes as part of planned maintenance. You can schedule when those activities happen. For more information, check your [portal](https://aka.ms/servicehealthpm). | 
| <b>Minor version upgrades (Azure-initiated) | Azure Database for PostgreSQL automatically patches database servers to the minor version determined by Azure. This patching happens as part of the service's planned maintenance. The process automatically restarts the database server with the new minor version. For more information, see [documentation](../concepts-monitoring.md#planned-maintenance-notification). You can also check your [portal](https://aka.ms/servicehealthpm).| 

When you configure the Azure Database for PostgreSQL flexible server instance with **high availability**, the service performs the scaling and the maintenance operations on the standby server first. For more information, see [Concepts - High availability]/azure/reliability/reliability-postgresql-flexible-server.

##  Unplanned downtime mitigation

Unplanned downtimes can occur as a result of unforeseen disruptions such as underlying hardware fault, networking issues, and software bugs. If the database server configured with high availability goes down unexpectedly, the service activates the standby replica and the clients can resume their operations. If you don't configure the server with high availability (HA), the service automatically provisions a new database server if the restart attempt fails. While you can't avoid unplanned downtime, Azure Database for PostgreSQL helps mitigate the downtime by automatically performing recovery operations without requiring human intervention. 

Though the engineering team continuously strives to provide high availability, there are times when Azure Database for PostgreSQL does incur an outage that causes unavailability of the databases and thus impacts your application. When the service monitoring detects issues that cause widespread connectivity errors, failures, or performance problems, the service automatically declares an outage to keep you informed.

### Service outage

If an Azure Database for PostgreSQL flexible server instance goes down, you can find more details about the outage in the following places:

* **Azure portal banner**: If your subscription is impacted, the Azure portal **Notifications** displays an outage alert for a service issue.
  
:::image type="content" source="./media/business-continuity/notification-service-issue-example.png" alt-text=" Screenshot showing notifications in Azure portal.":::

* **Help + support** or **Support + troubleshooting**: When you create a support ticket from **Help + support** or **Support + troubleshooting**, the portal includes information about any issues that impact your resources. Select **View outage details** for more information and a summary of impact. The **New support request** page also includes an alert.
  
:::image type="content" source="./media/business-continuity/help-support-service-health-notification.png" alt-text=" Screenshot showing Help Support notifications in Azure portal.":::

* **Service Health**: The **Service Health** page in the Azure portal contains information about Azure data center status globally. Search for "service health" in the search bar in the Azure portal, and then view service problems in the **Active events** category. You can also view the health of individual resources in the **Resource health** page of any resource under the **Help** menu. The following screenshot of the **Service Health** page shows information about an active service problem in Southeast Asia.

:::image type="content" source="./media/business-continuity/service-health-service-issues-example-map.png" alt-text=" Screenshot showing service outage in Service Health portal.":::

* **Email notification**: If you set up alerts, you receive an email notification when a service outage impacts your subscription and resource. The emails come from "azure-noreply@microsoft.com". The body of the email begins with "The activity log alert ... was triggered by a service issue for the Azure subscription...". For more information about service health alerts, see [Receive activity log alerts on Azure service notifications using Azure portal](/azure/service-health/alerts-activity-log-service-notifications-portal).


> [!IMPORTANT]
> As the name implies, temporary tablespaces in PostgreSQL are used for temporary objects, as well as other internal database operations, such as sorting. Therefore, don't create user schema objects in temporary tablespace, as durability of these objects after server restarts, HA failovers, and similar events isn't guaranteed.


### Unplanned downtime: failure scenarios and service recovery

The following table describes common unplanned failure scenarios and the recovery process. 

| **Scenario** | **Recovery process** <br> [Servers configured without zone-redundant HA]| **Recovery process** <br> [Servers configured with Zone-redundant HA] |
| ---------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------- |
| **Database server failure** | If the database server goes down, Azure attempts to restart the database server. If that attempt fails, Azure restarts the database server on another physical node.  <br /> <br /> The recovery time (RTO) depends on various factors, including the activity at the time of fault, such as a large transaction, and the volume of recovery to perform during the database server startup process. <br /> <br /> Applications that use the PostgreSQL databases need to detect and retry dropped connections and failed transactions.                                                                                                                                                                  | If the database server failure is detected, the server fails over to the standby server, which reduces downtime. For more information, see [HA concepts page]/azure/reliability/reliability-postgresql-flexible-server. RTO is expected to be 60-120 seconds, with zero data loss. |
| **Storage failure** | Applications don't see any impact from any storage-related issues such as a disk failure or a physical block corruption. Because the data is stored in three copies, the surviving storage serves the copy of the data. The corrupted data block is automatically repaired and a new copy of the data is automatically created. | For any rare and non-recoverable errors, such as when the entire storage is inaccessible, the Azure Database for PostgreSQL flexible server instance fails over to the standby replica to reduce the downtime. For more information, see [HA concepts page]/azure/reliability/reliability-postgresql-flexible-server. |
| **Logical or user errors** | To recover from user errors, such as accidentally dropped tables or incorrectly updated data, perform a [point-in-time recovery](../concepts-backup.md) (PITR). While performing the restore operation, specify the custom restore point, which is the time right before the error occurred.<br> <br>  If you want to restore only a subset of databases or specific tables rather than all databases in the database server, you can restore the database server in a new instance, export the tables via [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html), and then use [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) to restore those tables into your database. | These user errors aren't protected by high availability as all changes are replicated to the standby replica synchronously. You need to perform point-in-time restore to recover from such errors. |
| **Availability zone failure** | To recover from a zone-level failure, perform point-in-time restore using the backup and choose a custom restore point with the latest time to restore the latest data. Deploy a new Azure Database for PostgreSQL flexible server instance in another non-impacted zone. The time taken to restore depends on the previous backup and the volume of transaction logs to recover. | An Azure Database for PostgreSQL flexible server instance automatically fails over to the standby server within 60-120 seconds with zero data loss. For more information, see [HA concepts page]/azure/reliability/reliability-postgresql-flexible-server. | 
| **Region failure** | If your server is configured with geo-redundant backup, you can perform geo-restore in the paired region. Azure provisions and recovers a new server to the last available data that was copied to this region. <br /> <br /> You can also use cross region read replicas. In the event of region failure, you can perform disaster recovery operation by promoting your read replica to be a standalone read-writeable server. RPO is expected to be up to five minutes (data loss possible) except in the case of severe regional failure when the RPO can be close to the replication lag at the time of failure.                                                                                                               | Same process. |


### Configure your database after recovery from regional failure

* If you use geo-restore or geo-replica to recover from an outage, make sure that the connectivity to the new server is properly configured so that the normal application function can resume. Follow the [Post-restore tasks](concepts-backup-restore.md#geo-redundant-backup-and-restore).
* If you previously set up a diagnostic setting on the original server, make sure to do the same on the target server if necessary as explained in [Configure and Access Logs in Azure Database for PostgreSQL](../monitor/how-to-configure-and-access-logs.md).
* To set up telemetry alerts, make sure your existing alert rule settings are updated to map to the new server. For more information about alert rules, see [Use the Azure portal to set up alerts on metrics for Azure Database for PostgreSQL](../monitor/how-to-alert-on-metrics.md).

> [!IMPORTANT]
> You can restore deleted servers. If you delete the server, follow the guidance in [Restore a deleted server](how-to-restore-deleted-server.md) to recover. Use Azure resource lock to help prevent accidental deletion of your server.

## Related content

- [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server).
- [Restore to latest restore point](how-to-restore-latest-restore-point.md).
- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
- [Restore to full backup (fast restore)](how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](how-to-restore-paired-region.md).
