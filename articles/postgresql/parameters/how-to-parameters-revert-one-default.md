---
title: Revert One Parameter to its Default in Azure Database for PostgreSQL Flexible Server
description: This article describes how to revert one parameter to its default of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to revert one parameter to its default value in Azure Database for PostgreSQL flexible server, so that I can undo a specific configuration change without affecting other parameters.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
---

# Revert one parameter to its default in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to revert one parameter to its default for an Azure Database for PostgreSQL flexible server.

## Steps to revert one parameter to its default

### [Portal](#tab/portal-revert-one-to-default)

Use the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot showing the Parameters page." lightbox="./media/how-to-configure-parameters/parameters.png":::

1. Select the **Modified** tab.

    :::image type="content" source="./media/how-to-configure-parameters/modified-parameters.png" alt-text="Screenshot showing the list of modified parameters." lightbox="./media/how-to-configure-parameters/modified-parameters.png":::

1. Find the read-write parameter that you want to revert to its default value. Select the ellipsis at the right end of the screen, and select **Reset to default**.

    :::image type="content" source="./media/how-to-configure-parameters/reset-one-to-default.png" alt-text="Screenshot showing how to of reset the value of one parameter to its default." lightbox="./media/how-to-configure-parameters/reset-one-to-default.png":::

> [!IMPORTANT]
> For parameters designated as read-only, selecting the ellipsis doesn't display the **Reset to default** menu option.

1. If the **Parameter type** for the parameter you want to reset to default is **Static**, the server requires a restart for the change to take effect. In this case, a dialog appears so that you can select if you want to:
    - **Save and Restart**: Persist all changes you made to all parameters whose values you modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: Persist all changes you made to all parameters whose set values changed, but defer the server restart to a later time. Until you complete the server restart action, changes to static parameters don't take effect.
    - **Cancel**: Don't implement any changes yet.

    :::image type="content" source="./media/how-to-configure-parameters/reset-one-to-default-save-restart-cancel.png" alt-text="Screenshot showing the dialog requesting a restart of the server after modifying the value of a static parameter." lightbox="./media/how-to-configure-parameters/reset-one-to-default-save-restart-cancel.png":::

### [CLI](#tab/cli-revert-one-to-default)

Use the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to revert a parameter value to its default.

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

To conditionally restart the server if the parameter change requires a restart, use the following script:

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
- [Revert all parameters to their default](how-to-parameters-revert-all-default.md).
