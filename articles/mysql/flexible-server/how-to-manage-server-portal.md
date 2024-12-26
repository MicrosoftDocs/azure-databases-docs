---
title: Manage Server - Azure Portal
description: Learn how to manage Azure Database for MySQL - Flexible Server from the Azure portal.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Manage Azure Database for MySQL - Flexible Server using the Azure portal

This article shows you how to manage your Azure Database for MySQL Flexible Server instances. Management tasks include compute and storage scaling, resetting the server administrator password, and deleting your server.

## Prerequisites

- Sign in to the [Azure portal](https://portal.azure.com).
- Go to your Azure Database for MySQL Flexible Server resource in the Azure portal.

## Scale compute and storage

After server creation you can scale between the various [pricing tiers](https://azure.microsoft.com/pricing/details/mysql/) as your needs change. You can also scale up or down your compute and memory by increasing or decreasing vCores.

1. Select your Azure Database for MySQL Flexible Server instance in the Azure portal. Select **Compute + Storage**, located in the **Settings** section.

1. You can change the **Compute Tier**, **vCore**, **Storage** to scale up the server using higher compute tier or scale up within the same tier by increasing storage or vCores to a value you want.

   > [!div class="mx-imgBorder"]
   > :::image type="content" source="media/how-to-manage-server-portal/scale-server.png" alt-text="Screenshot of scaling storage for Azure Database for MySQL Flexible Server." lightbox="media/how-to-manage-server-portal/scale-server.png":::

   > [!IMPORTANT]  
      > - Storage cannot be scaled down.
      > - Scaling vCores causes a server restart.

1. Select **OK** to save changes.

## Reset admin password

You can change the administrator role's password using the Azure portal.

1. Select your Azure Database for MySQL Flexible Server instance in the Azure portal. In the **Overview** window, select **Reset password**.

1. Enter a new password and confirm the password. The textbox prompts you about password complexity requirements.

   > [!div class="mx-imgBorder"]
   > :::image type="content" source="media/how-to-manage-server-portal/reset-password.png" alt-text="Screenshot of resetting your password for Azure Database for MySQL Flexible Server." lightbox="media/how-to-manage-server-portal/reset-password.png":::

1. Select **Save** to save the new password.

## Delete a server

You can delete your server if you no longer need it.

1. Select your Azure Database for MySQL Flexible Server instance in the Azure portal. In the Overview window, select **Delete**.

1. Type the name of the server into the input box to confirm that you want to delete the server.

   > [!div class="mx-imgBorder"]
   > :::image type="content" source="media/how-to-manage-server-portal/delete-server.png" alt-text="Screenshot of deleting the Azure Database for MySQL Flexible Server instance." lightbox="media/how-to-manage-server-portal/delete-server.png":::

   > [!IMPORTANT]  
   > Deleting a server is irreversible.

1. Select **Delete**.

## Related content

- [Stop/Start an Azure Database for MySQL - Flexible Server instance](how-to-stop-start-server-portal.md)
- [Point-in-time restore in Azure Database for MySQL - Flexible Server with the Azure portal](how-to-restore-server-portal.md)
- [Troubleshoot connection issues to Azure Database for MySQL - Flexible Server](how-to-troubleshoot-common-connection-issues.md)
