---
title: Deny Public Network by Using the Azure Portal
description: Learn how to configure public network access for Azure Database for MySQL - Flexible Server by using the Azure portal.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
---

# Deny Public Network Access in Azure Database for MySQL - Flexible Server by using the Azure portal

This tutorial describes how to configure an Azure Database for MySQL Flexible Server instance to:

- Deny all public network access and
- Allow only connections through private endpoints.

## Deny public access during the creation of MySQL flexible server

1. During [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md): In the Networking tab, choose `Public access (allowed IP addresses)` and `Private endpoint` as the connectivity method.

1. To disable public access on the Azure Database for MySQL Flexible Server instance you're creating, uncheck Allow public access to this resource through the internet using a public IP address under `Public access`.

   :::image type="content" source="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql.png" alt-text="Screenshot of denying public access from the portal." lightbox="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql.png":::

1. After entering the remaining information in the other tabs, select `Review + Create` to deploy the Azure Database for MySQL Flexible Server instance without public access.

## Deny public access to an existing MySQL flexible server

> [!NOTE]  
> Requirement: the server is deployed with connectivity **Public access (allowed IP addresses) and Private endpoint**.

1. On the Azure Database for MySQL Flexible Server page, under **Settings**, select **Networking**.

1. To disable public access on the Azure Database for MySQL Flexible Server instance, uncheck Allow public access to this resource through the internet using a public IP address under **Public access**.

   :::image type="content" source="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql-2.png" alt-text="Screenshot of denying public access from the portal next screen." lightbox="media/how-to-networking-private-link-deny-public-access/deny-public-access-networking-page-mysql-2.png":::

1. Select **Save** to save the changes.

## Related content

- [Create and manage Private Link for Azure Database for MySQL - Flexible Server using the portal](how-to-networking-private-link-portal.md)
- [Connectivity and networking concepts for Azure Database for MySQL - Flexible Server](concepts-networking.md)
- [Data encryption with customer managed keys for Azure Database for MySQL](security-customer-managed-key.md)
- [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](security-entra-authentication.md)
