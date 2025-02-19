---
title: Scheduled Maintenance
description: This article describes the scheduled maintenance feature in Azure Database for MySQL - Flexible Server.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Scheduled maintenance in Azure Database for MySQL - Flexible Server

Azure Database for MySQL Flexible Server performs periodic maintenance to keep your managed database secure, stable, and up-to-date. During maintenance, the server gets new features, updates, and patches.
> [!IMPORTANT]  
> Please avoid all server operations (modifications, configuration changes, starting/stopping server) during Azure Database for MySQL Flexible Server maintenance. Engaging in these activities can lead to unpredictable outcomes, possibly affecting server performance and stability. Wait until maintenance concludes before conducting server operations.

## Maintenance Cycle

### Routine Maintenance

Our standard maintenance cycle is scheduled no less frequently than every 30 days. This period allows us to ensure system stability and performance while minimizing disruption to your services.

### Critical Maintenance

In certain scenarios, such as the need to deploy urgent security fixes or updates critical to maintaining availability and data integrity, maintenance might be conducted more frequently. These exceptions are made to safeguard your data and ensure the continuous operation of your services.

<a id="locating-maintenance-details"></a>

### Virtual Canary Maintenance (Public Preview)
Virtual Canary is an experimental maintenance program offering early access to updates, enabling customers to test workload compatibility with new Azure MySQL versions. Unlike routine maintenance, Virtual Canary doesn't follow the 30-day minimum gap or the 7-day notification period. This program helps customers proactively validate new features and contribute early feedback for product improvements. Burstable SKU servers, commonly used for non-production environments, are automatically enrolled in the Virtual Canary program.

#### Managing Virtual Canary Enrollment  

Azure Database for MySQL provides flexibility for customers to manage their participation in the Virtual Canary program. Virtual Canary allows early access to maintenance updates, enabling proactive compatibility testing and feedback on new features.  

- Checking Virtual Canary Enrollment  

To verify if your server is enrolled in the Virtual Canary program, use the following command:  

```bash  
az mysql flexible-server show --resource-group {resourcegroupname} --name {servername} --query "maintenancePolicy"
```  

If the result includes `"patchStrategy": "VirtualCanary"`, the server is enrolled in the Virtual Canary program.  

- Enrolling in Virtual Canary  

To enroll a server in the Virtual Canary program, run the following command:  

```bash  
az mysql flexible-server update --resource-group {resourcegroupname} --name {servername} --maintenance-policy-patch-strategy VirtualCanary
```  

- Exiting Virtual Canary  

To exit the Virtual Canary program and revert to the standard maintenance policy, use this command:  

```bash  
az mysql flexible-server update --resource-group {resourcegroupname} --name {servername} --maintenance-policy-patch-strategy Regular
```  

This straightforward process allows customers to opt in or out of Virtual Canary as needed, ensuring alignment with their operational requirements.

### Locate Maintenance Details

For specific details about what each maintenance update entails, please refer to our release notes. These notes provide comprehensive information about the updates applied during maintenance, allowing you to understand and prepare for any changes affecting your environment.

> [!NOTE]  
> Not all servers will necessarily undergo maintenance during scheduled updates, whether routine or Critical. The Azure MySQL team employs specific criteria to determine which servers require maintenance. This selective approach ensures that maintenance is both efficient and essential, tailored to the unique needs of each server environment, and minimize the downtime of your production.

## Select a maintenance window

You can schedule maintenance during a specific day of the week and a time window within that day. Or you can let the system pick a day and a time window time for you automatically. Either way, the system will alert you seven days before running any maintenance. The system will also let you know when maintenance is started, and when it's successfully completed.

Notifications about upcoming scheduled maintenance can be:

- Emailed to a specific address
- Emailed to an Azure Resource Manager Role
- Sent in a text message (SMS) to mobile devices
- Pushed as a notification to an Azure app
- Delivered as a voice message

When specifying preferences for the maintenance schedule, you can pick a day of the week and a time window. If you don't specify, the system will pick times between 11pm and 7am in your server's region time. You can define different schedules for each Flexible Server in your Azure subscription.

You can update scheduling settings at any time. If there's a maintenance scheduled for your Flexible server and you update scheduling preferences, the current rollout will proceed as scheduled and the scheduling settings change will become effective upon its successful completion for the next scheduled maintenance.

You can define system-managed schedule or custom schedule for each Flexible Server in your Azure subscription.
- With custom schedule, you can specify your maintenance window for the server by choosing the day of the week and a one-hour time window.
- With system-managed schedule, the system will pick any one-hour window between 11pm and 7am in your server's region time.

> [!IMPORTANT]  
> Starting from 31st August 2024, Azure Database for MySQL will no longer support custom maintenance windows for burstable SKU instances. This change is due to the need for simplifying maintenance processes, ensuring optimal performance, and our analysis indicating that the number of users utilizing custom maintenance windows on burstable SKUs is minimal. Existing burstable SKU instances with custom maintenance window configurations will remain unaffected; however, users won't be able to modify these custom maintenance window settings moving forward.
>  
> For customers requiring custom maintenance windows, we recommend upgrading to General Purpose or Business Critical SKUs to continue using this feature.

In rare cases, maintenance event can be canceled by the system or might fail to complete successfully. If the update fails, the update is reverted, and the previous version of the binaries is restored. In such failed update scenarios, you might still experience restart of the server during the maintenance window. If the update is canceled or failed, the system will create a notification about canceled or failed maintenance event respectively notifying you. The next attempt to perform maintenance will be scheduled as per your current scheduling settings and you'll receive notification about it five days in advance.

## Near zero downtime maintenance (Public preview) ##

Azure Database for MySQL Flexible Server's "Near Zero Downtime Maintenance" feature is a groundbreaking development for **HA (High Availability) enabled servers**. This feature is designed to substantially reduce maintenance downtime, ensuring that in most cases, maintenance downtime is expected to be between 40 to 60 seconds. This capability is pivotal for businesses that demand high availability and minimal interruption in their database operations.

### Precise Downtime Expectations ###

- **Downtime Duration:** In most cases, the downtime during maintenance ranges from 10 to 30 seconds.
- **Additional Considerations:** After a failover event, there's an inherent DNS Time-To-Live (TTL) period of approximately 30 seconds. This period isn't directly controlled by the maintenance process but is a standard part of DNS behavior. So, from a customer's perspective, the total downtime experienced during maintenance could be in the range of 40 to 60 seconds.

### Limitations and Prerequisites ###

To achieve the optimal performance promised by this feature, certain conditions and limitations should be noted:

- **Primary Keys in All Tables:** Ensuring that every table has a primary key is critical. Lack of primary keys can significantly increase replication lag, affecting the downtime.
- **Low Workload During Maintenance Times:** Maintenance periods should coincide with times of low workload on the server to ensure the downtime remains minimal. We encourage you to use the [custom maintenance window](how-to-maintenance-portal.md#specify-maintenance-schedule-options) feature to schedule maintenance during off-peak hours.
- **Downtime Guarantees：** While we strive to keep the maintenance downtime as low as possible, we don't guarantee that it will always be less than 60 seconds in all circumstances. Various factors, such as high workload or specific server configurations, can lead to longer downtime. In the worst-case scenario, downtime might be similar to that of a standalone server.

## Maintenance reschedule

The **maintenance reschedule** feature grants you greater control over the timing of maintenance activities on your Azure Database for MySQL Flexible Server instance. After receiving a maintenance notification, you can reschedule it to a more convenient time, irrespective of whether it was system or custom managed. Please note that maintenance rescheduling isn't available for Burstable SKUs, as this feature is intended for production environment servers, whereas Burstable SKU compute tiers are designed for non-production purposes.

### Reschedule parameters and notifications

Rescheduling isn't confined to fixed time slots; it depends on the earliest and latest permissible times in the current maintenance cycle, which typically spans from the first to the last day of the maintenance window for the region. Upon rescheduling, a notification will be sent out to confirm the changes, following the standard notification policies.

### Considerations and limitations

Be aware of the following when using this feature:

- **Demand Constraints:** Your rescheduled maintenance might be canceled due to a high number of maintenance activities occurring simultaneously in the same region.
- **Lock-in Period:** Rescheduling is unavailable 15 minutes prior to the initially scheduled maintenance time to maintain the reliability of the service.
- **Reschedule Throttle** If too many servers in the same region are scheduled for maintenance during the same time, rescheduling requests might fail. Users will receive an error notification if this occurs and are advised to choose an alternative time slot. Successfully rescheduled maintenance is unlikely to be canceled.

There's no limitation on how many times a maintenance can be rescheduled, as long as the maintenance hasn't entered into the "In preparation" state, you can always reschedule your maintenance to another time.

> [!NOTE]  
> We recommend monitoring notifications closely during the preview stage to accommodate potential adjustments.

Use this feature to avoid disruptions during critical database operations. We encourage your feedback as we continue to develop this functionality.

## FAQ

**Q: Why did some of my servers receive maintenance notifications while others did not?**

A: The maintenance start times differ across regions, so servers in different regions might receive maintenance notifications at different times.

**Q: Why did some servers in the same region receive maintenance notifications while others did not?**

A: This could be because the servers that didn't receive notifications were created more recently, and the system determined that they don't yet require maintenance.

**Q: Can I opt out of scheduled maintenance?**

A: No, opting out of scheduled maintenance isn't allowed. However, you can use the maintenance reschedule feature to adjust the timing or enable the High Availability (HA) feature to minimize downtime. As a PaaS database product, it's essential to perform timely maintenance to ensure the security and reliability of your database.

## Related content

- [change the maintenance schedule](how-to-maintenance-portal.md)
- [get notifications about upcoming maintenance](/azure/service-health/service-notifications)
- [set up alerts about upcoming scheduled maintenance events](/azure/service-health/resource-health-alert-monitor-guide)
