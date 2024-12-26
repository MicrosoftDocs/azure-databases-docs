---
title: Scheduled maintenance - Azure portal
description: Learn how to configure scheduled maintenance settings for an Azure Database for PostgreSQL - Flexible Server from the Azure portal.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Manage scheduled maintenance settings for Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]
 
You can specify maintenance options for each Azure Database for PostgreSQL flexible server instance in your Azure subscription. Options include the maintenance schedule and notification settings for upcoming and finished maintenance events.

## Prerequisites

To complete this how-to guide, you need:
- An [Azure Database for PostgreSQL flexible server](quickstart-create-server-portal.md) instance
 
## Specify maintenance schedule options
 
1. On the Azure Database for PostgreSQL flexible server instance page, under the **Settings** heading, choose **Maintenance** to open scheduled maintenance options.
2. The default (system-managed) schedule is a random day of the week, and 60-minute window for maintenance start between 11pm and 7am local server time. If you want to customize this schedule, choose **Custom schedule**. You can then select a preferred day of the week, and a 60-minute window for maintenance start time.
 
## Notifications about scheduled maintenance events
 
You can use Azure Service Health to [view notifications](/azure/service-health/service-notifications) about upcoming and performed scheduled maintenance on your Azure Database for PostgreSQL flexible server instance. You can also [set up](/azure/service-health/resource-health-alert-monitor-guide) alerts in Azure Service Health to get notifications about maintenance events.
 
[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Scheduled maintenance in Azure Database for PostgreSQL - Flexible Server](concepts-maintenance.md).
- [Azure Service Health](/azure/service-health/overview).
