---
title: Perform On-Demand Backups in Azure Database for PostgreSQL Flexible Server
description: Perform on-demand backups in Azure Database for PostgreSQL flexible server using the Azure portal or CLI. Follow these instructions to perform on-demand backups.
#customer intent: As a user, I want to learn how can I performn on-demand backups of an Azure Database for PostgreSQL.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/05/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
ai-usage: ai-assisted
---

# Perform on-demand backups in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions for performing on-demand backups of an Azure Database for PostgreSQL flexible server.

## Steps to perform on-demand backups

### [Portal](#tab/portal-perform-on-demand-backups)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-restore.png" alt-text="Screenshot showing the Backup and restore page." lightbox="./media/how-to-on-demand-backup/backup-restore.png":::

1. Select **Backup**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-now.png" alt-text="Screenshot showing the Backup now button in the Backup and restore page." lightbox="./media/how-to-on-demand-backup/backup-now.png":::

1.  In the **Backup** pane, the **Backup name** text box is prefilled with a unique name automatically generated for your backup. Change the name if you want.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-name.png" alt-text="Screenshot showing the Backup pane with the text box in which you have to provide the backup name." lightbox="./media/how-to-on-demand-backup/backup-name.png":::

1. Select the **Backup** button.

    :::image type="content" source="./media/how-to-on-demand-backup/backup.png" alt-text="Screenshot showing the Trigger button." lightbox="./media/how-to-on-demand-backup/backup.png":::

1.  A notification informs you that the on-demand backup is initiated.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-initiated.png" alt-text="Screenshot showing the notification informing that on-demand backup is initiated." lightbox="./media/how-to-on-demand-backup/notification-initiated.png":::

1.  Upon successful completion, a notification informs you that the on-demand backup is completed.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-completed.png" alt-text="Screenshot showing the notification informing that on-demand backup is completed." lightbox="./media/how-to-on-demand-backup/notification-completed.png":::

### [CLI](#tab/cli-perform-on-demand-backups)

Use the [az postgres flexible-server backup create](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-create) command to start an on-demand backup of a server.

```azurecli-interactive
az postgres flexible-server backup create \
  --resource-group <resource_group> \
  --name <server> \
  --backup-name <backup>
```

---

> [!NOTE]
> You receive an InternalServerError under any of the following circumstances:
> - If another on-demand backup with the same name already exists in that server.
> - If another on-demand backup is in progress and isn't finished yet.

## Related content

- [List all backups](how-to-list-all-backups.md).
- [Delete on-demand backups](how-to-delete-backups.md)
