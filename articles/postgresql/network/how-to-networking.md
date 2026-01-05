---
title: Networking
description: This article describes how to configure networking related settings of an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure network related settings of an Azure Database for PostgreSQL.
---

# Networking

When you deploy your Azure Database for PostgreSQL flexible server, you can choose between configuring its networking mode as **Public access (allowed IP addresses)** or as **Private access (VNET Integration)**.

For more information about these options, see [Networking with public access (allowed IP addresses)](concepts-networking-public.md) and [Networking with private access (VNET integration)](concepts-networking-private.md).

Depending on the networking mode you selected when you deployed your server, you can perform different operations. The following two sections cover the two available networking modes, and list the operations available in each of them.

## Public access (allowed IP addresses)

If your server was deployed with **Networking with public access (allowed IP addresses)** mode, you can perform the following operations:

- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).

## Private access (VNET Integration)

If your server was deployed with **Networking with private access (VNET Integration)** mode, you can perform the following operation:

- [Change private DNS zone](how-to-networking-servers-deployed-vent-integration-change-private-dns-zone.md).

## Related content

- [Server lifecycle](how-to-networking.md).
- [Server administration](how-to-networking.md).
- [Compute and storage](how-to-networking.md).
- [Monitoring](how-to-networking.md).
- [Intelligent performance](how-to-networking.md).
- [Extensions](how-to-networking.md).
- [Replication](how-to-networking.md).
