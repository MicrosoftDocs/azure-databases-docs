---
title: Revert all server parameters to their defaults
description: This article describes how to revert all server parameters to their defaults of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to revert all server parameters to their defaults of an Azure Database for PostgreSQL.
---

# Revert all server parameters to their defaults

This article provides step-by-step instructions to revert all server parameters to their defaults of an Azure Database for PostgreSQL flexible server.

## Steps to revert all server parameters to their defaults

### [Portal](#tab/portal-revert-all-to-default)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Select the **Modified** tab.

    :::image type="content" source="./media/how-to-configure-server-parameters/modified-parameters.png" alt-text="Screenshot that shows the list of modified server parameters." lightbox="./media/how-to-configure-server-parameters/modified-parameters.png":::

4. Select **Reset all to default**.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-all-to-default.png" alt-text="Screenshot that shows the Reset all to default button." lightbox="./media/how-to-configure-server-parameters/reset-all-to-default.png":::

5. If you want to proceed with resetting all modified server parameters to their default values, confirm the operation in the **Reset all to default values** dialog.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-all-to-default-confirm.png" alt-text="Screenshot that shows the Reset all to default values confirmation dialog." lightbox="./media/how-to-configure-server-parameters/reset-all-to-default-confirm.png":::

6. If, for any of the parameters whose current value doesn't match their default, the column **Parameter type** is equal to **Static**, the server requires a restart for the change to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: In case you want to persist all changes made to all parameters whose values were modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: In case you want to persist all changes made to all parameters whose set values changed, but want to defer the server restart to a later time. Until you don't complete the server restart action, changes made to any static server parameters don't take effect.
    - **Cancel**: To not implement any changes yet.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-all-to-default-save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after having reset all to default." lightbox="./media/how-to-configure-server-parameters/reset-all-to-default-save-restart-cancel.png":::

### [CLI](#tab/cli-revert-all-to-default)

You can revert the value of all read-write server parameters to their defaults via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

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

And you can use the following script to conditionally restart the server, if any of the parameters changed require a restart for their change to take effect:

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

- [List all server parameters](how-to-server-parameters-list-all.md).
- [List server parameters with modified values](how-to-server-parameters-list-modified.md).
- [List read-write static server parameters](how-to-server-parameters-list-read-write-static.md).
- [List read-write dynamic server parameters](how-to-server-parameters-list-read-write-dynamic.md).
- [List read-only server parameters](how-to-server-parameters-list-read-only.md).
- [Set the value of one or more server parameters](how-to-server-parameters-set-value.md).
- [Revert one server parameter to its default](how-to-server-parameters-revert-one-default.md).
