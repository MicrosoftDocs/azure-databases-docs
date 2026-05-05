---
title: Approve Private Endpoint Connections in Azure HorizonDB
description: This article describes how to approve private endpoint connections in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
# customer intent: As a user, I want to learn how to approve private endpoint connections in Azure HorizonDB.
---

# Approve private endpoint connections in Azure HorizonDB

Azure HorizonDB is an Azure Private Link service. This means that you can create private endpoints so that your client applications can connect privately and securely to your Azure HorizonDB.

A private endpoint to your Azure HorizonDB is a network interface that you can inject in a subnet of an Azure virtual network. Any host or service that can route network traffic to that subnet, are able to communicate with your flexible server so that the network traffic doesn't have to traverse the internet. All traffic is sent privately using Microsoft backbone.

For more information about Azure Private Link and Azure Private Endpoint, see [Azure Private Link frequently asked questions](/azure/private-link/private-link-faq).

In many enterprises, networking and database operation duties are clearly separated.

In such organizations, network administrators create the cloud networking infrastructure, such as Azure Private Link services, and database administrator create and manage the database servers, such as Azure HorizonDB.

Therefore, network administrators wouldn't have permissions to approve and reject private endpoint connections on Azure HorizonDB. Likewise, database administrators wouldn't have permissions to deploy private endpoints, integrate them with private DNS zones, or link the private DNS zones to virtual networks.

In these scenarios, after network administrators create a private endpoint, the database administrators are responsible for approving or rejecting the connections that are created from those private endpoints.

## [Portal](#tab/portal-approve-private-endpoint-connections)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, select **Networking**.

   :::image type="content" source="media/how-to-networking/public-access-networking-disabled-pending-endpoint.png" alt-text="Screenshot showing the Networking page." lightbox="media/how-to-networking/public-access-networking-disabled-pending-endpoint.png":::

1. Select the private endpoint connection whose state is **Pending**, and you want to approve. Select **Approve** to trigger the approval of the private endpoint connection.

   :::image type="content" source="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approve.png" alt-text="Screenshot showing the Approve button to trigger the approval of an existing private endpoint connection." lightbox="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approve.png":::

1. If you consider it necessary, in the **Description** box of the **Approve** dialog, type the reason why you're deciding to approve this private endpoint connection, and select **Yes**.

   :::image type="content" source="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approve-confirm.png" alt-text="Screenshot showing the Approve dialog to provide reason why the request is approved." lightbox="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approve-confirm.png":::

1. A notification informs you that the private endpoint connection is being approved.

   :::image type="content" source="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approving-notification.png" alt-text="Screenshot showing the notification informing that it's approving the private endpoint connection." lightbox="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approving-notification.png":::

1. When the operation completes, a notification informs you that the private endpoint connection was successfully approved.

   :::image type="content" source="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approved-notification.png" alt-text="Screenshot showing the notification informing that private endpoint connection is approved." lightbox="media/how-to-networking/public-access-networking-disabled-pending-endpoint-approved-notification.png":::

## [CLI](#tab/cli-approve-private-endpoint-connection)

You can approve one private endpoint connection that is in pending state to a server via the [az network private-endpoint-connection approve](/cli/azure/network/private-endpoint-connection#az-network-private-endpoint-connection-approve) command.

```azurecli-interactive
az network private-endpoint-connection approve --description <description> --resource-group <resource_group> --resource-name <server> --type Microsoft.DBforPostgreSQL/flexibleServers --name <connection>
```

---

## Related content

- [Networking in Azure HorizonDB](how-to-networking.md)
- [Enable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-enable-public-access.md)
- [Disable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-disable-public-access.md)
- [Add firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-firewall-rules.md)
- [Delete firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md)
- [Delete private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md)
- [Approve private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md)
- [Reject private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md)
