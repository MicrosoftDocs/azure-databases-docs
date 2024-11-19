---
title: How to Use PostgreSQL Extensions in Azure Database for PostgreSQL
description: Introduction to the PostgreSQL Extensions for Azure Database for PostgreSQL.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 11/19/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# How to use PostgreSQL extensions for Azure Database for PostgreSQL

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server allows you to extend the functionality of your database using extensions. Extensions bundle multiple related SQL objects in a single package that can be loaded or removed from your database with a command. After being loaded into the database, extensions function like built-in features.

## Allow extensions

Before installing extensions in Azure Database for PostgreSQL flexible server, you must allow these extensions to be listed for use.

#### [Portal](#tab/portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.
1. From the resource menu, under **Settings** section, select **Server parameters**.
1. Search for the `azure.extensions` parameter.
1. Select the extensions you wish to allow.

    :::image type="content" source="media/how-to-allow-extensions/allow-list.png" alt-text="Screenshot of allowlist." lightbox="media/how-to-allow-extensions/allow-list.png":::

#### [Azure CLI](#tab/cli)

You can allow extensions via the CLI parameter set [command](/cli/azure/postgres/flexible-server/parameter?view=azure-cli-latest&preserve-view=true).

```azurecli
    az postgres flexible-server parameter set --resource-group <resource_group>  --server-name <server> --subscription <subscription_id> --name azure.extensions --value <extension_name>,<extension_name>
```

#### [Resource Manager Template](#tab/azure-resource-manager)

Using the [ARM Template](/azure/azure-resource-manager/templates/):

The following example adds extensions to the allowlist `dblink`, `dict_xsyn`, `pg_buffercache` on a server whose name is `postgres-test-server`:

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "flexibleServers_name": {
            "defaultValue": "postgres-test-server",
            "type": "String"
        },
        "azure_extensions_set_value": {
            "defaultValue": " dblink,dict_xsyn,pg_buffercache",
            "type": "String"
        }
    },
    "variables": {},
    "resources": [
        {
            "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
            "apiVersion": "2021-06-01",
            "name": "[concat(parameters('flexibleServers_name'), '/azure.extensions')]",
            "properties": {
                "value": "[parameters('azure_extensions_set_value')]",
                "source": "user-override"
            }
        }
    ]
}
```

---

## Load libraries

`shared_preload_libraries` is a server configuration parameter that determines which libraries have to be loaded when Azure Database for PostgreSQL flexible server starts. Any libraries that use shared memory must be loaded via this parameter. If your extension needs to be added to the shared preload libraries, follow these steps:

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.
1. From the resource menu, under **Settings** section, select **Server parameters**.
1. Search for the `shared_preload_libraries` parameter.
1. Select the libraries you wish to add.

    :::image type="content" source="media/how-to-allow-extensions/shared-libraries.png" alt-text="Screenshot of shared libraries." lightbox="media/how-to-allow-extensions/shared-libraries.png":::

You can set `shared_preload_libraries` via the CLI [parameter set](/cli/azure/postgres/flexible-server/parameter?view=azure-cli-latest&preserve-view=true) command.

```azurecli
az postgres flexible-server parameter set --resource-group <resource_group> --server-name <server> --subscription <subscription_id> --name shared_preload_libraries --value <extension_name>,<extension_name>
```

## Create Extension

After extensions are allowlisted and loaded, they must be installed in each database on which they're to be used.

1. To create an extension, a user must be a member of the `azure_pg_admin` role. A member of the `azure_pg_admin` role can grant privileges to other users to create extensions.

1. Run the [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command to install a particular extension. This command loads the packaged objects into your database.

> [!NOTE]  
> Third-party extensions offered in Azure Database for PostgreSQL flexible server are open-source licensed code. We don't offer any third-party extensions or extension versions with premium or proprietary licensing models.

Azure Database for PostgreSQL flexible server instance supports a subset of key PostgreSQL extensions, as listed in the following table. This information is also available by running `SHOW azure.extensions;`. Extensions not listed in this document aren't supported on Azure Database for PostgreSQL flexible server. You can't create or load your extension in Azure Database for PostgreSQL flexible server.

## Upgrading PostgreSQL extensions

A simple command allows in-place upgrades of database extensions. This feature enables customers to automatically update their third-party extensions to the latest versions, maintaining current and secure systems without manual effort.

### Updating extensions

To update an installed extension to the latest available version supported by Azure, use the following SQL command:

```sql
ALTER EXTENSION <extension_name> UPDATE;
```

This command simplifies the management of database extensions by allowing users to manually upgrade to the latest version approved by Azure, enhancing both compatibility and security.

### Installed extensions

To list the extensions currently installed on your database, use the following SQL command:

```sql
SELECT * FROM pg_extension;
```

View the list of [available extension](concepts-extensions-versions.md).

### Limitations

While updating extensions is straightforward, there are certain limitations:

- **Selection of a specific version**: The command doesn't support updating to intermediate versions of an extension.
    - It constantly updates the [latest available version](concepts-extensions-versions.md).

- **Downgrading**: Doesn't support downgrading an extension to a previous version. If a downgrade is necessary, it might require support assistance and depends on the availability of the previous version.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Extension versions](concepts-extensions-versions.md)
- [Extension considerations](concepts-extensions-considerations.md)
- [Feedback forum](https://aka.ms/pgfeedback)
