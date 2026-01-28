---
title: Revert one server parameter to its default
description: This article describes how to revert one server parameter to its default of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to revert one server parameter to its default of an Azure Database for PostgreSQL.
---

# Revert one server parameter to its default

This article provides step-by-step instructions to revert one server parameter to its default of an Azure Database for PostgreSQL flexible server.

## Steps to revert one server parameter to its default

### [Portal](#tab/portal-revert-one-to-default)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Select the **Modified** tab.

    :::image type="content" source="./media/how-to-configure-server-parameters/modified-parameters.png" alt-text="Screenshot that shows the list of modified server parameters." lightbox="./media/how-to-configure-server-parameters/modified-parameters.png":::

4. Locate the read-write parameter whose current value you want to revert to its default, select the ellipsis at the right end side of the screen, and select **Reset to default**.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-one-to-default.png" alt-text="Screenshot of resetting the value of one server parameter to its default." lightbox="./media/how-to-configure-server-parameters/reset-one-to-default.png":::

> [!IMPORTANT]
> For parameters designated as read-only, selecting the ellipsis doesn't pop up the **Reset to default** menu option.

5. If the column **Parameter type** for the parameter you're trying to reset to default is equal to **Static**, the server requires a restart for the change to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: In case you want to persist all changes made to all parameters whose values were modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: In case you want to persist all changes made to all parameters whose set values changed, but want to defer the server restart to a later time. Until you don't complete the server restart action, changes made to any static server parameters don't take effect.
    - **Cancel**: To not implement any changes yet.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-one-to-default-save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after modifying the value of a static parameter." lightbox="./media/how-to-configure-server-parameters/reset-one-to-default-save-restart-cancel.png":::

### [CLI](#tab/cli-revert-one-to-default)

You can revert the value of a server parameter to its default via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --source user-override \
  --name <parameter> \
  --value $(az postgres flexible-server parameter show \
              --resource-group <resource_group> \
              --server-name <server> \
              --name <parameter> \
              --output tsv) 
```

And you can use the following script to conditionally restart the server, if the parameter changed requires a restart for the change to take effect:

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
- [Revert all server parameters to their default](how-to-server-parameters-revert-all-default.md).
