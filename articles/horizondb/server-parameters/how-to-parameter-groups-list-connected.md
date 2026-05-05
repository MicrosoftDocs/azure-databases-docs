---
title: List Clusters Connected to Parameter Groups
description: This article describes how to list clusters connected to parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to list clusters connected to parameter groups in Azure HorizonDB.
---

# List clusters connected to parameter groups

Given a parameter group, you can list the clusters which are connected to it and current synchronization status for each of them.

## Steps to list clusters connected to parameter groups

### [Portal](#tab/portal-list)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can list clusters connected to parameter groups using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/parameterGroups/{parameterGroupName}/connections?api-version=2026-01-20-preview"
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.

The output that command returns would look like the following:

```json
{
    "connections": [
        {
            "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDb/clusters/{clusterName-1}",
            "name": "{clusterName-1}",
            "type": "Microsoft.HorizonDb/clusters",
            "status": "{syncStatus}"
        },
    .
    .
    .
        {
            "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDb/clusters/{clusterName-N}",
            "name": "{clusterName-N}",
            "type": "Microsoft.HorizonDb/clusters",
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
