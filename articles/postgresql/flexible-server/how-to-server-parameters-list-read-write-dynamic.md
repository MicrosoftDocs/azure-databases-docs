---
title: List read-write dynamic server parameters
description: This article describes how to list read-write dynamic server parameters of an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to list read-write dynamic server parameters of an Azure Database for PostgreSQL flexible server.
---

# List read-write dynamic server parameters

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to list read-write dynamic server parameters of an Azure Database for PostgreSQL flexible server.

## Steps to list read-write dynamic server parameters

### [Portal](#tab/portal-list-dynamic)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Select the **Dynamic** tab. The page shows a list of read-write parameters for which, if their value is changed, require a restart of the server for the new value to take effect.

    :::image type="content" source="./media/how-to-configure-server-parameters/dynamic-parameters.png" alt-text="Screenshot that shows the list of dynamic server parameters." lightbox="./media/how-to-configure-server-parameters/dynamic-parameters.png":::

### [CLI](#tab/cli-list-dynamic)

You can list all server parameters that don't require a restart after their values are changed for the changes to take effect, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isDynamicConfig==\`true\` && isReadOnly==\`false\`] | [].name"
```

---

## Related contents

- [List all server parameters](how-to-server-parameters-list-all.md).
- [List server parameters with modified values](how-to-server-parameters-list-modified.md).
- [List read-write static server parameters](how-to-server-parameters-list-read-write-static.md).
- [List read-only server parameters](how-to-server-parameters-list-read-only.md).
- [Set the value of one or more server parameters](how-to-server-parameters-set-value.md).
- [Revert one server parameter to its default](how-to-server-parameters-revert-one-default.md).
- [Revert all server parameters to their default](how-to-server-parameters-revert-all-default.md).
