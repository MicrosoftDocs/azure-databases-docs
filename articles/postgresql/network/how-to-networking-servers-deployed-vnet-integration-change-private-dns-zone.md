---
title: Change Private DNS Zone in Azure Database for PostgreSQL Flexible Server
description: This article describes how to change the private DNS zone of your Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to change the private DNS zone of my existing Azure Database for PostgreSQL flexible server, so that I can use a different DNS zone than the one I set during server creation.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
---

# Change private DNS zone in Azure Database for PostgreSQL flexible server

[Azure Private DNS](/azure/dns/private-dns-overview) provides a reliable and secure DNS service for your virtual network. Azure Private DNS manages and resolves domain names in the virtual network, without the need to configure a custom DNS solution.

When you deploy an Azure Database for PostgreSQL flexible server with **Networking with private access (VNET Integration)** mode, you must provide the private DNS zone to enable DNS resolution. For new Azure Database for PostgreSQL flexible server creation by using private network access, you need to use private DNS zones while configuring Azure Database for PostgreSQL flexible servers with private access.

On existing servers, you can change the private DNS zone from the one that you provided during server creation, to another one that already exists. The other private DNS zone can be on any resource group of any subscription to which you have access.

## [Portal](#tab/portal-change-private-dns-zone)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/private-access-networking.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/private-access-networking.png":::

1. For servers deployed with **Private access (VNET Integration)**, the only network-related setting you can change is the private DNS zone where the server is integrated. To change it, in the **Private DNS integration** section, expand the **Subscription** and **Private DNS zone** dropdowns to select an existing private DNS zone where you want to integrate your server.

    :::image type="content" source="./media/how-to-networking/private-access-change-private-dns-zone.png" alt-text="Screenshot showing how to select a different private DNS zone." lightbox="./media/how-to-networking/private-access-change-private-dns-zone.png":::

1. If the selected private DNS zone isn't linked to the virtual network where your server is injected, you see the **Link private DNS zone to your virtual network** checkbox. It's selected by default, and that means the selected private DNS zone is linked to the virtual network of your server. By clearing the checkbox, you decide to not link that private DNS zone to the virtual network of your server. As a consequence, none of the hosts in that virtual network can resolve the name of your server by using the A record that the server persists in that private zone. Select **Save**.

    :::image type="content" source="./media/how-to-networking/private-access-link-to-vnet.png" alt-text="Screenshot showing how to choose if you want to link the new private DNS zone to the virtual network in which the server is injected." lightbox="./media/how-to-networking/private-access-link-to-vnet.png":::

1. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/private-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/private-access-progressing-notification.png":::

1. When the process finishes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/private-access-progressing-notification-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/private-access-progressing-notification-succeeded-notification.png":::

## [CLI](#tab/cli-change-private-dns-zone)

Use the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command to change the private DNS zone associated with your server.

```azurecli-interactive
privateZoneId=$(az network private-dns zone show --resource-group <private_dns_zone_resource_group> --name <private_dns_zone> --query id --output tsv)
az postgres flexible-server update \
  --resource-group <server_resource_group> \
  --name <server> \
  --private-dns-zone $privateZoneId
```

To link the private DNS zone to the virtual network of your server, run the following commands:

```azurecli-interactive
# Obtain the delegated subnet in which your server is integrated 
subnetId=$(az postgres flexible-server show --resource-group <server_resource_group> --name <server> --query network.delegatedSubnetResourceId --output tsv)
# Trim the subnet part, to end up having the identifier of the virtual network
virtualNetworkId=$(echo $subnetId | sed 's/\/subnets.*//')
virtualNetworkName=$(echo $subnetId | sed -n 's|.*/virtualNetworks/\(.*\)/subnets/.*|\1|p')
# Link the private DNS zone to the virtual network
az network private-dns link vnet create --resource-group <private_dns_zone_resource_group> --zone-name <private_dns_zone> --virtual-network $virtualNetworkId --registration-enabled false --name $virtualNetworkName
```

---

## Related content

- [Networking](how-to-networking.md).
