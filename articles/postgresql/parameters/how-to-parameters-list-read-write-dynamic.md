---
title: List read-write dynamic parameters
description: This article describes how to list read-write dynamic parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 06/26/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to list read-write dynamic parameters of an Azure Database for PostgreSQL.
---

# List read-write dynamic parameters

This article provides step-by-step instructions to list read-write dynamic parameters of an Azure Database for PostgreSQL flexible server.

## Steps to list read-write dynamic parameters

### [Portal](#tab/portal-list-dynamic)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot showing the Parameters page." lightbox="./media/how-to-configure-parameters/parameters.png":::

1. Select the **Dynamic** tab. The page shows a list of read-write parameters for which, if you change their value, the new value takes effect **immediately without requiring a server restart**.

    :::image type="content" source="./media/how-to-configure-parameters/dynamic-parameters.png" alt-text="Screenshot showing the list of dynamic parameters." lightbox="./media/how-to-configure-parameters/dynamic-parameters.png":::

### [CLI](#tab/cli-list-dynamic)

Use the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command to list all parameters that don't require a restart after you change their values.

```azurecli-interactive
az postgres flexible-server parameter list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "[?isDynamicConfig==\`true\` && isReadOnly==\`false\`] | [].name"
```

---

## Related contents

- [List all parameters](how-to-parameters-list-all.md).
- [List parameters with modified values](how-to-parameters-list-modified.md).
- [List read-write static parameters](how-to-parameters-list-read-write-static.md).
- [List read-only parameters](how-to-parameters-list-read-only.md).
- [Set the value of one or more parameters](how-to-parameters-set-value.md).
- [Revert one parameter to its default](how-to-parameters-revert-one-default.md).
- [Revert all parameters to their default](how-to-parameters-revert-all-default.md).
