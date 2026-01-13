---
title: Disable public access
description: This article describes how to disable public access in an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 03/30/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to disable public network access in an Azure Database for PostgreSQL.
---

# Disable public access

If you disable public access, connectivity to the server is only possible via private endpoints.

You must configure those private endpoints so that hosts that can route traffic to the Azure virtual network in which you inject the private endpoints, can access your Azure Database for PostgreSQL flexible server.

When public access is disabled, any firewall rules you created while public access was enabled, aren't enforced.

Also, any modifications made to the firewall rules are discarded.

## [Portal](#tab/portal-disable-public-access)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-enabled.png":::

3. Clear the **Allow public access to this resource through the internet using a public IP address** checkbox.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access.png" alt-text="Screenshot showing how to disable public access." lightbox="./media/how-to-networking/public-access-disable-public-access.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/public-access-disable-public-access-save.png":::

5. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/public-access-disable-public-access-progressing-notification.png":::

6. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/public-access-updating.png":::

7. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/public-access-disable-public-access-succeeded-notification.png":::

8. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-networking/public-access-available.png" alt-text="Screenshot showing that server status is Ready." lightbox="./media/how-to-networking/public-access-available.png":::

## [CLI](#tab/cli-disable-public-access)

You can disable public access on a server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --public-access disabled
```

If you attempt to disable public access on a server which isn't in `Ready` state, you receive an error like this:

```output
Code: 
Message: Server <server> is busy with other operations. Please try later
```

If you attempt to disable public access on a server which wasn't deployed with networking mode public access (allowed IP addresses), you don't receive an error. The request to change that configuration is ignored.

To determine if a server has public access disabled or enabled, run the following command:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{"publicAccess":network.publicNetworkAccess}'
```

---

## Related content

- [Networking](how-to-networking.md).
- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
