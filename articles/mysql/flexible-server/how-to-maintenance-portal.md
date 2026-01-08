---
title: Set up Scheduled Maintenance in the Azure portal
description: Learn how to configure scheduled maintenance settings for Azure Database for MySQL - Flexible server from the Azure portal.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: sunaray, maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Manage scheduled maintenance settings for Azure Database for MySQL - Flexible server

You can specify maintenance options for each Azure Database for MySQL flexible server instance in your Azure subscription. Options include the maintenance schedule and notification settings for upcoming and finished maintenance events.
> [!NOTE]
> These new maintenance features are being rolled out progressively across Azure regions. If you do not see them immediately in the Azure portal, please allow some time for full deployment. Availability may vary depending on your subscription and region.

## Prerequisites

To complete this how-to guide, you need:

- An [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)

## Maintenance Configuration and Experience

Azure Database for MySQL – Flexible Server now offers an enhanced maintenance experience that gives you more control and visibility over how your servers receive updates. Under **Settings > Maintenance**, you’ll find three main areas:

- Maintenance Policy  
- Custom Schedule Configuration  
- Maintenance Status and Rescheduling

## Maintenance Policy Options

You can choose from the following maintenance policy types, depending on your workload requirements:

### Virtual Canary

Virtual Canary is intended for nonproduction workloads that want to validate updates early. Servers under this policy receive updates ahead of general availability and do **not** follow the standard update cadence—there’s no guaranteed 30-day interval and no 7-day advance notice.

:::image type="content" source="media/how-to-maintenance-portal/virtual-canary.png" alt-text="Screenshot that high light virtual canary.":::

Burstable SKU servers are enrolled in the Virtual Canary policy by default.

### System Managed Maintenance Window (SMW)

This maintenance policy is the default option for servers on **General Purpose** and **Business Critical** compute tiers. Maintenance is automatically scheduled on a random day and time, typically between **11:00 PM and 7:00 AM server local time**. This policy follows the standard maintenance behavior—updates occur no more than once every 30 days and are announced at least seven days in advance.

### Custom Managed Maintenance Window (CMW)

Choose this maintenance policy if you want to control when maintenance happens. CMW lets you define a preferred **day of the week** and **start time** (in a 60-minute UTC window). This is especially useful for production environments where update timing needs to align with change control policies.

You can also assign the server to a **batch** (`Batch 1` or `Batch 2`) to help stagger maintenance across environments like TEST and PROD:

- **Batch 1**: Maintenance occurs in the **first 7 days** of the regional maintenance window.
- **Batch 2**: Maintenance occurs in the **second 7 days**.

:::image type="content" source="media/how-to-maintenance-portal/maintenance-batch.png" alt-text="Screenshot that showcases maintenance batch.":::

> [!NOTE]  
> The 7-day maintenance batches are **not aligned with calendar weeks** (for example, starting on Sunday or Monday). Instead, the first 7-day period begins from the actual start date of the maintenance cycle in the server's region.

Once CMW is configured, the new schedule takes effect in the **next regional maintenance cycle**.  
To change the timing of a **currently scheduled** maintenance, use the **Maintenance Reschedule** feature.

## View and Manage Upcoming Maintenance

The **Maintenance Status** section displays any currently scheduled or recently completed maintenance events for the server. Typically, one entry is shown at a time.

:::image type="content" source="media/how-to-maintenance-portal/maintenance-status.png" alt-text="Screenshot that showcases maintenance status.":::

### Reschedule

If maintenance hasn't started yet, you can select a new date and time by choosing **Reschedule**. This helps you avoid conflicts with business operations or planned deployments.

:::image type="content" source="media/how-to-maintenance-portal/maintenance-reschedule.png" alt-text="Screenshot that showcases maintenance reschedule.":::

The rescheduled feature is only available for servers on **General Purpose** and **Business Critical** compute tiers. It’s not supported for **Burstable SKU** servers.

#### Reschedule to now

You can click **Reschedule to now** to start the maintenance immediately. This is useful if you want to apply the update right away, or if you want a more precise control over when the maintenance occurs. **Reschedule to now** is available only if the server is in the **Scheduled** or **Rescheduled** state. Once you click **Reschedule to now**, the server enters the **In preparation** state. This means that the server is preparing for the maintenance event, and it will start the maintenance shortly after couple minutes.

> [!NOTE]  
> In certain cases, the **Reschedule to now** may hang for a while in the **In preparation** state. This is usually due to too many servers in the same region being scheduled for maintenance at the same time. If this happens, you can either wait for the server to finish preparing or raise a support ticket to get help.

#### Reschedule considerations and limitations

Be aware of the following points about the feature:

- **Tier availability**: Maintenance rescheduling isn't available for the Burstable compute tier. This feature is intended for servers in the production environment, whereas the Burstable tier is designed for nonproduction purposes.
- **Demand constraints**: Your rescheduled maintenance might be canceled if a high number of maintenance activities occur simultaneously in the same region.
- **Lock-in period**: Rescheduling is unavailable 15 minutes before the initially scheduled maintenance time, to maintain the reliability of the service.
- **Rescheduling throttle**: If too many servers in the same region are scheduled for maintenance during the same time, rescheduling requests might fail. If this failure occurs, you receive an error notification that advises you to choose an alternative time slot. Successfully rescheduled maintenance is unlikely to be canceled.

There is no limitation on how many times a maintenance event can be rescheduled. As long as a maintenance event hasn't entered the **In preparation** state, you can always reschedule it to another time.

### Maintenance rollout progress view (Public Preview)

Each maintenance event includes a **Tracking ID**. Clicking this ID opens a detailed view of all servers in your subscription that are part of the same maintenance rollout. This gives you a consolidated overview across your fleet—no need to check each server individually or rely solely on email notifications.

:::image type="content" source="media/how-to-maintenance-portal/maintenance-trackingid.png" alt-text="Screenshot that showcases maintenance TrackingID.":::

:::image type="content" source="media/how-to-maintenance-portal/maintenance-impacted-resource.png" alt-text="Screenshot that showcases impacted resource page.":::

You can access the tracking ID view at any time, whether the maintenance is pending or already completed.

### Using Azure Resource Graph to Audit Maintenance History

Customers who manage multiple Azure Database for MySQL flexible servers can use Azure Resource Graph to perform bulk queries across subscriptions and resource groups. This is especially useful for auditing maintenance history, identifying impacted resources, and tracking maintenance events over time.
For example, the following Kusto query retrieves the maintenance status, start and end times, and tracking ID for all MySQL flexible servers under the customer's subscription. This allows customers to monitor maintenance activities over the past three months in a scalable and automated way:

```sql

ServiceHealthResources
| where type == "microsoft.resourcehealth/events/impactedresources"
| extend TrackingId = split(split(id, "/events/", 1)[0], "/impactedResources", 0)[0]
| extend p = parse_json(properties)
| project subscriptionId, TrackingId, resourceName= p.resourceName, resourceGroup=p.resourceGroup, resourceType=p.targetResourceType, status= p.status, maintenanceStartTime=todatetime(p.maintenanceStartTime),  maintenanceEndTime=todatetime( p.maintenanceEndTime), details = p, id
| where resourceType == "Microsoft.DBforMySQL/flexibleServers" 
| order by maintenanceEndTime

```

This query can be executed in Azure Resource Graph Explorer or via Azure CLI/PowerShell using the az graph query command. It helps teams proactively track and report on maintenance events across their MySQL fleet.

---

## Notifications about scheduled maintenance events

You can use Azure Service Health to [view notifications](/azure/service-health/service-notifications) about upcoming and performed scheduled maintenance on your Azure Database for MySQL Flexible Server instance. You can also [set up](/azure/service-health/resource-health-alert-monitor-guide) alerts in Azure Service Health to get notifications about maintenance events.

## Related content

- [scheduled maintenance in Azure Database for MySQL flexible server](concepts-maintenance.md)
- [Azure Service Health](/azure/service-health/overview)
