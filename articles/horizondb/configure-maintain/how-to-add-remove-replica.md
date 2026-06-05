---
title: How to Add or Remove a Replica (Preview)
description: This article describes the steps to add or remove a HorizonDB replica.
author: DDL-PM
ms.author: ludingding
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: configuration
ms.topic: how-to
---

# Add or remove a replica for Azure HorizonDB (Preview)

An Azure HorizonDB cluster can have up to 15 replicas. Because a replica of Azure HorizonDB is a readable standby replica, adding or removing a replica can affect the high availability behavior of an Azure HorizonDB cluster. This article provides step-by-step instructions to add or remove a replica to or from an Azure HorizonDB cluster.

## Prerequisites

Before you begin, make sure you have an existing Azure HorizonDB cluster. If you don't, create an Azure HorizonDB cluster.

## Add a replica

If you configure your Azure HorizonDB cluster with high availability, your cluster already has at least one replica. You can add a replica:

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB cluster.
1. In the resource menu, under **Settings**, select **Compute**.

   :::image type="content" source="media/how-to-add-remove-replica/compute.png" alt-text="Screenshot showing the Compute page of an Azure HorizonDB cluster." lightbox="media/how-to-add-remove-replica/compute.png" :::

1. Under **High availability replicas**, select **Change** next to the **Readable high availability replicas**. It takes you to the **Replicas**.
1. Alternatively, you can skip previous two steps, and in the resource menu, under **Settings**, select **Replicas**.
1. Select **Add new replicas**, and then choose the number of replicas that you want to add. An Azure HorizonDB cluster can have a maximum of 15 replicas.

   :::image type="content" source="media/how-to-add-remove-replica/add-replicas.png" alt-text="Screenshot showing the Replicas page to add new replicas to a cluster." lightbox="media/how-to-add-remove-replica/add-replicas.png" :::

1. Select **Save**.

If you don't configure your Azure HorizonDB cluster with high availability, your cluster only has the primary.

## Remove a replica

If your Azure HorizonDB cluster has more than one replica, you can remove a replica:

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB cluster.
1. In the resource menu, under **Settings**, select **Replicas**.
1. For the replica that you want to remove, select the **...** next to the replica name, and then select **Remove replica**.

   :::image type="content" source="media/how-to-add-remove-replica/remove-replica.png" alt-text="Screenshot showing the Replicas page to remove replicas from a cluster." lightbox="media/how-to-add-remove-replica/remove-replica.png" :::

1. Removing a replica reduces the read capacity of this Azure HorizonDB cluster. Select **Remove** to confirm.

If your Azure HorizonDB cluster has only one replica, removing this replica results in high availability being disabled. Select **Remove** to confirm.

## Related content

- [What is Azure HorizonDB (Preview)?](../overview.md)
