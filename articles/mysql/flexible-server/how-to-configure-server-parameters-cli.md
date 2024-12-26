---
title: Configure Server Parameters - Azure CLI
description: This article describes how to configure the service parameters in Azure Database for MySQL - Flexible Server by using the Azure CLI command line utility.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - devx-track-azurecli
ms.devlang: azurecli
---

# Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI

You can list, show, and update parameters for an Azure Database for MySQL Flexible Server instance by using Azure CLI, the Azure command-line utility. The server parameters are configured with the default and recommended value when you create the server.

This article describes how to list, show, and update server parameters by using the Azure CLI.

> [!NOTE]  
> Server parameters can be updated globally at the server-level, use the [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-configure-server-parameters-cli.md) or [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md)

## Prerequisites

To step through this how-to guide, you need:

- [Quickstart: Create an instance of Azure Database for MySQL - Flexible Server by using the Azure CLI](quickstart-create-server-cli.md)
- [Azure CLI](/cli/azure/install-azure-cli) command-line utility or use the Azure Cloud Shell in the browser.

## List server parameters for an Azure Database for MySQL Flexible Server instance

To list all parameters in an Azure Database for MySQL Flexible Server instance and their values, run the [az mysql flexible-server parameter list](/cli/azure/mysql/flexible-server/parameter) command.

You can list the server parameters for the server **mydemoserver.mysql.database.azure.com** under resource group **myresourcegroup**.

```azurecli-interactive
az mysql flexible-server parameter list --resource-group myresourcegroup --server-name mydemoserver
```
For the definition of each of the listed parameters, see the MySQL reference section on [Server System Variables](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html).

## Show server parameter details

To show details about a particular parameter for an Azure Database for MySQL Flexible Server instance, run the [az mysql flexible-server parameter show](/cli/azure/mysql/flexible-server/parameter) command.

This example shows details of the **slow\_query\_log** server parameter for server **mydemoserver.mysql.database.azure.com** under resource group **myresourcegroup.**

```azurecli-interactive
az mysql flexible-server parameter show --name slow_query_log --resource-group myresourcegroup --server-name mydemoserver
```

## Modify a server parameter value

You can also modify the value of a certain Azure Database for MySQL Flexible Server instance parameter, which updates the underlying configuration value for the MySQL server engine. To update the server parameter, use the [az mysql flexible-server parameter set](/cli/azure/mysql/flexible-server/parameter) command.

To update the **slow\_query\_log** server parameter of server **mydemoserver.mysql.database.azure.com** under resource group **myresourcegroup.**

```azurecli-interactive
az mysql flexible-server parameter set --name slow_query_log --resource-group myresourcegroup --server-name mydemoserver --value ON
```

To update multiple server parameters like **slow\_query\_log** and **audit\_log\_enabled** of server **mydemoserver.mysql.database.azure.com** under resource group **myresourcegroup.**

```azurecli-interactive
az mysql flexible-server parameter set-batch -resource-group myresourcegroup --server-name mydemoserver --source "user-override" --args slow_query_log="ON" audit_log_enabled="ON"
```

If you want to reset the value of a parameter, omit the optional `--value` parameter, and the service applies the default value. For the example above, it would look like:

```azurecli-interactive
az mysql flexible-server parameter set --name slow_query_log --resource-group myresourcegroup --server-name mydemoserver
```
This code resets the **slow\_query\_log** to the default value **OFF**.

<a id="setting-non-modifiable-server-parameters"></a>

## Set non-modifiable server parameters

If the Azure Database for MySQL Flexible Server parameter you want to update is non-modifiable, you can optionally set the parameter at the connection level using `init_connect`. This sets the server parameters for each client connecting to the server.

Update the **init\_connect** server parameter of server **mydemoserver.mysql.database.azure.com** under resource group **myresourcegroup** to set values such as character set.

```azurecli-interactive
az mysql flexible-server parameter set --name init_connect --resource-group myresourcegroup --server-name mydemoserver --value "SET character_set_client=utf8;SET character_set_database=utf8mb4;SET character_set_connection=latin1;SET character_set_results=latin1;"
```
> [!NOTE]  
> `init_connect` can be used to change parameters that do not require SUPER privilege(s) at the session level. To verify if you can set the parameter using `init_connect`, execute the `set session parameter_name=YOUR_DESIRED_VALUE;` command and if it errors out with **Access denied; you need SUPER privileges(s)** error, then you cannot set the parameter using `init_connect'.

<a id="working-with-the-time-zone-parameter"></a>

## Work with the time zone parameter

<a id="setting-the-global-level-time-zone"></a>

### Set the global level time zone

The global level time zone can be set using the [az mysql flexible-server parameter set](/cli/azure/mysql/flexible-server/parameter) command.

The following command updates the **time\_zone** server parameter of server **mydemoserver.mysql.database.azure.com** under resource group **myresourcegroup** to **US/Pacific**.

```azurecli-interactive
az mysql flexible-server parameter set --name time_zone --resource-group myresourcegroup --server-name mydemoserver --value "US/Pacific"
```

<a id="setting-the-session-level-time-zone"></a>

### Set the session level time zone

The session level time zone can be set by running the `SET time_zone` command from a tool like the MySQL command line or MySQL Workbench. The example below sets the time zone to the **US/Pacific** time zone.

```sql
SET time_zone = 'US/Pacific';
```

Refer to the MySQL documentation for [Date and Time Functions](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_convert-tz).

> [!NOTE]  
> To change time zone at session level, Server parameter time_zone has to be updated globally to required timezone at least once, in order to update the [mysql.time_zone_name](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html) table.

## Next step

> [!div class="nextstepaction"]
> [server parameters in Azure portal](how-to-configure-server-parameters-portal.md)
