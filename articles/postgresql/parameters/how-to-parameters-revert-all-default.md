---
title: Revert all parameters to their default values
description: This article describes how to revert all parameters to their default values of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 06/26/2026
ms.service: azure-database-postgresql
ms.subservice: parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to revert all parameters to their default values of an Azure Database for PostgreSQL.
---

# Revert all parameters to their default values

This article provides step-by-step instructions to revert all parameters to their default values for an Azure Database for PostgreSQL flexible server.

## Steps to revert all parameters to their default values

### [Portal](#tab/portal-revert-all-to-default)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot showing the Parameters page." lightbox="./media/how-to-configure-parameters/parameters.png":::

1. Select the **Modified** tab.

    :::image type="content" source="./media/how-to-configure-parameters/modified-parameters.png" alt-text="Screenshot showing the list of modified parameters." lightbox="./media/how-to-configure-parameters/modified-parameters.png":::

1. Select **Reset all to default**.

    :::image type="content" source="./media/how-to-configure-parameters/reset-all-to-default.png" alt-text="Screenshot showing the Reset all to default button." lightbox="./media/how-to-configure-parameters/reset-all-to-default.png":::

1. If you want to proceed with resetting all modified parameters to their default values, confirm the operation in the **Reset all to default values** dialog.

    :::image type="content" source="./media/how-to-configure-parameters/reset-all-to-default-confirm.png" alt-text="Screenshot that shows the Reset all to default values confirmation dialog." lightbox="./media/how-to-configure-parameters/reset-all-to-default-confirm.png":::

1. If, for any of the parameters whose current value doesn't match their default, the column **Parameter type** is equal to **Static**, the server requires a restart for the change to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: Persist all changes you made to all parameters whose values you modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: Persist all changes you made to all parameters whose set values changed, but defer the server restart to a later time. Until you complete the server restart action, changes to static parameters don't take effect.
    - **Cancel**: Don't implement any changes yet.

    :::image type="content" source="./media/how-to-configure-parameters/reset-all-to-default-save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after having reset all to default." lightbox="./media/how-to-configure-parameters/reset-all-to-default-save-restart-cancel.png":::

### [CLI](#tab/cli-revert-all-to-default)

Use the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to revert the value of all read-write parameters to their default values.

```azurecli-interactive
parameters_to_reset=$(az postgres flexible-server parameter list \
                        --resource-group <resource_group> \
                        --server-name <server> \
                        --query "[?value!=defaultValue && isReadOnly==\`false\`].name" \
                        -output tsv)
for parameter_to_reset in $parameters_to_reset; do
  az postgres flexible-server parameter set \
    --resource-group <resource_group> \
    --server-name <server> \
    --name $parameter_to_reset \
    --value $(az postgres flexible-server parameter show \
                --resource-group <resource_group> \
                --server-name <server> \
                --name $parameter_to_reset \
                --output tsv)
done
```

To conditionally restart the server if any parameter changes require a restart, use the following script:

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
- [Set the value of one or more parameters](how-to-parameters-set-value.md).
- [Revert one parameter to its default](how-to-parameters-revert-one-default.md).
