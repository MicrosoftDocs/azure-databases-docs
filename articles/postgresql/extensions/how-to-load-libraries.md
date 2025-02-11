---
title: Load Libraries
description: This article describes how to load libraries in an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to load libraries in an Azure Database for PostgreSQL flexible server.
---

# Load libraries

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

`shared_preload_libraries` is a server configuration parameter that determines which libraries have to be loaded when Azure Database for PostgreSQL flexible server starts. Any libraries that use shared memory must be loaded via this parameter. If your extension needs to be added to the shared preload libraries, follow these steps:

## Steps to load libraries

### [Portal](#tab/load-libraries-portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.
1. From the resource menu, under **Settings** section, select **Server parameters**.
1. Include the libraries you wish to add in the value of `shared_preload_libraries`, and select **Save**.

    :::image type="content" source="media/how-to-allow-extensions/shared-libraries.png" alt-text="Screenshot of Server parameters page while setting shared_preload_libraries." lightbox="media/how-to-allow-extensions/shared-libraries.png":::

1. Because `shared_preload_libraries`is a static server parameter, it requires a server restart so that the changes take effect.

    :::image type="content" source="media/how-to-allow-extensions/save-and-restart.png" alt-text="Screenshot of Server parameters page, showing the dialog from which you can save changes and restart." lightbox="media/how-to-allow-extensions/save-and-restart.png":::

### [CLI](#tab/load-libraries-cli)

You can set `shared_preload_libraries` using the CLI [parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set --resource-group <resource_group> --server-name <server> --name shared_preload_libraries --value <extension_name>,<extension_name>
```

And can restart the server using the CLI [parameter set](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

```azurecli-interactive
az postgres flexible-server restart --resource-group <resource_group> --name <server>
```

---

## Related content

- [Allow extensions](how-to-allow-extensions.md)
- [Create extensions](how-to-create-extensions.md)
- [Drop extensions](how-to-drop-extensions.md)
- [Update extensions](how-to-update-extensions.md)
- [View installed extensions](how-to-view-installed-extensions.md)
