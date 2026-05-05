---
title: Major Version Upgrade in Azure HorizonDB
description: This article describes how to perform an in-place major version upgrade of an Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
ms.custom:
  - sfi-image-nochange
# customer intent: As a user, I want to learn how to perform an in-place major version upgrade of an Azure HorizonDB.
---

# Major version upgrade in Azure HorizonDB

This article provides step-by-step instructions to perform a major version upgrade of an Azure HorizonDB instance.

> [!NOTE]  
> The major version upgrade action is irreversible. Make sure that you perform a point in time restore (PITR) of the production server that you want to upgrade. Test the upgrade in that restored, nonproduction instance before you upgrade the production environment.

## Steps to upgrade to a higher major version

### [Portal](#tab/portal-major-version-upgrade)

Using the [Azure portal](https://portal.azure.com/):

1. Select the instance of Azure HorizonDB which you want to upgrade.

1. From the resource menu, select **Overview**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/overview.png" alt-text="Screenshot showing the Overview page, to demonstrate how to initiate major version upgrade of an Azure HorizonDB." lightbox="media/how-to-perform-major-version-upgrade/overview.png":::

1. The status of the server must be **Ready**, for the **Upgrade** button to be enabled.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="media/how-to-perform-major-version-upgrade/server-status.png":::

1. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-button.png" alt-text="Screenshot showing the Upgrade button through which you can initiate the major version upgrade of an Azure HorizonDB." lightbox="media/how-to-perform-major-version-upgrade/upgrade-button.png":::

1. The **Upgrade** pane provides some recommendations, and warns you about the consequences of initiating the upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-pane.png" alt-text="Screenshot showing the Upgrade pane." lightbox="media/how-to-perform-major-version-upgrade/upgrade-pane.png":::

1. Expand **PostgreSQL version to upgrade**, and select the major version to which you want to upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/set-postgresql-version.png" alt-text="Screenshot showing the Upgrade pane, from where you can select the major version to which you want to upgrade." lightbox="media/how-to-perform-major-version-upgrade/set-postgresql-version.png":::

1. Select **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade.png" alt-text="Screenshot showing the Upgrade button, to initiate the upgrade." lightbox="media/how-to-perform-major-version-upgrade/upgrade.png":::

1. During upgrade, users have to wait for the process to complete. You can resume accessing the server when the server is back online.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-progress.png" alt-text="Screenshot showing of progress of the deployment initiated to perform the major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-progress.png":::

1. Once the upgrade completes successfully, you can expand **Deployment details**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/deployment-details.png" alt-text="Screenshot showing how to expand the deployment details after a successful deployment of a major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/deployment-details.png":::

1. Select **Operation details** if you want to see more information about the upgrade process.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/operation-details.png" alt-text="Screenshot showing how access the operation details of a successful deployment of a major version upgrade." lightbox="media/how-to-perform-major-version-upgrade/operation-details.png":::

1. Then, you can select the **Go to resource** button to validate your upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/go-to-resource.png" alt-text="Screenshot showing the Go to resource button, through which you can access the Overview page of the upgraded Azure HorizonDB." lightbox="media/how-to-perform-major-version-upgrade/go-to-resource.png":::

1. Observe that the name of the server remains unchanged.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification-server-name.png" alt-text="Screenshot showing the Overview page of the upgraded Azure HorizonDB, after major version upgrade, highlighting the name of the server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification-server-name.png":::

1. The version of PostgreSQL is upgraded to the major version you selected as target. The minor version corresponds to the most recent minor version supported by Azure HorizonDB at the time of the upgrade.

   :::image type="content" source="media/how-to-perform-major-version-upgrade/upgrade-verification-server-version.png" alt-text="Screenshot showing the Overview page of the upgraded Azure HorizonDB, after major version upgrade, highlighting the version of the server." lightbox="media/how-to-perform-major-version-upgrade/upgrade-verification-server-version.png":::

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

- [Overview of business continuity in Azure HorizonDB](../backup-restore/concepts-business-continuity.md)
- [Major version upgrades in Azure HorizonDB](concepts-major-version-upgrade.md)
- [High availability in Azure HorizonDB](/azure/reliability/reliability-postgresql-flexible-server)
- [Backup and restore in Azure HorizonDB](../backup-restore/concepts-backup-restore.md)
