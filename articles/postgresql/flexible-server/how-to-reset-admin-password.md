---
title: Reset admin password of PostgreSQL flexible server
description: This article describes how to reset the password of the administrator of an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to reset the administrator password of an Azure Database for PostgreSQL flexible server.
---

# Reset administrator password of an Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to reset the administrator password of an Azure Database for PostgreSQL flexible server.

## Reset server administrator password

### [Portal](#tab/portal-reset-admin-password)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

3. The status of the server must be **Available** for the **Reset password** button to be enabled on the toolbar.

4. Select the **Reset password** button.

    :::image type="content" source="./media/how-to-reset-admin-password/reset-password.png" alt-text="Screenshot showing how to reset password of the server administrator." lightbox="./media/how-to-reset-admin-password/reset-password.png":::

5. In the **Reset admin password** panel, enter the new password in the **Password** and **Confirm password** text boxes, and select **Save**.

    :::image type="content" source="./media/how-to-reset-admin-password/save-password.png" alt-text="Screenshot showing how to enter new password for the server administrator." lightbox="./media/how-to-reset-admin-password/save-password.png":::

6. A notification informs you that the password of the server administrator is being reset.

    :::image type="content" source="./media/how-to-reset-admin-password/notification-resetting-password.png" alt-text="Screenshot showing a server whose administrator's password is being reset." lightbox="./media/how-to-reset-admin-password/notification-resetting-password.png":::

7. When the process completes, a notification informs you that the password was successfully reset.

    :::image type="content" source="./media/how-to-reset-admin-password/notification-reset-password.png" alt-text="Screenshot showing a server whose administrator's password reset completed successfully." lightbox="./media/how-to-reset-admin-password/notification-reset-password.png":::

### [CLI](#tab/cli-reset-admin-password)

You can reset the password of as server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --admin-password <new_password>
```

If you attempt to reset the administrator password of a server which isn't in `Available` state, you receive an error like this:

```output
() Server <server> is busy with other operations. Please try later
Code: 
Message: Server <server> is busy with other operations. Please try later
```

---

> [!NOTE]
> Resetting the password of the server administrator in [read replicas](concepts-read-replicas.md) isn't supported. You can reset the password of the server administrator in the primary server. That password change operation, which is recorded in the Write-Ahead Log of the primary server, is sent asynchronously to all read replicas. When a read replica receives and applies that change locally, any attempt to connect to those replicas with the server administrator user name, must be made using the new password.

## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Restart an Azure Database for PostgreSQL flexible server](how-to-restart-server.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
