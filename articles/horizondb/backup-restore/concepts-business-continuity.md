---
title: Overview of Business Continuity in Azure HorizonDB
description: Learn about the concepts of business continuity with an Azure HorizonDB.
#customer intent: As a user, I want to understand the business continuity features in Azure HorizonDB, so that I can plan for application availability during disruptive events.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: backup-restore
ms.topic: concept-article
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

The following table illustrates the features that Azure HorizonDB offers.

| **Feature** | **Description** | **Considerations** |
| --- | --- | --- |
| **Automatic backups** | Azure HorizonDB cluster automatically performs daily backups of your database files and continuously archives write-ahead log (WAL). Backups are currently retained for seven days. You can restore your database server to any point in time within your backup retention period. The recovery time objective (RTO) for restore operations depends on the time required to complete the WAL recovery and not on total data size. For more information, see [Backups in Azure HorizonDB (Preview)](concepts-backup-restore.md). | Backup data remains within the region. |
| **Zone redundant high availability** | Azure HorizonDB needs at least two compute replicas on the cluster to have zonal resilience. You can add more or remove replicas to the Azure HorizonDB cluster as your workload needs it. | Protects against availability zone outages. |
| **Zone redundant backup** | Azure HorizonDB cluster backups are automatically and securely stored in a zone redundant storage within a region. | Protects against availability zone outages. |
| **Read Replicas** | Azure HorizonDB supports in region replicas, which you can use to offload readonly workloads. Replicas also act as failover targets for primary cluster. | Supports up to 15 replicas. |

## Planned downtime events

Here are some planned maintenance scenarios. These events typically cause a few minutes of downtime, but they don't cause data loss.

| **Scenario** | **Process** |
| --- | --- |
| <b>Compute scaling (User-initiated) | During a compute scaling operation, active checkpoints finish. The service drains client connections, cancels any uncommitted transactions, detaches storage, and then shuts down the cluster. Azure HorizonDB then provisions new compute with the same server name and the updated compute configuration. The service attaches the existing storage to the new cluster and starts the database. During startup, recovery runs if needed before the service accepts client connections. |
| <b>New software deployment (Azure-initiated) | New features rollout or bug fixes automatically happen as part of service's planned maintenance. |
| <b>Minor version upgrades (Azure-initiated) | Azure HorizonDB automatically patches database servers to the minor version determined by Azure. This patching happens as part of the service's planned maintenance. The database server automatically restarts with the new minor version. You can also check your [portal](/azure/service-health/service-health-portal-update). |

## Unplanned downtime mitigation

Unplanned downtime can occur due to unexpected events such as hardware failures, network problems, or software defects. If you configure high availability (HA) and the primary database server becomes unavailable, Azure HorizonDB automatically fails over to a standby replica. This process allows client operations to resume with minimal interruption. If you don't configure HA and the restart attempt fails, the service provisions new compute. Although you can't fully prevent unplanned downtime, Azure HorizonDB reduces its impact by performing automated recovery operations without requiring manual intervention.

Though the engineering team continuously strives to provide high availability, there are times when Azure HorizonDB incurs an outage that causes unavailability of the databases and affects your application. When the service monitoring detects problems that cause widespread connectivity errors, failures, or performance problems, the service automatically declares an outage to keep you informed.

### Service outage

If an Azure HorizonDB cluster outage occurs, you can find more details about the outage in the following places:

- **Azure portal banner**: If your subscription is affected, Azure posts a service issue alert in the **Notifications** section of the Azure portal.

  :::image type="content" source="media/concepts-business-continuity/notification-service-issue-example.png" alt-text="Screenshot showing notifications in Azure portal.":::

- **Help + support** or **Support + troubleshooting**: When you create a support request from *Help + support* or *Support + troubleshooting*, Azure displays any known issues that impact your resources. Select *View outage details* to see more information and a summary of the impact. An alert also appears on the New support request page.

  :::image type="content" source="media/concepts-business-continuity/help-support-service-health-notification.png" alt-text="Screenshot showing Help Support notifications in Azure portal." lightbox="media/concepts-business-continuity/help-support-service-health-notification.png" :::

- **Service Health**: The *Service Health* page in the Azure portal provides a personalized view of the health status of Azure services across regions that affect your resources. To open the page, search for **Service Health** in the Azure portal. In the **Active events** section, review **Service issues** to see ongoing problems that affect your resources. You can also check the health of individual resources on the **Resource health** page for each resource under **Help**. The following example shows the **Service Health** page displaying an active service issue in Southeast Asia.

  :::image type="content" source="media/concepts-business-continuity/service-health-service-issues-example-map.png" alt-text="Screenshot showing service outage in Service Health portal." lightbox="media/concepts-business-continuity/service-health-service-issues-example-map.png" :::

- **Email notification**: If you configure alerts, Azure sends an email notification when a service outage affects your subscription or resources. The email is sent from `azure-noreply@microsoft.com` and includes details about the service issue. The email message begins with a standard notification indicating that an activity log alert was triggered by a service issue for your Azure subscription. For more information, see Azure Service Health documentation [Receive activity log alerts on Azure service notifications using Azure portal](/azure/service-health/alerts-activity-log-service-notifications-portal).

> [!IMPORTANT]  
> Temporary tablespaces in PostgreSQL store temporary objects and support internal operations such as sorting. Don't create user schema objects in temporary tablespaces, because these objects might not persist after server restarts, high availability (HA) failovers, or similar events.

> [!IMPORTANT]  
> Currently, you can't restore deleted servers. Use Azure resource lock to help prevent accidental deletion of your server.

## Related content

- [Restore in Azure HorizonDB (Preview)](how-to-restore-custom-restore-point.md)
