---
title: List parameters with modified defaults
description: This article describes how to list all parameters with modified defaults of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 06/26/2026
ms.service: azure-database-postgresql
ms.subservice: parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to list all parameters with modified defaults of an Azure Database for PostgreSQL.
---

# List parameters with modified defaults

This article provides step-by-step instructions to list all parameters with modified defaults of an Azure Database for PostgreSQL flexible server.

## Steps to list parameters with modified defaults

### [Portal](#tab/portal-list-modified)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot showing the Parameters page." lightbox="./media/how-to-configure-parameters/parameters.png":::

1. Select the **Modified** tab. The page shows a list of parameters whose currently set value deviates from the default.

    :::image type="content" source="./media/how-to-configure-parameters/modified-parameters.png" alt-text="Screenshot showing the list of modified parameters." lightbox="./media/how-to-configure-parameters/modified-parameters.png":::

### [CLI](#tab/cli-list-modified)

Use the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command to list all parameters whose values are modified from defaults.

```azurecli-interactive
az postgres flexible-server parameter list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "[?value!=defaultValue && isReadOnly==\`false\` && name!='temp_tablespaces' && name!='vacuum_cost_page_miss'] | [].name"
```

> [!NOTE]  
> The previous CLI command doesn't consider parameters as modified if they're designated as read-only, `temp_tablespaces`, and  `vacuum_cost_page_miss`. It follows the exact same criteria as the **Parameters** page in the Azure portal.

---

## Related contents

- [List all parameters](how-to-parameters-list-all.md).
- [List read-write static parameters](how-to-parameters-list-read-write-static.md).
- [List read-write dynamic parameters](how-to-parameters-list-read-write-dynamic.md).
- [List read-only parameters](how-to-parameters-list-read-only.md).
- [Set the value of one or more parameters](how-to-parameters-set-value.md).
- [Revert one parameter to its default](how-to-parameters-revert-one-default.md).
- [Revert all parameters to their default](how-to-parameters-revert-all-default.md).
