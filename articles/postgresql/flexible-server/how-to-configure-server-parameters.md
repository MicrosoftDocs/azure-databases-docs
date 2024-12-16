---
title: Configure server parameters
description: This article describes how to configure the Postgres parameters in Azure Database for PostgreSQL - Flexible Server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 12/08/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Configure server parameters in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You can list, show, and update configuration parameters for an Azure Database for PostgreSQL flexible server instance.


## Parameter customization

Various methods and levels are available to customize your parameters according to your specific needs.

### Global level

For viewing current configured values for server parameters or for altering them  globally at the instance or server level, you can use the **Server parameters** page in the Azure portal. You can also interact with server parameters globally by using the [CLI](/cli/azure/postgres/flexible-server/parameter), the [REST API](/rest/api/postgresql/flexibleserver/configurations), [Azure Resource Manager templates](/azure/azure-resource-manager/templates/overview), or third-party IaC tools.

> [!NOTE]
> Because Azure Database for PostgreSQL is a managed database service, users don't have host or operating system access to view or modify configuration files such as *postgresql.conf*. The content of the files is automatically updated based on parameter changes that you make.

In this same article you can find sections to interact with server parameters globally to:
- [List all server parameters](#list-all-server-parameters).
- [List server parameters with modified defaults](#list-server-parameters-with-modified-defaults).
- [List read-write static server parameters](#list-read-write-static-server-parameters).
- [List read-write dynamic server parameters](#list-read-write-dynamic-server-parameters).
- [List read-only server parameters](#list-read-only-server-parameters).
- [Set the value of one or more server parameters](#set-the-value-of-one-or-more-server-parameters).
- [Revert one server parameter to its default](#revert-one-server-parameter-to-its-default).
- [Revert all server parameter to their defaults](#revert-all-server-parameters-to-their-defaults).

### Granular levels

You can adjust parameters at more granular levels. These adjustments override globally set values. Their scope and duration depend on the level at which you make them:

* **Database level**: Use the `ALTER DATABASE` command for database-specific configurations.
* **Role or user level**: Use the `ALTER USER` command for user-centric settings.
* **Function, procedure level**: When you're defining a function or procedure, you can specify or alter the configuration parameters that are used when the function is called.
* **Table level**: As an example, you can modify parameters related to autovacuum at this level.
* **Session level**: For the life of an individual database session, you can adjust specific parameters. PostgreSQL facilitates this adjustment with the following SQL commands:

  * Use the `SET` command to make session-specific adjustments. These changes serve as the default settings during the current session. Access to these changes might require specific `SET` privileges, and the limitations for modifiable and read-only parameters described earlier don't apply. The corresponding SQL function is `set_config(setting_name, new_value, is_local)`.
  * Use the `SHOW` command to examine existing parameter settings. Its SQL function equivalent is `current_setting(setting_name text)`.

## List all server parameters

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**. The page shows a list of parameters, their configured values, optional units, whether they're read-only/dynamic/static, and their descriptions.

    :::image type="content" source="./media/how-to-configure-server-parameters/server-parameters.png" alt-text="Screenshot of Server parameters page." lightbox="./media/how-to-configure-server-parameters/server-parameters.png":::

3. Select or hover over the **i** (information) icon, to see the allowed values to which each parameter can be set to. Depending on the data type of the parameter, which can be string, enumeration, integer, boolean, numeric, set, the allowed values vary. And it can be regular expression, list of values, range of integers, on/off, range of decimals, list of values, respectively.

    :::image type="content" source="./media/how-to-configure-server-parameters/information-icon.png" alt-text="Screenshot showing balloon that pops up when hovering on the information icon." lightbox="./media/how-to-configure-server-parameters/information-icon.png":::

4. The list of server parameters supported by the instance consists of several hundred items, which are rendered in pages of 20 items each. At the bottom of the page, there's a control to inform you of the position you're at. There's also a paging control which you can use to navigate through the whole set of pages.

    :::image type="content" source="./media/how-to-configure-server-parameters/paging.png" alt-text="Screenshot paging control in Server parameters page." lightbox="./media/how-to-configure-server-parameters/paging.png":::

5. If needed, use the **Search to filter items...** text box to narrow down the list to those parameters containing the search term in their name or in their description.

    :::image type="content" source="./media/how-to-configure-server-parameters/search.png" alt-text="Screenshot of search in Server parameters." lightbox="./media/how-to-configure-server-parameters/search.png":::


The **Parameter type** column can show any of the following values for each parameter:

| Parameter type | Description |
| --- | --- |
| **Static** | Requires a server restart to make the change effective. |
| **Dynamic** | Can be altered without the need to restart the server instance. However, changes will apply only to new connections established after the modification. |
| **Read-only** | Isn't user configurable, because of their critical role in maintaining reliability, security, or other operational aspects of the service. |


### [CLI](#tab/cli-list)

You can list all server parameters in a server via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server>
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
| **isReadOnly** | Indicates if the default value assigned for the parameter can or cannot be overridden by the user. | `true`: for parameters that are designated as read-only and the user can't change. `false`: for parameters that are designated as read-write and the user can set to a different value than their default. |
| **name** | Name of the parameter. | Any valid name for a server parameter. |
| **resourceGroup** | Name of the resource group in which the server is deployed. | Any valid name for a resource group in Azure. |
| **source** | Source from which the value currently set for the parameter originates. | `system-default` or `user-override`, depending on whether **value** is set to the system default or the user override it. |
| **unit** | Optional text describing the units in which the parameter is expressed. | When set to something, it can be any of `8KB`, `bytes`, `days`, `KB`, `megabytes`, `microseconds`, `milliseconds`, `minutes`, `percentage`, `seconds`. |
| **value** | Value currently assigned to the parameter. | Varies, depending on the data type and allowed values of the parameter. |

---

## List server parameters with modified defaults

### [Portal](#tab/portal-list-modified)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**, and then select the **Modified** tab. The page shows a list of parameters whose currently set value deviates from the default.

    :::image type="content" source="./media/how-to-configure-server-parameters/modified-parameters.png" alt-text="Screenshot of modified server parameters." lightbox="./media/how-to-configure-server-parameters/modified-parameters.png":::

### [CLI](#tab/cli-list-modified)

You can list all server parameters whose values are modified from defaults, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?value!=defaultValue && isReadOnly==\`false\` && name!='temp_tablespaces' && name!='vacuum_cost_page_miss'] | [].name"
```

> [!NOTE]  
> Previous CLI command doesn't consider modified server parameters those which are designated as read-only, `temp_tablespaces` and  `vacuum_cost_page_miss`, following the exact same criteria as the **Server parameters** page in the Azure portal.

---

## List read-write static server parameters

### [Portal](#tab/portal-list-static)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**, and then select the **Static** tab. The page shows a list of read-write parameters for which, if their value is changed, require a restart of the server for the new value to take effect.

    :::image type="content" source="./media/how-to-configure-server-parameters/static-parameters.png" alt-text="Screenshot of static server parameters." lightbox="./media/how-to-configure-server-parameters/static-parameters.png":::

### [CLI](#tab/cli-list-static)

You can list all server parameters that require a restart after their values are changed, so that the changes take effect, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isDynamicConfig==\`false\` && isReadOnly==\`false\`] | [].name"
```

---

## List read-write dynamic server parameters

### [Portal](#tab/portal-list-dynamic)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**, and then select the **Dynamic** tab. The page shows a list of read-write parameters for which, if their value is changed, require a restart of the server for the new value to take effect.

    :::image type="content" source="./media/how-to-configure-server-parameters/dynamic-parameters.png" alt-text="Screenshot of dynamic server parameters." lightbox="./media/how-to-configure-server-parameters/dynamic-parameters.png":::

### [CLI](#tab/cli-list-dynamic)

You can list all server parameters that don't require a restart after their values are changed for the changes to take effect, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isDynamicConfig==\`true\` && isReadOnly==\`false\`] | [].name"
```

---

## List read-only server parameters

### [Portal](#tab/portal-list-read-only)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**, and then select the **Read-Only** tab. The page shows a list of read-only parameters.

    :::image type="content" source="./media/how-to-configure-server-parameters/read-only-parameters.png" alt-text="Screenshot of read-only server parameters." lightbox="./media/how-to-configure-server-parameters/read-only-parameters.png":::

### [CLI](#tab/cli-list-read-only)

You can list all server parameters that are designated as read-only, whose values can't be changed by users, via the [az postgres flexible-server parameter list](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-list) command.

```azurecli-interactive
az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isReadOnly==\`true\`] | [].name"
```

---

## Set the value of one or more server parameters

### [Portal](#tab/portal-set-value)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**.

3. Locate the read-write parameters whose current values you want to change, set them to the new desired values, notice that an informational message indicates how many server parameter changes aren't saved yet, and select **Save**.

    :::image type="content" source="./media/how-to-configure-server-parameters/set-value.png" alt-text="Screenshot of setting the value of a server parameter." lightbox="./media/how-to-configure-server-parameters/set-value.png":::

4. If the column **Parameter type** for any of the parameters changed is equal to **Static**, the server requires a restart for the changes to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: In case you want to persist all changes made to all parameters whose values were modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: In case you want to persist all changes made to all parameters whose set values changed, but want to defer the server restart to a later time. Until you don't complete the server restart action, changes made to any static server parameters don't take effect.
    - **Cancel**: To not implement any changes yet.

    :::image type="content" source="./media/how-to-configure-server-parameters/save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after modifying a static parameter." lightbox="./media/how-to-configure-server-parameters/save-restart-cancel.png":::

### [CLI](#tab/cli-set-value)

You can set the value of a server parameter via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set --resource-group <resource_group> --server-name <server> --source user-override --name <parameter> --value <value>
```

And you can use the following script to conditionally restart the server, if any of the parameters changed require a restart for the change to take effect:

```azurecli-interactive
parameters_requiring_restart=$(az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isConfigPendingRestart==\`true\`] | length(@)")

if [ "$parameters_requiring_restart" -gt 0 ]; then
  az postgres flexible-server restart --resource-group <resource_group> --name <server>
fi
```

---

## Revert one server parameter to its default

### [Portal](#tab/portal-revert-one-to-default)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**.

3. Locate the read-write parameter whose current value you want to revert to its default, select the ellipsis at the right end side of the scree, and select **Reset to default**.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-one-to-default.png" alt-text="Screenshot of resetting the value of one server parameter to its default." lightbox="./media/how-to-configure-server-parameters/reset-one-to-default.png":::

> [!IMPORTANT]
> For parameters designated as read-only, selecting the ellipsis doesn't pop up the **Reset to default** menu option.

4. If the column **Parameter type** for the parameter you're trying to reset to default is equal to **Static**, the server requires a restart for the change to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: In case you want to persist all changes made to all parameters whose values were modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: In case you want to persist all changes made to all parameters whose set values changed, but want to defer the server restart to a later time. Until you don't complete the server restart action, changes made to any static server parameters don't take effect.
    - **Cancel**: To not implement any changes yet.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-one-to-default-save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after modifying the value of a static parameter." lightbox="./media/how-to-configure-server-parameters/reset-one-to-default-save-restart-cancel.png":::

### [CLI](#tab/cli-revert-one-to-default)

You can revert the value of a server parameter to its default via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set --resource-group <resource_group> --server-name <server> --source user-override --name <parameter> --value $(az postgres flexible-server parameter show --resource-group <resource_group> --server-name <server> --name <parameter> --output tsv) 
```

And you can use the following script to conditionally restart the server, if the parameter changed requires a restart for the change to take effect:

```azurecli-interactive
parameters_requiring_restart=$(az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isConfigPendingRestart==\`true\`] | length(@)")

if [ "$parameters_requiring_restart" -gt 0 ]; then
  az postgres flexible-server restart --resource-group <resource_group> --name <server>
fi
```

---

## Revert all server parameters to their defaults

### [Portal](#tab/portal-revert-all-to-default)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Server parameters**.

3. Select **Reset all to default**.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-all-to-default.png" alt-text="Screenshot of resetting the value of all server parameters to their defaults." lightbox="./media/how-to-configure-server-parameters/reset-all-to-default.png":::

4. If, for any of the parameters whose current value doesn't match their default, the column **Parameter type** is equal to **Static**, the server requires a restart for the change to take effect. In that case, a dialog pops up so that you can select if you want to:
    - **Save and Restart**: In case you want to persist all changes made to all parameters whose values were modified, and immediately after restart the server for any changes to static parameters to take effect.
    - **Save only**: In case you want to persist all changes made to all parameters whose set values changed, but want to defer the server restart to a later time. Until you don't complete the server restart action, changes made to any static server parameters don't take effect.
    - **Cancel**: To not implement any changes yet.

    :::image type="content" source="./media/how-to-configure-server-parameters/reset-all-to-default-save-restart-cancel.png" alt-text="Screenshot of dialog requesting a restart of the server after having reset all to default." lightbox="./media/how-to-configure-server-parameters/reset-all-to-default-save-restart-cancel.png":::

### [CLI](#tab/cli-revert-all-to-default)

You can revert the value of all read-write server parameters to their defaults via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
parameters_to_reset=$(az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?value!=defaultValue && isReadOnly==\`false\`].name" -o tsv)
for parameter_to_reset in $parameters_to_reset; do
  az postgres flexible-server parameter set --resource-group <resource_group> --server-name <server> --name $parameter_to_reset --value $(az postgres flexible-server parameter show --resource-group <resource_group> --server-name <server> --name $parameter_to_reset --output tsv)
done
```

And you can use the following script to conditionally restart the server, if any of the parameters changed require a restart for their change to take effect:

```azurecli-interactive
parameters_requiring_restart=$(az postgres flexible-server parameter list --resource-group <resource_group> --server-name <server> --query "[?isConfigPendingRestart==\`true\`] | length(@)")

if [ "$parameters_requiring_restart" -gt 0 ]; then
  az postgres flexible-server restart --resource-group <resource_group> --name <server>
fi
```

---

## Working with time zone parameters
If you plan to work with date and time data in PostgreSQL, make sure that you set the correct time zone for your location. All timezone-aware dates and times are stored internally in PostgreSQL in UTC. They're converted to local time in the zone specified by the **TimeZone** server parameter before being displayed to the client. This parameter can be edited on **Server parameters** page. 
PostgreSQL allows you to specify time zones in three different forms:

- A full time zone name, for example America/New_York. The recognized time zone names are listed in the [**pg_timezone_names**](https://www.postgresql.org/docs/9.2/view-pg-timezone-names.html) view.  
   Example to query this view in psql and get list of time zone names:
   <pre>select name FROM pg_timezone_names LIMIT 20;</pre>

   You should see result set like:

   <pre>
            name
        -----------------------
        GMT0
        Iceland
        Factory
        NZ-CHAT
        America/Panama
        America/Fort_Nelson
        America/Pangnirtung
        America/Belem
        America/Coral_Harbour
        America/Guayaquil
        America/Marigot
        America/Barbados
        America/Porto_Velho
        America/Bogota
        America/Menominee
        America/Martinique
        America/Asuncion
        America/Toronto
        America/Tortola
        America/Managua
        (20 rows)
    </pre>
   
- A time zone abbreviation, for example PST. Such a specification merely defines a particular offset from UTC, in contrast to full time zone names which can imply a set of daylight savings transition-date rules as well. The recognized abbreviations are listed in the [**pg_timezone_abbrevs view**](https://www.postgresql.org/docs/current/view-pg-timezone-abbrevs.html)
   Example to query this view in psql and get list of time zone abbreviations:

   <pre> select abbrev from pg_timezone_abbrevs limit 20;</pre>

    You should see result set like:

     <pre>
        abbrev|
        ------+
        ACDT  |
        ACSST |
        ACST  |
        ACT   |
        ACWST |
        ADT   |
        AEDT  |
        AESST |
        AEST  |
        AFT   |
        AKDT  |
        AKST  |
        ALMST |
        ALMT  |
        AMST  |
        AMT   |
        ANAST |
        ANAT  |
        ARST  |
        ART   |
    </pre>

- In addition to the timezone names and abbreviations, PostgreSQL accepts POSIX-style time zone specifications of the form STDoffset or STDoffsetDST, where STD is a zone abbreviation, offset is a numeric offset in hours west from UTC, and DST is an optional daylight-savings zone abbreviation, assumed to stand for one hour ahead of the given offset. 

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related contents
- [overview of server parameters](concepts-server-parameters.md)