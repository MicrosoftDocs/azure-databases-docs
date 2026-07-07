---
title: Networking in Azure HorizonDB
description: This article describes how to configure networking related settings in Azure HorizonDB.
#customer intent: As a user, I want to configure networking settings in Azure HorizonDB, so that I can control how my cluster connects to other resources.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: networking
ms.topic: how-to
---

# Networking in Azure HorizonDB (Preview)

When you deploy your Azure HorizonDB, the cluster connectivity mode is **Public access (allowed IP addresses) and private endpoints**.

For more information about public access, see [Networking overview with public access (allowed IP addresses) and private endpoints in Azure HorizonDB (Preview)](concepts-network-public.md).

## Public access (allowed IP addresses)

If you deploy your cluster with **Networking with public access (allowed IP addresses)** mode, you can perform the following operations:

- [Add firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-add-firewall.md).
- [Delete firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-delete-firewall.md).

## Related content

- [Networking overview with public access (allowed IP addresses) and private endpoints in Azure HorizonDB (Preview)](concepts-network-public.md)
