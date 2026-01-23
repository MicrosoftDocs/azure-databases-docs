---
title: Enable public access
description: This article describes how to enable public access in an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 03/30/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to enable public network access in an Azure Database for PostgreSQL.
---

# Enable public access

This article explains how to enable public network access on an Azure Database for PostgreSQL flexible server that was originally deployed with public access networking mode. Public access allows connections from the internet using a public IP address, which you can secure using firewall rules and private endpoints.

## Prerequisites 

This article applies only to servers that were originally deployed with public access networking mode. If your server is currently configured with Private Access (VNet Integration), you cannot directly enable public access. To switch from private to public access, you would need to restore the server to a new instance with public access enabled, or create a new server. See [Networking overview](concepts-networking.md) for more information about networking modes.

## How to enable public access

If you enable public access, connectivity to the server is also possible via private endpoints.

With public access enabled, you can also configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service.

When you enable public access, any firewall rules that already existed last time the server was configured with enabled public access are enforced again.

## [Portal](#tab/portal-enable-public-access)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-disabled.png":::

3. Select the **Allow public access to this resource through the internet using a public IP address** checkbox.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access.png" alt-text="Screenshot showing how to enable public access." lightbox="./media/how-to-networking/public-access-enable-public-access.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/public-access-enable-public-access-save.png":::

5. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/public-access-enable-public-access-progressing-notification.png":::

6. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/public-access-updating.png":::

7. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/public-access-enable-public-access-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/public-access-enable-public-access-succeeded-notification.png":::

8. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-networking/public-access-available.png" alt-text="Screenshot showing that server status is Ready." lightbox="./media/how-to-networking/public-access-available.png":::

## [CLI](#tab/cli-enable-public-access)

You can enable public access on a server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --public-access enabled
```

If you attempt to enable public access on a server which isn't in `Ready` state, you receive an error like this:

```output
Code: 
Message: Server <server> is busy with other operations. Please try later
```

If you attempt to enable public access on a server which wasn't deployed with networking mode public access (allowed IP addresses), you don't receive an error. The request to change that configuration is ignored.

To determine if a server has public access enabled or disabled, run the following command:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{"publicAccess":network.publicNetworkAccess}'
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
