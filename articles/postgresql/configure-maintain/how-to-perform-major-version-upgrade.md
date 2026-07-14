---
title: Major version upgrade in Azure Database for PostgreSQL Flexible Server
description: This article describes how to perform an in-place major version upgrade of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to learn how to perform an in-place major version upgrade of an Azure Database for PostgreSQL.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ai-usage: ai-assisted
ms.custom: sfi-image-nochange
---

# Major version upgrade in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to perform a major version upgrade of an Azure Database for PostgreSQL flexible server.

> [!NOTE]  
> The major version upgrade action is irreversible. Make sure that you perform a point in time restore (PITR) of the production server that you want to upgrade. Test the upgrade in that restored, nonproduction instance before you upgrade the production environment.

## Steps to upgrade to a higher major version

### [Portal](#tab/portal-major-version-upgrade)

Use the [Azure portal](https://portal.azure.com/):

1. Select the Azure Database for PostgreSQL flexible server that you want to upgrade.

1. From the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/overview.png" alt-text="Screenshot showing the Overview page, to demonstrate how to initiate major version upgrade of an Azure Database for PostgreSQL flexible server." lightbox="media/how-to-perform-major-version-upgrade/overview.png":::

1. The server status must be **Ready** for the **Upgrade** button to be enabled.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="media/how-to-perform-major-version-upgrade/server-status.png":::

1. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-button.png" alt-text="Screenshot showing the Upgrade button through which you can initiate the major version upgrade of an Azure Database for PostgreSQL flexible server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-button.png":::

1. The **Upgrade** pane provides some recommendations.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-pane.png" alt-text="Screenshot showing the Upgrade pane." lightbox="media/how-to-perform-major-version-upgrade/upgrade-pane.png":::

1. Expand **PostgreSQL version to upgrade**, and select the major version to which you want to upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/set-postgresql-version.png" alt-text="Screenshot showing the Upgrade pane, from where you can select the major version to which you want to upgrade." lightbox="media/how-to-perform-major-version-upgrade/set-postgresql-version.png"::: 

1. For **Action**, select **Validate and upgrade** to run the validation rules and, if they all pass, it immediately upgrades the server to the selected target version. It warns you about the consequences of initiating the upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/action.png" alt-text="Screenshot showing the Action option configured as Validate and upgrade." lightbox="media/how-to-perform-major-version-upgrade/action.png"::: 

1. Select **Start**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/start.png" alt-text="Screenshot showing the Start button, to initiate the upgrade." lightbox="media/how-to-perform-major-version-upgrade/start.png"::: 

1. During upgrade, wait for the process to complete. You can resume accessing the server when the server is back online.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-progressing.png" alt-text="Screenshot showing the progress of the deployment initiated to perform the major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-progressing.png":::

1. When the upgrade finishes, you select the **Go to resource** button to validate your upgrade.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-completed.png" alt-text="Screenshot showing the Go to resource button, through which you can access the Overview page of the upgraded Azure Database for PostgreSQL flexible server." lightbox="media/how-to-perform-major-version-upgrade/deployment-completed.png":::

1. The name of the server remains unchanged.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification-server-name.png" alt-text="Screenshot showing the Overview page of the upgraded Azure Database for PostgreSQL flexible server, after major version upgrade, highlighting the name of the server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification-server-name.png":::

1. The version of PostgreSQL is upgraded to the major version you selected as target. The minor version corresponds to the most recent minor version supported by Azure Database for PostgreSQL flexible server at the time of the upgrade.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification-server-version.png" alt-text="Screenshot showing the Overview page of the upgraded Azure Database for PostgreSQL flexible server, after major version upgrade, highlighting the version of the server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification-server-version.png":::

### [CLI](#tab/cli-major-version-upgrade)

Use the [az postgres flexible-server upgrade](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-upgrade) command to upgrade the major version of a server.

```azurecli-interactive
az postgres flexible-server upgrade \
  --resource-group <resource_group> \
  --name <server> \
  --version <target_version>
```

---

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL flexible server](../backup-restore/concepts-business-continuity.md).
- [Major version upgrades in Azure Database for PostgreSQL flexible server](concepts-major-version-upgrade.md).
- [High availability in Azure Database for PostgreSQL flexible server](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL flexible server](../backup-restore/concepts-backup-restore.md).
