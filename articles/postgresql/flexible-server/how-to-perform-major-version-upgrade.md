---
title: Major version upgrade
description: This article describes how to perform an in-place major version upgrade of an Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to perform an in-place major version upgrade of an Azure Database for PostgreSQL flexible server.
---

# Major version upgrade

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to perform a major version upgrade of an Azure Database for PostgreSQL flexible server instance.

> [!NOTE]  
> The major version upgrade action is irreversible. Make sure that you perform a point in time restore (PITR) of the production server that you want to upgrade. Test the upgrade in that restored, nonproduction instance before you upgrade the production environment.

## Steps to upgrade to a higher major version

### [Portal](#tab/portal-major-version-upgrade)

Using the [Azure portal](https://portal.azure.com/):

1. Select the instance of Azure Database for PostgreSQL flexible server which you want to upgrade.

2. From the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-tab.png" alt-text="Screenshot of Overview page to demonstrate how to initiate major version upgrade of an instance of Azure Database for PostgreSQL Flexible Server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-tab.png":::

3. The status of the server must be **Available**, for the **Upgrade** button to be enabled.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="media/how-to-perform-major-version-upgrade/server-status.png":::

4. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-tab.png" alt-text="Screenshot of Overview page to demonstrate how to initiate major version upgrade of an instance of Azure Database for PostgreSQL Flexible Server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-tab.png":::

5. Expand **PostgreSQL version to upgrade** and select the major version to which you want to upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/set-postgresql-version.png" alt-text="Screenshot of the Upgrade pane, from where you can select the target major version to which you want to upgrade." lightbox="media/how-to-perform-major-version-upgrade/set-postgresql-version.png"::: 

6. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade.png" alt-text="Screenshot showing the Upgrade button in the Upgrade pane, to initiate the upgrade." lightbox="media/how-to-perform-major-version-upgrade/upgrade.png"::: 

7. During upgrade, users have to wait for the process to complete. You can resume accessing the server when the server is back online.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-progress.png" alt-text="Diagram of deployment progress for major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-progress.png":::

8. Once the upgrade completes successfully, you can expand **Deployment details**, and select **Operation details** to see more information about the upgrade process. You can see details like duration, provisioning state, etc. Then, you can select the **Go to resource** button to validate your upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-success.png" alt-text="Diagram of successful deployment of for Major Version Upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-success.png":::
 
9. Observe that the name of the server remains unchanged, and PostgreSQL version is upgraded to the desired target major version. The minor version corresponds to the most recent minor version supported by Azure Database for PostgreSQL - Flexible Server at the time of the upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification.png" alt-text="Diagram of upgraded version to Azure Database for PostgreSQL flexible server, after major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification.png":::

### [CLI](#tab/cli-major-version-upgrade)

You can upgrade the major version via the [az postgres flexible-server upgrade](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-upgrade).

```azurecli
az postgres flexible-server upgrade --resource-group <resource_group> --name <server> --version <target_version>
```

---

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [Major version upgrades in Azure Database for PostgreSQL - Flexible Server](concepts-major-version-upgrade.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL - Flexible Server](concepts-backup-restore.md).
