---
title: How to Add or Remove a Replica (Preview)
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

An Azure HorizonDB cluster can have up to 15 replicas. Because a replica of Azure HorizonDB is a readable standby replica, adding or removing a replica can affect the high availability behavior of an Azure HorizonDB cluster. This article provides step-by-step instructions to add or remove a replica to or from an Azure HorizonDB cluster.

## Prerequisites

Before you begin, make sure you have an existing Azure HorizonDB cluster. If you don't, create an Azure HorizonDB cluster.

## Add a replica

If you configure your Azure HorizonDB cluster with high availability, your cluster already has at least one replica. You can add a replica:

1. Select your Azure HorizonDB cluster in the Azure portal.
1. Select **Compute**, located in the **Settings** section.

   :::image type="content" source="media/how-to-add-remove-replica/screenshot-compute.png" alt-text="Screenshot of the Compute settings page for an Azure HorizonDB cluster in the Azure portal." lightbox="media/how-to-add-remove-replica/screenshot-compute.png" :::

1. Under **High availability replicas**, select **Change** next to the **Readable high availability replicas**. It takes you to the **Replicas** page.
1. Alternatively, you can skip step 2 and step 3 by directly selecting **Replicas** located in the **Settings** section.
1. Select **Add new replicas**, and then select the number of replicas you want to add from the dropdown list. An Azure HorizonDB cluster can have a maximum of 15 replicas.

   :::image type="content" source="media/how-to-add-remove-replica/screenshot-add-replica.png" alt-text="Screenshot of the Replicas page showing the Add new replicas dropdown in the Azure portal." lightbox="media/how-to-add-remove-replica/screenshot-add-replica.png" :::

1. Select **Save**.

If you don't configure your Azure HorizonDB cluster with high availability, your cluster only has the primary.

## Remove a replica

If your Azure HorizonDB cluster has more than one replica, you can remove a replica:

1. Select your Azure HorizonDB cluster in the Azure portal.
1. Select **Replicas** located in the **Settings** section.
1. Select the replica you want to remove by selecting the **...** next to the replica name, and then select **Remove replica**.

   :::image type="content" source="media/how-to-add-remove-replica/screenshot-remove-replica.png" alt-text="Screenshot of the Replicas page showing the Remove replica option on a replica's context menu." lightbox="media/how-to-add-remove-replica/screenshot-remove-replica.png" :::

1. Removing a replica reduces the read capacity of this Azure HorizonDB cluster. Select **Remove** to confirm.

If your Azure HorizonDB cluster has only one replica, removing this replica results in high availability being disabled. Select **Remove** to confirm.

## Related content

- [What is Azure HorizonDB?](../overview.md)
