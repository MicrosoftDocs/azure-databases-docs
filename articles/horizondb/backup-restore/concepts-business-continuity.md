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

# Overview of business continuity in Azure HorizonDB (Preview)

**Business continuity** in Azure HorizonDB refers to the mechanisms, policies, and procedures that enable applications and business processes to continue operating during and after disruptive events, particularly those events that affect computing infrastructure. Azure HorizonDB is designed to automatically handle many types of failures within the cloud environment, helping maintain application availability and operational continuity. However, some scenarios require explicit user action or planning, including:

- Accidental data modifications or deletions (for example, a user deleting or updating rows in a table)
- Regional or zonal outages caused by events such as natural disasters
- Planned maintenance operations, such as patching to address bugs or security vulnerabilities

## Built-in resilience and protection
Azure HorizonDB provides a set of features designed to protect data and minimize downtime during both planned and unplanned events. These capabilities are built on Azure infrastructure, which offers high levels of resiliency and availability.
Business continuity features in Azure HorizonDB are designed to:

- Provide extra fault protection beyond underlying infrastructure
- Support defined recovery objectives
- Reduce potential data loss exposure


The table illustrates the features that Azure HorizonDB offers.

| **Feature** | **Description** | **Considerations** |
| ---------- | ----------- | ------------ |
| **Automatic backups** | Azure HorizonDB cluster automatically performs daily backups of your database files and continuously backs up transaction logs. Backups are retained from 7 days. You're able to restore your database server to any point in time within your backup retention period. The recovery time objective (RTO) for restore operations depends on the time required to complete  the write-ahead log (WAL) recovery and not on total data size. For more information, see [Concepts - Backup and Restore](concepts-backup-restore.md). | Backup data remains within the region. |
| **Zone redundant high availability** | Azure HorizonDB need at least two replicas on the cluster to have zonal resilience. You can add or remove replicas to the Azure HorizonDB cluster as your workload needs it. | Protects against availability zone outages. |
| **Zone redundant backup** | Azure HorizonDB cluster backups are automatically and securely stored in a zone redundant storage within a region. |Protects against availability zone outages. |
| **Read Replicas** | Azure HorizonDB supports in region replicas, which can be used to offload readonly workloads. Replicas also act as failover targets for primary cluster. | Supports up to 15 replicas. |

## Planned downtime events

Here are some planned maintenance scenarios. These events typically incur up to few minutes of downtime, and without data loss.

| **Scenario** | **Process**|
| ------------------- | ----------- | 
| <b>Compute scaling (User-initiated)| During a compute scaling operation, active checkpoints are allowed to complete. The service drains client connections, cancels any uncommitted transactions, detaches storage, and then shuts down the cluster.Azure HorizonDB then provisions a new compute with the same server name and the updated compute configuration. The service attaches the existing storage to the new cluster and starts the database. During startup, recovery runs if needed before the service accepts client connections. |
| <b>New software deployment (Azure-initiated) | New features rollout or bug fixes automatically happen as part of service’s planned maintenance. | 
| <b>Minor version upgrades (Azure-initiated) | Azure HorizonDB automatically patches database servers to the minor version determined by Azure. It happens as part of the service's planned maintenance. The database server is automatically restarted with the new minor version. You can also check your [portal](https://aka.ms/servicehealthpm).| 


##  Unplanned downtime mitigation

Unplanned downtime can occur due to unexpected events such as hardware failures, network issues, or software defects. If high availability (HA) is configured and the primary database server becomes unavailable, Azure HorizonDB automatically fails over to a standby replica. This process allows client operations to resume with minimal interruption. If HA isn't configured and the restart attempt fails, the service provisions a new database server. Although unplanned downtime can't be fully prevented, Azure HorizonDB reduces its impact by performing automated recovery operations without requiring manual intervention.

Though we continuously strive to provide high availability, there are times when Azure HorizonDB does incur outage causing unavailability of the databases and thus impacting your application. When our service monitoring detects issues that cause widespread connectivity errors, failures or performance issues, the service automatically declares an outage to keep you informed.

### Service Outage

In the event of Azure HorizonDB cluster outage, you can see more details related to the outage in the following places:

* **Azure portal banner**: If your subscription is affected, Azure posts a service issue alert in the **Notifications** section of the Azure portal.
  
:::image type="content" source="./media/business-continuity/notification-service-issue-example.png" alt-text=" Screenshot showing notifications in Azure portal.":::

* **Help + support** or **Support + troubleshooting**: When you create a support request from **Help + support** or **Support + troubleshooting**, Azure displays any known issues that impact your resources. Select View outage details to see more information and a summary of the impact. An alert also appears on the New support request page.
  
:::image type="content" source="./media/business-continuity/help-support-service-health-notification.png" alt-text=" Screenshot showing Help Support notifications in Azure portal.":::

*  **Service Help**: The **Service Health** page in the Azure portal provides a personalized view of the health status of Azure services across regions that affect your resources.To open the page, search for **Service Health** in the Azure portal. In the **Active events** section, review **Service issues** to see ongoing problems that affect your resources.You can also check the health of individual resources on the **Resource health** page for each resource under **Help**. The following example shows the **Service Health** page displaying an active service issue in Southeast Asia.

:::image type="content" source="./media/business-continuity/service-health-service-issues-example-map.png" alt-text=" Screenshot showing service outage in Service Health portal.":::

*  **Email notification**: f you configure alerts, Azure sends an email notification when a service outage affects your subscription or resources. The email is sent from "azure-noreply@microsoft.com"and includes details about the service issue. The email message begins with a standard notification indicating that an activity log alert was triggered by a service issue for your Azure subscription.For more information about service health alerts, see Azure Service Health documentation [Receive activity log alerts on Azure service notifications using Azure portal](/azure/service-health/alerts-activity-log-service-notifications-portal).


> [!IMPORTANT]
> Temporary tablespaces in PostgreSQL store temporary objects and support internal operations such as sorting. Do not create user schema objects in temporary tablespaces, because these objects might not persist after server restarts, high availability (HA) failovers, or similar events..


> [!IMPORTANT]
> Currently, deleted servers can't be restored. Use Azure resource lock to help prevent accidental deletion of your server.



## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).


