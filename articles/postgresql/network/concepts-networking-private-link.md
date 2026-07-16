---
title: Networking with Private Link Azure Database for PostgreSQL Flexible Server
description: Learn about connectivity and networking options for an Azure Database for PostgreSQL flexible server with Azure Private Link.
#customer intent: As a user, I want to set up private endpoints for my Azure Database for PostgreSQL flexible server, so that I can keep traffic off the public internet.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: concept-article
---

# Networking with Private Link in Azure Database for PostgreSQL flexible server

Azure Private Link enables you to create private endpoints for your Azure Database for PostgreSQL flexible server, bringing the server into your virtual network. This functionality is a recommended alternative to the [networking capabilities provided by virtual network integration](concepts-networking-private.md).

By using Private Link, traffic between your virtual network and the service travels over the Microsoft backbone network. You no longer need to expose your service to the public internet. You can create your own private link service in your virtual network and deliver it to your customers. Setup and consumption by using Private Link is consistent across Azure PaaS, customer-owned, and shared partner services.

Two Azure resource types expose Private Link to users:

- Private endpoints (Microsoft.Network/PrivateEndpoints)
- Private Link services (Microsoft.Network/PrivateLinkServices)

## Private endpoints

A *private endpoint* adds a network interface to a resource, giving it a private IP address assigned from your virtual network. After you apply it, you can communicate with this resource exclusively through the virtual network.
For a list of PaaS services that support Private Link functionality, see the Private Link [documentation](/azure/private-link/private-link-overview). A private endpoint is a private IP address within a specific [virtual network](/azure/virtual-network/virtual-networks-overview) and a subnet.

Multiple private endpoints in different virtual networks or subnets, even if they have overlapping address spaces, can reference the same public service.

## Key benefits of Private Link

Private Link provides the following benefits:

- **Privately access services on the Azure platform:** Connect your virtual network by using private endpoints to all services that you can use as application components in Azure. Service providers can render their services in their own virtual network. Consumers can access those services in their local virtual network. The Private Link platform handles the connectivity between the consumer and services over the Azure backbone network.
- **On-premises and peered networks:** Access services running in Azure from on-premises over Azure ExpressRoute private peering, virtual private network (VPN) tunnels, and peered virtual networks by using private endpoints. You don't need to configure ExpressRoute Microsoft peering or traverse the internet to reach the service. Private Link provides a secure way to migrate workloads to Azure.
- **Protection against data leakage:** A private endpoint maps to an instance of a PaaS resource instead of the entire service. Consumers can only connect to the specific resource. Access to any other resource in the service is blocked. This mechanism provides protection against data leakage risks.
- **Global reach: Connect privately to services running in other regions:** The consumer's virtual network can be in region A. It can connect to services behind Private Link in region B.

## Use cases for Private Link with Azure Database for PostgreSQL 

Clients can connect to the private endpoint from:

- The same virtual network.
- A peered virtual network in the same region or across regions.
- A [network-to-network connection](/azure/vpn-gateway/vpn-gateway-howto-vnet-vnet-resource-manager-portal) across regions.

Clients can also connect from on-premises by using ExpressRoute, private peering, or VPN tunneling. The following simplified diagram shows the common use cases.

:::image type="content" source="media/concepts-networking-private-link/show-private-link-overview.png" alt-text="Diagram that shows how Private Link works with private endpoints." lightbox="media/concepts-networking-private-link/show-private-link-overview.png":::

### Supported features for Private Link

Here's a cross-feature availability matrix for private endpoints in an Azure Database for PostgreSQL flexible server.

| Feature | Availability | Notes |
| --- | --- | --- |
| High availability | Yes | Works as designed. |
| Read replica | Yes | Works as designed. |
| Read replica with virtual endpoints | Yes | Works as designed. |
| Point-in-time restore | Yes | Works as designed. |
| Allowing also public/internet access with firewall rules | Yes | Works as designed. |
| Major version upgrade | Yes | Works as designed. |
| Microsoft Entra authentication | Yes | Works as designed. |
| Connection pooling with PGBouncer | Yes | Works as designed. |
| Private endpoint DNS | Yes | Works as designed and [documented](/azure/private-link/private-endpoint-dns). |
| Encryption with customer-managed keys | Yes | Works as designed. |

Private endpoints can only be configured for servers that you create after Azure Database for PostgreSQL introduces support for Private Link. You must configure the networking mode to not use virtual network integration but public access.

You can't configure private endpoints for servers that you created before that date if you configured the networking mode to not use virtual network integration but public access.
The use of private endpoints isn't currently supported on servers created with virtual network integration.

### Connect from an Azure VM in a peered virtual network

Configure [virtual network peering](/azure/virtual-network/tutorial-connect-virtual-networks-powershell) to establish connectivity to an Azure Database for PostgreSQL flexible server from an Azure virtual machine (VM) in a peered virtual network.

### Connect from an Azure VM in a network-to-network environment

Configure a [network-to-network VPN gateway](/azure/vpn-gateway/vpn-gateway-howto-vnet-vnet-resource-manager-portal) connection to establish connectivity to an Azure Database for PostgreSQL flexible server from an Azure VM in a different region or subscription.

### Connect from an on-premises environment over VPN

To connect from an on-premises environment to Azure Database for PostgreSQL flexible server, choose and implement one of the following options:

- [Point-to-site connection](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-rm-ps)
- [Site-to-site VPN connection](/azure/vpn-gateway/vpn-gateway-create-site-to-site-rm-powershell)
- [ExpressRoute circuit](/azure/expressroute/expressroute-howto-linkvnet-portal-resource-manager)

## Network security and Private Link

When you use private endpoints, you secure traffic to a *private-link resource*. The platform validates network connections and only allows connections that reach the specified private-link resource. To access more subresources within the same Azure service, you need more private endpoints with corresponding targets. For example, for Azure Storage, you need separate private endpoints to access the file and blob subresources.

Private endpoints provide a privately accessible IP address for the Azure service but don't necessarily restrict public network access to it. All other Azure services require another [access control](/azure/event-hubs/event-hubs-ip-filtering). These controls provide an extra network security layer to your resources, helping prevent access to the Azure service associated with the private-link resource.

Private endpoints support network policies. Network policies enable support for network security groups (NSGs), user-defined routes (UDRs), and application security groups (ASGs). For more information about enabling network policies for a private endpoint, see [Manage network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy). To use an ASG with a private endpoint, see [Configure an application security group with a private endpoint](/azure/private-link/configure-asg-private-endpoint).

## Private Link and DNS

When you use a private endpoint, you need to connect to the same Azure service but use the private endpoint IP address. The private endpoint connection requires separate domain name system (DNS) settings to resolve the private IP address to the resource name.

[Private DNS zones](/azure/dns/private-dns-overview) provide domain name resolution within a virtual network without a custom DNS solution. You link the private DNS zones to each virtual network to provide DNS services to that network.

Private DNS zones provide separate DNS zone names for each Azure service. For example, if you configured a Private DNS zone for the storage account blob service in the previous image, the DNS zone name is `privatelink.blob.core.windows.net`. Review the Microsoft documentation to see more of the private DNS zone names for all Azure services.

> [!NOTE]  
> Private endpoint Private DNS zone configurations automatically generate only if you use the recommended naming scheme: `privatelink.postgres.database.azure.com`.
> On newly provisioned public access (not virtual network integrated) servers, there's a change in the DNS layout. The server's FQDN now becomes a CNAME record in the form `servername.postgres.database.azure.com` which points to an A record in one of the following formats:
> 1. If the server has a private endpoint with a default private DNS zone linked, the A record uses this format: `server_name.privatelink.postgres.database.azure.com`.
> 1. If the server doesn't have private endpoints, the A record uses this format: `server_name.rs-<15 semi-random bytes>.postgres.database.azure.com`.

### Hybrid DNS for Azure and on-premises resources

DNS is a critical design consideration in the overall landing zone architecture. Some organizations might want to use their existing investments in DNS. Others might want to adopt native Azure capabilities for all their DNS needs.

You can use [Azure DNS Private Resolver](/azure/dns/dns-private-resolver-overview) along with Azure Private DNS zones for cross-premises name resolution. DNS Private Resolver can forward a DNS request to another DNS server and also provides an IP address that an external DNS server can use to forward requests. So, external on-premises DNS servers can resolve names located in a Private DNS zone.

For more information about using DNS Private Resolver with an on-premises DNS forwarder to forward DNS traffic to Azure DNS, see:

- [Azure private endpoint DNS integration](/azure/private-link/private-endpoint-dns-integration#on-premises-workloads-using-a-dns-forwarder)
- [Create a private endpoint DNS infrastructure with Azure Private Resolver for an on-premises workload](/azure/private-link/tutorial-dns-on-premises-private-resolver)

The described solutions extend an on-premises network that already has a DNS solution in place to resolve resources in `Azure.Microsoft` architecture.

### Private Link and DNS integration in hub-and-spoke network architectures

You typically host private DNS zones centrally in the same Azure subscription where you deploy the hub virtual network. This central hosting practice is driven by cross-premises DNS name resolution and other needs for central DNS resolution, such as Microsoft Entra. In most cases, only networking and identity administrators have permissions to manage DNS records in the zones.

In such architecture, you configure the following components:

- On-premises DNS servers have conditional forwarders configured for each private endpoint public DNS zone, pointing to the Private DNS Resolver hosted in the hub virtual network.
- The Private DNS Resolver hosted in the hub virtual network uses the Azure-provided DNS (168.63.129.16) as a forwarder.
- You link the hub virtual network to the Private DNS zone names for Azure services (such as `privatelink.postgres.database.azure.com`, for an Azure Database for PostgreSQL flexible server).
- All Azure virtual networks use the Private DNS Resolver hosted in the hub virtual network.
- The Private DNS Resolver isn't authoritative for a customer's corporate domains because it's just a forwarder (for example, Microsoft Entra domain names). It should have outbound endpoint forwarders to the customer's corporate domains, pointing to the on-premises DNS servers, or DNS servers deployed in Azure that are authoritative for such zones.

## Private Link and network security groups

By default, network policies are disabled for a subnet in a virtual network. To use network policies like UDRs and NSGs support, you must enable network policy support for the subnet. This setting applies only to private endpoints within the subnet. This setting affects all private endpoints within the subnet. For other resources in the subnet, access is controlled based on security rules in the NSG.

You can enable network policies for NSGs only, for UDRs only, or for both. For more information, see [Manage network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy?tabs=network-policy-portal).

Limitations to NSGs and private endpoints are listed in [What is a private endpoint?](/azure/private-link/private-endpoint-overview).

> [!IMPORTANT]  
> Protection against data leakage: A private endpoint is mapped to an instance of a PaaS resource instead of the entire service. Consumers can only connect to the specific resource. Access to any other resource in the service is blocked. This mechanism provides basic protection against data leakage risks.

## Private Link combined with firewall rules

The following situations and outcomes are possible when you use Private Link in combination with firewall rules:

- If you don't configure any firewall rules, by default, traffic can't access the Azure Database for PostgreSQL flexible server.

- If you configure public traffic or a service endpoint and you create private endpoints, different types of incoming traffic are authorized by the corresponding type of firewall rule.

- If you don't configure any public traffic or service endpoint and you create private endpoints, the Azure Database for PostgreSQL flexible server is accessible only through private endpoints. If you don't configure public traffic or a service endpoint, after all approved private endpoints are rejected or deleted, no traffic can access the Azure Database for PostgreSQL flexible server.

## Troubleshoot

When you use Private Link endpoints with an Azure Database for PostgreSQL flexible server, connectivity issues might occur due to misconfigurations or network constraints. To troubleshoot these issues, verify the setup of private endpoints, DNS configurations, network security groups (NSGs), and route tables. Systematically addressing these areas can help you identify and resolve common problems, ensuring seamless connectivity and secure access to your database.

### Connectivity problems with private endpoint-based networking

If you experience connectivity problems when using private endpoint-based networking, check the following areas:

- **Verify IP address assignments:** Make sure the private endpoint has the correct IP address assigned and that it doesn't conflict with other resources. For more information about private endpoints and IP, see [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint).
- **Check NSGs:** Review the NSG rules for the private endpoint's subnet to ensure the necessary traffic is allowed and there are no conflicting rules. For more information about NSGs, see [Network security groups](/azure/virtual-network/network-security-groups-overview).
- **Validate route table configuration:** Ensure that the route tables associated with the private endpoint's subnet and the connected resources are correctly configured with the appropriate routes.
- **Use network monitoring and diagnostics:** Use Azure Network Watcher to monitor and diagnose network traffic by using tools like Connection Monitor or Packet Capture. For more information about network diagnostics, see [What is Azure Network Watcher?](/azure/network-watcher/network-watcher-overview).

For more information about troubleshooting private endpoints, see [Troubleshoot Azure private endpoint connectivity problems](/azure/private-link/troubleshoot-private-endpoint-connectivity).

### DNS resolution with private endpoint-based networking

If you experience DNS resolution problems when using private endpoint-based networking, check the following areas:

- **Validate DNS resolution:** Check if the DNS server or service used by the private endpoint and the connected resources is functioning correctly. Ensure that the private endpoint's DNS settings are accurate. For more information about private endpoints and DNS zone settings, see [Azure private endpoint Private DNS zone values](/azure/private-link/private-endpoint-dns).
- **Clear the DNS cache:** Clear the DNS cache on the private endpoint or client machine to ensure the latest DNS information is retrieved and to avoid inconsistent errors.
- **Analyze DNS logs:** Review DNS logs for error messages or unusual patterns, such as DNS query failures, server errors, or timeouts. For more information about DNS metrics, see [Azure DNS metrics and alerts](/azure/dns/dns-alerts-metrics).

## Limitations and considerations

- You can only configure private endpoints for servers created after the introduction of Private Link. Servers that use virtual network (VNet) integration aren't eligible for private endpoint configuration.

- Azure networking constraints, not the database service itself, limit the number of private endpoints. Specifically, they limit the number of private endpoints that you can inject into a given subnet within a VNet.

- Virtual machines can connect to the database through private endpoints, provided they're correctly configured within the same virtual network or have appropriate routing in place.

## Related content

- [Azure portal](../network/how-to-networking.md)
- [Azure CLI](../network/how-to-networking.md)
