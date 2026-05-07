---
title: Allow Extensions in Azure HorizonDB
description: This article describes how to allow extensions in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: how-to
# customer intent: As a user, I want to learn how to allow extensions in Azure HorizonDB.
---

# Allow extensions in Azure HorizonDB

Before creating extensions in Azure HorizonDB, you must allowlist them.

## Steps to allow extensions

### [Portal](#tab/allow-extensions-portal)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB instance.

1. From the resource menu, under **Settings** section, select **Server parameters**.

   :::image type="content" source="media/how-to-allow-extensions/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="media/how-to-allow-extensions/server-parameters.png":::

1. Select the extensions that you want to allowlist, from the ones available in the `azure.extensions` parameter.

   :::image type="content" source="media/how-to-allow-extensions/allow-list.png" alt-text="Screenshot that shows how to allowlist some extensions." lightbox="media/how-to-allow-extensions/allow-list.png":::

1. Select **Save**.

   :::image type="content" source="media/how-to-allow-extensions/save-extensions.png" alt-text="Screenshot that shows the Save button in the Server parameters page." lightbox="media/how-to-allow-extensions/save-extensions.png":::

### [CLI](#tab/allow-extensions-cli)

You can allow extensions via the CLI parameter set [command](/cli/azure/postgres/flexible-server/parameter).

```azurecli-interactive
    az postgres flexible-server parameter set --resource-group <resource_group>  --server-name <server> --subscription <subscription_id> --name azure.extensions --value <extension_name>,<extension_name>
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

- [Extensions and modules in Azure HorizonDB](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB](concepts-extensions-by-engine.md)
