---
title: Delete Private Endpoint Connections in Azure Database for PostgreSQL Flexible Server
description: This article describes how to delete private endpoint connections to an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to delete a private endpoint connection to my Azure Database for PostgreSQL flexible server, so that I can remove access that's no longer needed.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
---

# Delete private endpoint connections in Azure Database for PostgreSQL flexible server

Azure Database for PostgreSQL flexible server is an Azure Private Link service. This feature enables you to create private endpoints so your client applications can connect privately and securely to your Azure Database for PostgreSQL flexible server.

A private endpoint for your Azure Database for PostgreSQL flexible server is a network interface that you add to a subnet of an Azure virtual network. Any host or service that can route network traffic to that subnet can communicate with your flexible server. The network traffic doesn't have to traverse the internet. All traffic is sent privately over the Microsoft backbone.

For more information about Azure Private Link and Azure Private Endpoint, see [Azure Private Link frequently asked questions](/azure/private-link/private-link-faq).

## [Portal](#tab/portal-delete-private-endpoint-connections)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint.png":::

1. Select the private endpoint connection that you want to delete, and select **Delete** to start the deletion process.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-delete.png" alt-text="Screenshot showing the Delete button to trigger the deletion of an existing private endpoint connection." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-delete.png":::

1. A notification informs you that the private endpoint connection is being deleted.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleting-notification.png" alt-text="Screenshot showing the notification informing that it's deleting the private endpoint connection." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleting-notification.png":::

1. When the operation completes, a notification informs you that the private endpoint connection was successfully deleted.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleted-notification.png" alt-text="Screenshot showing the notification informing that private endpoint connection is deleted." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleted-notification.png":::

> [!IMPORTANT]
> The previous procedure doesn't delete the private endpoint, but only the connection between that private endpoint and your instance of Azure Database for PostgreSQL flexible server. To learn how to delete the private endpoint, see [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint).


## [CLI](#tab/cli-delete-private-endpoint-connection)

Use the [az network private-endpoint-connection delete](/cli/azure/network/private-endpoint-connection#az-network-private-endpoint-connection-delete) command to delete one private endpoint connection.

```azurecli-interactive
az network private-endpoint-connection delete --resource-group <resource_group> --resource-name <server> --type Microsoft.DBforPostgreSQL/flexibleServers --name <connection> --yes
```

> [!IMPORTANT]
> The previous procedure doesn't delete the private endpoint, but only the connection between that private endpoint and your instance of Azure Database for PostgreSQL flexible server. To learn how to delete the private endpoint, see [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint).

---

## Related content

- [Networking](how-to-networking.md).
- [Enable or disable public access](how-to-networking-servers-deployed-public-access-enable-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
