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
# customer intent: As a user, I want to learn how to list parameter groups in Azure HorizonDB.
---

# Connect clusters to parameter groups

You can connect one parameter group to one or more clusters, as long as the region of the parameter group and the region of the cluster matches.

## Steps to connect parameter groups to clusters

### [Portal](#tab/portal-list)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can connect one specific parameter group to a cluster using the `az rest` command:

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/clusters/{clusterName}?api-version=2026-01-20-preview" \
  --body '{
    "properties": {
        "createMode": "Update",
            "parameterGroup": {
            "Id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDb/parameterGroups/{parameterGroupName}"
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

---

## Possible errors

| Error code | Description |
| --- | --- |
| `ParameterGroupApplyFailed` | When the attempt to apply the parameter group to the cluster fails. |

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
