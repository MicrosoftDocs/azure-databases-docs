---
title: Scale Compute in Azure Database for PostgreSQL Flexible Server
description: This article describes how to scale the compute of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to scale the compute resources of my Azure Database for PostgreSQL flexible server, so that I can match capacity to my application's changing demands.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: scale-out
ms.topic: how-to
---

# Scale compute in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions for scaling the compute resources of an Azure Database for PostgreSQL flexible server.

You can change your compute tier between the burstable, general purpose, and memory optimized tiers. Within each tier, you can choose the number of virtual cores (vCores) that best fits your application. For more information about the different compute tiers available in Azure Virtual Machines and the use cases they're best suited for, see [size for virtual machines in Azure](/azure/virtual-machines/sizes/overview).

When you request a scaling operation for the compute resources used by your Azure Database for PostgreSQL flexible server, the server restarts. This restart makes your server unavailable for some time. For more information about how the process works and the expected duration of the downtime, see [near-zero downtime scaling](concepts-scaling-resources.md#near-zero-downtime-scaling).

## Steps to scale compute

### [Portal](#tab/portal-scale-compute)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-compute/compute-storage.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-compute/compute-storage.png":::

1. To choose a different tier, in the **Compute tier** group, select the option that best fits your needs.

    :::image type="content" source="./media/how-to-scale-compute/compute-tier.png" alt-text="Screenshot showing where to select a different compute tier." lightbox="./media/how-to-scale-compute/compute-tier.png":::

1. If the region of your server supports Intel and AMD processors, use the **Compute processor** option to filter the options listed in the **Compute size** drop-down to only hardware produced by the manufacturer you select.

    :::image type="content" source="./media/how-to-scale-compute/compute-processor.png" alt-text="Screenshot showing where to select a different compute processor manufacturer." lightbox="./media/how-to-scale-compute/compute-processor.png":::

1. To select a different machine size, expand the **Compute size** drop-down and select the size that best suits your needs.

    :::image type="content" source="./media/how-to-scale-compute/compute-size.png" alt-text="Screenshot showing where to select a different compute size." lightbox="./media/how-to-scale-compute/compute-size.png":::

1. When you choose your desired configuration, select **Save**.

    :::image type="content" source="./media/how-to-scale-compute/save.png" alt-text="Screenshot showing the location of the Save button, enabled once you make some changes to current configuration." lightbox="./media/how-to-scale-compute/save.png":::

1. If the changes you request require a server restart and its associated service disruption, confirm or cancel your decision to apply the configuration change.

    :::image type="content" source="./media/how-to-scale-compute/confirm-scale-compute-storage.png" alt-text="Screenshot showing the Compute + server dialog to confirm or abort the operation." lightbox="./media/how-to-scale-compute/confirm-scale-compute-storage.png":::

1. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-compute/deployment-progress-notification.png" alt-text="Screenshot showing a deployment is in progress to scale the compute." lightbox="./media/how-to-scale-compute/deployment-progress-notification.png":::

1. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-compute/deployment-succeeded-notification.png" alt-text="Screenshot showing that the deployment to scale the compute succeeded." lightbox="./media/how-to-scale-compute/deployment-succeeded-notification.png":::

### [CLI](#tab/cli-scale-compute)

Use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command to scale your compute.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --tier <tier> \
  --sku-name <sku_name>
```

> [!NOTE]
> You might need to include other parameters with the previous command. The presence and values of these parameters depend on how you want to configure other features of the existing server.

The list of allowed values for the `--sku-name` parameter depends on the value you pass to the `--tier` parameter and the region where you're trying to deploy your server.

If you pass an incorrect value to `--sku-name`, you get the following error with the list of supported SKU names:

```output
Invalid value for --sku-name. The SKU name is not available in the <tier> tier. Provide a valid SKU name for this tier, or specify --tier with the correct tier. Allowed values: ['<sku_name_1>', '<sku_name_2>', ..., '<sku_name_n>']
```

If the changes you're requesting require a server restart and its associated service disruption, and you didn't provide the `--yes` parameter, you receive the following prompt:

```output
You are trying to update the compute or storage size assigned to your server in a way that requires a server restart. During the restart, you'll experience some downtime of the server. Do you want to proceed? (y/n): 
```

---

## Related content

- [Compute options](../compute-storage/concepts-compute.md).
- [Limits in Azure Database for PostgreSQL flexible server](../configure-maintain/concepts-limits.md).
- [Near-zero downtime scaling](concepts-scaling-resources.md#near-zero-downtime-scaling).
