---
title: Load Libraries in Azure HorizonDB
description: This article describes how to load libraries in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to load libraries in Azure HorizonDB.
---

# Load libraries in Azure HorizonDB

`shared_preload_libraries` is a server configuration parameter that determines which libraries have to be loaded when an Azure HorizonDB instance starts. Any libraries that use shared memory must be loaded via this parameter. If your extension needs to be added to the shared preload libraries, follow these steps:

## Steps to load libraries

### [Portal](#tab/load-libraries-portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB instance.

1. From the resource menu, under **Settings** section, select **Server parameters**.

   :::image type="content" source="media/how-to-allow-extensions/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="media/how-to-allow-extensions/server-parameters.png":::

1. Include the libraries that you want to add in the value of `shared_preload_libraries`.

   :::image type="content" source="media/how-to-load-libraries/shared-libraries.png" alt-text="Screenshot that shows how to select libraries to be loaded in memory when the server starts." lightbox="media/how-to-load-libraries/shared-libraries.png":::

1. Select **Save**.

   :::image type="content" source="media/how-to-load-libraries/save-libraries.png" alt-text="Screenshot that shows the Save button in the Server parameters page." lightbox="media/how-to-load-libraries/save-libraries.png":::

1. Because `shared_preload_libraries` is a static server parameter, it requires a server restart so that the changes take effect.

   :::image type="content" source="media/how-to-load-libraries/save-and-restart.png" alt-text="Screenshot of Server parameters page, showing the dialog from which you can save changes and restart." lightbox="media/how-to-load-libraries/save-and-restart.png":::

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

- [Extensions and modules in Azure HorizonDB](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB](concepts-extensions-by-engine.md)
