---
title: Overview of business continuity in Azure HorizonDB
description: Learn about the concepts of business continuity with an Azure HorizonDB flexible server instance.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
ms.custom:
  - sfi-image-nochange
---

# Overview of business continuity in Azure HorizonDB

**Business continuity** in Azure HorizonDB refers to the mechanisms, policies, and procedures that enable your business to continue operating in the face of disruption, particularly to its computing infrastructure. In most of the cases, Azure HorizonDB handles disruptive events that might happen in the cloud environment and keep your applications and business processes running. However, there are some events that can't be handled automatically such as:

- User accidentally deletes or updates a row in a table.
- Earthquake causes a power outage and temporarily disables an availability zone or a region.
- Database patching required to fix a bug or security issue.

Azure HorizonDB provides features that protect data and mitigates downtime for your mission-critical databases during planned and unplanned downtime events. Built on top of the Azure infrastructure that offers robust resiliency and availability, Azure HorizonDB has business continuity features that provide another fault protection, address recovery time requirements, and reduce data loss exposure. As you architect your applications, you should consider the downtime tolerance - the recovery time objective (RTO), and data loss exposure - the recovery point objective (RPO). For example, your business-critical database requires stricter uptime than a test database.

The table below illustrates the features that Azure HorizonDB offers.
The table below illustrates the features that Azure Database for PostgreSQL offers.

| **Feature** | **Description** | **Considerations** |
| ---------- | ----------- | ------------ |
| **Automatic backups** | Azure HorizonDB cluster automatically performs daily backups of your database files and continuously backs up transaction logs. Backups can be retained from 7 days up to 35 days. You're able to restore your database server to any point in time within your backup retention period. RTO is dependent on the size of the data to restore + the time to perform log recovery. It can be from few minutes up to few hours. For more details, see [Concepts - Backup and Restore](concepts-backup-restore.md). | Backup data remains within the region. |
| **Zone redundant high availability** | Azure HorizonDB need atleast two replicas on the cluster to have zonal resilience.You can add or remove replicas to the Azure HorizonDB cluster as your workload needs it. |
| **Zone redundant backup** | Azure HorizonDB cluster backups are automatically and securely stored in a zone redundant storage within a region. |


### Service Outage

In the event of Azure HorizonDB cluster outage, you can see more details related to the outage in the following places:

* **Azure portal banner**: If your subscription is identified to be impacted, there will be an outage alert of a Service Issue in your Azure portal **Notifications**.
  
:::image type="content" source="./media/business-continuity/notification-service-issue-example.png" alt-text=" Screenshot showing notifications in Azure portal.":::

* **Help + support** or **Support + troubleshooting**: When you create support ticket from **Help + support** or **Support + troubleshooting**, there will be information about any issues impacting your resources. Select View outage details for more information and a summary of impact. There will also be an alert in the New support request page.
  
:::image type="content" source="./media/business-continuity/help-support-service-health-notification.png" alt-text=" Screenshot showing Help Support notifications in Azure portal.":::

*  **Service Help**: The **Service Health** page in the Azure portal contains information about Azure data center status globally. Search for "service health" in the search bar in the Azure portal, then view Service issues in the Active events category. You can also view the health of individual resources in the **Resource health** page of any resource under the Help menu. A sample screenshot of the Service Health page follows, with information about an active service issue in Southeast Asia.

:::image type="content" source="./media/business-continuity/service-health-service-issues-example-map.png" alt-text=" Screenshot showing service outage in Service Health portal.":::

*  **Email notification**: If you've set up alerts, an email notification will arrive when a service outage impacts your subscription and resource. The emails arrive from "azure-noreply@microsoft.com". The body of the email begins with "The activity log alert ... was triggered by a service issue for the Azure subscription...". For more information on service health alerts, see [Receive activity log alerts on Azure service notifications using Azure portal](/azure/service-health/alerts-activity-log-service-notifications-portal).


> [!IMPORTANT]
> As the name implies, temporary tablespaces in PostgreSQL are used for temporary objects, as well as other internal database operations, such as sorting. Therefore we do not recommend creating user schema objects in temporary tablespace, as we don't guarantee durability of such objects after Server restarts, HA failovers, etc.


### Unplanned downtime: failure scenarios and service recovery

Below are some unplanned failure scenarios and the recovery process. 

| **Scenario** | **Recovery process** <br> [Servers configured without zone-redundant HA]| **Recovery process** <br> [Servers configured with Zone-redundant HA] |
| ---------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------- |
| **Database server failure** | If the database server is down, Azure will attempt to restart the database server. If that fails, the database server will be restarted on another physical node.  <br /> <br /> The recovery time (RTO) is dependent on various factors including the activity at the time of fault, such as large transaction, and the volume of recovery to be performed during the database server startup process. <br /> <br /> Applications using the PostgreSQL databases need to be built in a way that they detect and retry dropped connections and failed transactions.                                                                                                                                                                  | If the database server failure is detected, the server is failed over to the standby server, thus reducing downtime. For more information, see [HA concepts page]/azure/reliability/reliability-postgresql-flexible-server. RTO is expected to be 60-120s, with zero data loss. |
| **Storage failure** | Applications don't see any impact for any storage-related issues such as a disk failure or a physical block corruption. As the data is stored in three copies, the copy of the data is served by the surviving storage. The corrupted data block is automatically repaired and a new copy of the data is automatically created. | For any rare and non-recoverable errors such as the entire storage is inaccessible, the Azure Database for PostgreSQL flexible server instance is failed over to the standby replica to reduce the downtime. For more information, see [HA concepts page]/azure/reliability/reliability-postgresql-flexible-server. |
| **Logical/user errors** | To recover from user errors, such as accidentally dropped tables or incorrectly updated data, you have to perform a [point-in-time recovery](../concepts-backup-restore.md) (PITR). While performing the restore operation, you specify the custom restore point, which is the time right before the error occurred.<br> <br>  If you want to restore only a subset of databases or specific tables rather than all databases in the database server, you can restore the database server in a new instance, export the table(s) via [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html), and then use [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) to restore those tables into your database. | These user errors aren't protected with high availability as all changes are replicated to the standby replica synchronously. You have to perform point-in-time restore to recover from such errors. |
| **Availability zone failure** | To recover from a zone-level failure, you can perform point-in-time restore using the backup and choosing a custom restore point with the latest time to restore the latest data. A new Azure Database for PostgreSQL flexible server instance is deployed in another non-impacted zone. The time taken to restore depends on the previous backup and the volume of transaction logs to recover. | An Azure Database for PostgreSQL flexible server instance is automatically failed over to the standby server within 60-120s with zero data loss. For more information, see [HA concepts page]/azure/reliability/reliability-postgresql-flexible-server. | 
| **Region failure** | If your server is configured with geo-redundant backup, you can perform geo-restore in the paired region. A new server will be provisioned and recovered to the last available data that was copied to this region. <br /> <br /> You can also use cross region read replicas. In the event of region failure you can perform disaster recovery operation by promoting your read replica to be a standalone read-writeable server. RPO is expected to be up to 5 minutes (data loss possible) except in the case of severe regional failure when the RPO can be close to the replication lag at the time of failure.                                                                                                               | Same process. |


### Configure your database after recovery from regional failure

* If you are using geo-restore or geo-replica to recover from an outage, you must make sure that the connectivity to the new server is properly configured so that the normal application function can be resumed. 
* If you've previously set up a diagnostic setting on the original server, make sure to do the same on the target server if necessary as explained in [Configure and Access Logs in Azure Database for PostgreSQL](../monitor/how-to-configure-and-access-logs.md).
* Setup telemetry alerts, you need to make sure your existing alert rule settings are updated to map to the new server. For more information about alert rules, see [Use the Azure portal to set up alerts on metrics for Azure Database for PostgreSQL](../monitor/how-to-alert-on-metrics.md).

> [!IMPORTANT]
> Deleted servers cannot be restored. Use Azure resource lock to help prevent accidental deletion of your server.



## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).


