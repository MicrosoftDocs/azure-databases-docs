---
title: Reject private endpoint connections
description: This article describes how to reject private endpoint connections to an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to reject private endpoint connections to an Azure Database for PostgreSQL flexible server.
---

# Reject private endpoint connections

Azure Database for PostgreSQL - Flexible Server is an Azure Private Link service. This means that you can create private endpoints so that your client applications can connect privately and securely to your Azure Database for PostgreSQL flexible server.

A private endpoint to your Azure Database for PostgreSQL flexible server is a network interface that you can inject in a subnet of an Azure virtual network. Any host or service that can route network traffic to that subnet, are able to communicate with your flexible server so that the network traffic doesn't have to traverse the internet. All traffic is sent privately using Microsoft backbone.

For more information about Azure Private Link and Azure Private Endpoint, see [Azure Private Link frequently asked questions](/azure/private-link/private-link-faq).

In many enterprises, networking and database operation duties are clearly separated.

In such organizations, network administrators create the cloud networking infrastructure, such as Azure Private Link services, and database administrator create and manage the database servers, such as Azure Database for PostgreSQL flexible server.

Therefore, network administrators wouldn't have permissions to approve and reject private endpoint connections on Azure Database for PostgreSQL flexible server. Likewise, database administrators wouldn't have permissions to deploy private endpoints, integrate them with private DNS zones, or link the private DNS zones to virtual networks.

In these scenarios, after network administrators create a private endpoint, the database administrators are responsible for approving or rejecting the connections that are created from those private endpoints.

## [Portal](#tab/portal-reject-private-endpoint-connections)

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

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-external-approved-endpoint.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-disabled-external-approved-endpoint.png":::

6. Select the private endpoint connection whose state is **Pending** or **Approved**, and that you want to reject.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-external-approved-endpoint-select.png" alt-text="Screenshot showing how to begin rejecting an existing private endpoint connection with Approved state." lightbox="./media/how-to-networking/public-access-networking-disabled-external-approved-endpoint-select.png":::

7. Select **Reject** to trigger the rejection of the private endpoint connection.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-external-approved-endpoint-reject.png" alt-text="Screenshot showing the Reject button to trigger the rejection of an existing private endpoint connection." lightbox="./media/how-to-networking/public-access-networking-disabled-external-approved-endpoint-reject.png":::

8. If you consider it necessary, in the **Description** box of the **Reject** dialog, type the reason why you're deciding to reject this private endpoint connection.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-reject-confirm.png" alt-text="Screenshot showing the Reject dialog to provide reason why the request is rejected." lightbox="./media/how-to-networking/public-access-networking-disabled-approved-endpoint-reject-confirm.png":::

9. A notification informs you that the private endpoint connection is being rejected.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-pending-endpoint-rejecting-notification.png" alt-text="Screenshot showing the notification informing that its rejecting the private endpoint connection." lightbox="./media/how-to-networking/public-access-networking-disabled-pending-endpoint-rejecting-notification.png":::

8. When the operation completes, a notification informs you that the private endpoint connection was successfully rejected.

    :::image type="content" source="./media/how-to-networking/public-access-networking-disabled-pending-endpoint-rejected-notification.png" alt-text="Screenshot showing the notification informing that private endpoint connection is rejected." lightbox="./media/how-to-networking/public-access-networking-disabled-pending-endpoint-rejected-notification.png":::

## [CLI](#tab/cli-rejected-private-endpoint-connection)

You can reject one private endpoint connection that is in pending state to a server via the [az network private-endpoint-connection reject](/cli/azure/network/private-endpoint-connection#az-network-private-endpoint-connection-reject) command.

```azurecli-interactive
az network private-endpoint-connection reject --description <description> --resource-group <resource_group> --resource-name <server> --type Microsoft.DBforPostgreSQL/flexibleServers --name <connection>
```

---

## Related content

- [Networking](how-to-networking.md).
- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
