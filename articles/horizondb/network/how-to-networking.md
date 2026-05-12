---
title: Networking in Azure HorizonDB
description: This article describes how to configure networking related settings in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
# customer intent: As a user, I want to learn how to configure network related settings in Azure HorizonDB.
---

# Networking in Azure HorizonDB

When you deploy your Azure HorizonDB, you can choose between configuring its networking mode as **Public access (allowed IP addresses)** or as **Private access (VNET Integration)**.

For more information about these options, see [Networking overview with public access (allowed IP addresses) in Azure HorizonDB](concepts-networking-public.md) and [Network with private access (virtual network integration) in Azure HorizonDB](concepts-networking-private.md).

Depending on the networking mode you selected when you deployed your server, you can perform different operations. The following two sections cover the two available networking modes, and list the operations available in each of them.

## Public access (allowed IP addresses)

If your server was deployed with **Networking with public access (allowed IP addresses)** mode, you can perform the following operations:

- [Enable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).

## Private access (VNET Integration)

If your server was deployed with **Networking with private access (VNET Integration)** mode, you can perform the following operation:

- [Change private DNS zone in Azure HorizonDB](how-to-networking-servers-deployed-vent-integration-change-private-dns-zone.md).

## Related content

- [Networking in Azure HorizonDB](how-to-networking.md)
