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

3. You're redirected to the **Create Azure HorizonDB  - Restore** wizard, from where you can configure some settings for the new cluster that is getting created. In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point**.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/how-to-restore-server/custom-restore-point.png":::

4. In **Custom restore point (UTC)**, select a date from the calendar control, and specify a time in the time text box. Select a restore point based on your requirements. The most recent available restore point is always at least 5 minutes behind the current time.

    :::image type="content" source="./media/how-to-restore-server/custom-restore-point-date-time.png" alt-text="Screenshot showing the date picker and time textbox, available to configure the custom restore point." lightbox="./media/how-to-restore-server/custom-restore-point-date-time.png":::

> [!NOTE]
>  Point-in-time restore is limited to timestamps that are at least 300 seconds earlier than the current time. Select a restore point that is at least 5 minutes in the past.

5. If you want to change the type of compute assigned to the new server, or if you want to deploy it with high availablity or replicas, select **Configure server**:

    :::image type="content" source="./media/how-to-restore-server/configure-server-button.png" alt-text="Screenshot showing the location of the Configure server link." lightbox="./media/how-to-restore-server/configure-server-button.png":::

7. The **Compute** opens to show compute options for the new server:

    :::image type="content" source="./media/how-to-restore-server/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/how-to-restore-server/configure-server-page.png":::

8. Use the following table to understand the meaning of the different fields available in the **Compute +** page, and as guidance to fill the page:

    | Section | Setting | Suggested value | Description | Can be changed after instance creation |
    | --- | --- | --- | --- | --- |
    | **Compute** | | | | |
    | | **Compute size** | Change the processor and vcores as per your needs. | Notice that the list of supported values might vary across regions, depending on the hardware available on each region. For more information, see [Compute options in Azure HorizonDB ](../compute-storage/concepts-compute.md). | Can be changed after instance is created. |
    | **Replicas** | | | | |
    | | **High Availability** | Choose *Zone redundant - Replica ina different availability zone* or  *Disabled* based upon your high availability needs. |
    | | **Readable high availability replicas** | use the slider to configure number of replicas.

    | **Backups** | | | | |
    | | **Backup retention period (in days)** | Can't be changed and is automatically set to 7. | The default backup retention period is 7 days. ||
    
9. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/how-to-restore-server/restore-point-review-create.png":::

10. Review that all configurations for the new deployment are correctly set, and select **Create**.

    :::image type="content" source="./media/how-to-restore-server/restore-point-create.png" alt-text="Screenshot showing the location of the Create button." lightbox="./media/how-to-restore-server/restore-point-create.png":::

11. A new deployment is launched to create your new Azure HorizonDB  and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure HorizonDB , on which the most recent data available on the source server is restored." lightbox="./media/how-to-restore-server/restore-point-deployment-progress.png":::

12. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure HorizonDB , and start using it:

    :::image type="content" source="./media/how-to-restore-server/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure HorizonDB ." lightbox="./media/how-to-restore-server/restore-point-deployment-completed.png":::



## Related content

- [Overview of business continuity in Azure HorizonDB](../backup-restore/concepts-business-continuity.md)

