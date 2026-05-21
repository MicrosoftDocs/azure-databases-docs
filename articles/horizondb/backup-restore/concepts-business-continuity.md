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
| **Automatic backups** | Azure HorizonDB cluster automatically performs daily backups of your database files and continuously backs up transaction logs. Backups are retained from 7 days. You're able to restore your database server to any point in time within your backup retention period. RTO is dependent on the size of the data to restore + the time to perform log recovery. It can be from few minutes up to few hours. For more information, see [Concepts - Backup and Restore](concepts-backup-restore.md). | Backup data remains within the region. |
| **Zone redundant high availability** | Azure HorizonDB need at least two replicas on the cluster to have zonal resilience. You can add or remove replicas to the Azure HorizonDB cluster as your workload needs it. |
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
> As the name implies, temporary tablespaces in PostgreSQL are used for temporary objects, and other internal database operations, such as sorting. Therefore we don't recommend creating user schema objects in temporary tablespace, as we don't guarantee durability of such objects after Server restarts, HA failovers, etc.


> [!IMPORTANT]
> Currently,deleted servers can't be restored. Use Azure resource lock to help prevent accidental deletion of your server.



## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).


