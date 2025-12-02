---
title: Scale or configure a cluster
description: Scale an Azure DocumentDB cluster by changing the compute tier and storage size or change the configuration by enabling in-region high availability.
author: niklarin
ms.author: nlarin
ms.topic: how-to
ms.date: 10/13/2025
ms.custom:
- build-2025
- sfi-image-nochange
---

# Scaling and configuring Azure DocumentDB cluster

Azure DocumentDB provides seamless [scalability](./scalability-overview.md) and [in-region high availability (HA)](./high-availability.md). This document serves as a quick guide for developers who want to learn how to scale and configure their clusters. 

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

## Scale cluster compute

[The cluster tier](./compute-storage.md#compute-in-azure-documentdb) allows you to configure number of vCores and amount of RAM on your cluster's [physical shards](./partitioning.md#physical-shards). You can change the cluster tier to suit your needs at any time without interruption. For example, you can increase from **M50** to **M60** or decrease **M50** to **M40**.

### [Azure portal](#tab/portal)

1. On the cluster sidebar, under **Settings**, select **Scale**.

1. To change the cluster tier, select the new tier from the drop-down menu.

   :::image type="content" source="media/how-to-scale-cluster/configure-tier.png" alt-text="Screenshot of how to change the cluster compute tier on the Scale page of a cluster and save changes." lightbox="media/how-to-scale-cluster/configure-tier.png":::

2. Select **Save** to persist your change.

### [Azure CLI](#tab/cli)

1. To scale cluster compute tier up or down, update the existing cluster with an `update` operation by changing the `MXXX` value in the `compute.tier` property.

    ```azurecli-interactive
    az resource update \
      --resource-type "Microsoft.DocumentDB/mongoClusters" \
      --name "<cluster-name>" \
      --resource-group "<resource-group>" \
      --set properties.compute.tier="<compute-tier>"
    ```
    
### [REST APIs](#tab/rest-apis)

You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1. Use this command to change cluster compute tier:
    
   ```azurecli-interactive
   az rest \
      --method "PATCH" \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-09-01" \
      --body "{\"location\":\"<cluster-region>\",\"properties\":{\"compute\":{\"tier\":\"<compute-tier>\"}}}"
   ```
    > [!TIP]
    > If you're using the Azure Cloud Shell, you can upload/download files directly to the shell. For more information, see [managed files in Azure Cloud Shell](/azure/cloud-shell/using-the-shell-window#upload-and-download-files).

---

> [!NOTE]
> Downgrade from regular compute tier to [a burstable tier](./compute-storage.md#what-is-burstable-compute) isn't supported.

## Increase storage size

You can increase [the storage size](./compute-storage.md#storage-in-azure-documentdb) to give your database more room to grow. For example, you can increase the storage from **128 GiB** to **256 GiB**.

### [Azure portal](#tab/portal)

1. To increase the storage size, select the new size from the drop-down menu.

   :::image type="content" source="media/how-to-scale-cluster/configure-storage.png" alt-text="Screenshot of the storage per physical shard option in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-storage.png":::

2. Select **Save** to persist your change.

### [Azure CLI](#tab/cli)

1. To increase cluster storage size, update the existing cluster with an `update` operation by increasing the value in the `storage.sizeGb` property. Supported storage sizes are listed on [the supported storage page](./compute-storage.md#storage-in-azure-documentdb).

    ```azurecli-interactive
    az resource update \
      --resource-type "Microsoft.DocumentDB/mongoClusters" \
      --name "<cluster-name>" \
      --resource-group "<resource-group>" \
      --set properties.storage.sizeGb="<new-size-in-GiB>"
    ```

### [REST APIs](#tab/rest-apis)

You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1. Use this command to change cluster compute tier:
    
   ```azurecli-interactive
   az rest \
      --method "PATCH" \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-09-01" \
      --body "{\"location\":\"<cluster-region>\",\"properties\":{\"storage\":{\"sizeGb\":\"<new-size-in-GiB>\"}}}"
   ```
    > [!TIP]
    > If you're using the Azure Cloud Shell, you can upload/download files directly to the shell. For more information, see [managed files in Azure Cloud Shell](/azure/cloud-shell/using-the-shell-window#upload-and-download-files).

---

> [!IMPORTANT]
> Storage size can only be increased, not decreased.

## Enable or disable high availability

You can enable or disable [in-region high availability (HA)](./high-availability.md) to suit your needs. In-region HA avoids database downtime by maintaining replica shards of every primary shard in a cluster. If a primary shard goes down, incoming connections are automatically redirected to its replica shard, ensuring that there's minimal downtime.

### [Azure portal](#tab/portal)

1. To enable or disable in-region HA, toggle the checkbox option.

   :::image type="content" source="media/how-to-scale-cluster/configure-high-availability.png" alt-text="Screenshot of the in-region high availability checkbox in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-high-availability.png":::

2. Select **Save** to persist your change.

### [Azure CLI](#tab/cli)

1. To *enable* in-region high availability on the cluster, update the existing cluster with an `update` operation by setting the value in the `highAvailability.targetMode` property to `ZoneRedundantPreferred`. 

    ```azurecli-interactive
    az resource update \
      --resource-type "Microsoft.DocumentDB/mongoClusters" \
      --name "<cluster-name>" \
      --resource-group "<resource-group>" \
      --set properties.highAvailability.targetMode="ZoneRedundantPreferred"
    ```

1. To *disable* in-region high availability on the cluster, update the existing cluster with an `update` operation by setting the value in the `highAvailability.targetMode` property to `Disabled`. 

    ```azurecli-interactive
    az resource update \
      --resource-type "Microsoft.DocumentDB/mongoClusters" \
      --name "<cluster-name>" \
      --resource-group "<resource-group>" \
      --set properties.highAvailability.targetMode="Disabled"
    ```

### [REST APIs](#tab/rest-apis)

You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1. Use this command to *enable* in-region high availability on the cluster:
    
   ```azurecli-interactive
   az rest \
      --method "PATCH" \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-09-01" \
      --body "{\"location\":\"<cluster-region>\",\"properties\":{\"highAvailability\":{\"targetMode\":\"ZoneRedundantPreferred\"}}}"
   ```

1. Use this command to *disable* in-region high availability on the cluster:
    
   ```azurecli-interactive
   az rest \
      --method "PATCH" \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-09-01" \
      --body "{\"location\":\"<cluster-region>\",\"properties\":{\"highAvailability\":{\"targetMode\":\"Disabled\"}}}"
   ```

---

## Increase the number of physical shards

When a database grows beyond the capacity of a single physical shard cluster, you can either increase the [storage size](#increase-storage-size) or add more [physical shards](./partitioning.md#physical-shards). After a new physical shard is added to the cluster, you must perform a cluster rebalancing operation to redistribute data across the shards. Each physical shard in a cluster always has the same [compute](#scale-cluster-compute) and [storage](#increase-storage-size) configuration.

### [Azure portal](#tab/portal)

1. To add physical shards, select new shard count from the list.

   :::image type="content" source="media/how-to-scale-cluster/configure-add-shards.png" alt-text="Screenshot of the physical shard count drop-down list in the Scale page of a cluster." lightbox="media/how-to-scale-cluster/configure-add-shards.png":::

1. Select **Save** to persist your change.

1. Select **Continue** in the pop-up window to persist your change.

### [Azure CLI](#tab/cli)

1. To add a physical shard to the cluster, update the existing cluster with an `update` operation by increasing the value for the `sharding.shardCount` property by one. 

    ```azurecli-interactive
    az resource update \
      --resource-type "Microsoft.DocumentDB/mongoClusters" \
      --name "<cluster-name>" \
      --resource-group "<resource-group>" \
      --set properties.sharding.shardCount="<current-shard-count-plus-one>"
    ```

    > [!NOTE]
    > You can add only one physical shard at a time. If you need to add more than one physical shard to the cluster, you need to do it sequentially.

### [REST APIs](#tab/rest-apis)

You can use the Azure REST API directly or wrapped into `az rest` from Azure CLI environment.

1. Use this command to add a physical shard to the cluster:
    
   ```azurecli-interactive
   az rest \
      --method "PATCH" \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.DocumentDB/mongoClusters/<cluster-name>?api-version=2025-09-01" \
      --body "{\"location\":\"<cluster-region>\",\"properties\":{\"sharding\":{\"shardCount\":\"<current-shard-count-plus-one>\"}}}"
   ```

    > [!NOTE]
    > You can add only one physical shard at a time. If you need to add more than one physical shard to the cluster, you need to do it sequentially.

---

> [!TIP]
> If you need more than 10 physical shards on your cluster, open a support ticket.

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
> The duration of the rebalancing process depends on the volume of data being moved between physical shards. The operation is performed online and doesn't affect cluster availability or functionality.

## Next steps

In this guide, we showed that scaling and configuring your Azure DocumentDB cluster in the Azure portal is a straightforward process. The Azure portal includes the ability to adjust the cluster tier, increase storage size, enable or disable high availability, and add physical shards without any downtime.

- [Compute and storage options](./compute-storage.md)
- [Check out sharding fundamentals](./partitioning.md)

> [!div class="nextstepaction"]
> [Restore an Azure DocumentDB cluster](how-to-restore-cluster.md)
