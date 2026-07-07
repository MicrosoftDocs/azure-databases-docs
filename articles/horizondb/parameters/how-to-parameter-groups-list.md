---
title: List Parameter Groups in Azure HorizonDB
description: This article describes how to list parameter groups in Azure HorizonDB.
#customer intent: As an user, I want to list all parameter groups in my subscription, so that I can review my current configuration inventory.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: parameters-group
ms.topic: how-to
---

# List parameter groups in Azure HorizonDB (Preview)

When you list parameter groups, you can scope the operation to a single parameter group, to all parameter groups in a resource group, or to all parameter groups in any resource group of a given subscription.

## Steps to list parameter groups

### [Portal](#tab/portal-list-parameter-groups)

Use the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview) parameter groups**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2F2FparameterGroups).

1. Use the filtering buttons and the search box to find the parameter groups that you want.

    :::image type="content" source="./media/how-to-list-parameter-groups/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page filtered by the name of the parameter group which you want to delete." lightbox="./media/how-to-list-parameter-groups/filter-search-parameter-groups.png":::


### [CLI](#tab/cli-list-parameter-groups)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

To list a specific parameter group, use the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}?api-version=2026-01-20-preview"
```

The output from this command looks like the following example:

```json
{
    "properties": {
        "parameters": [
            {
                "name": "{parameterName-1}",
                "description": "{parameterDescription-1}",
                "value": "{parameterValue-1}",
                "dataType": "{parameterDataType-1}",
                "allowedValues": "{parameterAllowedValues-1}",
                "documentationLink": "{parameterDocumentationLink-1}",
                "unit": "{parameterUnit-1}",
                "isDynamic": {parameterIsDynamic-1},
                "isReadOnly": {parameterIsReadOnly-1}
            },
      .
      .
      .
            {
                "name": "{parameterName-N}",
                "description": "{parameterDescription-N}",
                "value": "{parameterValue-N}",
                "dataType": "{parameterDataType-N}",
                "allowedValues": "{parameterAllowedValues-N}",
                "documentationLink": "{parameterDocumentationLink-N}",
                "unit": "{parameterUnit-N}",
                "isDynamic": {parameterIsDynamic-N},
                "isReadOnly": {parameterIsReadOnly-N}
            }
        ],
        "pgVersion": {postgresVersion},
        "version": {parameterGroupVersion},
        "provisioningState": "Succeeded",
        "createTime": "2026-04-26T17:17:37.1068799"
    },
    "location": "{location}",
    "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}",
    "name": "{parameterGroupName}",
    "type": "Microsoft.HorizonDB/parameterGroups"
}
```

To list all parameter groups in a resource group, use the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/parameterGroups?api-version=2026-01-20-preview"
```

To list all parameter groups in any resource group within a subscription, use the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.OrionDb/parameterGroups?api-version=2026-01-20-preview"
```

The output from either of these two commands looks like the following example:

```json
{
    "value": [
        {
            "properties": {
                "parameters": [
                    {
                        "name": "{parameterName-1}",
                        "description": "{parameterDescription-1}",
                        "value": "{parameterValue-1}",
                        "dataType": "{parameterDataType-1}",
                        "allowedValues": "{parameterAllowedValues-1}",
                        "documentationLink": "{parameterDocumentationLink-1}",
                        "unit": "{parameterUnit-1}",
                        "isDynamic": {parameterIsDynamic-1},
                        "isReadOnly": {parameterIsReadOnly-1}
                    },
              .
              .
              .
                    {
                        "name": "{parameterName-N}",
                        "description": "{parameterDescription-N}",
                        "value": "{parameterValue-N}",
                        "dataType": "{parameterDataType-N}",
                        "allowedValues": "{parameterAllowedValues-N}",
                        "documentationLink": "{parameterDocumentationLink-N}",
                        "unit": "{parameterUnit-N}",
                        "isDynamic": {parameterIsDynamic-N},
                        "isReadOnly": {parameterIsReadOnly-N}
                    }
                ],
                "pgVersion": {postgresVersion-1},
                "version": {parameterGroupVersion-1},
                "provisioningState": "Succeeded",
                "createTime": "2026-03-22T16:18:20.0000000"
            },
            "location": "{location-1}",
            "id": "/subscriptions/{subscriptionId-1}/resourceGroups/{resourceGroupName-1}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName-1}",
            "name": "{parameterGroupName-1}",
            "type": "Microsoft.HorizonDB/parameterGroups"
        },
        .
        .
        .
        {
            "properties": {
                "parameters": [
                    {
                        "name": "{parameterName-1}",
                        "description": "{parameterDescription-1}",
                        "value": "{parameterValue-1}",
                        "dataType": "{parameterDataType-1}",
                        "allowedValues": "{parameterAllowedValues-1}",
                        "documentationLink": "{parameterDocumentationLink-1}",
                        "unit": "{parameterUnit-1}",
                        "isDynamic": {parameterIsDynamic-1},
                        "isReadOnly": {parameterIsReadOnly-1}
                    },
              .
              .
              .
                    {
                        "name": "{parameterName-N}",
                        "description": "{parameterDescription-N}",
                        "value": "{parameterValue-N}",
                        "dataType": "{parameterDataType-N}",
                        "allowedValues": "{parameterAllowedValues-N}",
                        "documentationLink": "{parameterDocumentationLink-N}",
                        "unit": "{parameterUnit-N}",
                        "isDynamic": {parameterIsDynamic-N},
                        "isReadOnly": {parameterIsReadOnly-N}
                    }
                ],
                "pgVersion": {postgresVersion-N},
                "version": {parameterGroupVersion-N},
                "provisioningState": "Succeeded",
                "createTime": "2026-03-22T16:18:20.0000000"
            },
            "location": "{location-N}",
            "id": "/subscriptions/{subscriptionId-N}/resourceGroups/{resourceGroupName-N}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName-N}",
            "name": "{parameterGroupName-N}",
            "type": "Microsoft.HorizonDB/parameterGroups"
        }
    ]
}
```

Replace the placeholders:
- `{subscriptionId}` with your Azure subscription identifier.
- `{resourceGroupName}` with your resource group name.
- `{parameterGroupName}` with the parameter group name you want.

---

## Related content

- [Parameter groups in Azure HorizonDB (Preview)](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
- [Identity parameter group connected to a cluster](how-to-parameter-groups-identify-connected-cluster.md)
