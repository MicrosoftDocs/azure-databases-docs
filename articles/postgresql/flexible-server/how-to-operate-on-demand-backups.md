---
title: On-demand backups (preview)
description: This article describes how to perform, list, and delete on-demand backups of an Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 01/09/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how can I operate full backups of my Azure Database for PostgreSQL flexible server, including how to perform a backup, how to list, and how to delete existing backups.
---

# On-demand backups (Preview)

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to operate with on-demand backups of an Azure Database for PostgreSQL flexible server.

> [!IMPORTANT]
> On-demand backups are automatically deleted, according to your configured backup retention period. However, you can manually delete them earlier if they’re no longer needed.

## Perform on-demand backups

### [Portal](#tab/portal-perform-on-demand-backups)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-and-restore.png" alt-text="Screenshot showing the Backup and restore page." lightbox="./media/how-to-on-demand-backup/backup-and-restore.png":::

3. Select **Backup now**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-now.png" alt-text="Screenshot showing the Backup now button in the Backup and restore page." lightbox="./media/how-to-on-demand-backup/backup-now.png":::

4.  In the **Take backup** pane, the **Backup name** text box is prefilled with a unique name automatically generated for your backup. Feel free to change that name to any name of your preference.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-name.png" alt-text="Screenshot showing the Take backup pane and highlighting the text box in which you have to provide the backup name." lightbox="./media/how-to-on-demand-backup/backup-name.png":::

5. Select **Trigger**.

    :::image type="content" source="./media/how-to-on-demand-backup/trigger.png" alt-text="Screenshot showing the Trigger button." lightbox="./media/how-to-on-demand-backup/trigger.png":::

6.  A notification informs you that the on-demand backup is initiated.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-initiated.png" alt-text="Screenshot showing the notification informing that on-demand backup is initiated." lightbox="./media/how-to-on-demand-backup/notification-initiated.png":::

7.  Upon successful completion, a notification informs you that the on-demand backup is completed.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-completed.png" alt-text="Screenshot showing the notification informing that on-demand backup is completed." lightbox="./media/how-to-on-demand-backup/notification-completed.png":::

### [CLI](#tab/cli-perform-on-demand-backups)

You can initiate an on-demand backup of a server via the [az postgres flexible-server backup create](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-create) command.

```azurecli-interactive
az postgres flexible-server backup create --resource-group <resource_group> --name <server> --backup-name <backup>
```

---

> [!NOTE]
> Under any of the following circumstances, you receive an InternalServerError:
> - If another on-demand backup with the same name already exists in that server.
> - If another on-demand backup is being taken, and isn't completed yet.

## List on-demand backups

### [Portal](#tab/portal-list-on-demand-backups)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png" alt-text="Screenshot showing the Backup and restore page with some automatic and on-demand backups available." lightbox="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png":::

3. In **Backup types**, select **On-Demand backup** if you want to only see the on-demand backups which are still available to be restored.

    :::image type="content" source="./media/how-to-on-demand-backup/list-on-demand-backups.png" alt-text="Screenshot showing how to filter the list of backups to only display on-demand backups." lightbox="./media/how-to-on-demand-backup/list-on-demand-backups.png":::

### [CLI](#tab/cli-list-on-demand-backups)

You can list currently available on-demand backups of a server via the [az postgres flexible-server backup list](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-list) command.

```azurecli-interactive
az postgres flexible-server backup list --resource-group <resource_group> --name <server> --query "[?backupType=='Customer On-Demand']" --output table
```

---

## Delete on-demand backups

### [Portal](#tab/portal-delete-on-demand-backups)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png" alt-text="Screenshot showing the Backup and restore page with some automatic and on-demand backups available." lightbox="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png":::

3. In **Backup types**, select **On-Demand backup** if you want to only see the on-demand backups which are still available to be restored.

    :::image type="content" source="./media/how-to-on-demand-backup/list-on-demand-backups.png" alt-text="Screenshot showing how to filter the list of backups to only display on-demand backups." lightbox="./media/how-to-on-demand-backup/list-on-demand-backups.png":::

4. Identify the on-demand backup that you want to delete. Then, under the **Actions** column, select **Delete** to initiate the deletion of that particular on-demand backup.

    :::image type="content" source="./media/how-to-on-demand-backup/delete-on-demand-backup.png" alt-text="Screenshot showing how to delete an on-demand backup." lightbox="./media/how-to-on-demand-backup/delete-on-demand-backup.png":::

5.  A notification informs you that the on-demand backup is being deleted.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-backup-deleting.png" alt-text="Screenshot showing the notification informing that on-demand backup is being deleted." lightbox="./media/how-to-on-demand-backup/notification-backup-deleting.png":::

6.  Upon successful completion, a notification informs you that the on-demand backup is deleted.

    :::image type="content" source="./media/how-to-on-demand-backup/notification-backup-deleted.png" alt-text="Screenshot showing the notification informing that on-demand backup is deleted." lightbox="./media/how-to-on-demand-backup/notification-backup-deleted.png":::

### [CLI](#tab/cli-delete-on-demand-backups)

You can delete any of the currently available on-demand backups of a server via the [az postgres flexible-server backup delete](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-delete) command.

```azurecli-interactive
az postgres flexible-server backup delete --resource-group <resource_group> --name <server> --backup-name <backup>
```

If you run the previous command, it requires you to explicitly confirm, responding with a `y` (yes):

```output
Are you sure you want to delete the backup '<backup>' in server '<server>'
```

If you want to run the command without needing the user interaction, you can add the `--yes` parameter like this:

```azurecli-interactive
az postgres flexible-server backup delete --resource-group <resource_group> --name <server> --backup-name <backup> --yes
```

> [!NOTE]
> If you provide the name that doesn't match any of the available on-demand backups, the command doesn't report any error.

---

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).
