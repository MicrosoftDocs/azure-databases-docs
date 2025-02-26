---
title: Configure index tuning
description: This article describes how to configure the index tuning feature in your Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 02/26/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
# customer intent: As a user, I want to learn about how to enable, disable and configure the index tuning feature in an Azure Database for PostgreSQL flexible server.
---
# Configure index tuning

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Index tuning can be enabled, disabled, and configured through a [set of parameters](#configuration-options) that control its behavior, such as how often a tuning session can run.

Index tuning depends on [query store](concepts-query-store.md). We don't recommend enabling query store on the Burstable pricing tier, due to the performance implications it might have. For the same reason, index tuning isn't recommended for servers using compute from the Burstable tier.

Index tuning is an opt-in feature that isn't enabled by default on a server. It can be enabled or disabled globally for all databases on a given server and can't be turned on or off per database.

### Steps to enable index tuning

### [Portal](#tab/portal-enable)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under **Query Performance Insight**, select **Index tuning**.

   :::image type="content" source="media/how-to-configure-index-tuning/enable-index-tuning-via-page-index-tuning.png" alt-text="Screenshot that shows the Index tuning menu option under the Query Performance Insight section, to enable index tuning." lightbox="media/how-to-configure-index-tuning/enable-index-tuning-via-page-index-tuning.png":::

3. If either `pg_qs.query_capture_mode` is set to `NONE` or `index_tuning.mode` is set to `OFF`, the **Index tuning** page gives you the option to enable index tuning. Select on either of the two **Enable index tuning** buttons, to enable index tuning feature and its required query store dependency, if query store is disabled.

   :::image type="content" source="media/how-to-configure-index-tuning/enable-index-tuning-via-page-enable-index-tuning.png" alt-text="Screenshot that shows how to enable index tuning through the Index tuning page." lightbox="media/how-to-configure-index-tuning/enable-index-tuning-via-page-enable-index-tuning.png":::

4. Wait for the deployment to complete successfully before considering that the feature is enabled.

   :::image type="content" source="media/how-to-configure-index-tuning/wait-for-index-tuning-deployment.png" alt-text="Screenshot that shows the deployment completed to enable index tuning." lightbox="media/how-to-configure-index-tuning/wait-for-index-tuning-deployment.png":::

5. After enabling index tuning, allow 12 hours for the index tuning engine to analyze the workload collected by query store during that time, and eventually produce create or drop index recommendations.

> [!IMPORTANT]  
> When index tuning is enabled through the **Enable index tuning** button, if `pg_qs.query_capture_mode` is set to `NONE`, it's changed to `ALL`. If it was already set to either `TOP` or `ALL`, it's left in its current state.

### [CLI](#tab/cli-enable)

You can enable index tuning in an existing server via the [az postgres flexible-server index-tuning update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To enable index tuning, use this command:

```azurecli-interactive
az postgres flexible-server index-tuning update --resource-group <resource_group> --server-name <server> --enabled true
```

If the previous command executes successfully, you should see the following output:

```output
WARNING: Enabling index tuning for the server.
WARNING: Index tuning is enabled for the server.
```

---

### Steps to disable index tuning

### [Portal](#tab/portal-disable)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under **Query Performance Insight**, select **Index tuning**.

   :::image type="content" source="media/how-to-configure-index-tuning/disable-index-tuning-via-page-index-tuning.png" alt-text="Screenshot that shows the Index tuning menu option under the Query Performance Insight section, to disable index tuning." lightbox="media/how-to-configure-index-tuning/disable-index-tuning-via-page-index-tuning.png":::

3. Select the **Disable index tuning** button to disable the feature.

   :::image type="content" source="media/how-to-configure-index-tuning/disable-index-tuning-via-page-disable-index-tuning.png" alt-text="Screenshot that shows how to disable index tuning through the Index tuning page." lightbox="media/how-to-configure-index-tuning/disable-index-tuning-via-page-disable-index-tuning.png":::

4. Wait for the deployment to complete successfully before considering that the feature is disabled.

   :::image type="content" source="media/how-to-configure-index-tuning/wait-for-index-tuning-deployment.png" alt-text="Screenshot that shows the deployment completed to disable index tuning." lightbox="media/how-to-configure-index-tuning/wait-for-index-tuning-deployment.png":::

5. Assess whether you want to continue using [Monitor performance with query store](concepts-query-store.md) to monitor the performance of your workload and leave it enabled or, if you want to disable it, by setting `pg_qs.query_capture_mode` to `NONE`.

> [!IMPORTANT]  
> When index tuning is disabled through the **Disable index tuning** button, server parameter `pg_qs.query_capture_mode` isn't set to `NONE`, but left as it is configured.

### [CLI](#tab/CLI-disable)

You can disable index tuning in an existing server via the [az postgres flexible-server index-tuning update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To disable index tuning, use this command:

```azurecli-interactive
az postgres flexible-server index-tuning update --resource-group <resource_group> --server-name <server> --enabled false
```

If the previous command executes successfully, you should see the following output:

```output
WARNING: Disabling index tuning for the server.
WARNING: Index tuning is disabled for the server.
```

Assess whether you want to continue using [Monitor performance with query store](concepts-query-store.md) to monitor the performance of your workload and leave it enabled or, if you want to disable it, by setting `pg_qs.query_capture_mode` to `NONE`.

> [!IMPORTANT]  
> When index tuning is disabled through the CLI command, server parameter `pg_qs.query_capture_mode` isn't set to `NONE`, but left as it is configured.

---

### Steps to show state of index tuning

### [Portal](#tab/portal-show-state)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under **Query Performance Insight**, select **Index tuning**.

   :::image type="content" source="media/how-to-configure-index-tuning/index-tuning-page-disabled.png" alt-text="Screenshot that shows the Index tuning menu option under the Query Performance Insight section, to disable index tuning." lightbox="media/how-to-configure-index-tuning/index-tuning-page-disabled.png":::

3. If index tuning is enabled, the page displays the **Disable index tuning** button.

   :::image type="content" source="media/how-to-configure-index-tuning/index-tuning-page-enabled-disable-button.png" alt-text="Screenshot that shows the aspect of the Index tuning page when the feature is enabled." lightbox="media/how-to-configure-index-tuning/index-tuning-page-enabled-disable-button.png":::

4. If index tuning is disabled, the page displays the **Enable index tuning** button.

   :::image type="content" source="media/how-to-configure-index-tuning/index-tuning-page-disabled-enable-button.png" alt-text="Screenshot that shows the aspect of the Index tuning page when the feature is disabled." lightbox="media/how-to-configure-index-tuning/index-tuning-page-disabled-enable-button.png":::

### [CLI](#tab/CLI-show-state)

You can show the state of index tuning in an existing server via the [az postgres flexible-server index-tuning show](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To disable index tuning, use this command:

```azurecli-interactive
az postgres flexible-server index-tuning show --resource-group <resource_group> --server-name <server>
```

If index tuning is enabled, you should see the following output:

```output
WARNING: Index tuning is enabled for the server.
```

If index tuning is disabled, you should see the following output:

```output
WARNING: Index tuning is disabled for the server.
```

---


## Configuration options

When index tuning is enabled, it wakes up with a frequency configured in the `index_tuning.analysis_interval` server parameter (defaults to 720 minutes or 12 hours) and starts analyzing the workload recorded by query store during that period.

Notice that if you change the value for `index_tuning.analysis_interval`, it only is observed after the next scheduled execution completes. So, for example, if you enable index tuning one day at 10:00AM, because default value for `index_tuning.analysis_interval` is 720 minutes, the first execution is scheduled to start at 10:00PM that same day. Any changes you make to the value of `index_tuning.analysis_interval` between 10:00AM and 10:00PM won't affect that initial schedule. Only when the scheduled run completes, it will read current value set for `index_tuning.analysis_interval` and will schedule next execution according to that value.

The following options are available for configuring index tuning parameters:

| **Parameter** | **Description** | **Default** | **Range** | **Units** |
| --- | --- | --- | --- | --- |
| `index_tuning.analysis_interval` | Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to `REPORT`. | `720` | `60 - 10080` | minutes |
| `index_tuning.max_columns_per_index` | Maximum number of columns that can be part of the index key for any recommended index. | `2` | `1 - 10` | |
| `index_tuning.max_index_count` | Maximum indexes recommended for each database during one optimization session. | `10` | `1 - 25` | |
| `index_tuning.max_indexes_per_table` | Maximum number of indexes that can be recommended for each table. | `10` | `1 - 25` | |
| `index_tuning.max_queries_per_database` | Number of slowest queries per database for which indexes can be recommended. | `25` | `5 - 100` | |
| `index_tuning.max_regression_factor` | Acceptable regression introduced by a recommended index on any of the queries analyzed during one optimization session. | `0.1` | `0.05 - 0.2` | percentage |
| `index_tuning.max_total_size_factor` | Maximum total size, in percentage of total disk space, that all recommended indexes for any given database can use. | `0.1` | `0 - 1` | percentage |
| `index_tuning.min_improvement_factor` | Cost improvement that a recommended index must provide to at least one of the queries analyzed during one optimization session. | `0.2` | `0 - 20` | percentage |
| `index_tuning.mode` | Configures index optimization as disabled (`OFF`) or enabled to only emit recommendation. Requires query store to be enabled by setting `pg_qs.query_capture_mode` to `TOP` or `ALL`. | `OFF` | `OFF, REPORT` | |
| `index_tuning.unused_dml_per_table` | Minimum number of daily average DML operations affecting the table, so their unused indexes are considered for dropping. | `1000` | `0 - 9999999` | |
| `index_tuning.unused_min_period` | Minimum number of days the index hasn't been used, based on system statistics, so it's considered for dropping. | `35` | `30 - 70` | |
| `index_tuning.unused_reads_per_table` | Minimum number of daily average read operations affecting the table so that their unused indexes are considered for dropping. | `1000` | `0 - 9999999` | |

## Related content

- [Index tuning in Azure Database for PostgreSQL - Flexible Server](concepts-index-tuning.md).
- [Using index recommendations produced by index tuning in Azure Database for PostgreSQL - Flexible Server](how-to-get-and-apply-recommendations-from-index-tuning.md).
- [Monitor performance with query store](concepts-query-store.md).
- [Usage scenarios for query store - Azure Database for PostgreSQL - Flexible Server](concepts-query-store-scenarios.md).
- [Best practices for query store - Azure Database for PostgreSQL - Flexible Server](concepts-query-store-best-practices.md).
- [Query Performance Insight for Azure Database for PostgreSQL - Flexible Server](concepts-query-performance-insight.md).
