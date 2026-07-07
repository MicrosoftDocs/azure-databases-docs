---
title: Load Libraries in Azure HorizonDB
description: This article describes how to load libraries in Azure HorizonDB.
#customer intent: As a user, I want to load libraries in Azure HorizonDB so that I can enable extensions that use shared memory.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: extensions-modules
ms.topic: how-to
---

# Load libraries in Azure HorizonDB (Preview)

The `shared_preload_libraries` parameter determines which libraries load when an Azure HorizonDB cluster starts. You must load any libraries that use shared memory through this parameter. If you need to add your extension to the shared preload libraries, follow these steps:

## Steps to load libraries

[Create a parameter group](../parameters/how-to-parameter-groups-create.md) that modifies the value of `shared_preload_libraries` and assign it a comma-separated list of libraries you want to load.

Then, [connect your cluster to that parameter group](../parameters/how-to-parameter-groups-connect.md) for the value to take effect.

Because `shared_preload_libraries` is a static parameter, it requires a restart of your cluster. The restart occurs as soon as you connect the parameter group to the cluster.
<!--
### [Portal](#tab/load-libraries-portal)

Use the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB instance.

1. From the resource menu, under the **Settings** section, select **Parameters**.

   :::image type="content" source="media/how-to-allow-extensions/parameters.png" alt-text="Screenshot that shows the Parameters menu option." lightbox="media/how-to-allow-extensions/parameters.png":::

1. Add the libraries you want to include in the value of `shared_preload_libraries`.

   :::image type="content" source="media/how-to-load-libraries/shared-libraries.png" alt-text="Screenshot that shows how to select libraries to be loaded in memory when the server starts." lightbox="media/how-to-load-libraries/shared-libraries.png":::

1. Select **Save**.

   :::image type="content" source="media/how-to-load-libraries/save-libraries.png" alt-text="Screenshot that shows the Save button in the Parameters page." lightbox="media/how-to-load-libraries/save-libraries.png":::

1. Because `shared_preload_libraries` is a static parameter, it requires a server restart for the changes to take effect.

   :::image type="content" source="media/how-to-load-libraries/save-and-restart.png" alt-text="Screenshot of Parameters page, showing the dialog from which you can save changes and restart." lightbox="media/how-to-load-libraries/save-and-restart.png":::

### [CLI](#tab/load-libraries-cli)

Use the CLI [parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command to set `shared_preload_libraries`.

```azurecli-interactive
az postgres flexible-Parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name shared_preload_libraries \
  --value <extension_name>,<extension_name>
```

Use the CLI [restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command to restart the server.

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server>
```

---
-->

## Related content

- [Extensions and modules in Azure HorizonDB (Preview)](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB (Preview)](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB (Preview)](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB (Preview)](concepts-extensions-by-engine.md)
