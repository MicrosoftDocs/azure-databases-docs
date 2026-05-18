---
title: Connect Clusters to Parameter Groups
description: This article describes how to connect parameter groups to clusters in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to connect parameter groups to clusters in Azure HorizonDB.
---

# Connect clusters to parameter groups

You can connect one parameter group to one or more clusters, as long as the region of the parameter group and the region of the cluster matches.

## Steps to connect parameter groups to clusters

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview) parameter groups**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2F2FparameterGroups).

1. By using the filtering buttons and the search box, find the parameter group which you want to check what clusters are connected to it, and select it.

    :::image type="content" source="./media/how-to-connect-clusters-parameter-groups/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page filtered by the name of the parameter group which you want to connect to one or more clusters." lightbox="./media/how-to-connect-clusters--parameter-groups/filter-search-parameter-groups.png":::

1. In the **Connected clusters** section, select the **Connect clusters** command bar button.

    :::image type="content" source="./media/how-to-connect-clusters-parameter-groups/connect-clusters-first.png" alt-text="Screenshot that shows the Overview page of the selected parameter group from where you can connect it to one or more clusters." lightbox="./media/how-to-connect-clusters-parameter-groups/connect-clusters-first.png":::

1. In the **Connect clusters** page that opens on the side, use the filtering button and the search box to find the clusters that you want to connect to this parameter group. Select the checkbox of each cluster that you want to connect. Then, select **Connect clusters**.

    :::image type="content" source="./media/how-to-connect-clusters-parameter-groups/connect-clusters-second.png" alt-text="Screenshot that shows the Connect clusters page of the selected parameter group from where you can connect it to one or more clusters." lightbox="./media/how-to-connect-clusters-parameter-groups/connect-clusters-second.png":::

1. A notification indicates that the operation to connect the parameter group is to the clusters selected is initiated.

    :::image type="content" source="./media/how-to-connect-clusters-parameter-groups/notification-connecting.png" alt-text="Screenshot that shows the notification that indicates the connection of the parameter group to the selected clusters is initiated." lightbox="./media/how-to-connect-clusters-parameter-groups/notification-connecting.png":::

1. A few seconds later, a notification indicates that the operation completed successfully.

    :::image type="content" source="./media/how-to-connect-clusters-parameter-groups/notification-connected.png" alt-text="Screenshot that shows the notification that indicates the connection of the parameter group to the selected clusters completed successfuly." lightbox="./media/how-to-connect-clusters-parameter-groups/notification-connected.png":::


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
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
