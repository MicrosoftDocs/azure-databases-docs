---
title: How to add or remove a replica
description: This article describes the steps to add or remove a HorizonDB replica.
author: DDL-PM
ms.author: ludingding
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
---

# Add or remove a replica in Azure HorizonDB

An Azure HorizonDB cluster can have up to 15 replicas. Because a replica of Azure HorizonDB is a readable standby replica, adding or removing a replica can affect the high availability behavior of a HorizonDB cluster. This article provides step-by-step instructions to add or remove a replica to or from a HorizonDB cluster.

## Prerequisites

Before you begin, make sure you have an existing HorizonDB. If you don't, create an Azure HorizonDB cluster.

## Add a replica

### [Portal](#tab/portal-add-replica)

If you configure your HorizonDB cluster with high availability, your HorizonDB cluster already has at least one replica. You can add a replica:

1. Select your HorizonDB in the Azure portal.
1. Select **Compute**, located in the **Settings** section.
1. Under **High availability replicas**, select **Change** next to the **Readable high availability replicas**. It takes you to the **Replicas** page.
1. Alternatively, you can skip step 2 and step 3 by directly selecting **Replicas** located in the **Settings** section.
1. Select **Add new replicas**, and then select the number of replicas you want to add from the dropdown list. A HorizonDB cluster can have a maximum of 15 replicas.
1. Select **Save**.

If you don't configure your HorizonDB cluster with high availability, your HorizonDB cluster only has the primary.

## Remove a replica

### [Portal](#tab/portal-remove-replica)

If your HorizonDB cluster has more than one replica, you can remove a replica:

1. Select your HorizonDB in the Azure portal.
1. Select **Replicas** located in the **Settings** section.
1. Select the replica you want to remove by selecting the **...** next to the replica name, and then select **Remove replica**.
1. Removing a replica reduces the read capacity of this HorizonDB cluster. Select **Remove** to confirm.

If you create your HorizonDB with zone redundant HA and the replica you want to remove is the last replica that's in a different zone than the primary, removing this replica violates the zone redundant HA and isn't allowed. To remove this replica, you need to change your HA preference to allow same zone or disable HA.

If your HorizonDB cluster has only one replica, removing this replica results in HA being disabled. Select **Remove** to confirm.

## Related content

- [Azure HorizonDB overview](../overview.md)
