---
title: Change private DNS zone
description: This article describes how to change the private DNS zone of your Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to change the private DNS zone of an Azure Database for PostgreSQL flexible server.
---

# Change private DNS zone

[Azure Private DNS](/azure/dns/private-dns-overview) provides a reliable and secure DNS service for your virtual network. Azure Private DNS manages and resolves domain names in the virtual network, without the need to configure a custom DNS solution.

When you deploy an Azure Database for PostgreSQL flexible server with **Networking with private access (VNET Integration)** mode, you're required to provide the private DNS zone in which  is mandatory to be able to do DNS resolution. For new Azure Database for PostgreSQL flexible server creation by using private network access, Private DNS zones need to be used while you configure Azure Database for PostgreSQL flexible servers with private access.

On existing servers, you can change the private DNS zone from the one that you provided during server creation, to another one that exists already and that can be on any resource group of any subscription to which you have access.

## [Portal](#tab/portal-change-private-dns-zone)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-networking/networking-overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-networking/networking-overview.png":::

3. The status of the server must be **Ready**, for the **Networking** menu option to be enabled.

    :::image type="content" source="./media/how-to-networking/networking-server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-networking/networking-server-status.png":::

4. If the status of the server isn't **Ready**, the **Networking** option is disabled.

    :::image type="content" source="./media/how-to-networking/networking-disabled.png" alt-text="Screenshot showing that Networking menu is disabled when status of server isn't Ready." lightbox="./media/how-to-networking/networking-disabled.png":::

> [!NOTE]
> Any attempt to configure the networking settings of a server whose status is other than available, would fail with an error.

5. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/private-access-networking.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/private-access-networking.png":::

6. The only network related modifiable setting for servers deployed with **Private access (VNET Integration)** is the private DNS zone in which the server is integrated. To change it, in the **Private DNS integration** section, expand the **Subscription** and **Private DNS zone** comboboxes to select an existing private DNS zone in which you want to integrate your server.

    :::image type="content" source="./media/how-to-networking/private-access-change-private-dns-zone.png" alt-text="Screenshot showing how to select a different private DNS zone." lightbox="./media/how-to-networking/private-access-change-private-dns-zone.png":::

7. If the selected private DNS zone isn't linked to the virtual network in which your server is injected, you can see the **Link private DNS zone to your virtual network** checkbox. It's selected by default, and that means that the selected private DNS zone will be linked to the virtual network of your server. By clearing the checkbox, you're deciding to not link that private DNS zone to the virtual network of your server. As a consequence, none of the hosts in that virtual network wouldn't be able to resolve the name of your server using the A record persisted by the server in that private zone.

    :::image type="content" source="./media/how-to-networking/private-access-link-to-vnet.png" alt-text="Screenshot showing how to choose if you want to link the new private DNS zone to the virtual network in which the server is injected." lightbox="./media/how-to-networking/private-access-link-to-vnet.png":::

> [!NOTE]
> If you select **Link private DNS zone to your virtual network**

8. Select **Save**.

    :::image type="content" source="./media/how-to-networking/private-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/private-access-save.png":::

8. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/private-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/private-access-progressing-notification.png":::

9. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/public-access-updating.png":::

10. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/private-access-progressing-notification-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/private-access-progressing-notification-succeeded-notification.png":::

11. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-networking/public-access-available.png" alt-text="Screenshot showing that server status is Ready." lightbox="./media/how-to-networking/public-access-available.png":::

## [CLI](#tab/cli-change-private-dns-zone)

You can change the private DNS zone associated to your server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
privateZoneId=$(az network private-dns zone show --resource-group <private_dns_zone_resource_group> --name <private_dns_zone> --query id --output tsv)
az postgres flexible-server update --resource-group <server_resource_group> --name <server> --private-dns-zone $privateZoneId
```

If you want to link the private DNS zone to the virtual network of your server, run the following commands:

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
