---
title: List Versions of Parameter Groups
description: This article describes how to list the versions of parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to list the versions of parameter groups in Azure HorizonDB.
---

# List versions of parameter groups

> [!IMPORTANT]  
> Currently, because updating parameter groups isn't supported, each parameter group can only have one version.

When parameter groups are updated, a new immutable version is created. Each version contains a snapshot of the parameters at that point in time. This is helpful to determine who, when and which parameters changed their values throughout the lifespan of the parameter group.

## Steps to list versions of parameter groups

### [Portal](#tab/portal-list)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can list the versions of a parameter group using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}/versions?api-version=2026-01-20-Preview"
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.

The output that command returns would look like the following:

```json
```

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
