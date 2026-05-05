---
title: List all backups in Azure HorizonDB Cluster
description: This article describes how to list all backups of an Azure HorizonDB flexible server instance.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: how-to
# customer intent: As a user, I want to learn how can I list all full backups in Azure HorizonDB.
---

# List all backups in Azure HorizonDB

This article provides step-by-step instructions to list all full backups in Azure HorizonDB.

## Steps to list all backups

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB instance.

1. In the resource menu, under the **Settings** section, select **Backup and restore**.

   :::image type="content" source="media/how-to-on-demand-backup/backup-and-restore-with-backups.png" alt-text="Screenshot showing the Backup and restore page with some automatic and on-demand backups available." lightbox="media/how-to-on-demand-backup/backup-and-restore-with-backups.png":::

1. In **Backup type**, select **On-demand** if you want to only see the backups which are still available to be restored.

   :::image type="content" source="media/how-to-on-demand-backup/list-on-demand-backups.png" alt-text="Screenshot showing how to filter the list of backups to only display backups." lightbox="media/how-to-on-demand-backup/list-on-demand-backups.png":::

### [CLI](#tab/cli-list-on-demand-backups)

You can list currently available backups of a cluster via the [az horizondb cluster-backup list](/cli/azure/postgres/flexible-server/backup#az-postgres-flexible-server-backup-list) command.

```azurecli-interactive
az postgres flexible-server backup list \
  --resource-group <resource_group> \
  --name <server> \
  --output table
```

---

## Related content

- [Restore to custom restore point](how-to-restore-custom-restore-point.md).
- [Restore full backup (fast restore)](how-to-restore-full-backup.md).
