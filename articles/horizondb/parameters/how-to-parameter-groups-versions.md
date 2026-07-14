---
title: List Versions of Parameter Groups in Azure HorizonDB
description: This article describes how to list the versions of parameter groups in Azure HorizonDB.
#customer intent: As a user, I want to list the versions of a parameter group in Azure HorizonDB, so that I can track which parameter values changed over time.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: parameters-group
ms.topic: how-to
---

# List versions of parameter groups in Azure HorizonDB (Preview)

> [!IMPORTANT]  
> Currently, updating parameter groups isn't supported, so each parameter group has only one version.

When you update parameter groups, you create a new immutable version. Each version contains a snapshot of the parameters at that point in time. This snapshot helps you track who changed which parameters and when during the parameter group's lifespan.

## Steps to list versions of parameter groups

### [Portal](#tab/portal-list-versions-parameter-group)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list-versions-parameter-group)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

To list the versions of a parameter group, use the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}/versions?api-version=2026-01-20-preview"
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the parameter group name you want.

The output from this command looks like the following example:

```json
```

---

## Related content

- [Parameter groups in Azure HorizonDB (Preview)](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
