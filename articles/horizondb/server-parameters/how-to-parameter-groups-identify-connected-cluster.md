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

    :::image type="content" source="./media/how-to-identify-connected-cluster/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page filtered by the name of the parameter group which you want to connect to one or more clusters." lightbox="./media/how-to-identify-connected-cluster/filter-search-parameter-groups.png":::

1. In the resource menu, under **Settings**, select **Parameters**.

    :::image type="content" source="./media/how-to-identify-connected-cluster/parameters.png" alt-text="Screenshot that shows the Parameters page of the selected cluster, from where you can check which parameter group the cluster is connected to." lightbox="./media/how-to-identify-connected-cluster/parameters.png":::

.
.
.

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can connect one specific parameter group to a cluster using the `az rest` command:

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{clusterName}?api-version=2026-01-20-preview" \
  --body '{
    "properties": {
        "createMode": "Update",
            "parameterGroup": {
            "Id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}"
        }
    }
  }'
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.

> [!IMPORTANT]  
> Avoid passing properties other than createMode and parameterGroup or the parameter group connection to the cluster might not be processed. This is a current limitation that will be removed in the future.

#### Possible errors

| Error code | Description |
| --- | --- |
| `ParameterGroupApplyFailed` | When the attempt to apply the parameter group to the cluster fails. |

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
