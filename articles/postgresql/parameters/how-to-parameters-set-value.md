---
title: Set the value of one or more parameters
description: This article describes how to set the value of one or more parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 06/26/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to set the value of one or more parameters of an Azure Database for PostgreSQL.
---

# Set the value of one or more parameters

This article provides step-by-step instructions to set the value of one or more parameters of an Azure Database for PostgreSQL flexible server.

## Steps to set the value of one or more parameters

### [Portal](#tab/portal-set-value)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot showing the Parameters page." lightbox="./media/how-to-configure-parameters/parameters.png":::

1. Find the read-write parameters you want to change, and set them to the new values.

    :::image type="content" source="./media/how-to-configure-parameters/set-value.png" alt-text="Screenshot showing how to set the value of a parameter." lightbox="./media/how-to-configure-parameters/set-value.png":::

1. An informational message shows how many parameter changes aren't saved yet. Select **Save**.

    :::image type="content" source="./media/how-to-configure-parameters/set-value-unsaved-parameters.png" alt-text="Screenshot showing the information message indicating the values of how many parameters have been changed and not saved yet." lightbox="./media/how-to-configure-parameters/set-value-unsaved-parameters.png":::

1. If the column **Parameter type** for any of the parameters you changed is **Static**, the server requires a restart for the changes to take effect. In that case, a dialog appears so that you can select if you want to:
    - **Save and Restart**: Persist all changes you made to all parameters whose values you modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: Persist all changes you made to all parameters whose set values changed, but defer the server restart to a later time. Until you complete the server restart action, changes to static parameters don't take effect.
    - **Cancel**: Don't implement any changes yet.

    :::image type="content" source="./media/how-to-configure-parameters/save-restart-cancel.png" alt-text="Screenshot showing the dialog requesting a restart of the server after modifying the value of a static parameter." lightbox="./media/how-to-configure-parameters/save-restart-cancel.png":::

### [CLI](#tab/cli-set-value)

Use the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to set the value of a parameter.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --source user-override \
  --name <parameter> \
  --value <value>
```

You can use the following script to conditionally restart the server if any of the parameter changes require a restart for the change to take effect:

```azurecli-interactive
parameters_requiring_restart=$(az postgres flexible-server parameter list \
                                 --resource-group <resource_group> \
                                 --server-name <server> \
                                 --query "[?isConfigPendingRestart==\`true\`] | length(@)")

if [ "$parameters_requiring_restart" -gt 0 ]; then
  az postgres flexible-server restart \
    --resource-group <resource_group> \
    --name <server>
fi
```

---

## Related contents

- [List all parameters](how-to-parameters-list-all.md).
- [List parameters with modified values](how-to-parameters-list-modified.md).
- [List read-write static parameters](how-to-parameters-list-read-write-static.md).
- [List read-write dynamic parameters](how-to-parameters-list-read-write-dynamic.md).
- [List read-only parameters](how-to-parameters-list-read-only.md).
- [Revert one parameter to its default](how-to-parameters-revert-one-default.md).
- [Revert all parameters to their default](how-to-parameters-revert-all-default.md).
