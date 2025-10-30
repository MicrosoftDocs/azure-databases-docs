---
title: Azure Cosmos DB for PostgreSQL - Scheduled maintenance - Azure portal
description: Learn how to configure scheduled maintenance settings for an Azure Cosmos DB for PostgreSQL from the Azure portal.
ms.author: jonels
author: jonels-msft
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.topic: how-to
ms.date: 04/07/2021
appliesto:
  - ✅ PostgreSQL
---

# Manage scheduled maintenance settings for Azure Cosmos DB for PostgreSQL

[!INCLUDE [Note - Recommended services](includes/note-recommended-services.md)]

You can specify maintenance options for each cluster in your Azure subscription. Options include the maintenance schedule and notification settings for upcoming and finished maintenance events.

## Prerequisites

To complete this how-to guide, you need:

- An [Azure Cosmos DB for PostgreSQL cluster](quickstart-create-portal.md)

## Specify maintenance schedule options

1. On the cluster page, under the **Settings** heading, choose **Maintenance** to open scheduled maintenance options.
2. The default (system-managed) schedule is a random day of the week, and 30-minute window for maintenance start between 11pm and 7am cluster's
   [Azure region time](https://go.microsoft.com/fwlink/?linkid=2143646). If you want to customize this schedule, choose **Custom schedule**. You can then select a preferred day of the week, and a 30-minute window for maintenance start time.

## Notifications about scheduled maintenance events

You can use Azure Service Health to [view notifications](/azure/service-health/service-notifications) about upcoming and past scheduled maintenance on your cluster. You can also [set up](/azure/service-health/resource-health-alert-monitor-guide) alerts in Azure Service Health to get notifications about maintenance events.

## Next steps

* Learn about [scheduled maintenance in Azure Cosmos DB for PostgreSQL](concepts-maintenance.md)
* Lean about [Azure Service Health](/azure/service-health/overview)
