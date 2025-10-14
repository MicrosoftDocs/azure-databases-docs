---
title: Deny Public Network by Using the Azure Portal
description: Learn how to configure public network access for Azure Database for MySQL - Flexible Server by using the Azure portal.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
---

# Deny Public Network Access in Azure Database for MySQL - Flexible Server by using the Azure portal

This article describes how you can configure an Azure Database for MySQL Flexible Server instance to deny all public configurations and allow only connections through private endpoints to enhance network security further.

## Deny public access during the creation of MySQL flexible server

1. When creating an [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md) in the Networking tab, choose *Public access (allowed IP addresses) and Private endpoint* as the connectivity method.

1. To disable public access on the Azure Database for MySQL Flexible Server instance you are creating, uncheck Allow public access to this resource through the internet using a public IP address under *Public access*.

   :::image type="content" source="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql.png" alt-text="Screenshot of denying public access from the portal." lightbox="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql.png":::

1. After entering the remaining information in the other tabs, select *Review + Create* to deploy the Azure Database for MySQL Flexible Server instance without public access.

## Deny public access to an existing MySQL flexible server

> [!NOTE]  
> The Azure Database for MySQL Flexible Server instance must have been deployed with **Public access (allowed IP addresses) and Private endpoint** as the connectivity method to implement this.

1. On the Azure Database for MySQL Flexible Server page, under **Settings**, select **Networking**.

1. To disable public access on the Azure Database for MySQL Flexible Server instance, uncheck Allow public access to this resource through the internet using a public IP address under **Public access**.

   :::image type="content" source="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql-2.png" alt-text="Screenshot of denying public access from the portal next screen." lightbox="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql-2.png":::

1. Select **Save** to save the changes.

1. A notification will confirm that the connection security setting was successfully enabled.

## Related content

- [configure private link for Azure Database for MySQL Flexible Server from the Azure portal](how-to-networking-private-link-portal.md)
- [manage connectivity](concepts-networking.md)
- [add another layer of encryption to your Azure Database for MySQL Flexible Server instance using Customer Managed Keys](concepts-customer-managed-key.md)
- [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](concepts-azure-ad-authentication.md)
