---
title: Scale or configure a cluster
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Scale an Azure Cosmos DB for MongoDB vCore cluster by changing the compute tier and storage size or change the configuration by enabling in-region high availability.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 08/25/2025
appliesto:
- ✅ MongoDB (vCore)
ms.custom:
- build-2025
- sfi-image-nochange
---

# Scaling and configuring Azure Cosmos DB for MongoDB vCore cluster

Azure Cosmos DB for MongoDB vCore provides seamless [scalability](./scalability-overview.md) and [in-region high availability (HA)](./high-availability.md). This document serves as a quick guide for developers who want to learn how to scale and configure their clusters. 

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

## Navigate to the scale section

To change the configuration of your cluster, use the **Scale** section of the Azure Cosmos DB for MongoDB vCore cluster page in the Azure portal. The portal includes real-time costs for these changes.

1. Sign in to the [Azure portal](https://portal.azure.com).

2. Navigate to the existing Azure Cosmos DB for MongoDB vCore cluster page.

3. From the Azure Cosmos DB for MongoDB vCore cluster page, in the **Settings** section select the **Scale** navigation menu option.

   :::image type="content" source="media/how-to-scale-cluster/select-scale-option.png" lightbox="media/how-to-scale-cluster/select-scale-option.png" alt-text="Screenshot of the Scale option on the page for an Azure Cosmos DB for MongoDB vCore cluster.":::

## Scale cluster compute

[The cluster tier](./compute-storage.md#compute-in-azure-cosmos-db-for-mongodb-vcore) allows you to configure number of vCores and amount of RAM on your cluster's [physical shards](./partitioning.md#physical-shards). You can change the cluster tier to suit your needs at any time without interruption. For example, you can increase from **M50** to **M60** or decrease **M50** to **M40**.

### [Azure portal](#tab/portal)

1. On the cluster sidebar, under **Settings**, select **Scale**.

1. To change the cluster tier, select the new tier from the drop-down menu.

   :::image type="content" source="media/how-to-scale-cluster/configure-tier.png" alt-text="Screenshot of the cluster tier option in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-tier.png":::

2. Select **Save** to persist your change.

### [Azure CLI](#tab/cli)

1. To enable Microsoft Entra ID on the cluster, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes` in the `authConfig` property.

### [REST APIs](#tab/rest-apis)
You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1.  Use this command to add Microsoft Entra ID authentication method to the cluster:

---

> [!NOTE]
> Downgrade from regular compute tier to [a burstable tier](./burstable-tier.md) isn't supported.

## Increase storage size

You can increase [the storage size](./compute-storage.md#storage-in-azure-cosmos-db-for-mongodb-vcore) to give your database more room to grow. For example, you can increase the storage from **128 GiB** to **256 GiB**.

### [Azure portal](#tab/portal)

1. To increase the storage size, select the new size from the drop-down menu.

   :::image type="content" source="media/how-to-scale-cluster/configure-storage.png" alt-text="Screenshot of the storage per shard option in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-storage.png":::

    > [!NOTE]
    > This change is performed live to the cluster without downtime. Also, storage size can only be increased, not decreased.

2. Select **Save** to persist your change.

### [Azure CLI](#tab/cli)

1. To enable Microsoft Entra ID on the cluster, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes` in the `authConfig` property.

### [REST APIs](#tab/rest-apis)
You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1.  Use this command to add Microsoft Entra ID authentication method to the cluster:

---

## Enable or disable high availability

You can enable or disable [in-region high availability (HA)](./high-availability.md) to suit your needs. In-region HA avoids database downtime by maintaining replica shards of every primary shard in a cluster. If a primary shard goes down, incoming connections are automatically redirected to its replica shard, ensuring that there's minimal downtime.

### [Azure portal](#tab/portal)

1. To enable or disable in-region HA, toggle the checkbox option.

   :::image type="content" source="media/how-to-scale-cluster/configure-high-availability.png" alt-text="Screenshot of the in-region high availability checkbox in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-high-availability.png":::

2. Select **Save** to persist your change.

### [Azure CLI](#tab/cli)

1. To enable Microsoft Entra ID on the cluster, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes` in the `authConfig` property.

### [REST APIs](#tab/rest-apis)
You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1.  Use this command to add Microsoft Entra ID authentication method to the cluster:

---

## Increase the number of physical shards

[!INCLUDE[MongoDB vCore](./includes/notice-customer-add-physical-shard-preview.md)]

When a database grows beyond the capacity of a single physical shard cluster, you can either increase the [storage size](#increase-storage-size) or add more [physical shards](./partitioning.md#physical-shards). After a new physical shard is added to the cluster, you must perform a cluster rebalancing operation to redistribute data across the shards. Each physical shard in a cluster always has the same [compute](#scale-cluster-compute) and [storage](#increase-storage-size) configuration.

1. To add physical shards, select new shard count from the list.

   :::image type="content" source="media/how-to-scale-cluster/configure-add-shards.png" alt-text="Screenshot of the physical shard count drop-down list in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-add-shards.png":::

1. Select **Save** to persist your change.

If you need more than 10 physical shards on your cluster, open an [Azure support request](/azure/azure-portal/supportability/how-to-create-azure-support-request#create-a-support-request).

### Rebalance data

After [a physical shard is added to a cluster](#increase-the-number-of-physical-shards), or if multishard cluster has [uneven storage usage](./how-to-manage-alerts.md) across its physical shards, data rebalancing redistributes data between shards without any downtime.

In preview, data rebalancing needs to be enabled on cluster:

1. In the Azure portal, open cluster properties.
1. Under **Settings** on the **Features** page, select **Rebalancer for multishard clusters**.
1. In the **Rebalancer for multishard clusters** panel, select **Enable**.

To initiate data rebalancing, connect to the cluster using a management tool such as the [Mongo shell](./how-to-connect-mongo-shell.md).

1. Start the rebalancer with the ```sh.startBalancer()``` command.

1. Check the rebalancer status using ```sh.isBalancerRunning()```.

1. Stop the rebalancer with the ```sh.stopBalancer()``` command.

 > [!NOTE]
> The duration of the rebalancing process depends on the volume of data being moved between physical shards. The operation is performed online and doesn't impact cluster availability or functionality.

## Next steps

In this guide, we showed that scaling and configuring your Cosmos DB for MongoDB vCore cluster in the Azure portal is a straightforward process. The Azure portal includes the ability to adjust the cluster tier, increase storage size, enable or disable high availability, and add physical shards without any downtime.

- [Compute and storage options](./compute-storage.md)
- [Check out sharding fundamentals](./partitioning.md)

> [!div class="nextstepaction"]
> [Restore an Azure Cosmos DB for MongoDB vCore cluster](how-to-restore-cluster.md)
