---
title: Scheduled Maintenance
description: This article describes the scheduled maintenance feature in Azure Database for MySQL.
author: SudheeshGH 
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Scheduled maintenance in Azure Database for MySQL

Azure Database for MySQL performs periodic maintenance to help keep your managed database secure, stable, and up to date. During maintenance, the server gets new features, updates, and patches.

> [!IMPORTANT]  
> Avoid all server operations (modifications, configuration changes, starting/stopping) during Azure Database for MySQL maintenance. Engaging in these activities can lead to unpredictable outcomes that might affect server performance and stability. Wait until maintenance concludes before you conduct server operations.

## Maintenance cycle

The following sections describe the maintenance types. For specific details about what each maintenance update entails, refer to the release notes. These notes provide comprehensive information about the updates applied during maintenance, so that you can understand and prepare for any changes that affect your environment.

> [!NOTE]  
> Not all servers necessarily undergo maintenance during scheduled updates, whether routine or critical. The Azure MySQL team employs specific criteria to determine which servers require maintenance. This selective approach ensures that maintenance is both efficient and essential, is tailored to the unique needs of each server environment, and minimizes production downtime.

### Routine maintenance

Our standard maintenance cycle is no less frequent than every 30 days. This period helps ensure system stability and performance while minimizing disruption to your services.

### Critical maintenance

In certain scenarios, such as the need to deploy urgent security fixes or updates that are critical to maintaining availability and data integrity, we might conduct maintenance more frequently. These exceptions help safeguard your data and ensure the continuous operation of your services.

<a id="locating-maintenance-details"></a>

### Virtual Canary maintenance

Virtual Canary is an experimental maintenance program that offers early access to updates. It enables customers to test workload compatibility with new Azure Database for MySQL versions and provide feedback on new features.

Unlike routine maintenance, Virtual Canary doesn't follow the 30-day minimum gap or the 7-day notification period. This program helps customers proactively validate new features and contribute early feedback for product improvements. Burstable-tier servers, commonly used for non-production environments, are automatically enrolled in the Virtual Canary program.

#### Virtual Canary enrollment  

Azure Database for MySQL provides flexibility for customers to manage their participation in the Virtual Canary program. Customers can opt in or out of the program as needed for alignment with their operational requirements.

To verify if your server is enrolled in the Virtual Canary program, use the following command. If the result includes `"patchStrategy": "VirtualCanary"`, the server is enrolled in the program.

```bash  
az mysql flexible-server show --resource-group {resourcegroupname} --name {servername} --query "maintenancePolicy"
```  

To enroll a server in the Virtual Canary program, run the following command:  

```bash  
az mysql flexible-server update --resource-group {resourcegroupname} --name {servername} --maintenance-policy-patch-strategy VirtualCanary
```  

To leave the Virtual Canary program and revert to the standard maintenance policy, use this command:  

```bash  
az mysql flexible-server update --resource-group {resourcegroupname} --name {servername} --maintenance-policy-patch-strategy Regular
```  

## Maintenance windows

You can schedule maintenance during a specific day of the week and a time window within that day. Or you can let the system pick a day and a time window for you automatically. Either way, the system alerts you seven days before it runs any maintenance. The system also tells you when maintenance starts and when it successfully finishes.

Notifications about upcoming scheduled maintenance can be:

- Emailed to a specific address.
- Emailed to an Azure Resource Manager role.
- Sent in a text message (SMS) to mobile devices.
- Pushed as a notification to an Azure app.
- Delivered as a voice message.

When you specify preferences for the maintenance schedule, you can pick a day of the week and a time window. If you don't specify preferences, the system picks times between 11 PM and 7 AM in your server's region time. You can define different schedules for each flexible server in your Azure subscription.

You can update scheduling settings at any time. If maintenance is scheduled for your flexible server and you update scheduling preferences, the current rollout proceeds as scheduled. The change to scheduling settings becomes effective upon its successful completion for the next scheduled maintenance.

You can define a system-managed schedule or a custom schedule for each flexible server in your Azure subscription:

- With a custom schedule, you can specify your maintenance window for the server by choosing the day of the week and a one-hour time window.
- With a system-managed schedule, the system picks any one-hour window between 11 PM and 7 AM in your server's region time.

> [!IMPORTANT]  
> As of August 31, 2024, Azure Database for MySQL no longer supports custom maintenance windows for Burstable-tier instances. This change helps simplify maintenance processes and ensure optimal performance. Also, our analysis indicated that the number of users who use custom maintenance windows on Burstable tiers is minimal.
>
> Existing Burstable-tier instances with custom maintenance windows are unaffected. However, users can no longer modify these settings for custom maintenance windows.
>
> For customers who need custom maintenance windows, we recommend upgrading to the General Purpose or Memory-Optimized tier.

In rare cases, a maintenance event can be canceled by the system or might fail to finish successfully. If a maintenance event fails, the update is reverted, and the previous version of the binaries is restored. In scenarios of failed updates, you might still experience a restart of the server during the maintenance window.

If a maintenance event is canceled or fails, the system sends you a notification. The next attempt to perform maintenance is scheduled according to your current settings. You receive a notification about the next attempt five days in advance.

<a id="near-zero-downtime-maintenance-public-preview"></a>

## Maintenance status

For individual servers, you can view the maintenance status in Azure MySQL maintenance blade in the Azure portal. The maintenance status indicates whether maintenance is scheduled, in progress, completed, or canceled.

For customers managing multiple Azure Database for MySQL flexible servers, you can use Azure Resource Graph to perform bulk queries across subscriptions and resource groups. This is especially useful for auditing maintenance history, identifying impacted resources, and tracking maintenance events over time. Below is the Kusto query that retrieves the maintenance status, start and end times, and tracking ID for all MySQL flexible servers under the customer's subscription. This allows customers to monitor maintenance activities over the past three months in a scalable and automated way:

```sql

ServiceHealthResources
| where type == "microsoft.resourcehealth/events/impactedresources"
| extend TrackingId = split(split(id, "/events/", 1)[0], "/impactedResources", 0)[0]
| extend p = parse_json(properties)
| project subscriptionId, TrackingId, resourceName= p.resourceName, resourceGroup=p.resourceGroup, resourceType=p.targetResourceType, status= p.status, maintenanceStartTime=todatetime(p.maintenanceStartTime),  maintenanceEndTime=todatetime( p.maintenanceEndTime), details = p, id
| where resourceType == "Microsoft.DBforMySQL/flexibleServers" 
| order by maintenanceEndTime

```

You can also go to Azure Service Health's Impacted Resources tab to view the maintenance status for all your Azure resources, including Azure Database for MySQL flexible servers. Please note that the maintenance status that appears in Azure Service Health represents the overall status of the maintenance event at region level and might not reflect the status of individual servers.

## Near-zero-downtime maintenance

The Azure Database for MySQL *near-zero-downtime maintenance* feature is a groundbreaking development for high-availability servers. This feature is designed to substantially reduce maintenance downtime. This capability is pivotal for businesses that demand high availability and minimal interruption in their database operations.

### Conditions and limitations

To achieve the optimal performance that this feature offers, note these conditions and limitations:

- **Downtime duration**: In most cases, the downtime during maintenance ranges from 10 to 30 seconds.
- **Primary keys in all tables**: Ensuring that every table has a primary key is critical. A lack of primary keys can significantly increase replication lag and affect the downtime.
- **Low workload during maintenance times**: Maintenance periods should coincide with times of low workload on the server to minimize downtime. We encourage you to use the [custom maintenance window](how-to-maintenance-portal.md#custom-managed-maintenance-window-cmw) to schedule maintenance during off-peak hours.
- **Downtime guarantees**: Although we strive to keep the maintenance downtime as low as possible, we don't guarantee that it will be less than 60 seconds in all circumstances. Various factors, such as high workload or specific server configurations, can increase downtime. In the worst-case scenario, downtime might be similar to that of a standalone server.

<a id="maintenance-reschedule"></a>

## Maintenance rescheduling

The *maintenance rescheduling* feature gives you greater control over the timing of maintenance activities on your Azure Database for MySQL flexible server. After you receive a maintenance notification, you can reschedule it to a more convenient time, whether it was system managed or custom managed.

Use this feature to avoid disruptions during critical database operations. We encourage your feedback as we continue to develop this functionality.

### Rescheduling parameters and notifications

Rescheduling isn't confined to fixed time slots. It depends on the earliest and latest permissible times in the current maintenance cycle. The cycle typically spans from the first day to the last day of the maintenance window for the region. When you reschedule, you get a notification to confirm the changes, according to the standard notification policies.

### Considerations and limitations

Be aware of the following points about the feature:

- **Tier availability**: Maintenance rescheduling isn't available for the Burstable compute tier. This feature is intended for servers in the production environment, whereas the Burstable tier is designed for non-production purposes.
- **Demand constraints**: Your rescheduled maintenance might be canceled if a high number of maintenance activities occur simultaneously in the same region.
- **Lock-in period**: Rescheduling is unavailable 15 minutes before the initially scheduled maintenance time, to maintain the reliability of the service.
- **Rescheduling throttle**: If too many servers in the same region are scheduled for maintenance during the same time, rescheduling requests might fail. If this failure occurs, you receive an error notification that advises you to choose an alternative time slot. Successfully rescheduled maintenance is unlikely to be canceled.

There's no limitation on how many times a maintenance event can be rescheduled. As long as a maintenance event hasn't entered the **In preparation** state, you can always reschedule it to another time.

> [!NOTE]  
> We recommend that you monitor notifications closely during the preview stage to accommodate potential adjustments.

## FAQ

### Why did some of my servers receive maintenance notifications while others didn't?

The maintenance start times differ across regions. Servers in different regions might receive maintenance notifications at different times.

### Why did some servers in the same region receive maintenance notifications while others didn't?

It's possible that the servers that didn't receive notifications were created more recently, and the system determined that they don't yet need maintenance.

### Can I opt out of scheduled maintenance?

No, opting out of scheduled maintenance isn't allowed. However, you can use the maintenance rescheduling feature to adjust the timing. Or you can enable the high-availability feature to minimize downtime. Because Azure Database for MySQL is a platform as a service (PaaS) database product, performing timely maintenance helps ensure the security and reliability of your database.

## Related content

- [Change the maintenance schedule](how-to-maintenance-portal.md)
- [Get notifications about upcoming maintenance](/azure/service-health/service-notifications)
- [Set up alerts about upcoming scheduled maintenance events](/azure/service-health/resource-health-alert-monitor-guide)
