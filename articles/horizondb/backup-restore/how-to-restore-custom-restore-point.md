---
title: Point in Time Restore in Azure HorizonDB
description: This article describes how to restore to custom restore point an Azure HorizonDB.
#customer intent: As a user, I want to restore my Azure HorizonDB to a specific point in time, so that I can recover data after an accidental change or deletion.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: backup-restore
ms.topic: how-to
---

# Restore for Azure HorizonDB (Preview)

This article explains the point-in-time restore (PITR) feature in Azure HorizonDB.

Point-in-time restore (PITR) in Azure HorizonDB creates a new server in the same region as the source server. The HorizonDB service restores a database to any point in time within the configured retention period by using the following process:

1. Restores the most recent snapshot prior to the selected restore time.
1. Applies write-ahead logs (WAL) from that snapshot forward to the desired restore point to ensure transactional consistency.

If the most recent snapshot is taken at 6:00 PM and the specified restore point is 9:00 PM, the service restores the 6:00 PM snapshot and then replays WAL generated between 6:00 PM and 9:00 PM

Because restore operations are based on snapshots and WAL replay rather than full data movement, restore time isn't dependent on database size. As a result, restoring a HorizonDB database within the same region typically completes in minutes, even for large multi-terabyte databases.

## Restore to custom restore point in Azure HorizonDB

This article provides step-by-step instructions to perform a restore of an Azure HorizonDB to a custom restore point.

## Steps to restore to custom restore point

### [Portal](#tab/portal-restore-custom-restore-point)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, select **Overview** and select the **Restore** button.

   :::image type="content" source="media/how-to-restore-custom-restore-point/overview.png" alt-text="Screenshot showing the Overview page." lightbox="media/how-to-restore-custom-restore-point/overview.png":::

1. You're redirected to the **Create Azure HorizonDB - Restore** wizard, where you can configure settings for the new cluster being created. In the **Point-in-time-restore (PITR)** section, select **Select a custom restore point** and then choose a restore date and time from the calendar based on your requirements. The most recent available restore point is always at least 5 minutes behind the current time.

   :::image type="content" source="media/how-to-restore-custom-restore-point/custom-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="media/how-to-restore-custom-restore-point/custom-restore-point.png":::

   > [!NOTE]  
   > During Preview, point-in-time restore is limited to 5 minutes before current timestamp. Select a restore point that is at least 5 minutes in the past.

1. If you want to modify the compute tier for the new server, or enable high availability or replicas, select **Configure server** and update the settings as needed. If you prefer to use the source server's settings, you can skip this step.

   :::image type="content" source="media/how-to-restore-custom-restore-point/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="media/how-to-restore-custom-restore-point/configure-server-page.png":::

1. Review that all configurations for the new deployment are correct, and select **Create**.

   :::image type="content" source="media/how-to-restore-custom-restore-point/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="media/how-to-restore-custom-restore-point/restore-point-review-create.png":::

1. A new deployment is initiated to create a new Azure HorizonDB and restore it using the most recent data available.

   :::image type="content" source="media/how-to-restore-custom-restore-point/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure HorizonDB." lightbox="media/how-to-restore-custom-restore-point/restore-point-deployment-progress.png":::

1. When the deployment completes, you can select **Go to resource**, to get you to the **Overview** page of your new Azure HorizonDB, and start using it.

### [CLI](#tab/cli-restore-custom-restore-point)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to restore a new Azure HorizonDB cluster from the backups of an existing one.

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{targetSubscriptionId}/resourceGroups/{targetResourceGroupName}/providers/Microsoft.HorizonDB/clusters/{targetCluster}?api-version=2026-01-20-preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "createMode": "PointInTimeRestore",
      "pointInTimeUTC": "{YYYY-MM-DDTHH:mm:ss.SSSZ}"
      "sourceClusterResourceId": "/subscriptions/{sourceSubscriptionId}/resourceGroups/{sourceResourceGroupName}/providers/Microsoft.HorizonDB/clusters/{sourceCluster}"
    }
  }'

```

If you pass an invalid value for the `pointInTimeUTC` property, you receive the following error:

```output
"code": "InvalidPointInTimeRestore",
"message": "The supplied point-in-time restore timestamp is invalid (out of range, malformed, or in the future)."
```

---

## Related content

- [Backups in Azure HorizonDB (Preview)](concepts-backup-restore.md)
