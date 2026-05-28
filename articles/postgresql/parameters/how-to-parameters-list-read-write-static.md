---
title: List read-write static parameters
description: This article describes how to list read-write static parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to list read-write static parameters of an Azure Database for PostgreSQL.
---

# List read-write static parameters

This article provides step-by-step instructions to list read-write static parameters of an Azure Database for PostgreSQL flexible server.

## Steps to list read-write static parameters

### [Portal](#tab/portal-list-static)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot that shows the Parameters menu option." lightbox="./media/how-to-configure-parameters/parameters.png":::

3. Select the **Static** tab. The page shows a list of read-write parameters for which, if their value is changed, require a restart of the server for the new value to take effect.

    :::image type="content" source="./media/how-to-configure-parameters/static-parameters.png" alt-text="Screenshot that shows the list of static parameters." lightbox="./media/how-to-configure-parameters/static-parameters.png":::

### [CLI](#tab/cli-list-static)

You can list all parameters that require a restart, for changes to take effect, via the [az postgres flexible-parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-parameter-list) command.

```azurecli-interactive
az postgres flexible-parameter list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "[?isDynamicConfig==\`false\` && isReadOnly==\`false\`] | [].name"
```

---

## Related contents

- [List all parameters](how-to-parameters-list-all.md).
- [List parameters with modified values](how-to-parameters-list-modified.md).
- [List read-write dynamic parameters](how-to-parameters-list-read-write-dynamic.md).
- [List read-only parameters](how-to-parameters-list-read-only.md).
- [Set the value of one or more parameters](how-to-parameters-set-value.md).
- [Revert one parameter to its default](how-to-parameters-revert-one-default.md).
- [Revert all parameters to their default](how-to-parameters-revert-all-default.md).
