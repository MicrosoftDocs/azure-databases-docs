---
title: Allow Extensions in Azure HorizonDB
description: This article describes how to allow extensions in Azure HorizonDB.
#customer intent: As a user, I want to allow extensions in Azure HorizonDB, so that I can add specialized features to my database.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: extensions-modules
ms.topic: how-to
---

# Allow extensions in Azure HorizonDB (Preview)

Extensions enhance the functionality of Azure HorizonDB by adding specialized features and capabilities to your database. Before you can create and use extensions in Azure HorizonDB, you must first allowlist them through your cluster configuration. This article guides you through the process of allowlisting extensions by using the Azure portal, Azure CLI, or Azure Resource Manager templates.

## Steps to allow extensions

To allow an extension in Azure HorizonDB, [create a parameter group](../parameters/how-to-parameter-groups-create.md) and set the value of the `azure.extensions` parameter to include the extensions that you want to allowlist.

Then, [connect your cluster to that parameter group](../parameters/how-to-parameter-groups-connect.md) for the value to take effect.

<!--
### [Portal](#tab/allow-extensions-portal)

Use the [Azure portal](https://portal.azure.com):

1. Select your Azure HorizonDB instance.

1. From the resource menu, under the **Settings** section, select **Parameters**.

   :::image type="content" source="media/how-to-allow-extensions/parameters.png" alt-text="Screenshot that shows the Parameters menu option." lightbox="media/how-to-allow-extensions/parameters.png":::

1. Select the extensions that you want to allowlist from the ones available in the `azure.extensions` parameter.

   :::image type="content" source="media/how-to-allow-extensions/allow-list.png" alt-text="Screenshot that shows how to allowlist some extensions." lightbox="media/how-to-allow-extensions/allow-list.png":::

1. Select **Save**.

   :::image type="content" source="media/how-to-allow-extensions/save-extensions.png" alt-text="Screenshot that shows the Save button in the Parameters page." lightbox="media/how-to-allow-extensions/save-extensions.png":::

### [CLI](#tab/allow-extensions-cli)

You can allow extensions by using the CLI parameter set. For more information, see [command](/cli/azure/postgres/flexible-server/parameter).

```azurecli-interactive
    az postgres flexible-Parameter set --resource-group <resource_group>  --server-name <server> --subscription <subscription_id> --name azure.extensions --value <extension_name>,<extension_name>
```

### [Resource Manager Template](#tab/allow-extensions-azure-resource-manager)

To allow extensions, use the [ARM Template](/azure/azure-resource-manager/templates/):

The following example adds extensions to the allow list: `dblink`, `dict_xsyn`, and `pg_buffercache` on a server named `postgres-test-server`:

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
-->

## Related content

- [Extensions and modules in Azure HorizonDB (Preview)](concepts-extensions.md)
- [Considerations with the use of extensions and modules in Azure HorizonDB (Preview)](concepts-extensions-considerations.md)
- [List of extensions and modules by name in Azure HorizonDB (Preview)](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL in Azure HorizonDB (Preview)](concepts-extensions-by-engine.md)
