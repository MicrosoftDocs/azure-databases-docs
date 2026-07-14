---
title: Scheduled Maintenance in Azure HorizonDB
description: This article describes the scheduled maintenance feature in your Azure HorizonDB.
#customer intent: As a user, I want to understand how scheduled maintenance works so that I can plan around potential downtime.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: configuration
ms.topic: concept-article
ms.collection: ce-skilling-ai-copilot
---

# Scheduled maintenance in Azure HorizonDB (Preview)

Your Azure HorizonDB cluster periodically performs maintenance operations to help keep your managed database secure, stable, and up to date. During maintenance, the server gets new features, updates, and patches.

> [!IMPORTANT]  
> Avoid all cluster operations, such as modifications and configuration changes, during Azure HorizonDB cluster maintenance. Engaging in these activities can lead to unpredictable outcomes and possibly affect server performance and stability. Wait until maintenance concludes before you conduct cluster operations.

## Maintenance window

You can schedule maintenance during a specific day of the week, and a time window within that day. Or you can let the system choose a day and a time window for you automatically.

The system sends maintenance notifications five calendar days in advance, so that you have ample time to prepare. The system also informs you about when maintenance starts and when it successfully finishes.

You can receive notifications about upcoming scheduled maintenance through:

- Email to a specific address.
- Email to an Azure Resource Manager role.
- Text message to mobile devices.
- Push notification to an Azure app.
- Voice message.

When you specify preferences for the maintenance schedule, choose between a custom schedule and a system managed schedule. If you opt for a custom schedule, specify a day of the week and a time window. If you select a system managed schedule, the system chooses a day for you. Within that day, it chooses a one-hour time window, between 11:00 PM and 7:00 AM in your server region's time. You can configure different maintenance schedules for each of your Azure HorizonDB clusters.

> [!IMPORTANT]  
> Normally, the interval between successful scheduled maintenance events for a server is at least 30 days. But for a critical emergency update, such as a severe vulnerability, the notification window can be shorter than five days or even be omitted. The critical update might be applied to your server, even if the system performed scheduled maintenance in the last 30 days.

You can update your scheduled maintenance settings at any time. If maintenance is scheduled for your Azure HorizonDB cluster and you update your scheduled maintenance preferences, the current rollout isn't reprogrammed. It proceeds at the day and time it was scheduled already. Changes to scheduled maintenance settings take effect upon successful completion of the next scheduled maintenance.

## System-managed vs. custom maintenance

For each Azure HorizonDB cluster in your Azure subscription, you can define a system-managed schedule or a custom schedule:

- With a system-managed schedule, the system chooses any one-hour window between 11:00 PM and 7:00 AM in your server region's time.
- With a custom schedule, you specify your maintenance window for the server by choosing the day of the week and the start time of a one-hour time window.

Scheduled maintenance occurs first on servers that are configured with system-managed schedules. Servers with custom schedules follow after, at least, seven days within a region. To receive early updates for development and test servers, use a system-managed schedule. This schedule choice allows early testing and issue resolution, before updates reach production servers with custom schedules.

Updates for custom-schedule servers begin seven days later, during a defined maintenance window. After you're notified, you can't defer updates. Use custom schedules for production environments only.

In rare cases, the system cancels some maintenance events, or some events fail to finish successfully. If an update fails, the process rolls back, and your server restores to the previous version of the binaries. The server might still restart during the maintenance window.

If an update is canceled or failed, the system generates a notification about the canceled or failed maintenance event. The next attempt to perform maintenance is scheduled according to your current schedule settings, and you receive a notification about it 5 calendar days in advance.

## Considerations and limitations

Consider the following points during monthly maintenance:

- Monthly maintenance is impactful and involves some downtime.
- Downtime depends on the transactional load on the server at the time of maintenance.
- Once you schedule maintenance, any changes to the maintenance settings apply only to the next maintenance cycle, not the current one.

## Related content

- [Get notifications about upcoming maintenance](/azure/service-health/service-health-notifications-properties)
- [Set up alerts for upcoming scheduled maintenance events](/azure/service-health/resource-health-alert-monitor-guide)
