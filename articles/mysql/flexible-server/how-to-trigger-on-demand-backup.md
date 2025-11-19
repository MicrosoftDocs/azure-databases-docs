---
title: Trigger On-Demand Backup By Using the Azure Portal
description: This article provides a step-by-step guide on triggering an on-demand backup of an Azure Database for MySQL - Flexible Server instance.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to trigger an on-demand backup from the Azure portal so that I can have more control over my database backups.
---

# Trigger on-demand backup of an Azure Database for MySQL - Flexible Server instance by using the Azure portal

This article provides a step-by-step procedure to trigger an on-demand backup from the Azure portal.

## Prerequisites

You need an Azure Database for MySQL Flexible Server instance to complete this how-to guide.

- Create a MySQL flexible server instance by following the steps in the article [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md).

## Trigger on-demand backup

Follow these steps to trigger backup on demand:

1. In the [Azure portal](https://portal.azure.com/), choose your Azure Database for the MySQL flexible server instance you want to back up.

1. Under **Settings** select **Backup and restore** from the left panel.

1. From the **Backup and restore** page, select **Backup Now**.

1. Now on the **Take backup** page, in the **Backup name** field, provide a custom name for the backup.

1. Select **Trigger**

    :::image type="content" source="media/how-to-trigger-on-demand-backup/trigger-on-demand-backup.png" alt-text="Screenshot showing how to trigger an on-demand backup." lightbox="media/how-to-trigger-on-demand-backup/trigger-on-demand-backup.png":::

1. Once completed, the on-demand and automated backups are listed.
1. These on-demand backups can also be deleted if no longer needed. Select **Delete** to delete any on-demand backup.

## Related content

- [Point-in-time restore in Azure Database for MySQL - Flexible Server with the Azure portal](how-to-restore-server-portal.md)
- [Overview of business continuity with Azure Database for MySQL - Flexible Server](concepts-business-continuity.md)
