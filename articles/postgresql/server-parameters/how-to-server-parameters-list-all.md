---
title: List all server parameters
description: This article describes how to list all server parameters of an Azure Database for PostgreSQL flexible server.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: server-parameters
ms.topic: how-to
#customer intent: As a user, I want to learn how to list all server parameters of an Azure Database for PostgreSQL.
---

# List all server parameters

This article provides step-by-step instructions to list all server parameters of an Azure Database for PostgreSQL flexible server.

## Steps to list all server parameters

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under **Settings**, select **Server parameters**.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot that shows the Server parameters menu option." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. The page shows a list of parameters, their configured values, optional units, whether they're read-only, dynamic, or static, and their descriptions.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters-all.png" alt-text="Screenshot that shows the All tab of the Server parameters page." lightbox="./media/how-to-configure-server-parameters/server-parameters-all.png":::

4. Select or hover over the **i** (information) icon to see which values are allowed for each parameter. Depending on the data type of the parameter, which can be string, enumeration, integer, boolean, numeric, set, the allowed values vary. And it can be regular expression, list of values, range of integers, on/off, range of decimals, list of values, respectively.

    :::image type="content" source="./media/how-to-configure-server-parameters/information-icon.png" alt-text="Screenshot showing balloon that pops up when hovering on the information icon." lightbox="./media/how-to-configure-server-parameters/information-icon.png":::

5. The list of server parameters supported by the instance consists of several hundred items, which are rendered in pages of 20 items each. At the bottom of the page, there's a control to inform you of the position you're at.

    :::image type="content" source="./media/how-to-configure-server-parameters/paging-position.png" alt-text="Screenshot that shows your position while paging in the Server parameters page." lightbox="./media/how-to-configure-server-parameters/paging-position.png":::

6. There's also a paging control which you can use to navigate through the whole set of pages.

    :::image type="content" source="./media/how-to-configure-server-parameters/paging.png" alt-text="Screenshot that shows the paging control in the Server parameters page." lightbox="./media/how-to-configure-server-parameters/paging.png":::

7. If needed, use the **Search to filter items...** text box to narrow down the list to those parameters containing the search term in their name or in their description.

    :::image type="content" source="./media/how-to-configure-server-parameters/search.png" alt-text="Screenshot that shows how to search in Server parameters page." lightbox="./media/how-to-configure-server-parameters/search.png":::


The **Parameter type** column can show any of the following values for each parameter:

| Parameter type | Description |
| --- | --- |
| **Static** | Requires a server restart to make the change effective. |
| **Dynamic** | Can be altered without the need to restart the server instance. However, changes will apply only to new connections established after the modification. |
| **Read-only** | Isn't user configurable, because of their critical role in maintaining reliability, security, or other operational aspects of the service. |


### [CLI](#tab/cli-list)

You can list all server parameters in a server via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list \
  --resource-group <resource_group> \
  --server-name <server>
```

Each parameter has the following attributes:

| Attribute name | Description | Possible values |
| --- | --- | --- |
| **allowedValues** | Describes the values that are allowed for the parameter. | Depending on the value of **dataType**, can be a regular expression (string), list of values (enumeration), range of integers (integer), on/off (boolean), range of decimals (numeric), list of values (set). |
| **dataType** | Type of data used for the parameter. | Can be any of `boolean`, `enumeration`, `integer`, `numeric`, `set`, `string`. |
| **defaultValue** | Value assigned to the parameter when a new server is deployed. | Varies, depending on the data type and allowed values of the parameter. |
| **description** | Brief explanation of what the parameter controls. | Textual description which is different for each parameter. |
| **documentationLink** | URL address of the page pointing to the documentation of the parameter. | Some form of URL. |
| **id** | Resource identifier that uniquely refers to the server parameter in this particular instance of flexible server. | A string that follows the pattern `/subscriptions/<subscription_identifier>/resourceGroups/<resource_group_name>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server_name>/configurations/<parameter_name>`. |
| **isConfigPendingRestart** | Indicates whether a server restart is required for the value currently set in the **value** attribute to take effect. | `true`: for parameters whose value was changed and, because they aren't dynamic (that is, they're static), require a server restart for the change to take effect. `false`: for parameters whose value currently set in the **value** attribute is in effect, and aren't waiting for a server restart to take effect. |
| **isDynamicConfig** | Indicates whether a change in the value assigned to the parameter doesn't require or requires a server restart, for the change to take effect. | `true`: for parameters that, when their value changes, the change takes effect immediately. `false`: for parameters that, when their value changes, require a server restart for the change to take effect. |
| **isReadOnly** | Indicates if the user can or can't override the default value assigned to the parameter. | `true`: for parameters that are designated as read-only and the user can't change. `false`: for parameters that are designated as read-write and the user can set to a different value than their default. |
| **name** | Name of the parameter. | Any valid name for a server parameter. |
| **resourceGroup** | Name of the resource group in which the server is deployed. | Any valid name for a resource group in Azure. |
| **source** | Source from which the value currently set for the parameter originates. | `system-default` or `user-override`, depending on whether **value** is set to the system default or the user override it. |
| **unit** | Optional text describing the units in which the parameter is expressed. | When set to something, it can be any of `8KB`, `bytes`, `days`, `KB`, `megabytes`, `microseconds`, `milliseconds`, `minutes`, `percentage`, `seconds`. |
| **value** | Value currently assigned to the parameter. | Varies, depending on the data type and allowed values of the parameter. |

---

## Related contents

- [List server parameters with modified values](how-to-server-parameters-list-modified.md).
- [List read-write static server parameters](how-to-server-parameters-list-read-write-static.md).
- [List read-write dynamic server parameters](how-to-server-parameters-list-read-write-dynamic.md).
- [List read-only server parameters](how-to-server-parameters-list-read-only.md).
- [Set the value of one or more server parameters](how-to-server-parameters-set-value.md).
- [Revert one server parameter to its default](how-to-server-parameters-revert-one-default.md).
- [Revert all server parameters to their default](how-to-server-parameters-revert-all-default.md).
