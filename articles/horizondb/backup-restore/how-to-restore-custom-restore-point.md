---
title: Restore to custom restore point in Azure HorizonDB
description: This article describes how to restore to custom restore point an Azure HorizonDB.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
#customer intent: As a user, I want to learn how to restore to custom restore point an Azure HorizonDB.
---

# Restore to custom restore point in Azure HorizonDB

This article provides step-by-step instructions to perform a restore of an Azure HorizonDB  to a custom restore point.

## Steps to restore to custom restore point

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB .

2. In the resource menu, select **Overview** and click the **Restore** button.

    :::image type="content" source="./media/how-to-restore-server/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-restore-server/overview.png":::

3. You are redirected to the **Create Azure HorizonDB  - Restore** wizard, fwhere you can configure settings for the new cluster being created.In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point**  select Custom restore point, and then choose a restore date and time from the calendar based on your requirements. The most recent available restore point is always at least 5 minutes behind the current time.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/how-to-restore-server/custom-restore-point.png":::

 
> [!NOTE]
>  Point-in-time restore is limited to timestamps that are at least 300 seconds earlier than the current time. Select a restore point that is at least 5 minutes in the past.

4. If you want to change the type of compute assigned to the new server, or if you want to deploy it with high availablity or replicas, select **Configure server** and adjust the settings as needed.

     :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::
    

5. Review that all configurations for the new deployment are correctly set, and select **Create**.

      :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

6.  A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

  :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure HorizonDB ." lightbox="./media/how-to-restore-server/restore-point-deployment-process.png":::

7. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure HorizonDB , and start using it:

  

## Related content

- [Overview of business continuity in Azure HorizonDB](../backup-restore/concepts-business-continuity.md)

