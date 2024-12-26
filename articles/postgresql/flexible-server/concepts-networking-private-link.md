---
title: Networking overview with Private Link connectivity
description: Learn about connectivity and networking options for Azure Database for PostgreSQL - Flexible Server with Private Link.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 09/20/2024
ms.service: azure-database-postgresql
ms.subservice: 
ms.topic: conceptual
ms.custom:
  - ignite-2023
---

# Azure Database for PostgreSQL - Flexible Server networking with Private Link

Azure Private Link allows you to create private endpoints for Azure Database for PostgreSQL - Flexible Server to bring it inside your virtual network. That functionality is introduced in addition to already [existing networking capabilities provided by virtual network integration](concepts-networking-private.md), which is currently in general availability with Azure Database for PostgreSQL - Flexible Server.

With Private Link, traffic between your virtual network and the service travels the Microsoft backbone network. Exposing your service to the public internet is no longer necessary. You can create your own private link service in your virtual network and deliver it to your customers. Setup and consumption by using Private Link is consistent across Azure PaaS, customer-owned, and shared partner services.

> [!NOTE]  
> Private links are available only for servers that have public access networking. They can't be created for servers that have private access (virtual network integration).
> 
> Private links can be configured only for servers that were created after the release of this feature. Any server that existed before the release of the feature can't be set with private links.

Private Link is exposed to users through two Azure resource types:

- Private endpoints (Microsoft.Network/PrivateEndpoints)
- Private Link services (Microsoft.Network/PrivateLinkServices)

## Private endpoints

A *private endpoint* adds a network interface to a resource, providing it with a private IP address assigned from your virtual network. After it's applied, you can communicate with this resource exclusively via the virtual network.
For a list to PaaS services that support Private Link functionality, review the Private Link [documentation](/azure/private-link/private-link-overview). A private endpoint is a private IP address within a specific [virtual network](/azure/virtual-network/virtual-networks-overview) and a subnet.

The same public service instance can be referenced by multiple private endpoints in different virtual networks or subnets, even if they have overlapping address spaces.

## Key benefits of Private Link

Private Link provides the following benefits:

- **Privately access services on the Azure platform:** Connect your virtual network by using private endpoints to all services that can be used as application components in Azure. Service providers can render their services in their own virtual network. Consumers can access those services in their local virtual network. The Private Link platform handles the connectivity between the consumer and services over the Azure backbone network.
- **On-premises and peered networks:** Access services running in Azure from on-premises over Azure ExpressRoute private peering, virtual private network (VPN) tunnels, and peered virtual networks by using private endpoints. There's no need to configure ExpressRoute Microsoft peering or traverse the internet to reach the service. Private Link provides a secure way to migrate workloads to Azure.
- **Protection against data leakage:** A private endpoint is mapped to an instance of a PaaS resource instead of the entire service. Consumers can only connect to the specific resource. Access to any other resource in the service is blocked. This mechanism provides protection against data leakage risks.
- **Global reach: Connect privately to services running in other regions:** The consumer's virtual network could be in region A. It can connect to services behind Private Link in region B.

## Use cases for Private Link with Azure Database for PostgreSQL - Flexible Server

Clients can connect to the private endpoint from:

- The same virtual network.
- A peered virtual network in the same region or across regions.
- A [network-to-network connection](/azure/vpn-gateway/vpn-gateway-howto-vnet-vnet-resource-manager-portal) across regions.

Clients can also connect from on-premises by using ExpressRoute, private peering, or VPN tunneling. The following simplified diagram shows the common use cases.

:::image type="content" source="./media/concepts-networking/show-private-link-overview.png" alt-text="Diagram that shows how Private Link works with private endpoints." lightbox="./media/concepts-networking/show-private-link-overview.png":::

### Limitations and supported features for Private Link with Azure Database for PostgreSQL - Flexible Server

Here's a cross-feature availability matrix for private endpoints in Azure Database for PostgreSQL - Flexible Server.

| Feature | Availability | Notes |
| --- | --- | --- |
| High availability  | Yes |Works as designed. |
| Read replica | Yes | Works as designed. |
| Read replica with virtual endpoints|Yes| Works as designed. |
| Point-in-time restore  | Yes | Works as designed. |
| Allowing also public/internet access with firewall rules | Yes | Works as designed.|
| Major version upgrade  | Yes | Works as designed. |
| Microsoft Entra authentication  | Yes | Works as designed. |
| Connection pooling with PGBouncer | Yes | Works as designed. |
| Private endpoint DNS | Yes | Works as designed and [documented](/azure/private-link/private-endpoint-dns). |
| Encryption with customer-managed keys | Yes| Works as designed.|

### Connect from an Azure VM in a peered virtual network

Configure [virtual network peering](/azure/virtual-network/tutorial-connect-virtual-networks-powershell) to establish connectivity to Azure Database for PostgreSQL - Flexible Server from an Azure virtual machine (VM) in a peered virtual network.

### Connect from an Azure VM in a network-to-network environment

Configure a [network-to-network VPN gateway](/azure/vpn-gateway/vpn-gateway-howto-vnet-vnet-resource-manager-portal) connection to establish connectivity to an Azure Database for PostgreSQL flexible server from an Azure VM in a different region or subscription.

### Connect from an on-premises environment over VPN

To establish connectivity from an on-premises environment to the Azure Database for PostgreSQL flexible server, choose and implement one of the options:

- [Point-to-site connection](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-rm-ps)
- [Site-to-site VPN connection](/azure/vpn-gateway/vpn-gateway-create-site-to-site-rm-powershell)
- [ExpressRoute circuit](/azure/expressroute/expressroute-howto-linkvnet-portal-resource-manager)

## Network security and Private Link

When you use private endpoints, traffic is secured to a *private-link resource*. The platform validates network connections, allowing only those connections that reach the specified private-link resource. To access more subresources within the same Azure service, more private endpoints with corresponding targets are required. In the case of Azure Storage, for instance, you would need separate private endpoints to access the file and blob subresources.

Private endpoints provide a privately accessible IP address for the Azure service but don't necessarily restrict public network access to it. All other Azure services require another [access control](/azure/event-hubs/event-hubs-ip-filtering), however. These controls provide an extra network security layer to your resources, providing protection that helps prevent access to the Azure service associated with the private-link resource.

Private endpoints support network policies. Network policies enable support for network security groups (NSGs), user-defined routes (UDRs), and application security groups (ASGs). For more information about enabling network policies for a private endpoint, see [Manage network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy). To use an ASG with a private endpoint, see [Configure an application security group with a private endpoint](/azure/private-link/configure-asg-private-endpoint).

## Private Link and DNS

When you use a private endpoint, you need to connect to the same Azure service but use the private endpoint IP address. The intimate endpoint connection requires separate domain name system (DNS) settings to resolve the private IP address to the resource name.

[Private DNS zones](/azure/dns/private-dns-overview) provide domain name resolution within a virtual network without a custom DNS solution. You link the private DNS zones to each virtual network to provide DNS services to that network.

Private DNS zones provide separate DNS zone names for each Azure service. For example, if you configured a Private DNS zone for the storage account blob service in the previous image, the DNS zone name is `privatelink.blob.core.windows.net`. Review the Microsoft documentation to see more of the private DNS zone names for all Azure services.

> [!NOTE]
> Private endpoint Private DNS zone configurations automatically generate only if you use the recommended naming scheme: `privatelink.postgres.database.azure.com`.
> On newly provisioned public access (non-virtual network injected) servers, there will be a change in DNS layout. The server's FQDN now becomes a CName record in the form `servername.postgres.database.azure.com` which will point to an A record in one of the following formats:
>  1. If the server has a Private Endpoint with a default private dns zone linked, the A record will be in this format: `server_name.privatelink.postgres.database.azure.com`.
>  2. If the server has no Private Endpoints then the A record will be in this format `server_name.rs-<15 semi-random bytes>.postgres.database.azure.com`.

### Hybrid DNS for Azure and on-premises resources

DNS is a critical design topic in the overall landing zone architecture. Some organizations might want to use their existing investments in DNS. Others might want to adopt native Azure capabilities for all their DNS needs.

You can use [Azure DNS Private Resolver](/azure/dns/dns-private-resolver-overview) along with Azure Private DNS zones for cross-premises name resolution. DNS Private Resolver can forward a DNS request to another DNS server and also provides an IP address that can be used by an external DNS server to forward requests. So, external on-premises DNS servers are able to resolve names located in a Private DNS zone.

For more information on using DNS Private Resolver with an on-premises DNS forwarder to forward DNS traffic to Azure DNS, see:

- [Azure private endpoint DNS integration](/azure/private-link/private-endpoint-dns-integration#on-premises-workloads-using-a-dns-forwarder)
- [Create a private endpoint DNS infrastructure with Azure Private Resolver for an on-premises workload](/azure/private-link/tutorial-dns-on-premises-private-resolver)

The described solutions extend an on-premises network that already has a DNS solution in place to resolve resources in `Azure.Microsoft` architecture.

### Private Link and DNS integration in hub-and-spoke network architectures

Private DNS zones are typically hosted centrally in the same Azure subscription where the hub virtual network deploys. This central hosting practice is driven by cross-premises DNS name resolution and other needs for central DNS resolution, such as Microsoft Entra. In most cases, only networking and identity administrators have permissions to manage DNS records in the zones.

In such architecture, the following components are configured:

* On-premises DNS servers have conditional forwarders configured for each private endpoint public DNS zone, pointing to the Private DNS Resolver hosted in the hub virtual network.
* The Private DNS Resolver hosted in the hub virtual network uses the Azure-provided DNS (168.63.129.16) as a forwarder.
* The hub virtual network must be linked to the Private DNS zone names for Azure services (such as `privatelink.postgres.database.azure.com`, for Azure Database for PostgreSQL - Flexible Server).
* All Azure virtual networks use Private DNS Resolver hosted in the hub virtual network.
* The Private DNS Resolver isn't authoritative for a customer's corporate domains because it's just a forwarder (for example, Microsoft Entra domain names), it should have outbound endpoint forwarders to the customer's corporate domains, pointing to the on-premises DNS servers or DNS servers deployed in Azure that are authoritative for such zones.

## Private Link and network security groups

By default, network policies are disabled for a subnet in a virtual network. To utilize network policies like UDRs and NSGs support, you must enable network policy support for the subnet. This setting is applicable only to private endpoints within the subnet. This setting affects all private endpoints within the subnet. For other resources in the subnet, access is controlled based on security rules in the NSG.

You can enable network policies for NSGs only, for UDRs only, or for both. For more information, see [Manage network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy?tabs=network-policy-portal).

Limitations to NSGs and private endpoints are listed in [What is a private endpoint?](/azure/private-link/private-endpoint-overview).

 > [!IMPORTANT]
 > Protection against data leakage: A private endpoint is mapped to an instance of a PaaS resource instead of the entire service. Consumers can only connect to the specific resource. Access to any other resource in the service is blocked. This mechanism provides basic protection against data leakage risks.

## Private Link combined with firewall rules

The following situations and outcomes are possible when you use Private Link in combination with firewall rules:

- If you don't configure any firewall rules, by default, traffic can't access the Azure Database for PostgreSQL flexible server.

- If you configure public traffic or a service endpoint and you create private endpoints, different types of incoming traffic are authorized by the corresponding type of firewall rule.

- If you don't configure any public traffic or service endpoint and you create private endpoints, the Azure Database for PostgreSQL flexible server is accessible only through private endpoints. If you don't configure public traffic or a service endpoint, after all approved private endpoints are rejected or deleted, no traffic can access the Azure Database for PostgreSQL flexible server.

## Troubleshoot connectivity issues with private endpoint-based networking

If you have connectivity issues when you use private endpoint-based networking, check the following areas:

- **Verify IP address assignments:** Check that the private endpoint has the correct IP address assigned and that there are no conflicts with other resources. For more information on private endpoints and IP, see [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint).
- **Check NSGs:** Review the NSG rules for the private endpoint's subnet to ensure the necessary traffic is allowed and doesn't have conflicting rules. For more information on NSGs, see [Network security groups](/azure/virtual-network/network-security-groups-overview).
- **Validate route table configuration:** Ensure that the route tables associated with the private endpoint's subnet and the connected resources are correctly configured with the appropriate routes.
- **Use network monitoring and diagnostics:** Use Azure Network Watcher to monitor and diagnose network traffic by using tools like Connection Monitor or Packet Capture. For more information on network diagnostics, see [What is Azure Network Watcher?](/azure/network-watcher/network-watcher-overview).

More information on troubleshooting private endpoints is also available in [Troubleshoot Azure private endpoint connectivity problems](/azure/private-link/troubleshoot-private-endpoint-connectivity).

## Troubleshoot DNS resolution with private endpoint-based networking

 If you have DNS resolution issues when you use private endpoint-based networking, check the following areas:

- **Validate DNS resolution:** Check if the DNS server or service used by the private endpoint and the connected resources is functioning correctly. Ensure that the private endpoint's DNS settings are accurate. For more information on private endpoints and DNS zone settings, see [Azure private endpoint Private DNS zone values](/azure/private-link/private-endpoint-dns).
- **Clear the DNS cache:** Clear the DNS cache on the private endpoint or client machine to ensure the latest DNS information is retrieved and to avoid inconsistent errors.
- **Analyze DNS logs:** Review DNS logs for error messages or unusual patterns, such as DNS query failures, server errors, or timeouts. For more on DNS metrics, see [Azure DNS metrics and alerts](/azure/dns/dns-alerts-metrics).

## Related content

Learn how to create an Azure Database for PostgreSQL flexible server by using the **Private access (VNet integration)** option in the [Azure portal](how-to-manage-virtual-network-portal.md) or the [Azure CLI](how-to-manage-virtual-network-cli.md).
