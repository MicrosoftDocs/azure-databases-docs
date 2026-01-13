---
title: Perform on-demand backups
description: This article describes how to perform on-demand backups of an Azure Database for PostgreSQL flexible server.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.topic: how-to
# customer intent: As a user, I want to learn how can I performn on-demand backups of an Azure Database for PostgreSQL.
---

# Perform on-demand backups

This article provides step-by-step instructions to perform on-demand backups of an Azure Database for PostgreSQL flexible server.

## Steps to perform on-demand backups

### [Portal](#tab/portal-perform-on-demand-backups)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-and-restore.png" alt-text="Screenshot showing the Backup and restore page." lightbox="./media/how-to-on-demand-backup/backup-and-restore.png":::

3. Select **Backup**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-now.png" alt-text="Screenshot showing the Backup now button in the Backup and restore page." lightbox="./media/how-to-on-demand-backup/backup-now.png":::

4.  In the **Backup** pane, the **Backup name** text box is prefilled with a unique name automatically generated for your backup. Feel free to change that name to any name of your preference.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-name.png" alt-text="Screenshot showing the Take backup pane and highlighting the text box in which you have to provide the backup name." lightbox="./media/how-to-on-demand-backup/backup-name.png":::

5. Select the **Backup** button.

    :::image type="content" source="./media/how-to-on-demand-backup/backup.png" alt-text="Screenshot showing the Trigger button." lightbox="./media/how-to-on-demand-backup/backup.png":::

6.  A notification informs you that the on-demand backup is initiated.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-initiated.png" alt-text="Screenshot showing the notification informing that on-demand backup is initiated." lightbox="./media/how-to-on-demand-backup/notification-initiated.png":::

7.  Upon successful completion, a notification informs you that the on-demand backup is completed.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-completed.png" alt-text="Screenshot showing the notification informing that on-demand backup is completed." lightbox="./media/how-to-on-demand-backup/notification-completed.png":::

### [CLI](#tab/cli-perform-on-demand-backups)

You can initiate an on-demand backup of a server via the [az postgres flexible-server backup create](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-create) command.

```azurecli-interactive
az postgres flexible-server backup create \
  --resource-group <resource_group> \
  --name <server> \
  --backup-name <backup>
```

---

> [!NOTE]
> Under any of the following circumstances, you receive an InternalServerError:
> - If another on-demand backup with the same name already exists in that server.
> - If another on-demand backup is being taken, and isn't completed yet.

## Related content

- [List all backups](how-to-list-all-backups.md).
- [Delete on-demand backups](how-to-delete-backups.md).
