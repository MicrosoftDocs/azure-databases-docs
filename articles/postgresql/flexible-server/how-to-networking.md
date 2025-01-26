---
title: Configure networking
description: This article describes how to configure networking related settings of an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/26/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure network related settings of an Azure Database for PostgreSQL flexible server.
---

# Configure networking

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

When you deploy your Azure Database for PostgreSQL flexible server, you can choose between configuring its networking mode as **Public access (allowed IP addresses)** or as **Private access (VNET Integration)**. For more information about these options, see [Networking with public access (allowed IP addresses)](concepts-networking-public.md) and [Networking with private access (VNET integration)](concepts-networking-private.md).

This article provides step-by-step instructions to configure networking related settings of an Azure Database for PostgreSQL flexible server, regardless of the networking mode you selected to deploy it.

## Servers deployed with public access

### Enable public access

If public access is disabled, connectivity to the server is only possible via private endpoints. You must configure those private endpoints so that hosts that can route traffic to the Azure virtual network in which you inject the private endpoints, can access your Azure Database for PostgreSQL flexible server. While public access is disabled, any firewall rules you might have created while public access was enabled aren't enforced, and any modifications made to the firewall rules are discarded.
 
If you enable public access, connectivity to the server is also possible via private endpoints. With public access enabled, you can also configure firewall rules to allow connections originating from specific IP addresses or ranges of addresses, or from any Azure service. When you enable public access, any firewall rules that already existed last time the server was configured with enabled public access, and that weren't explicitly deleted, are enforced again.

#### [Portal](#tab/portal-configure-public-access)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-networking/networking-overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-networking/networking-overview.png":::

3. The status of the server must be **Available**, for the **Networking** menu option to be enabled.

    :::image type="content" source="./media/how-to-networking/networking-server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-networking/networking-server-status.png":::

4. If the status of the server isn't **Available**, the **Networking** option is disabled.

    :::image type="content" source="./media/how-to-networking/networking-disabled.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-networking/networking-disabled.png":::

> [!NOTE]
> Any attempt to configure the networking settings of a server whose status is other than available, would fail with an error.

5. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-networking.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/configure-public-access-networking.png":::

6. Select the **Allow public access to this resource through the internet using a public IP address** checkbox.

    :::image type="content" source="./media/how-to-networking/configure-public-access-networking.png" alt-text="Screenshot showing how to enable public access." lightbox="./media/how-to-networking/configure-public-access-networking.png":::

7. Select **Save**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-save.png":::

8. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-progressing-notification.png":::

9. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-updating.png":::

10. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/restarted-server-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/restarted-server-notification.png":::

11. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-available.png":::

#### [CLI](#tab/cli-configure-public-access)

You can restart a started server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

```azurecli-interactive
az postgres flexible-server restart --resource-group <resource_group> --name <server>
```

If you attempt to restart a server which isn't in `Available` state, you receive an error like this:

```output
Server will be automatically started after 7 days if you do not perform a manual start operation
(ServerIsNotReady) Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
Code: ServerIsNotReady
Message: Restart or Stop Server can only be performed on Started servers. Server Name = <server>, Current Server State = Stopped
```

---

> [!NOTE]
> Once the server is restarted, all management operations are available for the Azure Database for PostgreSQL flexible server.

## Servers deployed with private access

### Configure public access

#### [Portal](#tab/portal-restart-server)

## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Reset administrator password of an Azure Database for PostgreSQL flexible server](how-to-reset-admin-password.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
