---
title: Reset administrator password
description: This article describes how to reset the password of the administrator of an Azure Database for PostgreSQL flexible server.
author: Tameika-MSFT
ms.author: talawren
ms.reviewer: maghan
ms.date: 06/09/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom: horz-security
---

# Reset administrator password

This article provides step-by-step instructions to reset the administrator password for an Azure Database for PostgreSQL flexible server.

## Steps to reset administrator password

### [Portal](#tab/portal-reset-admin-password)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Overview**.

    :::image type="content" source="./media/security-reset-admin-password/overview.png" alt-text="Screenshot showing the Overview page of an Azure Database for PostgreSQL flexible server." lightbox="./media/security-reset-admin-password/overview.png":::

1. The server status must be **Ready** for the **Reset password** button to be enabled on the toolbar.

    :::image type="content" source="./media/security-reset-admin-password/server-status.png" alt-text="Screenshot showing the status of the server set to Ready." lightbox="./media/security-reset-admin-password/server-status.png":::

1. In the resource menu, under the **Security** section, select **Authentication**.

    :::image type="content" source="./media/security-reset-admin-password/authentication.png" alt-text="Screenshot showing the Authentication page of an Azure Database for PostgreSQL flexible server." lightbox="./media/security-reset-admin-password/authentication.png":::

1. The **Authentication method** must be either **PostgreSQL authentication only** or **PostgreSQL and Microsoft Entra authentication** for the **Reset password** button to be enabled on the toolbar. When set to **Microsoft Entra authentication only**, the **Reset password** button is disabled.

    :::image type="content" source="./media/security-reset-admin-password/microsoft-entra-authentication-only.png" alt-text="Screenshot showing that server's authentication is configured with Microsoft Entra authentication only." lightbox="./media/security-reset-admin-password/microsoft-entra-authentication-only.png":::

1. If the **Reset password** button is disabled, hover over it to see a tooltip that describes the reason why the button is disabled.

    :::image type="content" source="./media/security-reset-admin-password/reset-password-disabled.png" alt-text="Screenshot showing Reset password button disabled." lightbox="./media/security-reset-admin-password/reset-password-disabled.png":::

1. Select the **Reset password** button.

    :::image type="content" source="./media/security-reset-admin-password/reset-password.png" alt-text="Screenshot showing how to reset password of the server administrator." lightbox="./media/security-reset-admin-password/reset-password.png":::

1. In the **Reset admin password** panel, enter the new password in the **Password** text box.

    :::image type="content" source="./media/security-reset-admin-password/enter-password.png" alt-text="Screenshot showing how to enter new password for the server administrator." lightbox="./media/security-reset-admin-password/enter-password.png":::

1. In the **Reset admin password** panel, enter the new password in the **Confirm password** text box.

    :::image type="content" source="./media/security-reset-admin-password/confirm-password.png" alt-text="Screenshot showing how to confirm new password for the server administrator." lightbox="./media/security-reset-admin-password/confirm-password.png":::

1. Select **Save**.

    :::image type="content" source="./media/security-reset-admin-password/save-password.png" alt-text="Screenshot showing how to save the new password provided for the server administrator." lightbox="./media/security-reset-admin-password/save-password.png":::

1. A notification informs you that the password of the server administrator is being reset.

    :::image type="content" source="./media/security-reset-admin-password/notification-resetting-password.png" alt-text="Screenshot showing a server whose administrator password is being reset." lightbox="./media/security-reset-admin-password/notification-resetting-password.png":::

1. When the process completes, a notification informs you that the password was successfully reset.

    :::image type="content" source="./media/security-reset-admin-password/notification-reset-password.png" alt-text="Screenshot showing a server whose administrator password reset completed successfully." lightbox="./media/security-reset-admin-password/notification-reset-password.png":::

### [CLI](#tab/cli-reset-admin-password)

Use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command to reset the administrator password for a server.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --admin-password <new_password>
```

If you try to reset the administrator password for a server that isn't configured with password-based authentication enabled, the command doesn't report any error. However, it doesn't change the password for the server administrator, if one exists.

To determine if a server is configured to support password-based authentication, run the following command:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query authConfig.passwordAuth \
  --output tsv
```

If you try to reset the administrator password for a server that isn't in the `Ready` state, you receive an error like this:

```output
() Server <server> is busy with other operations. Please try later
Code: 
Message: Server <server> is busy with other operations. Please try later
```

---

> [!NOTE]
> Resetting the password for the server administrator in [read replicas](../read-replica/concepts-read-replicas.md) isn't supported. You can reset the password for the server administrator in the primary server. That password change operation, which is recorded in the Write-Ahead Log of the primary server, is sent asynchronously to all read replicas. When a read replica receives and applies that change locally, any attempt to connect to those replicas by using the server administrator user name, must use the new password.

## Related content

- [Security](../security/security-overview.md).
