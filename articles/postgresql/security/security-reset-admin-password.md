---
title: Reset administrator password
description: This article describes how to reset the password of the administrator of an Azure Database for PostgreSQL flexible server instance.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom: horz-security
---

# Reset administrator password

This article provides step-by-step instructions to reset the administrator password of an Azure Database for PostgreSQL flexible server instance.

## Steps to reset administrator password

### [Portal](#tab/portal-reset-admin-password)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/security-reset-admin-password/overview.png" alt-text="Screenshot showing the Overview page of an Azure Database for PostgreSQL flexible server instance." lightbox="./media/security-reset-admin-password/overview.png":::

3. The status of the server must be **Ready** for the **Reset password** button to be enabled on the toolbar.

    :::image type="content" source="./media/security-reset-admin-password/server-status.png" alt-text="Screenshot showing the status of the server set to Ready." lightbox="./media/security-reset-admin-password/server-status.png":::

4. In the resource menu, under the **Security** section, select **Authentication**.

    :::image type="content" source="./media/security-reset-admin-password/authentication.png" alt-text="Screenshot showing the Authentication page of an Azure Database for PostgreSQL flexible server instance." lightbox="./media/security-reset-admin-password/authentication.png":::

5. **Authentication method** must be either **PostgreSQL authentication only** or **PostgreSQL and Microsoft Entra authentication** for the **Reset password** button to be enabled on the toolbar. When set to **Microsoft Entra authentication only**, the **Reset password** button is disabled.

    :::image type="content" source="./media/security-reset-admin-password/microsoft-entra-authentication-only.png" alt-text="Screenshot showing that server's authentication is configured with Microsoft Entra authentication only." lightbox="./media/security-reset-admin-password/microsoft-entra-authentication-only.png":::

6. If **Reset password** button is disabled, you can hover the mouse over it, and a tooltip describes the reason why the button is disabled.

    :::image type="content" source="./media/security-reset-admin-password/reset-password-disabled.png" alt-text="Screenshot showing Reset password button disabled." lightbox="./media/security-reset-admin-password/reset-password-disabled.png":::

7. Select the **Reset password** button.

    :::image type="content" source="./media/security-reset-admin-password/reset-password.png" alt-text="Screenshot showing how to reset password of the server administrator." lightbox="./media/security-reset-admin-password/reset-password.png":::

8. In the **Reset admin password** panel, enter the new password in the **Password** text box.

    :::image type="content" source="./media/security-reset-admin-password/enter-password.png" alt-text="Screenshot showing how to enter new password for the server administrator." lightbox="./media/security-reset-admin-password/enter-password.png":::

9. In the **Reset admin password** panel, enter the new password in the **Confirm password** text box.

    :::image type="content" source="./media/security-reset-admin-password/confirm-password.png" alt-text="Screenshot showing how to confirm new password for the server administrator." lightbox="./media/security-reset-admin-password/confirm-password.png":::

10. Select **Save**.

    :::image type="content" source="./media/security-reset-admin-password/save-password.png" alt-text="Screenshot showing how to save the new password provided for the server administrator." lightbox="./media/security-reset-admin-password/save-password.png":::

11. A notification informs you that the password of the server administrator is being reset.

    :::image type="content" source="./media/security-reset-admin-password/notification-resetting-password.png" alt-text="Screenshot showing a server whose administrator's password is being reset." lightbox="./media/security-reset-admin-password/notification-resetting-password.png":::

12. When the process completes, a notification informs you that the password was successfully reset.

    :::image type="content" source="./media/security-reset-admin-password/notification-reset-password.png" alt-text="Screenshot showing a server whose administrator's password reset completed successfully." lightbox="./media/security-reset-admin-password/notification-reset-password.png":::

### [CLI](#tab/cli-reset-admin-password)

You can reset the password of as server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --admin-password <new_password>
```

If you attempt to reset the administrator password of a server which isn't configured with password-based authentication enabled, the command doesn't report any error. However, it doesn't change the password of the server administrator, provided one exists.

To determine if a server is configured to support password-based authentication, run the following command:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query authConfig.passwordAuth \
  --output tsv
```

If you attempt to reset the administrator password of a server which isn't in `Ready` state, you receive an error like this:

```output
() Server <server> is busy with other operations. Please try later
Code: 
Message: Server <server> is busy with other operations. Please try later
```

---

> [!NOTE]
> Resetting the password of the server administrator in [read replicas](../read-replica/concepts-read-replicas.md) isn't supported. You can reset the password of the server administrator in the primary server. That password change operation, which is recorded in the Write-Ahead Log of the primary server, is sent asynchronously to all read replicas. When a read replica receives and applies that change locally, any attempt to connect to those replicas with the server administrator user name, must be made using the new password.

## Related content

- [Security](../security/security-overview.md).
