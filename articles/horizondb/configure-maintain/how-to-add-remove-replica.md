---
title: How to Add or Remove a Replica in Azure HorizonDB
description: This article describes the steps to add or remove a HorizonDB replica.
#customer intent: As a user, I want to add a replica to my Azure HorizonDB cluster so that I can increase the read capacity and improve high availability.
author: DDL-PM
ms.author: ludingding
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: configuration
ms.topic: how-to
---

# Add or remove a replica in Azure HorizonDB (Preview)

An Azure HorizonDB cluster can have up to 15 replicas. Because a replica of Azure HorizonDB is a readable standby replica, adding or removing a replica can affect the high availability behavior of an Azure HorizonDB cluster. This article provides step-by-step instructions to add or remove a replica to or from an Azure HorizonDB cluster.

## Prerequisites

Before you begin, make sure you have an existing Azure HorizonDB cluster. If you don't, [create an Azure HorizonDB cluster](../configure-maintain/quickstart-create-cluster.md).

## Steps to add a replica

If you configure your Azure HorizonDB cluster with high availability, your cluster already has at least one replica. If you don't configure your Azure HorizonDB cluster with high availability, your cluster only has the primary.

### [Portal](#tab/portal-add-replica)

Use the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **Compute**.

   :::image type="content" source="media/how-to-add-remove-replica/compute.png" alt-text="Screenshot showing the Compute page of an Azure HorizonDB cluster." lightbox="media/how-to-add-remove-replica/compute.png" :::

1. Under **High availability replicas**, select **Change** next to the **Readable high availability replicas**. It takes you to the **Replicas**.

1. Alternatively, you can skip previous two steps, and in the resource menu, under **Settings**, select **Replicas**.

1. Select **Add new replicas**, and then choose the number of replicas that you want to add. An Azure HorizonDB cluster can have a maximum of 15 replicas.

   :::image type="content" source="media/how-to-add-remove-replica/add-replicas.png" alt-text="Screenshot showing the Replicas page to add new replicas to a cluster." lightbox="media/how-to-add-remove-replica/add-replicas.png" :::

1. Select **Save**.

### [CLI](#tab/cli-add-replica)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to add a replica and let the service choose the availability zone for deploying the replica.

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{cluster}/pools/DefaultPool/replicas/{replica}?api-version=2026-01-20-preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "role": "Read"
    }
  }'

```

Use the `az rest` command to add a replica and select the availability zone where you want to deploy the replica.

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{cluster}/pools/DefaultPool/replicas/{replica}?api-version=2026-01-20-preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "role": "Read",
      "availabilityZone": "{availabilityZone}"
    }
  }'

```

If a replica with that name already exists in the default pool of the cluster, you receive the following error:

```output
"code": "ReplicaAlreadyExists"
"message": "Replica with name '{replica}' already exists. Please use a different name."
```

If the cluster isn't in Ready state when the request is issued, you receive the following error:

```output
"code": "ClusterNotReady",
"message": "Cluster [{cluster}] is in state [{state}] and cannot accept the requested operation."
```

If the location specified in the request, where you want to create the replica, doesn't match the location of the cluster, you receive the following error:

```output
"code": "ReplicaLocationMismatch",
"message": "The replica location '{location}' does not match the parent cluster's location '{clusterLocation}'. Replicas must be created in the same Azure region as the source cluster."
```

---

## Steps to remove a replica

If your Azure HorizonDB cluster has more than one replica, you can remove a replica:

### [Portal](#tab/portal-remove-replica)

Use the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under **Settings**, select **Replicas**.

1. For the replica that you want to remove, select the **...** next to the replica name, and then select **Remove replica**.

   :::image type="content" source="media/how-to-add-remove-replica/remove-replica.png" alt-text="Screenshot showing the Replicas page to remove replicas from a cluster." lightbox="media/how-to-add-remove-replica/remove-replica.png" :::

1. Removing a replica reduces the read capacity of this Azure HorizonDB cluster. Select **Remove** to confirm.

If your Azure HorizonDB cluster has only one replica, removing this replica results in high availability being disabled. Select **Remove** to confirm.

### [CLI](#tab/cli-remove-replica)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to remove a replica from the default pool of a cluster.

```azurecli-interactive
az rest --method DELETE \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{cluster}/pools/DefaultPool/replicas/{replica}?api-version=2026-01-20-preview"
```

---

## Related content

- [What is Azure HorizonDB (Preview)?](../overview.md)
