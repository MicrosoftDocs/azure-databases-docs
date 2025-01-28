---
title: Configure networking
description: This article describes how to configure networking related settings of an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/26/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure network related settings of an Azure Database for PostgreSQL flexible server.
---

# Configure networking

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

When you deploy your Azure Database for PostgreSQL flexible server, you can choose between configuring its networking mode as **Public access (allowed IP addresses)** or as **Private access (VNET Integration)**.

For more information about these options, see [Networking with public access (allowed IP addresses)](concepts-networking-public.md) and [Networking with private access (VNET integration)](concepts-networking-private.md).

Depending on the networking mode you selected when you deployed your server, you can performn different operations.

- Networking with public access (allowed IP addresses)
    - [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
    - [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
    - [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
    - [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
    - [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint-connections.md).
    - [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint-connections.md).
    - [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint-connections.md).
    - [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint-connections.md).

- Networking with private access (VNET Integration)
    - TODO.
    - TODO.
    - TODO.

## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Reset administrator password of an Azure Database for PostgreSQL flexible server](how-to-reset-admin-password.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
