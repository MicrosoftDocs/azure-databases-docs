---
title: Delete on-demand backups
description: This article describes how to delete on-demand backups of an Azure Database for PostgreSQL flexible server instance.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
# customer intent: As a user, I want to learn how can I delete full on-demand backups of an Azure Database for PostgreSQL flexible server instance.
---

# Delete on-demand backups

This article provides step-by-step instructions to delete on-demand backups of an Azure Database for PostgreSQL flexible server instance.

> [!IMPORTANT]
> On-demand backups are automatically deleted, according to your configured backup retention period. However, you can manually delete them earlier if they’re no longer needed.

## Steps to delete on-demand backups

### [Portal](#tab/portal-delete-on-demand-backups)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png" alt-text="Screenshot showing the Backup and restore page with some automatic and on-demand backups available." lightbox="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png":::

3. In **Backup type**, select **On-demand** if you want to only see the on-demand backups which are still available to be restored.

    :::image type="content" source="./media/how-to-on-demand-backup/list-on-demand-backups.png" alt-text="Screenshot showing how to filter the list of backups to only display on-demand backups." lightbox="./media/how-to-on-demand-backup/list-on-demand-backups.png":::

4. Identify the on-demand backup that you want to delete. Then, under the **Actions** column, select **Delete**.

    :::image type="content" source="./media/how-to-on-demand-backup/delete-on-demand-backup.png" alt-text="Screenshot showing how to delete an on-demand backup." lightbox="./media/how-to-on-demand-backup/delete-on-demand-backup.png":::

5. A dialog asks for confirmation before the irreversible operation is initiated. Select **Delete** if you want to initiate the permanent deletion of that particular on-demand backup.

    :::image type="content" source="./media/how-to-on-demand-backup/delete-confirmation.png" alt-text="Screenshot showing the confirmation dialog to initiate the deletion of an on-demand backup." lightbox="./media/how-to-on-demand-backup/delete-confirmation.png":::

6.  A notification informs you that the on-demand backup is being deleted.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-backup-deleting.png" alt-text="Screenshot showing the notification informing that on-demand backup is being deleted." lightbox="./media/how-to-on-demand-backup/notification-backup-deleting.png":::

7.  Upon successful completion, a notification informs you that the on-demand backup is deleted.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-backup-deleted.png" alt-text="Screenshot showing the notification informing that on-demand backup is deleted." lightbox="./media/how-to-on-demand-backup/notification-backup-deleted.png":::

### [CLI](#tab/cli-delete-on-demand-backups)

You can delete any of the currently available on-demand backups of a server via the [az postgres flexible-server backup delete](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-delete) command.

```azurecli-interactive
az postgres flexible-server backup delete \
  --resource-group <resource_group> \
  --name <server> \
  --backup-name <backup>
```

If you run the previous command, it requires you to explicitly confirm, responding with a `y` (yes):

```output
Are you sure you want to delete the backup '<backup>' in server '<server>'
```

If you want to run the command without needing the user interaction, you can add the `--yes` parameter like this:

```azurecli-interactive
az postgres flexible-server backup delete \
  --resource-group <resource_group> \
  --name <server> \
  --backup-name <backup> \
  --yes
```

> [!NOTE]
> If you provide the name that doesn't match any of the available on-demand backups, the command doesn't report any error.

---

## Related content

- [Perform on-demand backups](how-to-perform-backups.md).
- [List all backups](how-to-list-all-backups.md).
