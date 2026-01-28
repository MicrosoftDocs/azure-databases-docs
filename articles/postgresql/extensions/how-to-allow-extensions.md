---
title: Allow extensions
description: This article describes how to allow extensions in an Azure Database for PostgreSQL flexible server instance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/17/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to allow extensions in an Azure Database for PostgreSQL flexible server instance.
---

# Allow extensions


Before creating extensions for an Azure Database for PostgreSQL flexible server instance, you must allowlist them.

## Steps to allow extensions

### [Portal](#tab/allow-extensions-portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. From the resource menu, under **Settings** section, select **Server parameters**.

    :::image type="content" source="media/how-to-allow-extensions/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="media/how-to-allow-extensions/server-parameters.png":::

3. Select the extensions that you want to allowlist, from the ones available in the `azure.extensions` parameter.

    :::image type="content" source="media/how-to-allow-extensions/allow-list.png" alt-text="Screenshot that shows how to allowlist some extensions." lightbox="media/how-to-allow-extensions/allow-list.png":::

4. Select **Save**.

    :::image type="content" source="media/how-to-allow-extensions/save-extensions.png" alt-text="Screenshot that shows the Save button in the Server parameters page." lightbox="media/how-to-allow-extensions/save-extensions.png":::

### [CLI](#tab/allow-extensions-cli)

You can allow extensions via the CLI parameter set [command](/cli/azure/postgres/flexible-server/parameter).

```azurecli-interactive
    az postgres flexible-server parameter set --resource-group <resource_group>  --server-name <server> --subscription <subscription_id> --name azure.extensions --value <extension_name>,<extension_name>
```

### [Resource Manager Template](#tab/allow-extensions-azure-resource-manager)

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

## Related content

- [Extensions and modules](concepts-extensions.md)
- [Special considerations with extensions and modules](concepts-extensions-considerations.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
