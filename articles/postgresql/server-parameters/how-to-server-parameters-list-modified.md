---
title: List server parameters with modified defaults
description: This article describes how to list all server parameters with modified defaults of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to list all server parameters with modified defaults of an Azure Database for PostgreSQL.
---

# List server parameters with modified defaults

This article provides step-by-step instructions to list all server parameters with modified defaults of an Azure Database for PostgreSQL flexible server.

## Steps to list server parameters with modified defaults

### [Portal](#tab/portal-list-modified)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Select the **Modified** tab. The page shows a list of parameters whose currently set value deviates from the default.

    :::image type="content" source="./media/how-to-configure-server-parameters/modified-parameters.png" alt-text="Screenshot that shows the list of modified server parameters." lightbox="./media/how-to-configure-server-parameters/modified-parameters.png":::

### [CLI](#tab/cli-list-modified)

You can list all server parameters whose values are modified from defaults, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "[?value!=defaultValue && isReadOnly==\`false\` && name!='temp_tablespaces' && name!='vacuum_cost_page_miss'] | [].name"
```

> [!NOTE]  
> Previous CLI command doesn't consider modified server parameters the ones which are designated as read-only, `temp_tablespaces`, and  `vacuum_cost_page_miss`, following the exact same criteria as the **Server parameters** page in the Azure portal.

---

## Related contents

- [List all server parameters](how-to-server-parameters-list-all.md).
- [List read-write static server parameters](how-to-server-parameters-list-read-write-static.md).
- [List read-write dynamic server parameters](how-to-server-parameters-list-read-write-dynamic.md).
- [List read-only server parameters](how-to-server-parameters-list-read-only.md).
- [Set the value of one or more server parameters](how-to-server-parameters-set-value.md).
- [Revert one server parameter to its default](how-to-server-parameters-revert-one-default.md).
- [Revert all server parameters to their default](how-to-server-parameters-revert-all-default.md).
