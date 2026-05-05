---
title: Create Parameter Groups
description: This article describes how to create parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to create parameter groups in Azure HorizonDB.
---

# Create parameter groups

When creating a parameter group, at least one parameter must be provided. The underlying operation in the backend will merge your input with the system defaults for the specified `pgVersion`.

## Steps to create parameter groups

### [Portal](#tab/portal-list)

[!INCLUDE [no-portal-support](../includes/no-portal-support.md)]

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can create a parameter group using the `az rest` command:

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/parameterGroups/{parameterGroupName}?api-version=2026-01-20-preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "pgVersion": 17,
      "description": "Production configuration for PG17",
      "parameters": [
        {
          "name": "max_connections",
          "value": "500"
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

---

## Possible errors

| Error code | Description |
| --- | --- |
| `ParameterGroupNameConflictsWithDefault` | When the name of the parameter group matches any of the ones reserved for default parameter groups. |
| `ParameterGroupAlreadyExists` | When a parameter group with the same resource identifier already exist. |
| `ParameterGroupPgVersionRequired` | When `pgVersion` isn't passed as one of the properties in the input. |
| `ParameterNotRecognized` | When one or more parameter names passed as input aren't recognized among the ones supported for the version of PostgreSQL for which the parameter group is defined. |
| `ParameterIsReadOnly` | When one or more parameters passed as input are read-only parameters. |
| `ParameterValueInvalid` | When the value assigned to one or more parameters passed as input isn't valid according to the data type and allowed values of that parameter. |
| `ParameterGroupParametersRequired` | When not even one parameter is passed as input. |

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
