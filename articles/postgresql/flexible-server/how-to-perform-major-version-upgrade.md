---
title: Major version upgrade - Azure portal
description: This article describes how to perform a major version upgrade in Azure Database for PostgreSQL - Flexible Server through the Azure portal.
author: rajsell
ms.author: kabharati
ms.reviewer: maghan
ms.date: 12/08/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Major version upgrade of Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides a step-by-step procedure to perform a major version upgrade of an Azure Database for PostgreSQL flexible server instance.

> [!NOTE]  
> The major version upgrade action is irreversible. Please perform a Point-In-Time Recovery (PITR) of your production server and test the upgrade in the non-production environment.

## Upgrade to the major version of your choice

### [Portal](#tab/portal)

Using the [Azure portal](https://portal.azure.com/):

1. Select the instance of Azure Database for PostgreSQL flexible server which you want to upgrade.

2. From the resource menu, select **Overview**, and then select **Upgrade**.
   
   :::image type="content" source="media/how-to-perform-major-version-upgrade-portal/upgrade-tab.png" alt-text="Screenshot of Overview page to demonstrate how to initiate major version upgrade of an instance of Azure Database for PostgreSQL Flexible Server." lightbox="media/how-to-perform-major-version-upgrade-portal/upgrade-tab.png":::


3. Choose the major version to which you want to upgrade your instance, and click **Upgrade**.

   :::image type="content" source="media/how-to-perform-major-version-upgrade-portal/set-postgresql-version.png" alt-text="Screenshot of the Upgrade pane from where you can select target major version to which you want to upgrade." lightbox="media/how-to-perform-major-version-upgrade-portal/set-postgresql-version.png"::: 


4. During upgrade, users have to wait for the process to complete. You can resume accessing the server once the server is back online.

   :::image type="content" source="media/how-to-perform-major-version-upgrade-portal/deployment-progress.png" alt-text="Diagram of deployment progress for Major Version Upgrade." lightbox="media/how-to-perform-major-version-upgrade-portal/deployment-progress.png":::


5. Once the upgrade completes successfully, you can expand **Deployment details**, and select **Operation details** to see more information about the upgrade process, like duration, provisioning state, etc. Then you can select the **Go to resource** button to validate your upgrade.


   :::image type="content" source="media/how-to-perform-major-version-upgrade-portal/deployment-success.png" alt-text="Diagram of successful deployment of for Major Version Upgrade." lightbox="media/how-to-perform-major-version-upgrade-portal/deployment-success.png":::
 

6. Notice that the name of the server remains unchanged and PostgreSQL version upgraded to desired target version, with the latest minor version.


   :::image type="content" source="media/how-to-perform-major-version-upgrade-portal/upgrade-verification.png" alt-text="Diagram of Upgraded version to Azure Database for PostgreSQL flexible server after Major Version Upgrade." lightbox="media/how-to-perform-major-version-upgrade-portal/upgrade-verification.png":::

### [CLI](#tab/cli)

You can upgrade the major version via the CLI upgrade [command](/cli/azure/postgres/flexible-server?view=azure-cli-latest#az-postgres-flexible-server-upgrade).

```azurecli
az postgres flexible-server upgrade --resource-group <resource_group> --name <server> --version <target_version>
```

---

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [business continuity](./concepts-business-continuity.md).
- [major version upgrade](./concepts-major-version-upgrade.md).
- [zone-redundant high availability](./concepts-high-availability.md).
- [backup and recovery](./concepts-backup-restore.md).
