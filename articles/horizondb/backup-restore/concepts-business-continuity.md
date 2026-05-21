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

**Business continuity** in Azure HorizonDB refers to the mechanisms, policies, and procedures that enable applications and business processes to continue operating during and after disruptive events, particularly those that affect computing infrastructure.Azure HorizonDB is designed to automatically handle many types of failures within the cloud environment, helping maintain application availability and operational continuity. However, some scenarios require explicit user action or planning, including:

- Accidental data modifications or deletions (for example, a user deleting or updating rows in a table)
- Regional or zonal outages caused by events such as natural disasters
- Planned maintenance operations, such as patching to address bugs or security vulnerabilities

## Built-in resilience and protection
Azure HorizonDB provides a set of features designed to protect data and minimize downtime during both planned and unplanned events. These capabilities are built on Azure infrastructure, which offers high levels of resiliency and availability.
Business continuity features in Azure HorizonDB are designed to:

Provide additional fault protection beyond underlying infrastructure
Support defined recovery objectives
Reduce potential data loss exposure


The table below illustrates the features that Azure HorizonDB offers.

| **Feature** | **Description** | **Considerations** |
| ---------- | ----------- | ------------ |
| **Automatic backups** | Azure HorizonDB cluster automatically performs daily backups of your database files and continuously backs up transaction logs. Backups are retained from 7 days. You're able to restore your database server to any point in time within your backup retention period. The recovery time objective (RTO) for restore operations is primarily influenced by the time required to apply write-ahead log (WAL) recovery and is independent of the total size of the database being restored.For more information, see [Concepts - Backup and Restore](concepts-backup-restore.md). | Backup data remains within the region. |
| **Zone redundant high availability** | Azure HorizonDB need at least two replicas on the cluster to have zonal resilience. You can add or remove replicas to the Azure HorizonDB cluster as your workload needs it. | Protects against availability zone outages. |
| **Zone redundant backup** | Azure HorizonDB cluster backups are automatically and securely stored in a zone redundant storage within a region. |Protects against availability zone outages. |
| **Read Replicas** | Azure HorizonDB supports in region replicas which can be used to offload readonly workloads. Replicas also act as failover targets for primary cluster. | Supports up to 15 replicas. |

## Planned downtime events

Below are some planned maintenance scenarios. These events typically incur up to few minutes of downtime, and without data loss.

| **Scenario** | **Process**|
| ------------------- | ----------- | 
| <b>Compute scaling (User-initiated)| During compute scaling operation, active checkpoints are allowed to complete, client connections are drained, any uncommitted transactions are canceled, storage is detached, and then it's shut down. A new Azure HorizonDB cluster with the same database server name is provisioned with the scaled compute configuration. The storage is then attached to the new cluster and the database is started which performs recovery, if necessary, before accepting client connections. |
| <b>New software deployment (Azure-initiated) | New features rollout or bug fixes automatically happen as part of service’s planned maintenance. | 
| <b>Minor version upgrades (Azure-initiated) | Azure HorizonDB automatically patches database servers to the minor version determined by Azure. It happens as part of the service's planned maintenance. The database server is automatically restarted with the new minor version. You can also check your [portal](https://aka.ms/servicehealthpm).| 


##  Unplanned downtime mitigation

Unplanned downtime can occur due to unexpected events such as hardware failures, network issues, or software defects.If high availability (HA) is configured and the primary database server becomes unavailable, Azure HorizonDB automatically fails over to a standby replica, allowing client operations to resume with minimal interruption. If HA is not configured, and the initial restart attempt is unsuccessful, a new database server is automatically provisioned.Although unplanned downtime cannot be entirely prevented, Azure HorizonDB mitigates its impact by performing automated recovery operations without requiring manual intervention.

Though we continuously strive to provide high availability, there are times when Azure HorizonDB does incur outage causing unavailability of the databases and thus impacting your application. When our service monitoring detects issues that cause widespread connectivity errors, failures or performance issues, the service automatically declares an outage to keep you informed.

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
> As the name implies, temporary tablespaces in PostgreSQL are used for temporary objects, and other internal database operations, such as sorting. Therefore we don't recommend creating user schema objects in temporary tablespace, as we don't guarantee durability of such objects after Server restarts, HA failovers, etc.


> [!IMPORTANT]
> Currently,deleted servers can't be restored. Use Azure resource lock to help prevent accidental deletion of your server.



## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).


