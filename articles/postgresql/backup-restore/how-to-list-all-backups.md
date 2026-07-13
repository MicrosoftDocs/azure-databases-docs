---
title: List All Backups in Azure Database for PostgreSQL Flexible Server
description: List all backups in Azure Database for PostgreSQL flexible server using the Azure portal or CLI. Follow these instructions to view your backups.
#customer intent: As a user, I want to learn how can I list all full backups of an Azure Database for PostgreSQL flexible server.
author: danyal-bukhari
ms.author: dabukhari
ms.reviewer: maghan
ms.date: 07/09/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
ai-usage: ai-assisted
---

# List all backups in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to list all full backups of an Azure Database for PostgreSQL flexible server.

## Steps to list all backups

### [Portal](#tab/portal-list-on-demand-backups)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Backup and restore**.

    :::image type="content" source="./media/how-to-on-demand-backup/backup-restore-with-backups.png" alt-text="Screenshot showing the Backup and restore page with some automatic and on-demand backups available." lightbox="media/how-to-on-demand-backup/backup-restore-with-backups.png":::

1. In **Backup type**, select **On-demand** to see only the on-demand backups that you can restore.

    :::image type="content" source="./media/how-to-on-demand-backup/list-on-demand-backups.png" alt-text="Screenshot showing how to filter the list of backups to only display on-demand backups." lightbox="./media/how-to-on-demand-backup/list-on-demand-backups.png":::

### [CLI](#tab/cli-list-on-demand-backups)

Use the [az postgres flexible-server backup list](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-list) command to list all available backups of a server.

```azurecli-interactive
az postgres flexible-server backup list \
  --resource-group <resource_group> \
  --name <server> \
  --output table
```

Use the [az postgres flexible-server backup list](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-list) command to list currently available on-demand backups of a server.

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
- [Delete on-demand backups](how-to-delete-backups.md)
