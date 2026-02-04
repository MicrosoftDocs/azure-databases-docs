---
title: "Networking Scenarios for the Migration Service"
titleSuffix: Azure Database for PostgreSQL flexible server
description: Learn about network scenarios for connecting supported source environments with Azure Database for PostgreSQL flexible server.
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Network scenarios for the migration service in Azure Database for PostgreSQL

This article outlines various scenarios for connecting a source database to an Azure Database for PostgreSQL flexible server by using the migration service in Azure Database for PostgreSQL. Each scenario has different networking requirements and configurations to successfully establish a connection for migration. Specific details vary based on the actual network setup and requirements of the source environment and the target environment.

The following table summarizes the migration scenarios. The table indicates whether each scenario is supported based on the configurations of the source and target environments.

| PostgreSQL source | Target | Supported |
| --- | --- | --- |
| On-premises with a public IP address | Azure Database for PostgreSQL flexible server with public access | Yes |
| On-premises with a private IP address via a virtual private network (VPN) or Azure ExpressRoute | Virtual network (VNet)-integrated Azure Database for PostgreSQL flexible server | Yes |
| Amazon Relational Database Service (Amazon RDS) for PostgreSQL or Amazon Aurora PostgreSQL with a public IP address | Azure Database for PostgreSQL flexible server with public access | Yes |
| Amazon RDS for PostgreSQL or Amazon Aurora PostgreSQL with private access via a VPN or ExpressRoute | VNet-integrated Azure Database for PostgreSQL flexible server | Yes |
| Google Cloud SQL for PostgreSQL | Azure Database for PostgreSQL flexible server with public access | Yes |
| Google Cloud SQL for PostgreSQL with private access via a VPN or ExpressRoute | VNet-integrated Azure Database for PostgreSQL flexible server | Yes |
| PostgreSQL installed on an Azure virtual machine (VM) in the same virtual network or in a different virtual network | VNet-integrated Azure Database for PostgreSQL flexible server in the same virtual network or in a different virtual network | Yes |
| PostgreSQL sources with private access | Azure Database for PostgreSQL flexible server with a private endpoint | Yes |
| PostgreSQL sources with private access | Azure Database for PostgreSQL flexible server with public access | No |

## On-premises (public IP) to flexible server (public access)

Networking steps:

1. Ensure that the source database server has a public IP address.
1. Configure the firewall to allow outbound connections on the PostgreSQL port (the default port is 5432).
1. Ensure that the source database server is accessible over the internet.
1. Test the setup by verifying connectivity from the target instance of Azure Database for PostgreSQL to the source database. Confirm that the migration service can access the source data.

## On-premises (private IP) to VNet-integrated flexible server (ExpressRoute or VPN)

:::image type="content" source="media/how-to-network-setup-migration-service/on-premises-to-azure-vpn.png" alt-text="Screenshot of an on-premises datacenter connected to Azure via ExpressRoute or Azure VPN Gateway. The on-premises PostgreSQL server connects through the secure link to Azure Database for PostgreSQL." lightbox="media/how-to-network-setup-migration-service/on-premises-to-azure-vpn.png":::

Networking steps:

1. Set up a site-to-site VPN or an ExpressRoute instance for a secure, reliable connection between the on-premises network and Azure.
1. Configure the Azure virtual network to allow access from the on-premises IP address range.
1. Set up network security group rules to allow traffic on the PostgreSQL port (the default port is 5432) from the on-premises network.
1. Test the setup by verifying connectivity from the target instance of Azure Database for PostgreSQL to the source database. Confirm that the migration service can access the source data.

## Managed PostgreSQL service (public IP) to flexible server (public/private access)

:::image type="content" source="media/how-to-network-setup-migration-service/aws-to-azure-vpn.png" alt-text="Screenshot of a PostgreSQL database from managed services (for example, from Amazon or Google) connecting to Azure Database for PostgreSQL via internet or private methods." lightbox="media/how-to-network-setup-migration-service/aws-to-azure-vpn.png":::

The source PostgreSQL instance in a cloud provider (for example, AWS or GCP) must have a public IP address or a direct connection to Azure.

Networking steps:

- **Public access**

  1. If your PostgreSQL instance in Amazon Web Services (AWS), Google Cloud Platform (GCP), or another managed PostgreSQL service isn't publicly accessible, modify the instance to allow connections from Azure. In the cloud provider's console (for example, in AWS Management Console or the Google Cloud console), change the setting to allow public accessibility.
  1. In the cloud provider's security settings (for example, in security groups in AWS or in firewall rules in GCP), add an inbound rule to allow traffic from the Azure Database for PostgreSQL public IP address or domain.

- **Private access**

  1. Establish a secure connection by using ExpressRoute, IPsec VPN, or an equivalent private connection service from the cloud provider (Azure ExpressRoute, AWS Direct Connect, GCP Interconnect) to Azure.
  1. In the source cloud provider's security settings (for example, AWS security groups or GCP firewall rules), add an inbound rule to allow traffic from the Azure Database for PostgreSQL public IP address or domain, or from the IP address range of the Azure virtual network on the PostgreSQL port (the default port is 5432).
  1. Create a virtual network in Azure in the same region as your instance of Azure Database for PostgreSQL. Set up the network security group to allow outbound connections to the source cloud provider's PostgreSQL instance's IP address on the default port 5432.
  1. Set up network security group rules in Azure to permit incoming connections from the cloud provider (for example, from AWS or GCP) to the Azure Database for PostgreSQL IP address range.
  1. Test the connectivity between your PostgreSQL instance in the managed PostgreSQL service (for example, in AWS, GCP, or Heroku) and Azure Database for PostgreSQL to ensure that no network issues occur.

## Azure VM (private access) to Azure Database for PostgreSQL (different virtual networks)

This scenario describes connectivity between an instance of Azure Virtual Machines and an Azure Database for PostgreSQL flexible server that are in different virtual networks. Virtual network peering and appropriate network security group rules are required to facilitate traffic between the VNets.

:::image type="content" source="media/how-to-network-setup-migration-service/vm-to-azure-peering.png" alt-text="Screenshot of an Azure VM in one virtual network connects to Azure Database for PostgreSQL in another virtual network." lightbox="media/how-to-network-setup-migration-service/vm-to-azure-peering.png":::

Networking steps:

1. Set up virtual network peering between the two VNets to enable direct network connectivity.
1. Configure network security group rules to allow traffic between the VNets on the PostgreSQL port.

## Azure VM to Azure Database for PostgreSQL (same virtual network)

Configuration is straightforward when an Azure VM and an Azure Database for PostgreSQL flexible server are in the same virtual network. Set network security group rules to allow internal traffic on the PostgreSQL port. No other firewall rules are necessary because the traffic remains in the virtual network.

:::image type="content" source="media/how-to-network-setup-migration-service/vm-to-azure-same-vnet.png" alt-text="Screenshot of an Azure VM in the same virtual network connects directly to the instance of Azure Database for PostgreSQL." lightbox="media/how-to-network-setup-migration-service/vm-to-azure-same-vnet.png":::

Networking steps:

1. Ensure that the VM and the PostgreSQL server are in the same virtual network.
1. Configure network security group rules to allow traffic within the virtual network on the PostgreSQL port.

## PostgreSQL source (private IP) to flexible server (private endpoint)

This section describes the networking steps to migrate a PostgreSQL database from a cloud-based PostgreSQL service, an on-premises setup, or a VM, all with private IP addresses, to an Azure Database for PostgreSQL flexible server that is secured with a private endpoint. The migration ensures secure data transfer within a private network space by using an Azure VPN or ExpressRoute for on-premises connections and virtual network peering or a VPN for cloud-to-cloud migrations. For more information, see [Migration runtime server](concepts-migration-service-runtime-server.md).

- Establish network connectivity:

  1. For on-premises sources, set up a site-to-site VPN or set up ExpressRoute to connect your local network to Azure's virtual network.
  1. For an Azure VM or an Amazon instance or a Google Compute Engine, ensure that virtual network peering, a VPN gateway, or an instance of ExpressRoute is in place for secure connectivity to Azure's virtual network.

- Gather VNet details for the migration runtime server:

  1. In the Azure portal, go to the migration runtime server. That is, go to the instance of VNet-integrated Azure Database for PostgreSQL flexible server.
  1. Record the virtual network and subnet details that are listed under the virtual network.

- Assess VNet peering requirements:

  1. Enable virtual network peering if the servers are in different VNets. No peering is needed if the servers are in the same virtual network but in different subnets.
  1. Ensure that no network security groups block traffic between the source server, the migration runtime server, and the target server.

- Private DNS zone configuration:

  1. On the **Networking** pane of the migration runtime server, confirm that a private DNS zone is in use.
  1. Ensure that both the VNets for the source and the target flexible server are linked to the private DNS zone of the migration runtime server.
  1. Attach a private DNS zone to the flexible server's private endpoint if it's not already configured.
  1. Add virtual network links for the flexible server and for the migration runtime server to the private DNS zone.

Alternatively, when a custom DNS server or custom DNS namespaces are in use, you can use the custom FQDN/IP field instead of linking a private DNS zone. This setup allows you to directly resolve FQDNs or IPs without requiring private DNS zone integration.

## Related content

- [What is Azure ExpressRoute?](/azure/expressroute/expressroute-introduction)
- [About point-to-site VPNs](/azure/vpn-gateway/point-to-site-about)
- [virtual network peering](/azure/virtual-network/virtual-network-peering-overview)
- [migration service](concepts-migration-service-postgresql.md)
- [known issues and limitations](concepts-known-issues-migration-service.md)
- [premigration validations](concepts-premigration-migration-service.md)
