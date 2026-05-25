---
title: Delete Parameter Groups
description: This article describes how to delete parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to delete parameter groups in Azure HorizonDB.
---

# Delete parameter groups

If you consider that an existing parameter group isn't needed any longer, you can delete it. The operation is irreversible. When attempting to delete a parameter group that is connected to some cluster, the operation fails.

## Steps to delete parameter groups

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview) parameter groups**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2F2FparameterGroups).

1. By using the filtering buttons and the search box, find the parameter group that you want to delete, and select it.

    :::image type="content" source="./media/how-to-delete-parameter-groups/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page filtered by the name of the parameter group that you want to delete." lightbox="./media/how-to-delete-parameter-groups/filter-search-parameter-groups.png":::

1. In the toolbar of the selected parameter group, select **Delete**.

    :::image type="content" source="./media/how-to-delete-parameter-groups/delete-button.png" alt-text="Screenshot that shows the Overview page of the parameter group that you want to delete." lightbox="./media/how-to-delete-parameter-groups/delete-button.png":::

1. Before you attempt to delete a parameter group, you must make sure it isn't connected to any cluster. Trying to delete a parameter group that is connected to some cluster raises an error. The error indicates that all connections to the parameter group must be removed before it can be deleted.

    :::image type="content" source="./media/how-to-delete-parameter-groups/deletion-blocked-clusters-connected.png" alt-text="Screenshot that shows the error message shown when trying to delete a parameter group that is connected to some cluster." lightbox="./media/how-to-delete-parameter-groups/deletion-blocked-clusters-connected.png":::

1. If the parameter group isn't connected to any cluster, you're prompted to confirm the operation. To proceed, select **Delete**.

    :::image type="content" source="./media/how-to-delete-parameter-groups/confirm-delete.png" alt-text="Screenshot that shows the prompt message to confirm the operation when you attempt to delete a parameter group." lightbox="./media/how-to-delete-parameter-groups/confirm-delete.png":::


1. A notification indicates that the operation to delete the parameter group is initiated.

    :::image type="content" source="./media/how-to-delete-parameter-groups/notification-deleting.png" alt-text="Screenshot that shows the notification that indicates the deletion of the parameter group is initiated." lightbox="./media/how-to-delete-parameter-groups/notification-deleting.png":::

1. A few seconds later, a notification indicates that the operation completed successfully.

    :::image type="content" source="./media/how-to-delete-parameter-groups/notification-deleted.png" alt-text="Screenshot that shows the notification that indicates the deletion of the parameter group completed successfully." lightbox="./media/how-to-delete-parameter-groups/notification-deleted.png":::

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can delete a parameter group using the `az rest` command:

```azurecli-interactive
az rest --method DELETE \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}?api-version=2026-01-20-Preview"
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.

#### Possible errors

| Error code | Description |
| --- | --- |
| `ParameterGroupHasActiveMappings` | When parameter group is connected to one or more clusters. |

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
- [Identity parameter group connected to a cluster](how-to-parameter-groups-identify-connected-cluster.md)
