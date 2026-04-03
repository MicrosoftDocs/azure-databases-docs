---
title: Migrate SSD Server to SSDv2 Using Point-in-Time-Restore
description: This article describes how to migrate a Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 08/10/2025
ms.service: azure-database-postgresql
ms.subservice: compute-storage
ms.topic:  concept-article
#customer intent: As a user, I want to learn how to migrate from Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
---

# Migrate or restore from Premium SSD to Premium SSDv2

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to perform a restore of an Azure Database for PostgreSQL flexible server to a custom restore point.

## Steps to migrate or restore from Premium SSD to Premium SSDv2

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.


    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/overview.png":::

3. Select the **Restore** button.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-button.png":::

4. You're redirected to the **Create Azure Database for PostgreSQL flexible server - Restore server** wizard, from where you can configure some settings for the new server that is getting created. In the **Point-in-time-restore (PITR)** section, select **Latest restore point**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/latest-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/latest-restore-point.png":::

5. Select **Configure server** and choose **Premium SSD v2** for the **Storage type** Field.
  
    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-page.png":::


6. Once all the new server is configured to your needs, select **Review + create**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-review-create.png":::


7. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-progress.png":::

8. When the deployment completes, you can select **Go to resource**, to get you to the **Compute +Storage** page of your new Azure Database for PostgreSQL flexible server, and start validate your **Storage type**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-custom-point)

You can restore a backup of a server to the latest restore point via the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command.

```azurecli-interactive
az postgres flexible-server restore \
  --resource-group <resource_group> \
  --name <server> \
  --source-server <source_server> \
  --restore-time 2025-04-26T02:10:00+00:00
  --storage-type PremiumV2_LRS
```

> [!NOTE]
> - The value passed to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If the `--restore-time` parameter isn't present, its value defaults to the current time in the system from where the command is executed.
> - If the value passed is in the future, the backend service that receives the request normalizes it to the current date and time.
> - If the value passed is earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Related content

- [Restore to latest restore point](../backup-restore/how-to-restore-latest-restore-point.md).
- [Restore full backup (fast restore)](../backup-restore/how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](../backup-restore/how-to-restore-paired-region.md).
- [Restore a dropped server](../backup-restore/how-to-restore-dropped-server.md).
