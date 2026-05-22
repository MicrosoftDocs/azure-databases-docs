---
title: Point in Time Restore in Azure HorizonDB
description: This article describes how to restore to custom restore point an Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 05/22/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
# customer intent: As a user, I want to learn how to restore to custom restore point an Azure HorizonDB.
---

# Restore in Azure HorizonDB (preview)

This article explains the Point-in-time restore (PITR) feature in Azure HorizonDB.

Point-in-time restore (PITR) in Azure HorizonDB creates a new server in the same region as the source server. HorizonDB service restores a database to any point in time within the configured retention period using the following process:

1. Restores the most recent snapshot prior to the selected restore time.
2. Applies write-ahead logs (WAL) from that snapshot forward to the desired restore point to ensure transactional consistency.

If the most recent snapshot is taken at 6:00 PM and the specified restore point is 9:00 PM, the service restores the 6:00 PM snapshot and then replays WAL generated between 6:00 PM and 9:00 PM

Because restore operations are based on snapshots and WAL replay rather than full data movement, restore time isn't dependent on database size. As a result, restoring a HorizonDB database within the same region typically completes in minutes, even for large multi-terabyte databases.

## Restore to custom restore point in Azure HorizonDB

This article provides step-by-step instructions to perform a restore of an Azure HorizonDB  to a custom restore point.

## Steps to restore to custom restore point

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

2. In the resource menu, select **Overview** and select the **Restore** button.

    :::image type="content" source="./media/how-to-restore-custom-restore-point/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-custom-restore-point/overview.png":::

3. You're redirected to the **Create Azure HorizonDB  - Restore** wizard, where you can configure settings for the new cluster being created. In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point**  and then choose a restore date and time from the calendar based on your requirements. The most recent available restore point is always at least 5 minutes behind the current time.

    :::image type="content" source="./media/how-to-restore-custom-restore-point/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/how-to-restore-custom-restore-point/custom-restore-point.png":::

> [!NOTE]  
> During Preview, point-in-time restore is limited to 5 minutes before current timestamp. Select a restore point that is at least 5 minutes in the past.

4. If you want to modify the compute tier for the new server, or enable high availability or replicas, select **Configure server** and update the settings as needed. If you prefer to use the source server's settings, you can skip this step.

     :::image type="content" source="./media/how-to-restore-custom-restore-point/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-custom-restore-point/configure-server-page.png":::

5. Review that all configurations for the new deployment are correctly set, and select **Create**.

      :::image type="content" source="./media/how-to-restore-custom-restore-point/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-custom-restore-point/restore-point-review-create.png":::

6. A new deployment is initiated to create a new Azure HorizonDB and restore it using the most recent data available.

      :::image type="content" source="./media/how-to-restore-custom-restore-point/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure HorizonDB." lightbox="./media/how-to-restore-custom-restore-point/restore-point-deployment-progress.png":::

7. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure HorizonDB, and start using it.

## Related content

- [Backups in Azure HorizonDB (preview)](concepts-backup-restore.md)
