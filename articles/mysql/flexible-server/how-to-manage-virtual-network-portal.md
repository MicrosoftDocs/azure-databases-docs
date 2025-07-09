---
title: Manage Virtual Networks - Azure Portal
description: Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal

Azure Database for MySQL Flexible Server supports two types of mutually exclusive network connectivity methods to connect to your Azure Database for MySQL Flexible Server instance. The two options are:

- Public access (allowed IP addresses)
- Private access (virtual network integration)

This article focuses on creation of MySQL server with **Private access (VNet Integration)** using Azure portal. With Private access (virtual network integration), you can deploy your Azure Database for MySQL Flexible Server instance into your own [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview). Azure Virtual Networks provide private and secure network communication. With private access, connections to the MySQL server are restricted to your virtual network. To learn more about it, refer to [Private access (virtual network Integration)](./concepts-networking-vnet.md#private-access-virtual-network-integration).

> [!NOTE]  
> You can deploy your Azure Database for MySQL Flexible Server instance into a virtual network and subnet during server creation. After the Azure Database for MySQL Flexible Server instance is deployed, you cannot move it into another virtual network or subnet.

## Prerequisites

To create an Azure Database for MySQL Flexible Server instance in a virtual network, you need:

- A [Virtual Network](/azure/virtual-network/quick-create-portal#create-a-virtual-network)
    > [!NOTE]  
    > The virtual network and subnet should be in the same region and subscription as your Azure Database for MySQL Flexible Server instance.

- To [delegate a subnet](/azure/virtual-network/manage-subnet-delegation#delegate-a-subnet-to-an-azure-service) to **Microsoft.DBforMySQL/flexibleServers**. This delegation means that only Azure Database for MySQL Flexible Server instances can use that subnet. No other Azure resource types can be in the delegated subnet.

## Create an Azure Database for MySQL Flexible Server instance in an already existing virtual network

1. Select **Create a resource** (+) in the upper-left corner of the portal.
1. Select **Databases** > **Azure Database for MySQL**. You can also enter **MySQL** in the search box to find the service.
1. Select **Flexible server** as the deployment option.
1. Fill out the **Basics** form
1. Go to the **Networking** tab.
1. In the **Connectivity method**, select **Private access (VNet Integration)**. Go to **Virtual Network** section, you can either select an already existing *virtual network* and *Subnet* that is delegated to *Microsoft.DBforMySQL/flexibleServers* or create a new one by selecting the *create virtual network* link.
    > [!NOTE]  
    > Only virtual networks and subnets in the same region and subscription are listed in the dropdown list. </br>
    > The chosen subnet is delegated to *Microsoft.DBforMySQL/flexibleServers*. It means that only Azure Database for MySQL Flexible Server instances can use that subnet.</br>

    :::image type="content" source="media/how-to-manage-virtual-network-portal/vnet-creation.png" alt-text="Screenshot of Vnet-integration." lightbox="media/how-to-manage-virtual-network-portal/vnet-creation.png":::
1. (Public Preview) You can now specify a custom database port between 25001 to 26000 for your server. Find more details about custom port supported scenarios and limitation [here](./concepts-networking.md).
1. Create a new or Select an existing **Private DNS Zone**.
    > [!NOTE]  
    > Private DNS zone names must end with `mysql.database.azure.com`. </br>
    > If you do not see the option to create a new private dns zone, enter the server name on the **Basics** tab.</br>
    > After the Azure Database for MySQL Flexible Server instance is deployed to a virtual network and subnet, you cannot move it to Public access (allowed IP addresses).</br>

    :::image type="content" source="media/how-to-manage-virtual-network-portal/private-dns-zone.png" alt-text="Screenshot of dnsconfiguration." lightbox="media/how-to-manage-virtual-network-portal/private-dns-zone.png":::
1. Select **Review + create** to review your Azure Database for MySQL Flexible Server configuration.
1. Select **Create** to provision the server. Provisioning can take a few minutes.

## Related content

- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-virtual-network-cli.md)
- [networking in Azure Database for MySQL Flexible Server](concepts-networking.md)
- [Azure Database for MySQL Flexible Server virtual network](./concepts-networking-vnet.md#private-access-virtual-network-integration)
