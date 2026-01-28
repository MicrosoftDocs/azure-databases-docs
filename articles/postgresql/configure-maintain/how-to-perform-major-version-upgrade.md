---
title: Major version upgrade
description: This article describes how to perform an in-place major version upgrade of an Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/04/2025
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ms.custom: sfi-image-nochange
#customer intent: As a user, I want to learn how to perform an in-place major version upgrade of an Azure Database for PostgreSQL.
---

# Major version upgrade

This article provides step-by-step instructions to perform a major version upgrade of an Azure Database for PostgreSQL flexible server instance.

> [!NOTE]  
> The major version upgrade action is irreversible. Make sure that you perform a point in time restore (PITR) of the production server that you want to upgrade. Test the upgrade in that restored, nonproduction instance before you upgrade the production environment.

## Steps to upgrade to a higher major version

### [Portal](#tab/portal-major-version-upgrade)

Using the [Azure portal](https://portal.azure.com/):

1. Select the instance of Azure Database for PostgreSQL flexible server which you want to upgrade.

2. From the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/overview.png" alt-text="Screenshot showing the Overview page, to demonstrate how to initiate major version upgrade of an Azure Database for PostgreSQL flexible server." lightbox="media/how-to-perform-major-version-upgrade/overview.png":::

3. The status of the server must be **Ready**, for the **Upgrade** button to be enabled.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="media/how-to-perform-major-version-upgrade/server-status.png":::

4. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-button.png" alt-text="Screenshot showing the Upgrade button through which you can initiate the major version upgrade of an Azure Database for PostgreSQL flexible server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-button.png":::

5. The **Upgrade** pane provides some recommendations, and warns you about the consequences of initiating the upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-pane.png" alt-text="Screenshot showing the Upgrade pane." lightbox="media/how-to-perform-major-version-upgrade/upgrade-pane.png":::

6. Expand **PostgreSQL version to upgrade**, and select the major version to which you want to upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/set-postgresql-version.png" alt-text="Screenshot showing the Upgrade pane, from where you can select the major version to which you want to upgrade." lightbox="media/how-to-perform-major-version-upgrade/set-postgresql-version.png"::: 

7. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade.png" alt-text="Screenshot showing the Upgrade button, to initiate the upgrade." lightbox="media/how-to-perform-major-version-upgrade/upgrade.png"::: 

8. During upgrade, users have to wait for the process to complete. You can resume accessing the server when the server is back online.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-progress.png" alt-text="Screenshot showing of progress of the deployment initiated to perform the major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-progress.png":::

9. Once the upgrade completes successfully, you can expand **Deployment details**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-details.png" alt-text="Screenshot showing how to expand the deployment details after a successful deployment of a major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-details.png":::

10. Select **Operation details** if you want to see more information about the upgrade process.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/operation-details.png" alt-text="Screenshot showing how access the operation details of a successful deployment of a major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/operation-details.png":::

11. Then, you can select the **Go to resource** button to validate your upgrade.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/go-to-resource.png" alt-text="Screenshot showing the Go to resource button, through which you can access the Overview page of the upgraded Azure Database for PostgreSQL flexible server." lightbox="media/how-to-perform-major-version-upgrade/go-to-resource.png":::

12. Observe that the name of the server remains unchanged.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification-server-name.png" alt-text="Screenshot showing the Overview page of the upgraded Azure Database for PostgreSQL flexible server, after major version upgrade, highlighting the name of the server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification-server-name.png":::

13. Notice that the version of PostgreSQL is upgraded to the major version you selected as target. The minor version corresponds to the most recent minor version supported by Azure Database for PostgreSQL flexible server at the time of the upgrade.

    :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification-server-version.png" alt-text="Screenshot showing the Overview page of the upgraded Azure Database for PostgreSQL flexible server, after major version upgrade, highlighting the version of the server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification-server-version.png":::

### [CLI](#tab/cli-major-version-upgrade)

You can upgrade the major version via the [az postgres flexible-server upgrade](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-upgrade).

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
