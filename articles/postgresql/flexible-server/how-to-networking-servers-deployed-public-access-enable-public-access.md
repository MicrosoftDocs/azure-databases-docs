---
title: Enable public access
description: This article describes how to enable public access in an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to enable public network access in an Azure Database for PostgreSQL flexible server.
---

# Enable public access
 
If you enable public access, connectivity to the server is also possible via private endpoints.

With public access enabled, you can also configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service.

When you enable public access, any firewall rules that already existed last time the server was configured with enabled public access are enforced again.

## [Portal](#tab/portal-enable-public-access)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-networking/networking-overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-networking/networking-overview.png":::

3. The status of the server must be **Available**, for the **Networking** menu option to be enabled.

    :::image type="content" source="./media/how-to-networking/networking-server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-networking/networking-server-status.png":::

4. If the status of the server isn't **Available**, the **Networking** option is disabled.

    :::image type="content" source="./media/how-to-networking/networking-disabled.png" alt-text="Screenshot showing that Networking menu is disabled when status of server isn't Available." lightbox="./media/how-to-networking/networking-disabled.png":::

> [!NOTE]
> Any attempt to configure the networking settings of a server whose status is other than available, would fail with an error.

5. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-disabled.png":::

6. Select the **Allow public access to this resource through the internet using a public IP address** checkbox.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access.png" alt-text="Screenshot showing how to enable public access." lightbox="./media/how-to-networking/public-access-enable-public-access.png":::

7. Select **Save**.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/public-access-enable-public-access-save.png":::

8. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/public-access-enable-public-access-progressing-notification.png":::

9. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/public-access-updating.png":::

10. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/public-access-enable-public-access-succeeded-notification.png":::

11. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/public-access-available.png":::

## [CLI](#tab/cli-enable-public-access)

You can enable public access on a server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --public-access enabled
```

If you attempt to enable public access on a server which isn't in `Available` state, you receive an error like this:

```output
Code: 
Message: Server <server> is busy with other operations. Please try later
```

If you attempt to enable public access on a server which wasn't deployed with networking mode public access (allowed IP addresses), you don't receive an error. The request to change that configuration is ignored.

To determine if a server has public access enabled or disabled, run the following command:

```azurecli-interactive
az postgres flexible-server show --resource-group <resource_group> --name <server> --query '{"publicAccess":network.publicNetworkAccess}'
```

---

## Related content

- [Networking](how-to-networking.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
