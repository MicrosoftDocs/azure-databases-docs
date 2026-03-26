---
title: Migrate SSD Server to SSDv2 Using Replicas
description: This article describes how to migrate a Premium SSD server to Premium SSDv2 using replicas in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 08/10/2025
ms.service: azure-database-postgresql
ms.subservice: compute-storage
ms.topic:  concept-article
#customer intent: As a user, I want to learn how to migrate from Premium SSD server to Premium SSDv2 in Azure Database for PostgreSQL flexible server.
---

# Migrate or replicate from Premium SSD to Premium SSDv2

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to migrate from Premium SSD to Premium SSDv2  using replication in Azure Database for PostgreSQL flexible server.

## Steps to migrate or replicate from Premium SSD to Premium SSDv2

### [Portal](#tab/portal-restore-custom-point)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Settings** go to **Replication** and click the **Create replica** button. 


    :::image type="content" source="./media/concepts-storage-replicate-ssd-to-ssd-v2/create-replica.png" alt-text="Screenshot showing the Replication page." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/create-replica.png":::

3.  Provide Server name and Select **Configure server**.

 :::image type="content" source="./media/concepts-storage-replicate-ssd-to-ssd-v2/configure-server-page.png" alt-text="Screenshot showing the Compute + storage page." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/configure-server-page.png":::


4. Choose **Premium SSD v2** for the **Storage type** Field.

    :::image type="content" source="./media/concepts-storage-replicate-ssd-to-ssd-v2/latest-restore-point.png" alt-text="Screenshot showing the Premium SSDv2 storage type button selected." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/premium-ssdv2.png":::

5.  Once all the replica server is configured to your needs, select **Review + create**.

    
      :::image type="content" source="./media/concepts-storage-replicate-ssd-to-ssd-v2/configure-server-page.png" alt-text="Screenshot showing the Add Replica page." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/Add-replica-validation.png":::


7. A new deployment is launched to create your new Azure Database for PostgreSQL flexible server with Premium SSD v2 storage type with the latest data using replication.

   
8. When the deployment completes, you can select **Go to resource**, to get you to the **Compute +Storage** page of your new Azure Database for PostgreSQL flexible server, and start validate your **Storage type**.

    :::image type="content" source="./media/concepts-storage-replicate-ssd-to-ssd-v2/restore-point-deployment-completed.png" alt-text="Screenshot that shows new server created using premium ssd v2." lightbox="./media/concepts-storage-replicate-ssd-to-ssd-v2/validate-ssdv2.png":::

9. Select **Replication** and click  **Switch over or promote to standalone**, select **Promote to standalone server and remove from replication.This won't impact primary server** for **Action**. And select **Planned-sync data before promoting**  and you have to mark the **I understand that this read replica will become an independent standalone server and this action can't be undone.** checkbox to acknowledge. Finally, select **Promote to standalone**.

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
