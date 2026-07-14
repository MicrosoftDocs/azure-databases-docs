---
title: Reset Administrator Password in Azure HorizonDB
description: This article describes how to reset the password of the administrator in Azure HorizonDB.
#customer intent: As a user, I want to change the administrator password in the Azure portal so that I can maintain secure credentials for my Azure HorizonDB cluster.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
---

# Reset administrator password in Azure HorizonDB (Preview)

This article provides step-by-step instructions to reset the administrator password in Azure HorizonDB.

## Steps to reset administrator password

### [Portal](#tab/portal-reset-admin-password)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, select **Overview**.

   :::image type="content" source="media/security-reset-admin-password/overview.png" alt-text="Screenshot showing the Overview page." lightbox="media/security-reset-admin-password/overview.png":::

1. **Authentication method** must include PostgreSQL authentication. In other words, **Authentication method** must be set to either **PostgreSQL authentication only** or **PostgreSQL and Microsoft Entra authentication** for the **Reset password** button to be enabled on the toolbar. To check the **Authentication method**, go to the resource menu and under the **Security** section select **Authentication**.

   :::image type="content" source="media/security-reset-admin-password/authentication.png" alt-text="Screenshot showing the Authentication page." lightbox="media/security-reset-admin-password/authentication.png":::

1. Select the **Reset password** button to open the **Reset admin password** pane.

   :::image type="content" source="media/security-reset-admin-password/reset-password.png" alt-text="Screenshot showing the Reset admin password pane to enter new password." lightbox="media/security-reset-admin-password/reset-password.png":::

1. Enter the new password in the **Password** text box and confirm it in the **Confirm password** text box. Then, select **Save**.

   :::image type="content" source="media/security-reset-admin-password/reset-password-save.png" alt-text="Screenshot showing how the Reset admin password pane prepared to select Save and persist new password for the administrator." lightbox="media/security-reset-admin-password/reset-password-save.png":::

1. A notification informs you that the password of the server administrator is being reset.

   :::image type="content" source="media/security-reset-admin-password/notification-resetting-password.png" alt-text="Screenshot showing a cluster whose administrator's password is being reset." lightbox="media/security-reset-admin-password/notification-resetting-password.png":::

1. When the process completes, a notification informs you that the password was successfully reset.

   :::image type="content" source="media/security-reset-admin-password/notification-reset-password.png" alt-text="Screenshot showing a cluster whose administrator's password reset completed successfully." lightbox="media/security-reset-admin-password/notification-reset-password.png":::

### [CLI](#tab/cli-reset-admin-password)

Use the [az horizondb cluster update](/cli/azure/horizondb#az-horizondb-update) command.

```azurecli-interactive
az horizondb cluster update \
  --resource-group <resource_group> \
  --name <cluster> \
  --administrator-login-password <new_password>
```

---

## Related content

- [Secure your Azure HorizonDB (Preview)](security-overview.md)
