---
title: Scale compute
description: This article describes how to scale the compute of an Azure Database for PostgreSQL flexible server.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to scale the compute of an Azure Database for PostgreSQL.
---

# Scale compute

This article provides step-by-step instructions to perform scaling operations for the compute of an Azure Database for PostgreSQL flexible server.

You're allowed to change your compute between the burstable, general purpose, and memory optimized tiers. And, among each of those tiers, you can choose the number of virtual cores (vCores) that is more suitable to run your application. To learn more about the different compute tiers available in Azure Virtual Machines, and the use case for which they're best suited, refer to [size for virtual machines in Azure](/azure/virtual-machines/sizes/overview).

When you request a scaling operation of the compute used by your Azure Database for PostgreSQL flexible server, your server undergoes a restart and so leaves your server unavailable for some time. For more information about how that process works, and the expected duration of the downtime, see [near-zero downtime scaling](concepts-scaling-resources.md#near-zero-downtime-scaling).

## Steps to scale compute

### [Portal](#tab/portal-scale-compute)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Compute + storage**.

    :::image type="content" source="./media/how-to-scale-compute/compute-storage.png" alt-text="Screenshot showing how to select the Compute + storage page." lightbox="./media/how-to-scale-compute/compute-storage.png":::

3. If you want to select a different tier than the one currently selected, in the **Compute tier** group of radio buttons, select the option that best adjusts to your needs.

    :::image type="content" source="./media/how-to-scale-compute/compute-tier.png" alt-text="Screenshot showing where to select a different compute tier." lightbox="./media/how-to-scale-compute/compute-tier.png":::

4. If the region of your server supports Intel and AMD processors, you can use the **Compute processor** radio button to filter the options listed in the **Compute size** drop-down to only hardware produced by the manufacturer selected.

    :::image type="content" source="./media/how-to-scale-compute/compute-processor.png" alt-text="Screenshot showing where to select a different compute processor manufacturer." lightbox="./media/how-to-scale-compute/compute-processor.png":::

5. If you want to select a different machine size among the ones available in the same tier, expand the **Compute size** drop-down and select the size that best suits your needs.

    :::image type="content" source="./media/how-to-scale-compute/compute-size.png" alt-text="Screenshot showing where to select a different compute size." lightbox="./media/how-to-scale-compute/compute-size.png":::

6. Once you choose your desired configuration, select **Save**.

    :::image type="content" source="./media/how-to-scale-compute/save.png" alt-text="Screenshot showing the location of the Save button, enabled once you make some changes to current configuration." lightbox="./media/how-to-scale-compute/save.png":::

> [!NOTE]
> Notice that when you select **Save** you're not asked for confirmation to proceed with the changes. The operation is immediately initiated and can't be aborted.

7. A notification shows that a deployment is in progress.

    :::image type="content" source="./media/how-to-scale-compute/deployment-progress-notification.png" alt-text="Screenshot showing a deployment is in progress to scale the compute." lightbox="./media/how-to-scale-compute/deployment-progress-notification.png":::

8. When the scale process completes, a notification shows that the deployment succeeded.

    :::image type="content" source="./media/how-to-scale-compute/deployment-succeeded-notification.png" alt-text="Screenshot showing that the deployment to scale the compute succeeded." lightbox="./media/how-to-scale-compute/deployment-succeeded-notification.png":::

### [CLI](#tab/cli-scale-compute)

You can initiate the scaling of your compute via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --tier <tier> \
  --sku-name <sku_name>
```

> [!NOTE]
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

The list of allowed values for the `--sku-name` parameter is dependent of the value passed to the `--tier` parameter, and of the region in which you're trying to deploy your server.

If you pass an incorrect value to `--sku-name`, you get the following error with the list of 

```output
Incorrect value for --sku-name. The SKU name does not match <tier> tier. Specify --tier if you did not. Or CLI will set GeneralPurpose as the default tier. Allowed values : ['<sku_name_1>', '<sku_name_2>', ..., '<sku_name_n>']
```

---

## Related content

- [Compute options](../configure-maintain/concepts-compute.md).
- [Limits in Azure Database for PostgreSQL flexible server](../configure-maintain/concepts-limits.md).
- [Near-zero downtime scaling](concepts-scaling-resources.md#near-zero-downtime-scaling)
