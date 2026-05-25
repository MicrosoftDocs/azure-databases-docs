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

When you create a parameter group, at least one parameter must be provided. The underlying operation in the backend merges your input with the system defaults for the specified `pgVersion`.

## Steps to create parameter groups

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Browse the [**Azure HorizonDB (Preview) parameter groups**](https://ms.portal.azure.com/#browse/Microsoft.HorizonDB%2F2FparameterGroups).

1. In the command bar, select **Create**.

    :::image type="content" source="./media/how-to-create-parameter-groups/browse-parameter-groups.png" alt-text="Screenshot that shows the browse for Azure HorizonDB (Preview) parameter groups page." lightbox="./media/how-to-create-parameter-groups/browse-parameter-groups.png":::

1. In the **Create a parameter group** page, select the subscription and resource group in which you want to create the parameter group.

    :::image type="content" source="./media/how-to-create-parameter-groups/select-subscription-resource-group.png" alt-text="Screenshot that shows the Create a parameter group page and a subscription and resource group selected." lightbox="./media/how-to-create-parameter-groups/select-subscription-resource-group.png":::

1. Provide a name which is unique among all the parameter groups that already exist in that resource group of that subscription. Preferably, embed some form of encoded description in the name so that you can later identify the potential target clusters of that configuration.

    :::image type="content" source="./media/how-to-create-parameter-groups/parameter-group-name.png" alt-text="Screenshot that shows the Create a parameter group page and a parameter group name provided." lightbox="./media/how-to-create-parameter-groups/parameter-group-name.png":::

1. Select a location in which you want to create the parameter group. Notice that you can only connect parameter groups created in a location to clusters that also exist in that same location.

    :::image type="content" source="./media/how-to-create-parameter-groups/location.png" alt-text="Screenshot that shows the Create a parameter group page and a location selected." lightbox="./media/how-to-create-parameter-groups/location.png":::

1. Although not required, we recommend providing a description explaining in more detail what's the purpose of the parameter group configuration you're creating. It can also describe what are the ideal target clusters for which it was conceived.

    :::image type="content" source="./media/how-to-create-parameter-groups/description.png" alt-text="Screenshot that shows the Create a parameter group page and a description provided." lightbox="./media/how-to-create-parameter-groups/description.png":::

1. Finally, select the version of PostgreSQL for which the parameter group is supported. Notice that parameter groups created for a given version of PostgreSQL can't be applied to clusters of a different version of PostgreSQL.

    :::image type="content" source="./media/how-to-create-parameter-groups/postgresql-version.png" alt-text="Screenshot that shows the Create a parameter group page and a PostgreSQL version selected." lightbox="./media/how-to-create-parameter-groups/postgresql-version.png":::

1. Select **Next** so that you can configure the values of the modifiable parameters whose defaults you want to change in this parameter group.

    :::image type="content" source="./media/how-to-create-parameter-groups/configure-parameters.png" alt-text="Screenshot that shows the Create a parameter group page and the first page of parameters available in the default parameter group selected." lightbox="./media/how-to-create-parameter-groups/configure-parameters.png":::

1. Search for the names of the parameters whose default values you want to override, and change their defaults. Once finished with the list of parameters whose defaults you want to change, select **Create**.

    :::image type="content" source="./media/how-to-create-parameter-groups/change-max-connections-parameter.png" alt-text="Screenshot that shows the Create a parameter group page and the max_connections parameter default value changed." lightbox="./media/how-to-create-parameter-groups/change-max-connections-parameter.png":::

1. A new deployment is initialized to create the parameter group.

    :::image type="content" source="./media/how-to-create-parameter-groups/initializing-deployment.png" alt-text="Screenshot that shows the Create a parameter group page and the initializing deployment notification." lightbox="./media/how-to-create-parameter-groups/initializing-deployment.png":::

1. Wait until the deployment completes.

    :::image type="content" source="./media/how-to-create-parameter-groups/deployment-progress.png" alt-text="Screenshot that shows the Deployment is in progress page." lightbox="./media/how-to-create-parameter-groups/deployment-progress.png":::

1. When the deployment completes, select **Go to resource** to visit the newly created parameter group.

    :::image type="content" source="./media/how-to-create-parameter-groups/deployment-completed.png" alt-text="Screenshot that shows the Deployment is completed page." lightbox="./media/how-to-create-parameter-groups/deployment-completed.png":::

1. You can now inspect all details associated to the newly created parameter group.

    :::image type="content" source="./media/how-to-create-parameter-groups/parameter-group-created.png" alt-text="Screenshot that shows the Overview page of the newly created parameter group." lightbox="./media/how-to-create-parameter-groups/parameter-group-created.png":::

### [CLI](#tab/cli-list)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

You can create a parameter group using the `az rest` command:

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/parameterGroups/{parameterGroupName}?api-version=2026-01-20-Preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "pgVersion": 17,
      "description": "{parameterGroupDescription}",
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
- `{parameterGroupDescription}` with the verbose description of the purpose for which this parameter group is created.

#### Possible errors

| Error code | Description |
| --- | --- |
| `ParameterGroupNameConflictsWithDefault` | When the name of the parameter group matches any of the ones reserved for default parameter groups. |
| `ParameterGroupAlreadyExists` | When a parameter group with the same resource identifier already exists. |
| `ParameterGroupPgVersionRequired` | When `pgVersion` isn't passed as one of the properties in the input. |
| `ParameterNotRecognized` | When one or more parameter names passed as input aren't recognized among the ones supported for the version of PostgreSQL for which the parameter group is defined. |
| `ParameterIsReadOnly` | When one or more parameters passed as input are read-only parameters. |
| `ParameterValueInvalid` | When the value assigned to one or more parameters passed as input isn't valid according to the data type and allowed values of that parameter. |
| `ParameterGroupParametersRequired` | When not even one parameter is passed as input. |

---

## Related content

- [Parameter groups in Azure HorizonDB](concepts-parameter-groups.md)
- [Update parameter groups](how-to-parameter-groups-update.md)
- [Delete parameter groups](how-to-parameter-groups-delete.md)
- [List parameter groups](how-to-parameter-groups-list.md)
- [Connect clusters to parameter groups](how-to-parameter-groups-connect.md)
- [List clusters connected to parameter groups](how-to-parameter-groups-list-connected.md)
- [Identity parameter group connected to a cluster](how-to-parameter-groups-identify-connected-cluster.md)
