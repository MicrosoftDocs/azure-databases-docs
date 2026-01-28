---
title: Networking overview with private access (virtual network)
description: Learn about connectivity and networking options for your Azure Database for PostgreSQL flexible server instance with private access (virtual network).
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 06/27/2024
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: concept-article
---

# Network with private access (virtual network integration) for Azure Database for PostgreSQL  

This article describes connectivity and networking concepts for Azure Database for PostgreSQL flexible server instances.

When you create an Azure Database for PostgreSQL flexible server instance, you must choose one of the following networking options:

- Private access (virtual network integration)
- Public access (allowed IP addresses) and private endpoint

This document describes the private access (virtual network integration) networking option.

## Private access (virtual network integration)

You can deploy an Azure Database for PostgreSQL flexible server instance into your [Azure virtual network](/azure/virtual-network/virtual-networks-overview) by using [virtual network injection](/azure/virtual-network/virtual-network-for-azure-services). Azure virtual networks provide private and secure network communication. Resources in a virtual network can communicate through private IP addresses that were assigned on this network.

Choose this networking option if you want the following capabilities:

- Connect from Azure resources in the same virtual network to your Azure Database for PostgreSQL flexible server instance by using private IP addresses.
- Use a VPN or Azure ExpressRoute to connect from non-Azure resources to your Azure Database for PostgreSQL flexible server instance.
- Ensure that the Azure Database for PostgreSQL flexible server instance has no public endpoint that's accessible through the internet.

:::image type="content" source="media/concepts-networking-private/flexible-pg-vnet-diagram.png" alt-text="Diagram that shows how peering works between virtual networks, one of which includes an Azure Database for PostgreSQL flexible server instance.":::

In the preceding diagram:

- Azure Database for PostgreSQL flexible server instances are injected into subnet 10.0.1.0/24 of the VNet-1 virtual network.
- Applications that are deployed on different subnets within the same virtual network can access Azure Database for PostgreSQL flexible server instances directly.
- Applications that are deployed on a different virtual network (VNet-2) don't have direct access to Azure Database for PostgreSQL flexible server instances. You have to perform [virtual network peering for a Private DNS zone](#private-dns-zone-and-virtual-network-peering) before they can access the flexible server instance.

### Virtual network concepts

An Azure virtual network contains a private IP address space that's configured for your use. Your virtual network must be in the same Azure region as your Azure Database for PostgreSQL flexible server instance. To learn more about virtual networks, see the [Azure Virtual Network overview](/azure/virtual-network/virtual-networks-overview).

Here are some concepts to be familiar with when you're using virtual networks where resources are [integrated into a virtual network](/azure/virtual-network/virtual-network-for-azure-services) with Azure Database for PostgreSQL flexible server instances:

- **Delegated subnet**: A virtual network contains subnets (subnetworks). Subnets enable you to segment your virtual network into smaller address spaces. Azure resources are deployed into specific subnets within a virtual network.

  Your Azure Database for PostgreSQL flexible server instance that's integrated in a virtual network must be in a subnet that's *delegated*. That is, only Azure Database for PostgreSQL flexible server instances can use that subnet. No other Azure resource types can be in the delegated subnet. You delegate a subnet by assigning its delegation property as `Microsoft.DBforPostgreSQL/flexibleServers`.

  The smallest CIDR range you can specify for the subnet is /28, which provides 16 IP addresses. The first and last address in any network or subnet can't be assigned to any individual host. Azure reserves five IPs to be used internally by Azure networking, which includes two IPs that can't be assigned to the host, as mentioned. This leaves you 11 available IP addresses for a /28 CIDR range. A single Azure Database for PostgreSQL flexible server instance with high-availability features uses four addresses.

  For replication and Microsoft Entra connections, make sure route tables don't affect traffic. A common pattern is to route all outbound traffic via an Azure Firewall or a custom on-premises network filtering appliance.

  If the subnet has a route table associated with the rule to route all traffic to a virtual appliance:

  * Add a rule with the destination service tag `AzureActiveDirectory` and the next hop `Internet`.
  * Add a rule with the destination IP range the same as the Azure Database for PostgreSQL flexible server instance subnet range and the next hop `Virtual Network`.

  > [!IMPORTANT]
  > The names `AzureFirewallSubnet`, `AzureFirewallManagementSubnet`, `AzureBastionSubnet`, and `GatewaySubnet` are reserved within Azure. Don't use any of these names as your subnet name. Additionally, virtual networks should not have overlapping address space for creating cross-region replicas.


- **Network security group (NSG)**: Security rules in NSGs enable you to filter the type of network traffic that can flow in and out of virtual network subnets and network interfaces. For more information, see the [NSG overview](/azure/virtual-network/network-security-groups-overview).

  Application security groups (ASGs) make it easy to control Layer-4 security by using NSGs for flat networks. You can quickly:

  - Join virtual machines to an ASG or remove virtual machines from an ASG.
  - Dynamically apply rules to those virtual machines or remove rules from those virtual machines.

  For more information, see the [ASG overview](/azure/virtual-network/application-security-groups).

  At this time, we don't support NSGs where an ASG is part of the rule with Azure Database for PostgreSQL flexible server instances. We currently advise using [IP-based source or destination filtering](/azure/virtual-network/network-security-groups-overview#security-rules) in an NSG.

    High availability and other features of Azure Database for PostgreSQL server require the ability to send/receive traffic to *destination port 5432* within the Azure virtual network subnet where an Azure Database for PostgreSQL flexible server instance is deployed and to Azure Storage for log archival. If you create [NSGs](/azure/virtual-network/network-security-groups-overview) to deny traffic flow to or from your Azure Database for PostgreSQL flexible server instance within the subnet where it's deployed, *make sure to allow traffic to destination port 5432* within the subnet, and also to Storage, by using the [service tag](/azure/virtual-network/service-tags-overview) Storage as a destination. For high availability, the best practice is to add a Microsoft.Storage service endpoint because it is ensures correct traffic routing to Azure storage account which is used for uploading Write Ahead Log(WAL) files.

   You can further [filter](/azure/virtual-network/tutorial-filter-network-traffic) this exception rule by adding your Azure region to the label like `us-east.storage`. Also, if you elect to use [Microsoft Entra authentication](../security/security-entra-concepts.md) to authenticate sign-ins to your Azure Database for PostgreSQL flexible server instance, allow outbound traffic to Microsoft Entra ID by using a Microsoft Entra [service tag](/azure/virtual-network/service-tags-overview).

   When you set up [Read Replicas across Azure regions](../read-replica/concepts-read-replicas.md), your Azure Database for PostgreSQL flexible server instance requires the ability to send or receive traffic to *destination port 5432* for both primary and replica and to [Azure Storage](/azure/virtual-network/service-tags-overview#available-service-tags) in primary and replica regions from both primary and replica servers. The required destination TCP port for Storage is 443.

- **Private DNS zone integration**: Azure Private DNS zone integration allows you to resolve the private DNS within the current virtual network or any in-region peered virtual network where the Private DNS zone is linked.

### Use a Private DNS zone

[Azure Private DNS](/azure/dns/private-dns-overview) provides a reliable and secure DNS service for your virtual network. Azure Private DNS manages and resolves domain names in the virtual network without the need to configure a custom DNS solution.

When you use private network access with an Azure virtual network, providing the Private DNS zone information is *mandatory* to be able to do DNS resolution. For a new Azure Database for PostgreSQL flexible server instance creation by using private network access, Private DNS zones need to be used while you configure Azure Database for PostgreSQL flexible server instances with private access.

  > [!IMPORTANT]
  > When using a private DNS zone in a different subscription, that subscription **must** have the Microsoft.DBforPostgreSQL resource provider registered as well, otherwise your deployment of an Azure Database for PostgreSQL flexible server instance won't complete.

For a new Azure Database for PostgreSQL flexible server instance creation by using private network access with an API, Azure Resource Manager template (ARM template), Bicep or Terraform, create Private DNS zones. Then use them while you configure Azure Database for PostgreSQL flexible server instances with private access. For more information, see [REST API specifications for Azure](https://github.com/Azure/azure-rest-api-specs/blob/master/specification/postgresql/resource-manager/Microsoft.DBforPostgreSQL/stable/2021-06-01/postgresql.json).

If you use the [Azure portal](../network/how-to-networking.md) or the [Azure CLI](../network/how-to-networking.md) to create Azure Database for PostgreSQL flexible server instances, you can provide a Private DNS zone name that you previously created in the same or a different subscription, or a default Private DNS zone is automatically created in your subscription.

If you use an Azure API, an ARM template, Bicep or Terraform, create Private DNS zones that end with `.postgres.database.azure.com`. Use those zones while you configure Azure Database for PostgreSQL flexible server instances with private access. For example, use the form `[name1].[name2].postgres.database.azure.com` or `[name].postgres.database.azure.com`. If you choose to use the form `[name].postgres.database.azure.com`, the name _can't_ be the name that you use for one of your Azure Database for PostgreSQL flexible server instances, or you'll get an error message during provisioning. For more information, see [Private DNS zones overview](/azure/dns/private-dns-overview).

When you use the Azure portal, APIs, the Azure CLI, or an ARM template, you can also change the Private DNS zone from the one that you provided when you created your Azure Database for PostgreSQL flexible server instance to another Private DNS zone that exists for the same or different subscription.

  > [!IMPORTANT]
  > The ability to change a Private DNS zone from the one that you provided when you created your Azure Database for PostgreSQL flexible server instance to another Private DNS zone is currently disabled for servers with the high-availability feature enabled.

After you create a Private DNS zone in Azure, you need to [link](/azure/dns/private-dns-virtual-network-links) a virtual network to it. Resources hosted in the linked virtual network can then access the Private DNS zone.

  > [!IMPORTANT]
  > We no longer validate virtual network link presence on server creation for Azure Database for PostgreSQL flexible server instances with private networking. When you create a server through the portal, we provide customer choice to create a link on server creation via the checkbox **Link a Private DNS zone to your virtual network** in the Azure portal.

[DNS private zones are resilient](/azure/dns/private-dns-overview) to regional outages because zone data is globally available. Resource records in a private zone are automatically replicated across regions. Azure Private DNS is an availability zone foundational, zone-redundant service. For more information, see [Azure services with availability zone support](/azure/reliability/availability-zones-service-support).

### Integration with a custom DNS server

If you're using a custom DNS server, you must use a DNS forwarder to resolve the FQDN of your Azure Database for PostgreSQL flexible server instance. The forwarder IP address should be [168.63.129.16](/azure/virtual-network/what-is-ip-address-168-63-129-16).

The custom DNS server should be inside the virtual network or reachable via the virtual network's DNS server setting. To learn more, see [Name resolution that uses your own DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server).

### Private DNS zone and virtual network peering

Private DNS zone settings and virtual network peering are independent of each other. If you want to connect to the Azure Database for PostgreSQL flexible server instance from a client that's provisioned in another virtual network from the same region or a different region, you have to *link* the Private DNS zone with the virtual network. For more information, see [Link the virtual network](/azure/dns/private-dns-getstarted-portal#link-the-virtual-network).

> [!NOTE]
> Only Private DNS zone names that end with `postgres.database.azure.com` can be linked. Your DNS zone name can't be the same as your Azure Database for PostgreSQL flexible server instances. Otherwise, name resolution fails.

To map a server name to the DNS record, you can run the `nslookup` command in [Azure Cloud Shell](/azure/cloud-shell/overview) by using Azure PowerShell or Bash. Substitute the name of your server for the <server_name> parameter in the following example:

```bash
nslookup -debug <server_name>.postgres.database.azure.com | grep 'canonical name'
```

### Use hub-and-spoke private networking design

Hub and spoke is a popular networking model for efficiently managing common communication or security requirements.

The hub is a virtual network that acts as a central location for managing external connectivity. It also hosts services used by multiple workloads. The hub coordinates all communications to and from the spokes. IT rules or processes like security can inspect, route, and centrally manage traffic. The spokes are virtual networks that host workloads and connect to the central hub through virtual network peering. Shared services are hosted in their own subnets for sharing with the spokes. A perimeter subnet then acts as a security appliance.

The spokes are also virtual networks in Azure that are used to isolate individual workloads. The traffic flow between the on-premises headquarters and Azure is connected through Azure ExpressRoute or site-to-site VPN, connected to the hub virtual network. The virtual networks from the spokes to the hub are peered and enable communication to on-premises resources. You can implement the hub and each spoke in separate subscriptions or resource groups.

There are three main patterns for connecting spoke virtual networks to each other:

- **Spokes are directly connected to each other**: Virtual network peerings or VPN tunnels are created between the spoke virtual networks to provide direct connectivity without traversing the hub virtual network.
- **Spokes communicate over a network appliance**: Each spoke virtual network has a peering to a virtual WAN or to a hub virtual network. An appliance routes traffic from spoke to spoke. The appliance can be managed by Microsoft (as with a virtual WAN) or by you.
- **A virtual network gateway is attached to the hub network and makes use of user-defined routes**: Enables communication between the spokes.

:::image type="content" source="media/concepts-networking-private/hub-spoke-architecture.png" alt-text="Diagram that shows basic hub-and-spoke architecture with hybrid connectivity via an express hub.":::

Use [Azure Virtual Network Manager](/azure/virtual-network-manager/overview) to create new (and onboard existing) hub-and-spoke virtual network topologies for the central management of connectivity and security controls.

### Communication with privately networked clients in different regions

Frequently, customers have a need to connect to clients' different Azure regions. More specifically, this question typically boils down to how to connect two virtual networks (one of which has an Azure Database for PostgreSQL flexible server instance and another has an application client) that are in different regions.

There are multiple ways to achieve such connectivity, including:

- [Global virtual network peering](/azure/virtual-network/virtual-network-peering-overview). This methodology is the most common because it's the easiest way to connect networks in different regions together. Global virtual network peering creates a connection over the Azure backbone directly between the two peered virtual networks. This method provides the best network throughput and lowest latencies for connectivity. When virtual networks are peered, Azure also handles the routing automatically for you. These virtual networks can communicate with all resources in the peered virtual network that are established on a VPN gateway.
- [Network-to-network connection](/azure/vpn-gateway/vpn-gateway-howto-vnet-vnet-resource-manager-portal). A connection between virtual networks (network-to-network connection) is essentially a VPN between the two Azure locations. The network-to-network connection is established on a VPN gateway. Your traffic incurs two more traffic hops as compared to global virtual network peering. There's also extra latency and lower bandwidth as compared to that method.
- **Communication via network appliance in hub-and-spoke architecture.** Instead of connecting spoke virtual networks directly to each other, you can use network appliances to forward traffic between spokes. Network appliances provide more network services like deep packet inspection and traffic segmentation or monitoring, but they can introduce latency and performance bottlenecks if they're not properly sized.

### Replication across Azure regions and virtual networks with private networking

Database replication is the process of copying data from a central or primary server to multiple servers known as replicas. The primary server accepts read and write operations, but the replicas serve read-only transactions. The primary server and replicas collectively form a database cluster. The goal of database replication is to ensure redundancy, consistency, high availability, and accessibility of data, especially in high-traffic, mission-critical applications.

Azure Database for PostgreSQL offers two methods for replications: physical (that is, streaming) via the [built-in Read Replica feature](../read-replica/concepts-read-replicas.md) and [logical replication](../configure-maintain/concepts-logical.md). Both are ideal for different use cases, and a user might choose one over the other depending on the end goal.

Replication across Azure regions, with separate [virtual networks](/azure/virtual-network/virtual-networks-overview) in each region, requires connectivity across regional virtual network boundaries that can be provided via [virtual network peering](/azure/virtual-network/virtual-network-peering-overview) or in hub-and-spoke architectures via a network appliance.

By default, DNS name resolution is scoped to a virtual network. Any client in one virtual network (VNET1) is unable to resolve the Azure Database for PostgreSQL flexible server instance FQDN in another virtual network (VNET2).

To resolve this issue, you must make sure clients in VNET1 can access the Azure Database for PostgreSQL flexible server instance Private DNS zone. Add a [virtual network link](/azure/dns/private-dns-virtual-network-links) to the Private DNS zone of your Azure Database for PostgreSQL flexible server instance.

### Unsupported virtual network scenarios

Here are some limitations for working with virtual networks created via virtual network integration:

- After an Azure Database for PostgreSQL flexible server instance is deployed to a virtual network and subnet, you can't move it to another virtual network or subnet. You can't move the virtual network into another resource group or subscription.
- Subnet size (address spaces) can't be increased after resources exist in the subnet.
- Virtual network injected resources can't interact with Private Link by default. If you want to use [Private Link](/azure/private-link/private-link-overview) for private networking, see [Azure Database for PostgreSQL networking with Private Link](concepts-networking-private-link.md).

> [!IMPORTANT]
> Azure Resource Manager supports the ability to *lock* resources as a security control. Resource locks are applied to the resource and are effective across all users and roles. There are two types of resource lock: `CanNotDelete` and `ReadOnly`. These lock types can be applied either to a Private DNS zone or to an individual record set.
>
> Applying a lock of either type against a Private DNS zone or an individual record set might interfere with the ability of an Azure Database for PostgreSQL flexible server instance to update DNS records. It might also cause issues during important operations on DNS, such as high-availability failover from primary to secondary. For these reasons, make sure you *aren't* using a DNS private zone or record locks when you use high-availability features with an Azure Database for PostgreSQL flexible server instance.

## Host name

Regardless of the networking option that you choose, we recommend that you always use an FQDN as the host name when you connect to your Azure Database for PostgreSQL flexible server instance. The server's IP address isn't guaranteed to remain static. Using the FQDN helps you avoid making changes to your connection string.

An example that uses an FQDN as a host name is `hostname = servername.postgres.database.azure.com`. Where possible, avoid using `hostname = 10.0.0.4` (a private address) or `hostname = 40.2.45.67` (a public address).

## Related content

- [Azure portal](../network/how-to-networking.md)
- [Azure CLI](../network/how-to-networking.md)
