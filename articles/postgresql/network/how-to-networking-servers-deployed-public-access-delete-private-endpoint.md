---
title: Delete private endpoint connections
description: This article describes how to delete private endpoint connections to an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/29/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to delete private endpoint connections to an Azure Database for PostgreSQL.
---

# Delete private endpoint connections

Azure Database for PostgreSQL flexible server is an Azure Private Link service. This means that you can create private endpoints so that your client applications can connect privately and securely to your Azure Database for PostgreSQL flexible server.

A private endpoint to your Azure Database for PostgreSQL flexible server is a network interface that you can inject in a subnet of an Azure virtual network. Any host or service that can route network traffic to that subnet, are able to communicate with your flexible server so that the network traffic doesn't have to traverse the internet. All traffic is sent privately using Microsoft backbone.

For more information about Azure Private Link and Azure Private Endpoint, see [Azure Private Link frequently asked questions](/azure/private-link/private-link-faq).

## [Portal](#tab/portal-delete-private-endpoint-connections)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint.png":::

3. Select the private endpoint connection that you want to delete, and select **Delete** to trigger the deletion of the private endpoint connection.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-delete.png" alt-text="Screenshot showing the Delete button to trigger the deletion of an existing private endpoint connection." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-delete.png":::

4. A notification informs you that the private endpoint connection is being deleted.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleting-notification.png" alt-text="Screenshot showing the notification informing that it-s deleting the private endpoint connection." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleting-notification.png":::

5. When the operation completes, a notification informs you that the private endpoint connection was successfully deleted.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleted-notification.png" alt-text="Screenshot showing the notification informing that private endpoint connection is deleted." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-deleted-notification.png":::

> [!IMPORTANT]
> The previous procedure doesn't delete the private endpoint, but only the connection established between that private endpoint and your instance of Azure Database for PostgreSQL flexible server. To learn how to delete the private endpoint, see [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint).


## [CLI](#tab/cli-delete-private-endpoint-connection)

You can delete one private endpoint connection to a server via the [az network private-endpoint-connection delete](/cli/azure/network/private-endpoint-connection#az-network-private-endpoint-connection-delete) command.

```azurecli-interactive
az network private-endpoint-connection delete --resource-group <resource_group> --resource-name <server> --type Microsoft.DBforPostgreSQL/flexibleServers --name <connection> --yes
```

> [!IMPORTANT]
> The previous procedure doesn't delete the private endpoint, but only the connection established between that private endpoint and your instance of Azure Database for PostgreSQL flexible server. To learn how to delete the private endpoint, see [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint).

---

## Related content

- [Networking](how-to-networking.md).
- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
