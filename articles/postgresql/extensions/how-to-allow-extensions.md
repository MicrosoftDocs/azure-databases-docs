---
title: Allow Extensions in Azure Database for PostgreSQL Flexible Server
description: This article describes how to allow extensions in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn how to allow extensions in Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan, randolphwest
ms.date: 07/10/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
---

# Allow extensions in Azure Database for PostgreSQL flexible server

Before creating extensions for an Azure Database for PostgreSQL flexible server, add them to the allow list.

## Steps to allow extensions

### [Portal](#tab/allow-extensions-portal)

Use the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. From the resource menu, under the **Settings** section, select **Parameters**.

   :::image type="content" source="media/how-to-allow-extensions/parameters.png" alt-text="Screenshot showing the Parameters menu option." lightbox="media/how-to-allow-extensions/parameters.png":::

1. Select the extensions that you want to allowlist from the ones available in the `azure.extensions` parameter.

   :::image type="content" source="media/how-to-allow-extensions/allow-list.png" alt-text="Screenshot showing how to allowlist some extensions." lightbox="media/how-to-allow-extensions/allow-list.png":::

1. Select **Save**.

   :::image type="content" source="media/how-to-allow-extensions/save-extensions.png" alt-text="Screenshot showing the Save button in the Parameters page." lightbox="media/how-to-allow-extensions/save-extensions.png":::

1. A new deployment is launched to set the value of the `azure.extensions` parameter on your Azure Database for PostgreSQL flexible server.

   :::image type="content" source="media/how-to-allow-extensions/deployment-progress.png" alt-text="Screenshot shopwing the deployment in progress to set the value of azure.extensions parameter on your Azure Database for PostgreSQL flexible server." lightbox="media/how-to-allow-extensions/deployment-progress.png":::

1. When the deployment completes, select **Go to resource** to go back to your Azure Database for PostgreSQL flexible server.

   :::image type="content" source="media/how-to-allow-extensions/deployment-completed.png" alt-text="Screenshot showing the deployment successfully completed to set the value of azure.extensions parameter on your Azure Database for PostgreSQL flexible server." lightbox="media/how-to-allow-extensions/deployment-completed.png":::

### [CLI](#tab/allow-extensions-cli)

Use the [`az postgres flexible-server parameter set`](/cli/azure/postgres/flexible-server/parameter?view=azure-cli-latest#az-postgres-flexible-server-parameter-set) command to add extensions to the allow list on your server.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name azure.extensions \
  --value "<extension_name>,<extension_name>"
```

---

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Considerations with the use of extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
