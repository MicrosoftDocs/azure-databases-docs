---
title: Manage server - Azure portal
description: Learn how to manage an Azure Database for PostgreSQL flexible server from the Azure portal.
#customer intent: As a user, I want to scale compute and storage resources for my PostgreSQL server, so that I can adjust capacity as my workload needs change.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ai-usage: ai-assisted
ms.custom:
- mvc
- sfi-image-nochange
---

# Manage Azure Database for PostgreSQL flexible server by using the Azure portal

This article shows you how to manage your Azure Database for PostgreSQL flexible server. Management tasks include compute and storage scaling, admin password reset, and viewing server details.

## Sign in

Sign in to the [Azure portal](https://portal.azure.com). Go to your Azure Database for PostgreSQL flexible server resource in the Azure portal.

## Scale compute and storage

After server creation, you can scale between the various [pricing tiers](https://azure.microsoft.com/pricing/details/postgresql/) as your needs change. You can also scale up or down your compute and memory by increasing or decreasing vCores.

> [!NOTE]
> You can't scale storage to a lower value.

1. Select your server in the Azure portal. Select **Compute + Storage**, located in the **Settings** section.
1. Change the **Compute yier**, **vCore**, and **Storage** values to scale up the server by using a higher compute tier or scale up within the same tier by increasing storage or vCores to your desired value.

> [!div class="mx-imgBorder"]
> :::image type="content" source="./media/how-to-manage-server-portal/scale-server.png" alt-text="Scaling storage for an Azure Database for PostgreSQL flexible server.":::

> [!Important]
> - You can't scale storage down.
> - Scaling vCores restarts the server.

1. Select **OK** to save your changes.

## Reset admin password

You can change the administrator role's password by using the Azure portal.

1. Select your server in the Azure portal. In the **Overview** window, select **Reset password**.
1. Enter a new password and confirm the password. The text box prompts you about password complexity requirements.

> [!div class="mx-imgBorder"]
> :::image type="content" source="./media/how-to-manage-server-portal/reset-password.png" alt-text="Reset your password for your Azure Database for PostgreSQL flexible server.":::

1. Select **Save** to save the new password.

## Delete a server

You can delete your server if you no longer need it.

1. Select your server in the Azure portal. In the **Overview** window, select **Delete**.
1. Type the name of the server into the input box to confirm that you want to delete the server.

   :::image type="content" source="./media/how-to-manage-server-portal/delete-server.png" alt-text="Delete the Azure Database for PostgreSQL flexible server.":::

1. Select **Delete**.

## Related content

- [Backup and restore in Azure Database for PostgreSQL](../backup-restore/concepts-backup-restore.md).
- [Monitor metrics in Azure Database for PostgreSQL](../monitor/concepts-monitoring.md).
