---
title: Scale Compute in Azure HorizonDB
description: This article describes how to scale the compute in Azure HorizonDB.
#customer intent: As a user, I want to scale compute resources in Azure HorizonDB, so that I can match capacity to changing workload demands.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: scale-out
ms.topic: how-to
---

# Scale compute in Azure HorizonDB (Preview)

This article provides step-by-step instructions for scaling the compute resources in Azure HorizonDB.

When you initiate a compute scaling operation in Azure HorizonDB, the server restarts as part of the process. During this restart, the database is temporarily unavailable, and existing connections are dropped. The service applies the new compute configuration during the restart and automatically brings the server back online once scaling is complete.

## Steps to scale compute

### [Portal](#tab/portal-scale-compute)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, under the **Settings** section, select **Compute**.

1. Use the **vCores** slider to adjust the number of cores as needed. The underlying memory is automatically adjusted.

   :::image type="content" source="media/how-to-scale-compute/scaling.png" alt-text="Screenshot showing the Compute page from where number of virtual cores can be scaled up or down." lightbox="media/how-to-scale-compute/scaling.png":::

1. When you choose your desired configuration, select **Save**.

> [!NOTE]  
> When you select **Save**, the changes are applied immediately. No confirmation prompt appears, and you can't cancel the operation.

1. A notification shows that a compute update is in progress.

:::image type="content" source="media/how-to-scale-compute/update-cores.png" alt-text="Screenshot showing the notification that configuration page." lightbox="media/how-to-scale-compute/update-cores.png":::

1. When the scaling process completes, a notification shows that the deployment succeeded.

:::image type="content" source="media/how-to-scale-compute/success-cores.png" alt-text="Screenshot showing the successful update." lightbox="media/how-to-scale-compute/success-cores.png":::

### [CLI](#tab/cli-scale-compute)

Use the [az horizondb update](/cli/azure/horizondb#az-horizondb-update) command to scale the number of vCores assigned to each compute replica of a cluster.

```azurecli-interactive
az horizondb cluster update \
  --resource-group <resource_group> \
  --name <cluster> \
  --v-cores <cores>
```

---

## Related content

- [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md)
