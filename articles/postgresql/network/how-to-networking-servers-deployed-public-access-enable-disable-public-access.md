---
title: Enable or Disable Public Access in Azure Database for PostgreSQL Flexible Server
description: This article describes how to disable public access in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to disable public access to my Azure Database for PostgreSQL flexible server, so that I can restrict connectivity to private endpoints only.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/09/2025
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
---

# Enable or disable public access in Azure Database for PostgreSQL flexible server

If you disable public access, you can connect to the server only through private endpoints.

You must configure those private endpoints so that hosts that can route traffic to the Azure virtual network in which you inject the private endpoints, can access your Azure Database for PostgreSQL flexible server.

When you disable public access, the firewall rules you created while public access was enabled aren't enforced.

Also, any modifications you made to the firewall rules are discarded.

## [Portal](#tab/portal-enable-disable-public-access)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-enabled.png":::

1. To disable public access, clear the **Allow public access to this resource through the internet using a public IP address** checkbox. To enable it, select the checkbox.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access.png" alt-text="Screenshot showing how to disable public access." lightbox="./media/how-to-networking/public-access-disable-public-access.png":::

1. Select **Save**.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/public-access-disable-public-access-save.png":::

1. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/public-access-disable-public-access-progressing-notification.png":::

1. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/public-access-disable-public-access-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/public-access-disable-public-access-succeeded-notification.png":::

## [CLI](#tab/cli-enable-disable-public-access)

To enable public access on a server, use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --public-access enabled
```

To disable public access on a server, use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --public-access disabled
```

If you try to enable or disable public access on a server that's not in the `Ready` state, you get an error like this:

```output
Code: 
Message: Server <server> is busy with other operations. Please try later
```

If you try to enable or disable public access on a server that wasn't deployed with networking mode public access (allowed IP addresses), you don't get an error. The request to change that configuration is ignored.

To check if a server has public access disabled or enabled, run the following command:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{"publicAccess":network.publicNetworkAccess}'
```

---

## Related content

- [Networking](how-to-networking.md).
- [Enable or disable public access](how-to-networking-servers-deployed-public-access-enable-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
