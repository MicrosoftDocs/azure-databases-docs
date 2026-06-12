---
title: Configure intelligent tuning
description: This article describes how to configure intelligent tuning of an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/08/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: how-to
---

# Configure intelligent tuning

This article provides step-by-step instructions to configure intelligent tuning of an Azure Database for PostgreSQL flexible server.

> [!IMPORTANT]
> Autovacuum tuning is deprecated and is replaced with [adaptive autovacuum](./concepts-adaptive-autovacuum.md). As a consequence, setting `intelligent_tuning.metric_targets` to any value that contains `tuning-autovacuum` is accepted but the backend function that automatically adjusts autovacuum tuning performance remains inactive.

## Steps to configure intelligent tuning

### [Portal](#tab/portal-list)

Using the [Azure portal](https://portal.azure.com):

1. Select your Azure Database for PostgreSQL flexible server instance.
1. In the resource menu, under **Settings**, select **Parameters**. In the search text box, type **intelligent_tuning**.
   :::image type="content" source="./media/how-to-configure-intelligent-tuning/enable-intelligent-tuning.png" alt-text="Screenshot that shows the Parameters menu option with a search for intelligent_tuning." lightbox="media/how-to-configure-intelligent-tuning/enable-intelligent-tuning.png":::
1. The page shows two parameters: `intelligent_tuning` and `intelligent_tuning.metric_targets`. To activate intelligent tuning, set `intelligent_tuning` to `on`. You can select one, multiple, or all available tuning targets in `intelligent_tuning.metric_targets`. Select the **Save** button to apply these changes.
   :::image type="content" source="./media/how-to-configure-intelligent-tuning/choose-tuning-targets.png" alt-text="Screenshot that shows the Parameters page with intelligent_tuning.tuning_targets supported values." lightbox="./media/how-to-configure-intelligent-tuning/choose-tuning-targets.png":::

> [!NOTE]
> Both `intelligent_tuning` and `intelligent_tuning.metric_targets` parameters are dynamic. That is, no server restart is required when their values are changed.

### [CLI](#tab/cli-list)

You can configure intelligent tuning in a server via the [az postgres flexible-server parameter set](/cli/azure/postgres/flexible-server/parameter#az-postgres-flexible-server-parameter-set) command.

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server>
  --name intelligent_tuning
  --value on
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server>
  --name intelligent_tuning.metrics_targets
  --value <comma-separated-list-of-allowed-values>
```

---

### Considerations for selecting values for tuning targets

When you're choosing values from the `intelligent_tuning.metric_targets` parameter, take the following considerations into account:

* The `none` value takes precedence over all other values. If you choose `none` alongside any combination of other values, the parameter is perceived as set to `none`. It's the equivalent to setting `intelligent_tuning` to `off`, so no tuning occurs.

* The `all` value takes precedence over all other values, except for `none`. If you choose `all` with any combination, barring `none`, all the listed parameters undergo tuning.

* The `all` value encompasses all existing metric targets. This value also automatically applies to any new metric targets that you might add in the future. This allows for comprehensive and future-proof tuning of your Azure Database for PostgreSQL flexible server.

## Related content

- [Intelligent tuning in Azure Database for PostgreSQL flexible server](./concepts-intelligent-tuning.md).
- [Adaptive autovacuum in Azure Database for PostgreSQL flexible server](./concepts-adaptive-autovacuum.md).
