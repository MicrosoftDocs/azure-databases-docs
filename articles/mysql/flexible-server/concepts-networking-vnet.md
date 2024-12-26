---
title: Private Network Access Overview
description: Learn about private access networking option in Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Private Network Access using virtual network integration for Azure Database for MySQL - Flexible Server

This article describes the private connectivity option for Azure Database for MySQL Flexible Server. You learn in detail the virtual network concepts for Azure Database for MySQL Flexible Server to create a server securely in Azure.

## Private access (Virtual Network integration)

[Azure Virtual Network)](/azure/virtual-network/virtual-networks-overview) is the fundamental building block for your private network in Azure. Virtual network integration with Azure Database for MySQL Flexible Server brings Azure's benefits of network security and isolation.

Virtual network integration for an Azure Database for MySQL Flexible Server instance enables you to lock down access to the server to only your virtual network infrastructure. Your virtual network can include all your application and database resources in a single virtual network or can stretch across different Virtual Networks in the same region or a different region. Seamless connectivity between various virtual networks can be established by [peering](/azure/virtual-network/virtual-network-peering-overview), which uses Microsoft's low latency, high-bandwidth private backbone infrastructure. The virtual networks appear as one for connectivity purposes.

Azure Database for MySQL Flexible Server supports client connectivity from:

- Virtual networks within the same Azure region (locally peered virtual networks)
- Virtual networks across Azure regions (Global peered virtual networks)

Subnets enable you to segment the virtual network into one or more subnetworks and allocate a portion of the virtual network's address space to which you can then deploy Azure resources. Azure Database for MySQL Flexible Server requires a [delegated subnet](/azure/virtual-network/subnet-delegation-overview). A delegated subnet is an explicit identifier that a subnet can host only Azure Database for MySQL Flexible Server instances. By delegating the subnet, the service gets direct permissions to create service-specific resources to manage your Azure Database for MySQL Flexible Server instance seamlessly.

> [!NOTE]  
> The smallest CIDR range you can specify for the subnet to host Azure Database for MySQL Flexible Server is /29, which provides eight IP addresses. However, the first and last address in any network or subnet can't be assigned to any individual host. Azure reserves five IP addresses for internal use by Azure networking, including the two IP addresses that can't be assigned to a host. This leaves three available IP addresses for a /29 CIDR range. For Azure Database for MySQL Flexible Server, it's required to allocate one IP address per node from the delegated subnet when private access is enabled. HA-enabled servers require two IP addresses, and a Non-HA server requires one IP address. It is recommended to reserve at least two IP addresses per Azure Database for MySQL Flexible Server instance, as high availability options can be enabled later.
Azure Database for MySQL Flexible Server integrates with Azure [Private DNS zones](/azure/dns/private-dns-privatednszone) to provide a reliable, secure DNS service to manage and resolve domain names in a virtual network without the need to add a custom DNS solution. A private DNS zone can be linked to one or more virtual networks by creating [virtual network links](/azure/dns/private-dns-virtual-network-links)

:::image type="content" source="media/concepts-networking-vnet/vnet-diagram.png" alt-text="Screenshot of Flexible server MySQL VNET." lightbox="media/concepts-networking-vnet/vnet-diagram.png":::

In the above diagram,

1. Azure Databases for MySQL Flexible Server instances are injected into a delegated subnet - 10.0.1.0/24 of virtual network **VNet-1**.
1. Applications deployed on different subnets within the same virtual network can access the Azure Database for MySQL Flexible Server instances directly.
1. Applications deployed on a different virtual network **VNet-2** don't have direct access to Azure Database for MySQL Flexible Server instances. Before they can access an instance, you must perform a [private DNS zone virtual network peering](#private-dns-zone-and-virtual-network-peering).

## Virtual network concepts

Here are some concepts to be familiar with when using Virtual Networks with Azure Database for MySQL Flexible Server instances.

- **Virtual network** -

   An Azure Virtual Network contains a private IP address space configured for your use. Visit the [Azure Virtual Network overview](/azure/virtual-network/virtual-networks-overview) to learn more about Azure virtual networking.

   Your virtual network must be in the same Azure region as your Azure Database for MySQL Flexible Server instance.

- **Delegated subnet** -

   A virtual network contains subnets (subnetworks). Subnets enable you to segment your virtual network into smaller address spaces. Azure resources are deployed into specific subnets within a virtual network.

   Your Azure Database for MySQL Flexible Server instance must be in a subnet that is **delegated** for Azure Database for MySQL Flexible Server use only. This delegation means that only Azure Database for MySQL Flexible Server instances can use that subnet. No other Azure resource types can be in the delegated subnet. You delegate a subnet by assigning its delegation property as Microsoft.DBforMySQL/flexibleServers.

- **Network security groups (NSG)**

   Security rules in network security groups enable you to filter the type of network traffic that can flow in and out of virtual network subnets and network interfaces. Review the [network security group overview](/azure/virtual-network/network-security-groups-overview) for more information.

- **Private DNS zone integration**

   Azure private DNS zone integration allows you to resolve the private DNS within the current virtual network or any in-region peered virtual network where the private DNS Zone is linked.

- **Virtual network peering**

   A virtual network peering enables you to connect two or more virtual networks in Azure seamlessly. The peered virtual networks appear as one for connectivity purposes. The traffic between virtual machines in peered virtual networks uses the Microsoft backbone infrastructure. The traffic between the client application and the Azure Database for MySQL Flexible Server instance in peered virtual networks is routed only through Microsoft's private network and is isolated to that network.

## Use Private DNS Zone

- If you use the Azure portal or the Azure CLI to create Azure Database for MySQL Flexible Server instances with a virtual network, a new private DNS zone ending with `mysql.database.azure.com` is autoprovisioned per server in your subscription using the server name provided. Alternatively, if you want to set up your own private DNS zone with the Azure Database for MySQL Flexible Server instance, see the [private DNS overview](/azure/dns/private-dns-overview) documentation.
- If you use Azure API, an Azure Resource Manager template (ARM template), or Terraform, create private DNS zones that end with `mysql.database.azure.com` and use them while configuring Azure Database for MySQL Flexible Server instances with private access. For more information, see the [private DNS zone overview](/azure/dns/private-dns-overview).

   > [!IMPORTANT]  
   > Private DNS zone names must end with `mysql.database.azure.com`. If you are connecting to an Azure Database for MySQL Flexible Server instance with SSL and you're using an option to perform full verification (sslmode=VERIFY_IDENTITY) with certificate subject name, use \<servername\>.mysql.database.azure.com in your connection string.

Learn how to create an Azure Database for MySQL Flexible Server instance with private access (virtual network integration) in [the Azure portal](how-to-manage-virtual-network-portal.md) or [the Azure CLI](how-to-manage-virtual-network-cli.md).

## Integration with a custom DNS server

If you're using the custom DNS server, then you must **use a DNS forwarder to resolve the FQDN of the Azure Database for MySQL Flexible Server instance**. The forwarder IP address should be [168.63.129.16](/azure/virtual-network/what-is-ip-address-168-63-129-16). The custom DNS server should be inside the virtual network or reachable via the virtual network's DNS Server setting. Refer to [name resolution that uses your DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server) to learn more.

> [!IMPORTANT]  
> For successful provisioning of the Azure Database for MySQL Flexible Server instance, even if you are using a custom DNS server, **you must not block DNS traffic to [AzurePlatformDNS](/azure/virtual-network/service-tags-overview) using [NSG](/azure/virtual-network/network-security-groups-overview)**.

## Private DNS zone and virtual network peering

Private DNS zone settings and virtual network peering are independent of each other. For more information on creating and using Private DNS zones, see the [Use Private DNS Zone](#use-private-dns-zone) section.

If you want to connect to the Azure Database for MySQL Flexible Server instance from a client that is provisioned in another virtual network from the same region or a different region, you have to link the private DNS zone with the virtual network. See [how to link the virtual network](/azure/dns/private-dns-getstarted-portal#link-the-virtual-network) documentation.

> [!NOTE]  
> Only private DNS zone names that end with `mysql.database.azure.com` can be linked.

## Connect from an on-premises server to an Azure Database for MySQL Flexible Server instance in a virtual network using ExpressRoute or VPN

For workloads requiring access to an Azure Database for MySQL Flexible Server instance in a virtual network from an on-premises network, you need an [ExpressRoute](/azure/architecture/reference-architectures/hybrid-networking/expressroute/) or [VPN](/azure/architecture/reference-architectures/hybrid-networking/vpn/) and virtual network [connected to on-premises](/azure/architecture/reference-architectures/hybrid-networking/). With this setup in place, you need a DNS forwarder to resolve the Azure Database for MySQL Flexible Server servername if you want to connect from client applications (like MySQL Workbench) running on on-premises virtual networks. This DNS forwarder is responsible for resolving all the DNS queries via a server-level forwarder to the Azure-provided DNS service [168.63.129.16](/azure/virtual-network/what-is-ip-address-168-63-129-16).

To configure correctly, you need the following resources:

- An On-premises network.
- An Azure Database for MySQL Flexible Server instance provisioned with private access (virtual network integration).
- A virtual network [connected to on-premises](/azure/architecture/reference-architectures/hybrid-networking/).
- A DNS forwarder [168.63.129.16](/azure/virtual-network/what-is-ip-address-168-63-129-16) deployed in Azure.

You can then use the Azure Database for MySQL Flexible Server servername (FQDN) to connect from the client application in the peered virtual network or on-premises network to the Azure Database for MySQL Flexible Server instance.

> [!NOTE]  
> We recommend you use the fully qualified domain name (FQDN) `<servername>.mysql.database.azure.com` in connection strings when connecting to your Azure Database for MySQL Flexible Server instance. The server's IP address is not guaranteed to remain static. Using the FQDN will help you avoid making changes to your connection string.

## Unsupported virtual network scenarios

- Public endpoint (or public IP or DNS) - An Azure Database for MySQL Flexible Server instance deployed to a virtual network can't have a public endpoint.
- After the Azure Database for MySQL Flexible Server instance is deployed to a virtual network and subnet, you can't move it to another virtual network or subnet. You can't move the virtual network into another resource group or subscription.
- Private DNS integration config can't be changed after deployment.
- Subnet size (address spaces) can't be increased after resources exist in the subnet.

## Move from private access (virtual network integrated) network to public access or private link

Azure Database for MySQL Flexible Server can be transitioned from private access (virtual network Integrated) to public access, with the option to use Private Link. This functionality enables servers to switch from virtual network integrated to Private Link/Public infrastructure seamlessly, without the need to alter the server name or migrate data, simplifying the process for customers.

> [!NOTE]  
> That once the transition is made, it cannot be reversed. The transition involves a downtime of approximately 5-10 minutes for Non-HA servers and about 20 minutes for HA-enabled servers.

The process is conducted in offline mode and consists of two steps:

1. Detaching the server from the virtual network infrastructure.
1. Establishing a Private Link or enabling public access.

- For guidance on transitioning from Private access network to Public access or Private Link, visit [Move from private access (virtual network integrated) to public access or Private Link with the Azure portal](how-to-network-from-private-to-public.md). This resource offers step-by-step instructions to facilitate the process.

## Related content

- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-virtual-network-cli.md)
- [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md)
