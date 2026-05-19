---
title: Reset Administrator Password in Azure HorizonDB
description: This article describes how to reset the password of the administrator in Azure HorizonDB.
author: avnishrastogimsft
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 05/15/2026
ms.service: azure-horizondb
ms.subservice: security
ms.topic: how-to
ms.custom: horz-security
---

# Reset administrator password in Azure HorizonDB

This article provides step-by-step instructions to reset the administrator password in Azure HorizonDB.

## Steps to reset administrator password

<!-- ### [Portal](#tab/portal-reset-admin-password) -->

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, select **Overview**.

    :::image type="content" source="./media/security-reset-admin-password/overview.png" alt-text="Screenshot showing the Overview page of an Azure HorizonDB cluster." lightbox="./media/security-reset-admin-password/overview.png":::

1. The status of the Azure HorizonDB cluster must be **Ready** for the **Reset password** button to be enabled on the toolbar.


1. **Authentication method** must include PostgreSQL aithentication. In other words **Authentication method** must be set to either **PostgreSQL authentication only** or **PostgreSQL and Microsoft Entra authentication** for the **Reset password** button to be enabled on the toolbar. To check the **Authentication method** go to the resource menu and under the **Security** section select **Authentication**.


1. Select the **Reset password** button and In the **Reset admin password** panel enter the new password in the **Password** text box. Confirm it in the **Confirm password** text box.

    :::image type="content" source="./media/security-reset-admin-password/reset-password.png" alt-text="Screenshot showing how to reset password of the server administrator." lightbox="./media/security-reset-admin-password/reset-password.png":::


1. Select **Save**.


1. A notification informs you that the password of the server administrator is being reset.

    :::image type="content" source="./media/security-reset-admin-password/notification-resetting-password.png" alt-text="Screenshot showing a server whose administrator's password is being reset." lightbox="./media/security-reset-admin-password/notification-resetting-password.png":::

1. When the process completes, a notification informs you that the password was successfully reset.

    :::image type="content" source="./media/security-reset-admin-password/notification-reset-password.png" alt-text="Screenshot showing a server whose administrator's password reset completed successfully." lightbox="./media/security-reset-admin-password/notification-reset-password.png":::

<!-- ### [CLI](#tab/cli-reset-admin-password)

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
-->


## Related content

- [Secure your Azure HorizonDB](security-overview.md)
