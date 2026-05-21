---
title: Scale Compute in Azure HorizonDB
description: This article describes how to scale the compute in Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: scale-out
ms.topic: how-to
# customer intent: As a user, I want to learn how to scale the compute in Azure HorizonDB.
---

# Scale compute in Azure HorizonDB (preview)

This article provides step-by-step instructions to perform scaling operations for the compute in Azure HorizonDB.

When you initiate a compute scaling operation in Azure HorizonDB, the server is restarted as part of the process. During this restart, the database becomes temporarily unavailable, and existing connections are dropped. The service applies the new compute configuration during the restart and automatically brings the server back online once scaling is complete. 

## Steps to scale compute

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

2. In the settings menu, select **Compute** blade.

3. Use the **vCores** slider to adjust the number of cores as needed. The underlying memory is automatically adjusted. 

    :::image type="content" source="./media/scaling.png" alt-text="Screenshot showing the scaling page." lightbox="./media/scaling.png":::

4. Once you choose your desired configuration, select **Save**.

> [!NOTE]  
>  When you select **Save**, the changes are applied immediately. No confirmation prompt is shown, and the operation can't be canceled.

5. A notification shows that a compute update is in progress.

 :::image type="content" source="./media/update-cores.png" alt-text="Screenshot showing the configuration page." lightbox="./media/update-cores.png":::

6. When the scaling process completes, a notification shows that the deployment succeeded.

 :::image type="content" source="./media/success-cores.png" alt-text="Screenshot showing the successful update." lightbox="./media/success-cores.png":::


## Related content

- [Backups in Azure HorizonDB](../backup-restore/concepts-backup-restore.md)
