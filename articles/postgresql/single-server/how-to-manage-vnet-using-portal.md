---
title: Use virtual network (VNet) rules - Azure portal - Azure Database for PostgreSQL - Single Server
description: Create and manage virtual network (VNet) service endpoints and rules Azure Database for PostgreSQL - Single Server using the Azure portal
author: niklarin
ms.author: nlarin
ms.reviewer: maghan
ms.date: 09/18/2024
ms.service: azure-database-postgresql
ms.subservice: single-server
ms.topic: how-to
---

# Create and manage virtual network (VNet) service endpoints and virtual network (VNet) rules in Azure Database for PostgreSQL - Single Server with the Azure portal

[!INCLUDE [applies-to-postgresql-single-server](../includes/applies-to-postgresql-single-server.md)]

[!INCLUDE [azure-database-for-postgresql-single-server-deprecation](../includes/azure-database-for-postgresql-single-server-deprecation.md)]

Virtual Network (VNet) services endpoints and rules extend the private address space of a Virtual Network to your Azure Database for PostgreSQL server. For an overview of Azure Database for PostgreSQL virtual network service endpoints, including limitations, see [Azure Database for PostgreSQL Server virtual network service endpoints](concepts-data-access-and-security-vnet.md). Virtual network service endpoints are available in all supported regions for Azure Database for PostgreSQL.

## Create a virtual network rule and enable service endpoints in the Azure portal

1. On the PostgreSQL server page, under the Settings heading, select **Connection Security** to open the Connection Security pane for Azure Database for PostgreSQL.

1. Ensure that the Allowed access to Azure services control is set to **OFF**.

1. Next, select on **+ Adding existing virtual network**. If you don't have an existing virtual network, you can select **+ Create new virtual network** to create one. See [Quickstart: Create a virtual network using the Azure portal](/azure/virtual-network/quick-create-portal).

   :::image type="content" source="media/how-to-manage-vnet-using-portal/1-connection-security.png" alt-text="Screenshot of Azure portal - select Connection security." lightbox="media/how-to-manage-vnet-using-portal/1-connection-security.png":::

1. Enter a virtual network rule name, select the subscription, Virtual network, and Subnet name and then select **Enable**. This automatically enables virtual network service endpoints on the subnet using the **Microsoft.SQL** service tag.

   :::image type="content" source="media/how-to-manage-vnet-using-portal/2-configure-vnet.png" alt-text="Screenshot of Azure portal - configure VNet." lightbox="media/how-to-manage-vnet-using-portal/2-configure-vnet.png":::

    The account must have the necessary permissions to create a virtual network and service endpoint.

    Service endpoints can be configured on virtual networks independently, by a user with write access to the virtual network.

    To secure Azure service resources to a virtual network, the user must have permission to "Microsoft.Network/virtualNetworks/subnets/joinViaServiceEndpoint/" for the subnets being added. This permission is included in the built-in service administrator roles, by default and can be modified by creating custom roles.

    Learn more about [built-in roles](/azure/role-based-access-control/built-in-roles) and assigning specific permissions to [custom roles](/azure/role-based-access-control/custom-roles).

    VNets and Azure service resources can be in the same or different subscriptions. If the virtual network and Azure service resources are in different subscriptions, the resources should be under the same Active Directory (AD) tenant. Ensure that both the subscriptions have the **Microsoft.Sql** resource provider registered.

1. Once enabled, select **OK** and you'll see that virtual network service endpoints are enabled along with a virtual network rule.

## Related content

- [Enable virtual network service endpoints and create a virtual network rule for Azure Database for PostgreSQL using Azure CLI](how-to-manage-vnet-using-cli.md)
- [Connection libraries for Azure Database for PostgreSQL](./concepts-connection-libraries.md)
