---
title: Identify which Parameter Group Connected to a Cluster
description: This article describes how to identify which parameter group is connected to a cluster in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to identify which parameter group is connected to a cluster in Azure HorizonDB.
---

# Identify which parameter group connected to a cluster

You can identify which parameter group is connected to a cluster.

## Steps to identify which parameter group connected to a cluster

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview)**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2Fclusters).

1. By using the filtering buttons and the search box, find the cluster for which you want to check what parameter group it's connected to, and select it.

    :::image type="content" source="./media/how-to-identify-connected-cluster/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page filtered by the name of the parameter group that you want to connect to one or more clusters." lightbox="./media/how-to-identify-connected-cluster/filter-search-parameter-groups.png":::

1. In the resource menu, under **Settings**, select **Parameters**. The name of the parameter group to which the cluster is connected appears to the side of the **Parameter group (create):** label. You can also scroll or search for parameter names to check how each parameter is configured in that parameter group.

    :::image type="content" source="./media/how-to-identify-connected-cluster/parameters.png" alt-text="Screenshot that shows the Parameters page of the selected cluster, from where you can check which parameter group the cluster is connected to." lightbox="./media/how-to-identify-connected-cluster/parameters.png":::

    > [!NOTE]
    > If the parameter group assigned to a cluster is the default, you don't see any parameters listed. This issue is known and will be fixed.

1. If you select the name, you're taken to the **Overview** page of the parameter group resource.

    :::image type="content" source="./media/how-to-identify-connected-cluster/parameter-group-overview.png" alt-text="Screenshot that shows the Overview page of the parameter group selected." lightbox="./media/how-to-identify-connected-cluster/parameter-group-overview.png":::

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can determine the resource identifier of the parameter group to which a cluster is connected using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{clusterName}?api-version=2026-01-20-preview" \
  --query properties.parameterGroup.id \
  --format tsv
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{clusterName}` with the desired cluster name.

You can extract the list of parameters in the parameter group to which a cluster is created using the `az rest` command:

```azurecli-interactive
az rest --method GET \
--url https://management.azure.com$(az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{clusterName}?api-version=2026-01-20-preview" \
  --query properties.parameterGroup.id \
  --output tsv)?api-version=2026-01-20-preview
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{clusterName}` with the desired cluster name.

> [!NOTE]
> If the parameter group assigned to a cluster is the default, you don't see any parameters listed. This issue is known and will be fixed.
> In this case, you receive the following error: `Not Found({"error":{"code":"ResourceNotFound","message":"The Resource 'Microsoft.HorizonDb/parameterGroups/default_pg17' under resource group '{resourceGroupName}' was not found. For more details please go to https://aka.ms/ARMResourceNotFoundFix"}})`

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
