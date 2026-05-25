---
title: List Parameter Groups
description: This article describes how to list parameter groups in Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
# customer intent: As a user, I want to learn how to list parameter groups in Azure HorizonDB.
---

# List parameter groups

When listing parameter groups, you can scope the operation to a single parameter group, to all parameter groups in a resource group, or to all parameter groups in any resource group of a given subscription.

## Steps to list parameter groups

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview) parameter groups**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2F2FparameterGroups).

1. By using the filtering buttons and the search box, find the parameter groups which you're looking for.

    :::image type="content" source="./media/how-to-list-parameter-groups/filter-search-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page filtered by the name of the parameter group which you want to delete." lightbox="./media/how-to-list-parameter-groups/filter-search-parameter-groups.png":::


### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can list one specific parameter group using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}?api-version=2026-01-20-Preview"
```

The output that command returns would look like the following:

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

You can list all parameter groups in a given resource group using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OrionDb/parameterGroups?api-version=2026-01-20-Preview"
```

You can list all parameter groups in any resource group of a given subscription using the `az rest` command:

```azurecli-interactive
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.OrionDb/parameterGroups?api-version=2026-01-20-Preview"
```

The output either of the two previous commands return would look like the following:

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
- `{parameterGroupName}` with the desired parameter group name.

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Create parameter groups](how-to-parameter-groups-create.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
- [Identity parameter group connected to a cluster](how-to-parameter-groups-identify-connected-cluster.md)
