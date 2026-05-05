---
title: Delete Parameter Groups
description: This article describes how to delete parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to delete parameter groups in Azure HorizonDB.
---

# Delete parameter groups

If you consider that an existing parameter group isn't needed any longer, you can delete it. The operation is irreversible. When attempting to delete a parameter group which is connected to any cluster, the operation fails.

## Steps to delete parameter groups

### [Portal](#tab/portal-list)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can delete a parameter group using the `az rest` command:

```azurecli-interactive
az rest --method DELETE \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/parameterGroups/{parameterGroupName}?api-version=2026-01-20-preview"
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.

---

## Possible errors

| Error code | Description |
| --- | --- |
| `ParameterGroupHasActiveMappings` | When parameter group is connected to one or more clusters. |

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
