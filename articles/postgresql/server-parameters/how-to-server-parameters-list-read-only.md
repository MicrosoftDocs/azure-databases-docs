---
title: List read-only dynamic server parameters
description: This article describes how to list read-only dynamic server parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to list read-only dynamic server parameters of an Azure Database for PostgreSQL.
---

# List read-only server parameters

This article provides step-by-step instructions to list read-only dynamic server parameters of an Azure Database for PostgreSQL flexible server.

## Steps to list read-only server parameters

### [Portal](#tab/portal-list-read-only)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Select the **Read-Only** tab. The page shows a list of read-only parameters.

    :::image type="content" source="./media/how-to-configure-server-parameters/read-only-parameters.png" alt-text="Screenshot that shows the list of read-only server parameters." lightbox="./media/how-to-configure-server-parameters/read-only-parameters.png":::

### [CLI](#tab/cli-list-read-only)

You can list all server parameters that are designated as read-only, the ones the user can't change, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "[?isReadOnly==\`true\`] | [].name"
```

---

## Related contents

- [List all server parameters](how-to-server-parameters-list-all.md).
- [List server parameters with modified values](how-to-server-parameters-list-modified.md).
- [List read-write static server parameters](how-to-server-parameters-list-read-write-static.md).
- [List read-write dynamic server parameters](how-to-server-parameters-list-read-write-dynamic.md).
- [Set the value of one or more server parameters](how-to-server-parameters-set-value.md).
- [Revert one server parameter to its default](how-to-server-parameters-revert-one-default.md).
- [Revert all server parameters to their default](how-to-server-parameters-revert-all-default.md).
