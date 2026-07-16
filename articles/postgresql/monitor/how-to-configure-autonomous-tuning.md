---
title: Configure Autonomous Tuning in Azure Database for PostgreSQL Flexible Server
description: This article describes how to configure the autonomous tuning feature in your Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to enable autonomous tuning on my Azure Database for PostgreSQL flexible server, so that I can get automated index recommendations for my workload.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Configure autonomous tuning in Azure Database for PostgreSQL flexible server

You can enable, disable, and configure autonomous tuning through a [set of parameters](concepts-autonomous-tuning.md#configuring-autonomous-tuning) that control its behavior, such as how often a tuning session should run.

Autonomous tuning depends on the data that [query store](concepts-query-store.md) persists locally to the `azure_sys` database. Don't enable query store on the Burstable pricing tier, due to the performance implications it might have. For the same reason, don't use autonomous tuning for servers that use compute from the Burstable tier.

Autonomous tuning is an opt-in feature that's disabled by default on a server. You can enable or disable it globally for all databases on a given server. You can't turn it on or off per database.

### Steps to enable autonomous tuning

### [Portal](#tab/portal-autonomous-tuning-enable)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under **Intelligent Performance**, select **Autonomous tuning**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/enable-autonomous-tuning-via-page-autonomous-tuning.png" alt-text="Screenshot that shows the Autonomous tuning menu option under the Intelligent Performance section, to enable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/enable-autonomous-tuning-via-page-autonomous-tuning.png":::

1. If either `pg_qs.query_capture_mode` is set to `none` or `index_tuning.mode` is set to `off`, the **Autonomous tuning** page gives you the option to enable autonomous tuning. Select on either of the two **Enable tuning** buttons, to enable autonomous tuning feature and its required query store dependency, if query store is disabled.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/enable-autonomous-tuning-via-page-enable-autonomous-tuning.png" alt-text="Screenshot that shows how to enable autonomous tuning through the Autonomous tuning page." lightbox="media/how-to-configure-autonomous-tuning/enable-autonomous-tuning-via-page-enable-autonomous-tuning.png":::

1. Wait for the deployment to complete successfully before considering that the feature is enabled.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/wait-for-autonomous-tuning-deployment.png" alt-text="Screenshot that shows the deployment completed to enable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/wait-for-autonomous-tuning-deployment.png":::

1. After enabling autonomous tuning, allow up to 12 hours for the autonomous tuning engine to analyze the workload collected by query store during that time, and eventually produce recommendations.

> [!IMPORTANT]  
> When you enable autonomous tuning by using the **Enable tuning** button, if `pg_qs.query_capture_mode` is set to `none`, the process changes it to `all`. If it's already set to `top` or `all`, the process leaves it unchanged.

### [CLI](#tab/cli-autonomous-tuning-enable)

Use the [az postgres flexible-server autonomous-tuning update](/cli/azure/postgres/flexible-server/autonomous-tuning#az-postgres-flexible-server-autonomous-tuning-update) command to enable autonomous tuning in an existing server.

To enable autonomous tuning, use this command:

```azurecli-interactive
az postgres flexible-server autonomous-tuning update \
  --resource-group <resource_group> \
  --server-name <server> \
  --enabled true
```

If the previous command executes successfully, you see the following output:

```output
WARNING: Enabling autonomous tuning for the server.
WARNING: Autonomous tuning is enabled for the server.
```

---

### Steps to disable autonomous tuning

### [Portal](#tab/portal-autonomous-tuning-disable)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under **Intelligent Performance**, select **Autonomous tuning**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/disable-autonomous-tuning-via-page-autonomous-tuning.png" alt-text="Screenshot that shows the Autonomous tuning menu option under the Intelligent Performance section, to disable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/disable-autonomous-tuning-via-page-autonomous-tuning.png":::

1. Select **Disable tuning** to disable the feature.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/disable-autonomous-tuning-via-page-disable-autonomous-tuning.png" alt-text="Screenshot that shows how to disable autonomous tuning through the Autonomous tuning page." lightbox="media/how-to-configure-autonomous-tuning/disable-autonomous-tuning-via-page-disable-autonomous-tuning.png":::

1. Wait for the deployment to complete successfully before considering that the feature is disabled.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/wait-for-autonomous-tuning-deployment.png" alt-text="Screenshot that shows the deployment completed to disable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/wait-for-autonomous-tuning-deployment.png":::

1. Assess whether you want to continue using [query store](concepts-query-store.md) to monitor the performance of your workload and leave it enabled or, if you want to disable it, do so by setting `pg_qs.query_capture_mode` to `none`.

> [!IMPORTANT]  
> When autonomous tuning is disabled through the **Disable tuning** button, parameter `pg_qs.query_capture_mode` isn't set to `none`, but left as it is configured.

### [CLI](#tab/CLI-autonomous-tuning-disable)

Use the [az postgres flexible-server autonomous-tuning update](/cli/azure/postgres/flexible-server/autonomous-tuning#az-postgres-flexible-server-autonomous-tuning-update) command to disable autonomous tuning in an existing server.

To disable autonomous tuning, use this command:

```azurecli-interactive
az postgres flexible-server autonomous-tuning update \
  --resource-group <resource_group> \
  --server-name <server> \
  --enabled false
```

If the previous command executes successfully, you see the following output:

```output
WARNING: Disabling autonomous tuning for the server.
WARNING: Autonomous tuning is disabled for the server.
```

Assess whether you want to continue using [query store](concepts-query-store.md) to monitor the performance of your workload and leave it enabled or, if you want to disable it, by setting `pg_qs.query_capture_mode` to `none`.

> [!IMPORTANT]  
> When autonomous tuning is disabled through the CLI command, parameter `pg_qs.query_capture_mode` isn't set to `none`, but left as it is configured.

---

### Steps to show the state of autonomous tuning

### [Portal](#tab/portal-show-state)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under **Intelligent Performance**, select **Autonomous tuning**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled.png" alt-text="Screenshot that shows the Autonomous tuning menu option under the Intelligent Performance section, to disable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled.png":::

1. If autonomous tuning is enabled, the page displays the **Disable tuning** button.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-enabled-disable-button.png" alt-text="Screenshot that shows the aspect of the Autonomous tuning page when the feature is enabled." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-enabled-disable-button.png":::

1. If autonomous tuning is disabled, the page displays the **Enable tuning** button.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled-enable-button.png" alt-text="Screenshot that shows the aspect of the Autonomous tuning page when the feature is disabled." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled-enable-button.png":::

### [CLI](#tab/CLI-show-state)

Use the [az postgres flexible-server autonomous-tuning show](/cli/azure/postgres/flexible-server/autonomous-tuning#az-postgres-flexible-server-autonomous-tuning-show) command to show the state of autonomous tuning in an existing server.

To show the state of autonomous tuning, use this command:

```azurecli-interactive
az postgres flexible-server autonomous-tuning show \
  --resource-group <resource_group> \
  --server-name <server>
```

If autonomous tuning is enabled, you should see the following output:

```output
WARNING: Autonomous tuning is enabled for the server.
```

If autonomous tuning is disabled, you should see the following output:

```output
WARNING: Autonomous tuning is disabled for the server.
```

---

### Steps to list autonomous tuning settings

### [Portal](#tab/portal-list-all-settings)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under **Intelligent Performance**, select **Autonomous tuning**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled.png" alt-text="Screenshot that shows the Autonomous tuning menu option under the Intelligent Performance section, to disable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled.png":::

1. Select **Tuning settings**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled-tune-settings.png" alt-text="Screenshot that shows the Tune settings button in the Autonomous tuning page." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled-tune-settings.png":::

### [CLI](#tab/CLI-list-all-settings)

Use the [az postgres flexible-server autonomous-tuning show-settings](/cli/azure/postgres/flexible-server/autonomous-tuning#az-postgres-flexible-server-autonomous-tuning-show-settings) command to show the value of a single autonomous tuning setting in an existing server.

For example, to show the value of the autonomous tuning setting called `analyze_interval`, use the following command:

```azurecli-interactive
az postgres flexible-server autonomous-tuning show-settings \
  --resource-group <resource_group> \
  --server-name <server> \
  --name analyze_interval
```

The command returns all information about the parameter corresponding to that setting of autonomous tuning. The output is similar to the following:

```output
{
  "allowedValues": "60-10080",
  "dataType": "Integer",
  "defaultValue": "720",
  "description": "Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to 'REPORT'.",
  "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.analysis_interval",
  "isConfigPendingRestart": false,
  "isDynamicConfig": true,
  "isReadOnly": false,
  "name": "index_tuning.analysis_interval",
  "resourceGroup": "<resource_group>",
  "source": "user-override",
  "systemData": null,
  "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
  "unit": "minutes",
  "value": "720"
}
```

Use the [az postgres flexible-server autonomous-tuning list-settings](/cli/azure/postgres/flexible-server/autonomous-tuning#az-postgres-flexible-server-autonomous-tuning-list-settings) command to show the list of all autonomous tuning settings in an existing server.

To list all autonomous tuning settings, use the following command:

```azurecli-interactive
az postgres flexible-server autonomous-tuning list-settings \
  --resource-group <resource_group> \
  --server-name <server>
```

The command returns all parameters that control the different settings of autonomous tuning. The output is similar to the following:

```output
[
  {
    "allowedValues": "60-10080",
    "dataType": "Integer",
    "defaultValue": "720",
    "description": "Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to 'REPORT'.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.analysis_interval",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.analysis_interval",
    "resourceGroup": "<resource_group>",
    "source": "user-override",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": "minutes",
    "value": "720"
  },
  {
    "allowedValues": "1-10",
    "dataType": "Integer",
    "defaultValue": "2",
    "description": "Maximum number of columns that can be part of the index key for any recommended index.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.max_columns_per_index",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.max_columns_per_index",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "2"
  },
  {
    "allowedValues": "1-25",
    "dataType": "Integer",
    "defaultValue": "10",
    "description": "Maximum number of indexes that can be recommended for each database during one optimization session.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.max_index_count",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.max_index_count",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "10"
  },
  {
    "allowedValues": "1-25",
    "dataType": "Integer",
    "defaultValue": "10",
    "description": "Maximum number of indexes that can be recommended for each table.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.max_indexes_per_table",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.max_indexes_per_table",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "10"
  },
  {
    "allowedValues": "5-100",
    "dataType": "Integer",
    "defaultValue": "25",
    "description": "Number of slowest queries per database for which indexes can be recommended.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.max_queries_per_database",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.max_queries_per_database",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "25"
  },
  {
    "allowedValues": "0.05-0.2",
    "dataType": "Numeric",
    "defaultValue": "0.1",
    "description": "Acceptable regression introduced by a recommended index on any of the queries analyzed during one optimization session.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.max_regression_factor",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.max_regression_factor",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": "percentage",
    "value": "0.1"
  },
  {
    "allowedValues": "0-1.0",
    "dataType": "Numeric",
    "defaultValue": "0.1",
    "description": "Maximum total size, in percentage of total disk space, that all recommended indexes for any given database can use.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.max_total_size_factor",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.max_total_size_factor",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": "percentage",
    "value": "0.1"
  },
  {
    "allowedValues": "0-20.0",
    "dataType": "Numeric",
    "defaultValue": "0.2",
    "description": "Cost improvement that a recommended index must provide to at least one of the queries analyzed during one optimization session.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.min_improvement_factor",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.min_improvement_factor",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": "percentage",
    "value": "0.2"
  },
  {
    "allowedValues": "off,report",
    "dataType": "Enumeration",
    "defaultValue": "off",
    "description": "Configures index optimization as disabled ('OFF') or enabled to only emit recommendation. Requires Query Store to be enabled by setting pg_qs.query_capture_mode to 'TOP' or 'ALL'.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.mode",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.mode",
    "resourceGroup": "<resource_group>",
    "source": "user-override",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "off"
  },
  {
    "allowedValues": "0-9999999",
    "dataType": "Integer",
    "defaultValue": "1000",
    "description": "Minimum number of daily average DML operations affecting the table, so that their unused indexes are considered for dropping.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.unused_dml_per_table",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.unused_dml_per_table",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "1000"
  },
  {
    "allowedValues": "30-720",
    "dataType": "Integer",
    "defaultValue": "35",
    "description": "Minimum number of days the index has not been used, based on system statistics, so that it is considered for dropping.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.unused_min_period",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.unused_min_period",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": "days",
    "value": "35"
  },
  {
    "allowedValues": "0-9999999",
    "dataType": "Integer",
    "defaultValue": "1000",
    "description": "Minimum number of daily average read operations affecting the table, so that their unused indexes are considered for dropping.",
    "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
    "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.unused_reads_per_table",
    "isConfigPendingRestart": false,
    "isDynamicConfig": true,
    "isReadOnly": false,
    "name": "index_tuning.unused_reads_per_table",
    "resourceGroup": "<resource_group>",
    "source": "system-default",
    "systemData": null,
    "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
    "unit": null,
    "value": "1000"
  }
]
```

---

### Steps to modify autonomous tuning settings

### [Portal](#tab/portal-modify-settings)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under **Intelligent Performance**, select **Autonomous tuning**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled.png" alt-text="Screenshot that shows the Autonomous tuning menu option under the Intelligent Performance section, to disable autonomous tuning." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled.png":::

1. Select **Tuning settings**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled-tune-settings.png" alt-text="Screenshot that shows the Tune settings button in the Autonomous tuning page." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-disabled-tune-settings.png":::

1. Modify the values of as many settings as you want to change, and select **Save**.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-tuning-settings-save.png" alt-text="Screenshot that shows the aspect of the Autonomous tuning page when the feature is enabled." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-tuning-settings-save.png":::

1. Wait for the deployment to complete successfully before considering that the value of the settings is changed.

   :::image type="content" source="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-tuning-settings-deployment.png" alt-text="Screenshot that shows a successfully completed deployment to modify one or more autonomous tuning settings." lightbox="media/how-to-configure-autonomous-tuning/autonomous-tuning-page-tuning-settings-deployment.png":::


### [CLI](#tab/CLI-modify-settings)

Use the [az postgres flexible-server autonomous-tuning set-settings](/cli/azure/postgres/flexible-server/autonomous-tuning#az-postgres-flexible-server-autonomous-tuning-set-settings) command to change the value of a single autonomous tuning setting in an existing server.

For example, to set the value of the autonomous tuning setting named `analyze_interval` to `1440`, use the following command:

```azurecli-interactive
az postgres flexible-server autonomous-tuning set-settings \
  --resource-group <resource_group> \
  --server-name <server> \
  --name analyze_interval \
  --value 1440
```

The command returns all information about the parameter corresponding to that setting of autonomous tuning. The output is similar to the following:

```output
{
  "allowedValues": "60-10080",
  "dataType": "Integer",
  "defaultValue": "720",
  "description": "Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to 'REPORT'.",
  "documentationLink": "https://go.microsoft.com/fwlink/?linkid=2274149",
  "id": "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<server>/configurations/index_tuning.analysis_interval",
  "isConfigPendingRestart": false,
  "isDynamicConfig": true,
  "isReadOnly": false,
  "name": "index_tuning.analysis_interval",
  "resourceGroup": "<resource_group>",
  "source": "user-override",
  "systemData": null,
  "type": "Microsoft.DBforPostgreSQL/flexibleServers/configurations",
  "unit": "minutes",
  "value": "1440"
}
```

---

## Related content

- [Autonomous tuning](concepts-autonomous-tuning.md)
- [Use autonomous tuning recommendations](how-to-get-apply-recommendations-from-autonomous-tuning.md)
- [Query store](concepts-query-store.md)