---
title: List read-only dynamic parameters
description: This article describes how to list read-only dynamic parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 06/26/2026
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to list read-only dynamic parameters of an Azure Database for PostgreSQL.
---

# List read-only parameters

This article provides step-by-step instructions to list read-only dynamic parameters of an Azure Database for PostgreSQL flexible server.

## Steps to list read-only parameters

### [Portal](#tab/portal-list-read-only)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under **Settings**, select **Parameters**.

    :::image type="content" source="./media/how-to-configure-parameters/parameters.png" alt-text="Screenshot showing the Parameters page." lightbox="./media/how-to-configure-parameters/parameters.png":::

1. Select the **Read-Only** tab. The page shows a list of read-only parameters.

    :::image type="content" source="./media/how-to-configure-parameters/read-only-parameters.png" alt-text="Screenshot showing the list of read-only parameters." lightbox="./media/how-to-configure-parameters/read-only-parameters.png":::

### [CLI](#tab/cli-list-read-only)

Use the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command to list all parameters that are designated as read-only (the ones you can't change).

```azurecli-interactive
az postgres flexible-server parameter list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "[?isReadOnly==\`true\`] | [].name"
```

---

## Related contents

- [List all parameters](how-to-parameters-list-all.md).
- [List parameters with modified values](how-to-parameters-list-modified.md).
- [List read-write static parameters](how-to-parameters-list-read-write-static.md).
- [List read-write dynamic parameters](how-to-parameters-list-read-write-dynamic.md).
- [Set the value of one or more parameters](how-to-parameters-set-value.md).
- [Revert one parameter to its default](how-to-parameters-revert-one-default.md).
- [Revert all parameters to their default](how-to-parameters-revert-all-default.md).
