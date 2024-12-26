---
title: Configure Server Parameters - Azure Portal
description: This article describes how to configure MySQL server parameters in Azure Database for MySQL - Flexible Server by using the Azure portal.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal

You can manage Azure Database for MySQL Flexible Server configuration using server parameters. The server parameters are configured with the default and recommended value when you create the server.

This article describes how to view and configure server parameters by using the Azure portal. The server parameter blade on Azure portal shows both the modifiable and nonmodifiable server parameters. The nonmodifiable server parameters are greyed out.

> [!NOTE]  
> Server parameters can be updated globally at the server-level, use the [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-configure-server-parameters-cli.md) or [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md).

## Configure server parameters

1. Sign in to the [Azure portal](https://portal.azure.com), and locate your Azure Database for MySQL Flexible Server instance.
1. Under the **SETTINGS** section, select **Server parameters** to open the server parameters page for the Azure Database for MySQL Flexible Server instance.
[:::image type="content" source="./media/how-to-server-parameters/azure-portal-server-parameters.png" alt-text="Azure portal server parameters page":::](./media/how-to-server-parameters/azure-portal-server-parameters.png#lightbox)
1. Locate any server parameter you need to adjust. Review the **Description** column to understand the purpose and allowed values.
[:::image type="content" source="./media/how-to-server-parameters/3-toggle-parameter.png" alt-text="Enumerate drop down":::](./media/how-to-server-parameters/3-toggle-parameter.png#lightbox)
1. Select **Save** to save your changes.
[:::image type="content" source="./media/how-to-server-parameters/4-save-parameters.png" alt-text="Save or Discard changes":::](./media/how-to-server-parameters/4-save-parameters.png#lightbox)
1. Static parameters are ones that require server reboot to take effect. If you're modifying a static parameter, you're prompted to **Restart now** or **Restart later**.
[:::image type="content" source="./media/how-to-server-parameters/5-save-parameter.png" alt-text="Restart on static parameter save":::](./media/how-to-server-parameters/5-save-parameter.png#lightbox)
1. If you saved new values for the parameters, you can always revert everything back to the default values by selecting **Reset all to default**.
[:::image type="content" source="./media/how-to-server-parameters/6-reset-parameters.png" alt-text="Reset all to default":::](./media/how-to-server-parameters/6-reset-parameters.png#lightbox)

<a id="setting-non-modifiable-server-parameters"></a>

## Set non-modifiable server parameters

If the server parameter you want to update is nonmodifiable, you can optionally set the parameter at the connection level using `init_connect`. This sets the server parameters for each client connecting to the server.

1. Under the **SETTINGS** section, select **Server parameters** to open the server parameters page for the Azure Database for MySQL Flexible Server instance.
1. Search for `init_connect`
1. Add the server parameters in the format: `SET parameter_name=YOUR_DESIRED_VALUE` in value the value column.

    For example, you can change the character set of your Azure Database for MySQL Flexible Server instance by setting `init_connect` to `SET character_set_client=utf8;SET character_set_database=utf8mb4;SET character_set_connection=latin1;SET character_set_results=latin1;`
1. Select **Save** to save your changes.

> [!NOTE]  
> `init_connect` can be used to change parameters that do not require SUPER privilege(s) at the session level. To verify if you can set the parameter using `init_connect`, execute the `set session parameter_name=YOUR_DESIRED_VALUE;` command and if it errors out with **Access denied; you need SUPER privileges(s)** error, then you cannot set the parameter using `init_connect'.

<a id="working-with-the-time-zone-parameter"></a>

## Work with the time zone parameter

<a id="setting-the-global-level-time-zone"></a>

### Set the global level time zone

The global level time zone can be set from the **Server parameters** page in the Azure portal. The following example sets the global time zone to the value "US/Pacific".

[:::image type="content" source="./media/how-to-server-parameters/timezone.png" alt-text="Set time zone parameter":::](./media/how-to-server-parameters/timezone.png#lightbox)

<a id="setting-the-session-level-time-zone"></a>

### Set the session level time zone

The session level time zone can be set by running the `SET time_zone` command from a tool like the MySQL command line or MySQL Workbench. The following example sets the time zone to the **US/Pacific** time zone.

```sql
SET time_zone = 'US/Pacific';
```

Refer to the MySQL documentation for [Date and Time Functions](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_convert-tz).

> [!NOTE]  
> To change time zone at session level, Server parameter time_zone has to be updated globally to required timezone at least once, in order to update the [mysql.time_zone_name](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html) table.

## Next step

> [!div class="nextstepaction"]
> [server parameters in Azure CLI](how-to-configure-server-parameters-cli.md)
