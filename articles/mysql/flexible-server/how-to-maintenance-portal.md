---
title: Set up Scheduled Maintenance in the Azure Portal
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

## Prerequisites

To complete this how-to guide, you need:

- An [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)

## Specify maintenance schedule options

1. On the Azure Database for MySQL flexible server page, under the **Settings** heading, choose **Maintenance** to open scheduled maintenance options.
1. The default (system-managed) schedule is a random day of the week, and 60-minute window for maintenance start between 11pm and 7am local server time. If you want to customize this schedule, choose **Custom schedule**. You can then select a preferred day of the week, and a 60-minute window for maintenance start time.

## Reschedule Maintenance

1. In the Maintenance window, you'll notice a new button labeled Reschedule.
1. Upon selecting **Reschedule**, a "Maintenance Reschedule" window appears where you can select a new date and time for the scheduled maintenance activity.
1. After selecting your preferred date and time, select **Reschedule** to confirm your choice.
1. You also have an option for on-demand maintenance by selecting **Reschedule to Now**. A confirmation dialog appears to verify that you understand the potential effect, including possible server downtime.

Rescheduling maintenance also triggers email notifications to keep you informed.

The availability of the rescheduling window isn't fixed, it often depends on the size of the overall maintenance window for the region in which your server resides. This means the reschedule options can vary based on regional operations and workload.

> [!NOTE]  
> Maintenance Reschedule is only available for General Purpose and Business Critical service tiers.

### Considerations and limitations

Be aware of the following when using this feature:

- **Demand Constraints:** Your rescheduled maintenance might be canceled due to a high number of maintenance activities occurring simultaneously in the same region.
- **Lock-in Period:** Rescheduling is unavailable 15 minutes prior to the initially scheduled maintenance time to maintain the reliability of the service.
- **Reschedule Throttle:** If too many servers in the same region are scheduled for maintenance during the same time, rescheduling requests might fail. Users will receive an error notification if this occurs and are advised to choose an alternative time slot. Successfully rescheduled maintenance is unlikely to be canceled.

There's no limitation on how many times a maintenance can be rescheduled, as long as the maintenance hasn't entered into the "In preparation" state, you can always reschedule your maintenance to another time.

## Notifications about scheduled maintenance events

You can use Azure Service Health to [view notifications](/azure/service-health/service-notifications) about upcoming and performed scheduled maintenance on your Azure Database for MySQL Flexible Server instance. You can also [set up](/azure/service-health/resource-health-alert-monitor-guide) alerts in Azure Service Health to get notifications about maintenance events.

## Related content

- [scheduled maintenance in Azure Database for MySQL flexible server](concepts-maintenance.md)
- [Azure Service Health](/azure/service-health/overview)
