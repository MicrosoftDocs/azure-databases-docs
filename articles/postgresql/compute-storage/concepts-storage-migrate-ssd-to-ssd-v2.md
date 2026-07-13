---
title: Migrate SSD Server to SSDv2 Using Point-in-Time-Restore
description: This article describes how to migrate a Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn how to migrate from Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: compute-storage
ms.topic: concept-article
---

# Migrate or restore from Premium SSD to Premium SSDv2

This article provides step-by-step instructions to restore an Azure Database for PostgreSQL flexible server to a custom restore point.

> [!NOTE]
> Premium SSD v2 provides a baseline of 3,000 IOPS and 125 MB/s throughput for disks up to 399 GiB, and 12,000 IOPS and 500 MB/s throughput for disks 400 GiB or larger, at no extra cost. After migration, you can adjust IOPS and throughput based on your workload requirements.

## Steps to migrate or restore from Premium SSD to Premium SSDv2

### [Portal](#tab/portal-restore-custom-point)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Overview**.


    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/overview.png":::

1. Select the **Restore** button.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-button.png" alt-text="Screenshot showing the location of the Restore button in the Overview page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-button.png":::

1. You're redirected to the **Create Azure Database for PostgreSQL flexible server - Restore server** wizard, where you can configure settings for the new server. In the **Point-in-time-restore (PITR)** section, select **Latest restore point**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/latest-restore-point.png" alt-text="Screenshot showing the Select a custom restore point radio button selected." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/latest-restore-point.png":::

1. Select **Configure server** and choose **Premium SSD v2** for the **Storage type** field.
  
    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/configure-server-page.png":::


1. When the new server is configured, select **Review + create**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-review-create.png" alt-text="Screenshot showing the location of the Review + create button." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-review-create.png":::


1. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server and restore the most recent data available on the source server at the time of restore:

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-progress.png" alt-text="Screenshot that shows the deployment in progress to create your new Azure Database for PostgreSQL Flexible server, on which the most recent data available on the source server is restored." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-progress.png":::

1. When the deployment completes, select **Go to resource**. You go to the **Compute +Storage** page of your new Azure Database for PostgreSQL flexible server, and start validate your **Storage type**.

    :::image type="content" source="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-completed.png" alt-text="Screenshot that shows the deployment successfully completed of your Azure Database for PostgreSQL Flexible server." lightbox="./media/concepts-storage-migrate-ssd-to-ssd-v2/restore-point-deployment-completed.png":::

### [CLI](#tab/cli-restore-custom-point)

To restore a server backup to the latest restore point, use the [az postgres flexible-server restore](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restore) command.

```azurecli-interactive
az postgres flexible-server restore \
  --resource-group <resource_group> \
  --name <server> \
  --source-server <source_server> \
  --restore-time 2025-04-26T02:10:00+00:00
  --storage-type PremiumV2_LRS
```

> [!NOTE]
> - The value you pass to the `--restore-time` parameter represents the point in time, in UTC, to restore from (ISO8601 format).
> - If you don't include the `--restore-time` parameter, the command uses the current time in the system where you run the command.
> - If you enter a future value, the backend service that receives the request normalizes it to the current date and time.
> - If you enter a value that's earlier than the earliest restore point available on the source server, you receive an InternalServerError.

---

## Related content

- [Restore to latest restore point](../backup-restore/how-to-restore-latest-restore-point.md).
- [Restore full backup (fast restore)](../backup-restore/how-to-restore-full-backup.md).
- [Restore to paired region (geo-restore)](../backup-restore/how-to-restore-paired-region.md).
- [Restore a deleted server](../backup-restore/how-to-restore-deleted-server.md).
