---
title: Scale or configure a cluster
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Scale an Azure Cosmos DB for MongoDB vCore cluster by changing the tier and disk size or change the configuration by enabling high availability.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 05/13/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Scaling and configuring Your Azure Cosmos DB for MongoDB vCore cluster

Azure Cosmos DB for MongoDB vCore provides seamless scalability and high availability. This document serves as a quick guide for developers who want to learn how to scale and configure their clusters. Changes to the cluster are performed live without downtime.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB vCore cluster.
  - If you don't have an Azure subscription, [create an account for free](https://azure.microsoft.com/free).
  - If you have an existing Azure subscription, [create a new Azure Cosmos DB for MongoDB vCore cluster](quickstart-portal.md).

## Navigate to the scale section

To change the configuration of your cluster, use the **Scale** section of the Azure Cosmos DB for MongoDB vCore cluster page in the Azure portal. The portal includes real-time costs for these changes.

> [!TIP]
> For this guide, we recommend using the resource group name ``msdocs-cosmos-howto-rg``.

1. Sign in to the [Azure portal](https://portal.azure.com).

2. Navigate to the existing Azure Cosmos DB for MongoDB vCore cluster page.

3. From the Azure Cosmos DB for MongoDB vCore cluster page, select the **Scale** navigation menu option.

   :::image type="content" source="media/how-to-scale-cluster/select-scale-option.png" lightbox="media/how-to-scale-cluster/select-scale-option.png" alt-text="Screenshot of the Scale option on the page for an Azure Cosmos DB for MongoDB vCore cluster.":::

## Change the cluster tier

The cluster tier you select influences the amount of vCores and RAM assigned to your cluster. You can change the cluster tier to suit your needs at any time without downtime. For example, you can increase from **M50** to **M60** or decrease **M50** to **M40** using the Azure portal.

1. To change the cluster tier, select the new tier from the drop-down menu.

   :::image type="content" source="media/how-to-scale-cluster/configure-tier.png" alt-text="Screenshot of the cluster tier option in the Scale page of a cluster.":::

    > [!NOTE]
    > This change is performed live to the cluster without downtime.
    >
    > Upgrade or downgrade from burstable tiers to regular compute tier isn't supported at the moment.

2. Select **Save** to persist your change.

## Increase disk size

You can increase the storage size to give your database more room to grow. For example, you can increase the storage from **128 GB** to **256 GB**.

1. To increase the storage size, select the new size from the drop-down menu.

   :::image type="content" source="media/how-to-scale-cluster/configure-storage.png" alt-text="Screenshot of the storage per shard option in the Scale page of a cluster.":::

    > [!NOTE]
    > This change is performed live to the cluster without downtime. Also, storage size can only be increased, not decreased.

2. Select **Save** to persist your change.

## Enable or disable high availability

You can enable or disable [high availability (HA)](./high-availability.md) to suit your needs. HA avoids database downtime by maintaining replica shards of every primary shard in a cluster. If a primary shard goes down, incoming connections are automatically redirected to its replica shard, ensuring that there's minimal downtime.

1. To enable or disable HA, toggle the checkbox option.

   :::image type="content" source="media/how-to-scale-cluster/configure-high-availability.png" alt-text="Screenshot of the high availability checkbox in the Scale page of a cluster.":::

2. Select **Save** to persist your change.

## Increase the number of physical shards

When a database grows beyond the capacity of a single physical shard cluster, you can either increase the [storage size](#increase-disk-size) or add additional [physical shards](./partitioning.md#physical-shards). After a new physical shard is added to the cluster, you must perform a cluster rebalancing operation to redistribute data across the shards.

1. To add physical shards, select new shard count from the list.

   :::image type="content" source="media/how-to-scale-cluster/configure-add-shards.png" alt-text="Screenshot of the physical shard count drop-down list in the Scale page of a cluster.":::

1. Select **Save** to persist your change.

If you need more than 10 physical shards on your cluster, open an [Azure support request](/azure/azure-portal/supportability/how-to-create-azure-support-request#create-a-support-request).

## Enable 'Query from any node' capability on a multishard cluster

When a multi-shard cluster receives a query, it must be routed to one or more physical shards. To improve overall cluster performance, this query dispatching workload can be evenly distributed across all nodes. To enable this distribution, turn on the **Query from any node** setting.

1. To enable or disable **Query from any node**, toggle the checkbox.

   :::image type="content" source="media/how-to-scale-cluster/configure-query-from-any-node.png" alt-text="Screenshot of the query from any node checkbox in the Scale page of a cluster.":::

1. Select **Save** to persist your change.

## Next steps

In this guide, we showed that scaling and configuring your Cosmos DB for MongoDB vCore cluster in the Azure portal is a straightforward process. The Azure portal includes the ability to adjust the cluster tier, increase storage size, enable or disable high availability, and add physical shards without any downtime.

> [!div class="nextstepaction"]
> [Restore an Azure Cosmos DB for MongoDB vCore cluster](how-to-restore-cluster.md)
