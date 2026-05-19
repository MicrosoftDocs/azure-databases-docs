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

# Scale compute in Azure HorizonDB

This article provides step-by-step instructions to perform scaling operations for the compute in Azure HorizonDB.

When you request a scaling operation of the compute used by your Azure HorizonDB, your server undergoes a restart.

## Steps to scale compute

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

2. In the settings menu, select **Compute** blade.

3. Use the **vCores** slider to adjust the number of cores as needed. The underlying memory is automatically adjusted. 

    :::image type="content" source="./media/how-to-scale-server/scaling.png" alt-text="Screenshot showing the scaling page." lightbox="./media/how-to-scale-server/scaling.png":::

4. Once you choose your desired configuration, select **Save**.

> [!NOTE]  
> When you select **Save** you're not asked for confirmation to proceed with the changes. The operation is immediately initiated and can't be aborted.

5. A notification shows that a compute update is in progress.

 :::image type="content" source="./media/how-to-scale-server/update-cores.png" alt-text="Screenshot showing the configuration page." lightbox="./media/how-to-scale-server/update-cores.png":::

6. When the scale process completes, a notification shows that the deployment succeeded.

 :::image type="content" source="./media/how-to-scale-server/success-cores.png" alt-text="Screenshot showing the successful update." lightbox="./media/how-to-scale-server/success-cores.png":::

> [!NOTE]  
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.


## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).




