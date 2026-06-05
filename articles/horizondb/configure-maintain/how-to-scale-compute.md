---
title: Scale Compute in Azure HorizonDB
description: This article describes how to scale the compute in Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: scale-out
ms.topic: how-to
# customer intent: As a user, I want to learn how to scale the compute in Azure HorizonDB.
---

# Scale compute for Azure HorizonDB (Preview)

This article provides step-by-step instructions to perform scaling operations for the compute in Azure HorizonDB.

When you initiate a compute scaling operation in Azure HorizonDB, the server is restarted as part of the process. During this restart, the database becomes temporarily unavailable, and existing connections are dropped. The service applies the new compute configuration during the restart and automatically brings the server back online once scaling is complete.

## Steps to scale compute

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, under **Settings**, select **Compute**.

1. Use the **vCores** slider to adjust the number of cores as needed. The underlying memory is automatically adjusted.

   :::image type="content" source="media/how-to-scale-compute/scaling.png" alt-text="Screenshot showing the Compute page from where number of virtual cores can be scaled up or down." lightbox="media/how-to-scale-compute/scaling.png":::

1. Once you choose your desired configuration, select **Save**.

> [!NOTE]  
> When you select **Save**, the changes are applied immediately. No confirmation prompt is shown, and the operation can't be canceled.

1. A notification shows that a compute update is in progress.

:::image type="content" source="media/how-to-scale-compute/update-cores.png" alt-text="Screenshot showing the notification that configuration page." lightbox="media/how-to-scale-compute/update-cores.png":::

1. When the scaling process completes, a notification shows that the deployment succeeded.

:::image type="content" source="media/how-to-scale-compute/success-cores.png" alt-text="Screenshot showing the successful update." lightbox="media/how-to-scale-compute/success-cores.png":::

## Related content

- [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md)
