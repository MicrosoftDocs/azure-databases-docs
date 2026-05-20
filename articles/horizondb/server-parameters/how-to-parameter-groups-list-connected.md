---
title: List Clusters Connected to Parameter Groups
description: This article describes how to list clusters connected to parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/18/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to list clusters connected to parameter groups in Azure HorizonDB.
---

# List clusters connected to parameter groups

Given a parameter group, you can list the clusters that are connected to it and identify what's the current synchronization status for each of them.

## Steps to list clusters connected to parameter groups

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview) parameter groups**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2F2FparameterGroups).

1. By using the filtering buttons and the search box, find the parameter group that you want to check what clusters are connected to it, and select it.

    :::image type="content" source="./media/how-to-list-connected-clusters-parameter-groups/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page. Filter by the name of the parameter group that you want to check what clusters are connected to it." lightbox="./media/how-to-list-connected-clusters-parameter-groups/filter-search-parameter-groups.png":::

1. In the **Connected clusters** section, find the list of clusters that are connected to the parameter group.

    :::image type="content" source="./media/how-to-list-connected-clusters-parameter-groups/connected-clusters.png" alt-text="Screenshot that shows the Overview page of the selected parameter group with the clusters that are connected to it." lightbox="./media/how-to-list-connected-clusters-parameter-groups/connected-clusters.png":::

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can list clusters connected to parameter groups using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}/connections?api-version=2026-01-20-preview"
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.

The output that command returns would look like this:

```json
{
    "connections": [
        {
            "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{clusterName-1}",
            "name": "{clusterName-1}",
            "type": "Microsoft.HorizonDB/clusters",
            "status": "{syncStatus}"
        },
    .
    .
    .
        {
            "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{clusterName-N}",
            "name": "{clusterName-N}",
            "type": "Microsoft.HorizonDB/clusters",
            "status": "{syncStatus}"
        },
    ]
}
```

Where `syncStatus` can be any of the following values:

| Value | Description |
| --- | --- |
| `ApplicationInProgress` | Parameter application is in progress on the cluster. |
| `InSync` | Parameters are in sync with the cluster. |
| `OutOfSync` | Parameters are out of sync with the cluster, meaning that changes aren't effective yet. |
| `PendingApply` | Parameter application is pending on the cluster. |
| `PendingReplace` | Parameter group connection with the cluster is being replaced by a new one and is pending rollback or drop. |

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [Identity parameter group connected to a cluster](how-to-parameter-groups-identify-connected-cluster.md)
