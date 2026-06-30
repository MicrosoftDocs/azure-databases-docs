---
title: Load Libraries
description: This article describes how to load libraries in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan, randolphwest
ms.date: 06/23/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to load libraries in an Azure Database for PostgreSQL flexible server.
---

# Load libraries

The server configuration parameter `shared_preload_libraries` determines which libraries load when an Azure Database for PostgreSQL flexible server starts. You must use this parameter to load any libraries that use shared memory. If you need to add your extension to the shared preload libraries, follow these steps:

## Steps to load libraries

### [Portal](#tab/allow-extensions-portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server.

1. From the resource menu, under the **Settings** section, select **Parameters**.

   :::image type="content" source="media/how-to-allow-extensions/parameters.png" alt-text="Screenshot showing the Parameters menu option." lightbox="media/how-to-allow-extensions/parameters.png":::

1. Add the libraries that you want to include in the value of `shared_preload_libraries`.

   :::image type="content" source="media/how-to-load-libraries/shared-libraries.png" alt-text="Screenshot showing how to select libraries to be loaded in memory when the server starts." lightbox="media/how-to-load-libraries/shared-libraries.png":::

1. Select **Save**.

   :::image type="content" source="media/how-to-load-libraries/save-libraries.png" alt-text="Screenshot that shows the Save button in the Parameters page." lightbox="media/how-to-load-libraries/save-libraries.png":::

1. Because `shared_preload_libraries` is a static parameter, it requires a server restart for the changes to take effect.

   :::image type="content" source="media/how-to-load-libraries/save-and-restart.png" alt-text="Screenshot of Parameters page, showing the dialog from which you can save changes and restart." lightbox="media/how-to-load-libraries/save-and-restart.png":::

1. A new deployment is launched to set the value of the `shared_preload_libraries` parameter on your Azure Database for PostgreSQL flexible server.

   :::image type="content" source="media/how-to-allow-extensions/deployment-progress.png" alt-text="Screenshot showing the deployment in progress to set the value of shared_preload_libraries parameter on your Azure Database for PostgreSQL flexible server." lightbox="media/how-to-allow-extensions/deployment-progress.png":::

1. When the deployment completes, select **Go to resource** to go back to your Azure Database for PostgreSQL flexible server.

   :::image type="content" source="media/how-to-allow-extensions/deployment-completed.png" alt-text="Screenshot showing the deployment successfully completed to set the value of shared_preload_libraries parameter on your Azure Database for PostgreSQL flexible server." lightbox="media/how-to-allow-extensions/deployment-completed.png":::

### [CLI](#tab/load-libraries-cli)

Use the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to set the value of `shared_preload_libraries`.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name shared_preload_libraries \
  --value <extension_name>,<extension_name>
```

Use the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command to restart the server.

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server>
```

---

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Considerations with the use of extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
