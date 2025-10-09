---
title: Load libraries
description: This article describes how to load libraries in an Azure Database for PostgreSQL flexible server instance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/17/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to load libraries in an Azure Database for PostgreSQL flexible server instance.
---

# Load libraries


`shared_preload_libraries` is a server configuration parameter that determines which libraries have to be loaded when an Azure Database for PostgreSQL flexible server instance starts. Any libraries that use shared memory must be loaded via this parameter. If your extension needs to be added to the shared preload libraries, follow these steps:

## Steps to load libraries

### [Portal](#tab/load-libraries-portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. From the resource menu, under **Settings** section, select **Server parameters**.

    :::image type="content" source="media/how-to-allow-extensions/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="media/how-to-allow-extensions/server-parameters.png":::

3. Include the libraries that you want to add in the value of `shared_preload_libraries`.

    :::image type="content" source="media/how-to-allow-extensions/shared-libraries.png" alt-text="Screenshot that shows how to select libraries to be loaded in memory when the server starts." lightbox="media/how-to-allow-extensions/shared-libraries.png":::

4. Select **Save**.

    :::image type="content" source="media/how-to-allow-extensions/save-libraries.png" alt-text="Screenshot that shows the Save button in the Server parameters page." lightbox="media/how-to-allow-extensions/save-libraries.png":::

5. Because `shared_preload_libraries` is a static server parameter, it requires a server restart so that the changes take effect.

    :::image type="content" source="media/how-to-allow-extensions/save-and-restart.png" alt-text="Screenshot of Server parameters page, showing the dialog from which you can save changes and restart." lightbox="media/how-to-allow-extensions/save-and-restart.png":::

### [CLI](#tab/load-libraries-cli)

You can set `shared_preload_libraries` using the CLI [parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name shared_preload_libraries \
  --value <extension_name>,<extension_name>
```

And can restart the server using the CLI [restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server>
```

---

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
