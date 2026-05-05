---
title: Update Parameter Groups
description: This article describes how to update parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to update parameter groups in Azure HorizonDB.
---

# Update parameter groups

> [!IMPORTANT]  
> Currently, parameter groups don't support updates.

Should you need to change the value of some parameters on a given cluster, [create a new parameter group](how-to-parameter-groups-create.md) overriding the values of all those parameters, and [connect that given cluster to the new parameter group](how-to-parameter-groups-connect.md).

<!--
When updating a parameter group, at least one parameter must be provided. The underlying operation in the backend will merge your input with the system defaults for the specified `pgVersion`.

## Steps to update parameter groups

### [Portal](#tab/portal-list)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can update a parameter group using the `az rest` command:

```azurecli-interactive
az rest --method PATCH \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/parameterGroups/{parameterGroupName}?api-version=2026-01-20-preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "pgVersion": 17,
      "description": "Production configuration for PG17",
      "parameters": [
        {
          "name": "max_connections",
          "value": "780"
        }
      ]
    }
  }'
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the desired parameter group name.
- `{location}` with the target location.

When a parameter group is updated, all clusters which are connected to the parameter group have their parameter group synchronization status marked as out of synchronization.

Running the following `az rest` command at that point in time for one of the clusters connected to the updated parameter group:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/clusters/{clusterName}?api-version=2026-01-20-preview" \
  --query properties.parameterGroup.syncStatus \
  --output tsv
```

Would return the following:

```json
OutOfSync
```

You can also see that change of synchronization status by [listing all clusters connected to the updated parameter group](how-to-parameter-groups-list-connected.md).

---

## Possible errors

| Error code | Description |
| --- | --- |
| `ParameterNotRecognized` | When one or more parameter names passed as input aren't recognized among the ones supported for the version of PostgreSQL for which the parameter group is defined. |
| `ParameterIsReadOnly` | When one or more parameters passed as input are read-only parameters. |
| `ParameterValueInvalid` | When the value assigned to one or more parameters passed as input isn't valid according to the data type and allowed values of that parameter. |
| `ParameterGroupParametersRequired` | When not even one parameter is passed as input. |
| --> |

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
