---
title: List all backups
description: This article describes how to list all backups of an Azure Database for PostgreSQL flexible server instance.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how can I list all full backups of an Azure Database for PostgreSQL flexible server instance.
---

# List all backups

This article provides step-by-step instructions to list all full backups of an Azure Database for PostgreSQL flexible server instance.

## Steps to list all backups

### [Portal](#tab/portal-list-on-demand-backups)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png" alt-text="Screenshot showing the Backup and restore page with some automatic and on-demand backups available." lightbox="./media/how-to-on-demand-backup/backup-and-restore-with-backups.png":::

3. In **Backup type**, select **On-demand** if you want to only see the on-demand backups which are still available to be restored.

    :::image type="content" source="./media/how-to-on-demand-backup/list-on-demand-backups.png" alt-text="Screenshot showing how to filter the list of backups to only display on-demand backups." lightbox="./media/how-to-on-demand-backup/list-on-demand-backups.png":::

### [CLI](#tab/cli-list-on-demand-backups)

You can list currently available on-demand backups of a server via the [az postgres flexible-server backup list](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-list) command.

```azurecli-interactive
az postgres flexible-server backup list \
  --resource-group <resource_group> \
  --name <server> \
  --query "[?backupType=='Customer On-Demand']" \
  --output table
```

---

## Related content

- [Perform on-demand backups](how-to-perform-backups.md).
- [Delete on-demand backups](how-to-delete-backups.md).
