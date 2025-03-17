---
title: Scheduled maintenance in Azure Database for PostgreSQL flexible server
description: This article describes the scheduled maintenance feature in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/23/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
# customer intent: As a user, I want to learn how my Azure Database for PostgreSQL flexible server is maintained, and what options do I have to control when schedule maintenance is executed.
---

# Scheduled maintenance

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Your Azure Database for PostgreSQL flexible server periodically undergoes maintenance operations, to help keep your managed database secure, stable, and up to date. During maintenance, the server gets new features, updates, and patches.

> [!IMPORTANT]  
> Avoid all server operations (modifications, configuration changes, starting/stopping the server) during Azure Database for PostgreSQL flexible server maintenance. Engaging in these activities can lead to unpredictable outcomes and possibly affect server performance and stability. Wait until maintenance concludes before you conduct server operations.

## Maintenance window

You can schedule maintenance during a specific day of the week, and a time window within that day. Or you can let the system choose a day and a time window for you automatically.

The system sends maintenance notifications 5 calendar days in advance, so that you have ample time to prepare. The system also informs you about when maintenance starts and when it successfully finishes.

Notifications about upcoming scheduled maintenance can be:

- Emailed to a specific address.
- Emailed to an Azure Resource Manager role.
- Sent in a text message to mobile devices.
- Pushed as a notification to an Azure app.
- Delivered as a voice message.

When you're specifying preferences for the maintenance schedule, you can choose between a custom schedule and a system managed schedule. If you opt for a custom schedule, you can specify a day of the week and a time window. But if you select a system managed schedule, the system chooses a day for you. And within that day, it chooses a one hour time window, between 11:00 PM and 7:00 AM in your server region's time. You can configure different maintenance schedules for each of your Azure Database for PostgreSQL flexible servers.

> [!IMPORTANT]
> Normally, the interval between successful scheduled maintenance events for a server is, at least, 30 days. But for a critical emergency update, such as a severe vulnerability, the notification window could be shorter than five days or even be omitted. The critical update might be applied to your server, even if the system successfully performed scheduled maintenance in the last 30 days.

You can update your scheduled maintenance settings at any time. If maintenance is scheduled for your Azure Database for PostgreSQL flexible server and you update your scheduled maintenance preferences, the current rollout isn't reprogrammed. It proceeds at the day and time it was scheduled already. Changes to scheduled maintenance settings become effective upon successful completion of the next scheduled maintenance.

## System-managed vs. custom maintenance

You can define a system-managed schedule or a custom schedule for each Azure Database for PostgreSQL flexible server in your Azure subscription:

- With a system-managed schedule, the system chooses any one hour window between 11:00 PM and 7:00 AM in your server region's time.
- With a custom schedule, you can specify your maintenance window for the server, by choosing the day of the week and the start time of a one hour time window.

Scheduled maintenance occurs first on servers that are configured with system managed schedules. Followed by servers with custom schedules after, at least, seven days within a region. To receive early updates for development and test servers, use a system-managed schedule. This choice allows early testing and issue resolution, before updates reach production servers with custom schedules.

Updates for custom-schedule servers begin seven days later, during a defined maintenance window. After you're notified, you can't defer updates. We advise that you use custom schedules for production environments only.

In rare cases, the system can cancel some maintenance events, or some events can fail to finish successfully. If an update fails, the process is rolled back, and your server restored to the previous version of the binaries. The server might still restart during the maintenance window.

If an update is canceled or failed, the system generates a notification about the canceled or failed maintenance event. The next attempt to perform maintenance is scheduled according to your current schedule settings, and you receive a notification about it 5 calendar days in advance.

## Consideration and limitations

Some considerations when considering during monthly maintenance:

- Monthly maintenance is impactful and they involve some downtime.
- Downtime depends on the transactional load on the server at the time of maintenance.
- Once maintenance is scheduled, any changes to the maintenance settings will apply only to the next maintenance cycle, not the current one.

## Related content

- [Configure scheduled maintenance](how-to-configure-scheduled-maintenance.md).
- [Get notifications about upcoming maintenance](/azure/service-health/service-notifications).
- [Set up alerts for upcoming scheduled maintenance events](/azure/service-health/resource-health-alert-monitor-guide).
