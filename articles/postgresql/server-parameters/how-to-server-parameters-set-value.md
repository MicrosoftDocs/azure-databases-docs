---
title: Set the value of one or more server parameters
description: This article describes how to set the value of one or more server parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to set the value of one or more server parameters of an Azure Database for PostgreSQL.
---

# Set the value of one or more server parameters

This article provides step-by-step instructions to set the value of one or more server parameters of an Azure Database for PostgreSQL flexible server.

## Steps to set the value of one or more server parameters

### [Portal](#tab/portal-set-value)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Locate the read-write parameters whose current values you want to change, and set them to the new desired values.

    :::image type="content" source="./media/how-to-configure-server-parameters/set-value.png" alt-text="Screenshot that shows how to set the value of a server parameter." lightbox="./media/how-to-configure-server-parameters/set-value.png":::

4. Observe that an informational message indicates how many server parameter changes aren't saved yet, and select **Save**.

    :::image type="content" source="./media/how-to-configure-server-parameters/set-value-unsaved-parameters.png" alt-text="Screenshot that shows the information message indicating the values of how many server parameters have been changed and not saved yet." lightbox="./media/how-to-configure-server-parameters/set-value-unsaved-parameters.png":::

5. If the column **Parameter type** for any of the parameters changed is equal to **Static**, the server requires a restart for the changes to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: In case you want to persist all changes made to all parameters whose values were modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: In case you want to persist all changes made to all parameters whose set values changed, but want to defer the server restart to a later time. Until you don't complete the server restart action, changes made to any static server parameters don't take effect.
    - **Cancel**: To not implement any changes yet.

    :::image type="content" source="./media/how-to-configure-server-parameters/save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after modifying a static parameter." lightbox="./media/how-to-configure-server-parameters/save-restart-cancel.png":::

### [CLI](#tab/cli-set-value)

You can set the value of a server parameter via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --source user-override \
  --name <parameter> \
  --value <value>
```

And you can use the following script to conditionally restart the server, if any of the parameters changed require a restart for the change to take effect:

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
- [Revert one server parameter to its default](how-to-server-parameters-revert-one-default.md).
- [Revert all server parameters to their default](how-to-server-parameters-revert-all-default.md).
