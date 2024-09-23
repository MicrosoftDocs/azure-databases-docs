---
title: "Networking scenarios in the migration service"
titleSuffix: Azure Database for PostgreSQL - Flexible Server
description: Network scenarios for connecting source and target
author: apduvuri
ms.author: adityaduvuri
ms.reviewer: maghan
ms.date: 09/11/2024
ms.service: azure-database-postgresql
ms.topic: how-to
---

# Network guide for migration service in Azure Database for PostgreSQL

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article outlines various scenarios for connecting a source database to an instance of Azure Database for PostgreSQL by using the migration service in Azure Database for PostgreSQL. Each scenario has different networking requirements and configurations to establish a successful connection for migration. Specific details vary based on the actual network setup and requirements of the source environment and the target environment.

The following table summarizes the migration scenarios. It indicates whether each scenario is supported based on the configurations of the source and target environments.

| PostgreSQL source | Target | Supported |
| --- | --- | --- |
| On-premises with a public IP address | Azure Database for PostgreSQL - Flexible Server with public access | Yes |
| On-premises with a private IP address via a virtual private network (VPN) or Azure ExpressRoute | Virtual network (VNet)-integrated Azure Database for PostgreSQL - Flexible Server | Yes |
| Amazon Relational Database Service (Amazon RDS) for PostgreSQL or Amazon Aurora PostgreSQL with a public IP address | Azure Database for PostgreSQL - Flexible Server with public access | Yes |
| Amazon RDS for PostgreSQL or Amazon Aurora PostgreSQL with private access via a VPN or ExpressRoute | VNet-integrated Azure Database for PostgreSQL - Flexible Server | Yes |
| Google Cloud SQL for PostgreSQL | Azure Database for PostgreSQL - Flexible Server with public access | Yes |
| Google Cloud SQL for PostgreSQL with private access via a VPN or ExpressRoute | VNet-integrated Azure Database for PostgreSQL - Flexible Server | Yes |
| PostgreSQL installed on an Azure virtual machine (VM) in the same or in a different virtual network | VNet-integrated Azure Database for PostgreSQL - Flexible Server in the same or in a different virtual network | Yes |
| Azure Database for PostgreSQL - Single Server with public access | VNet-integrated Azure Database for PostgreSQL - Flexible Server | Yes |
| Azure Database for PostgreSQL - Single Server with a private endpoint | VNet-integrated Azure Database for PostgreSQL - Flexible Server | Yes |
| Azure Database for PostgreSQL - Single Server with a private endpoint | Azure Database for PostgreSQL - Flexible Server with a private endpoint | Yes |
| PostgreSQL sources with private access | Azure Database for PostgreSQL - Flexible Server with private endpoint | Yes |
| PostgreSQL sources with private access | Azure Database for PostgreSQL - Flexible Server with public access | No |

## Scenario 1: On-premises source to Azure Database for PostgreSQL with public access

**Networking steps:**

1. Ensure that the source database server has a public IP address.
1. Configure the firewall to allow outbound connections on the PostgreSQL port (the default port is 5432).
1. Ensure that the source database server is accessible over the internet.
1. Verify the network configuration by testing connectivity from the target instance of Azure Database for PostgreSQL to the source database. Confirm that the migration service can access the source data.

## Scenario 2: Private IP address on-premises source to a VNet-integrated instance of Azure Database for PostgreSQL via ExpressRoute or an IPSec VPN

:::image type="content" source="media/how-to-network-setup-migration-service/on-premises-to-azure-vpn.png" alt-text="Screenshot of an on-premises data center connected to Azure via ExpressRoute or Azure VPN Gateway, with the on-premises PostgreSQL server connecting through the secure link to the Azure Database for PostgreSQL." lightbox="media/how-to-network-setup-migration-service/on-premises-to-azure-vpn.png":::

**Networking steps:**

1. Set up a site-to-site VPN or ExpressRoute instance for a secure, reliable connection between the on-premises network and Azure.
1. Configure Azure's Virtual Network (virtual network) to allow access from the on-premises IP range.
1. Set up Network Security Group (NSG) rules to allow traffic on the PostgreSQL port (default 5432) from the on-premises network.
1. Verify the network configuration by testing connectivity from the target Azure Database for PostgreSQL to the source database, confirming that the migration service can access the source data.

## Scenario 3: Managed PostgreSQL Services (AWS/GCP) to Azure Database for PostgreSQL

:::image type="content" source="media/how-to-network-setup-migration-service/aws-to-azure-vpn.png" alt-text="Screenshot of a PostgreSQL database from managed services (AWS, GCP, etc.) connecting to Azure Database for PostgreSQL via internet or private methods." lightbox="media/how-to-network-setup-migration-service/aws-to-azure-vpn.png":::

The source PostgreSQL instance in a cloud provider (AWS, GCP, etc.) must have a public IP or a direct connection to Azure.

**Networking steps:**

- **Public access**

  1. If your PostgreSQL instance in AWS, GCP, or other managed PostgreSQL services isn't publicly accessible, modify the instance to allow connections from Azure. This can be done by changing the Publicly Accessible setting to Yes within the respective cloud provider's console (e.g., AWS Management Console, GCP Console).
  1. In the cloud provider's security settings (e.g., security groups in AWS or firewall rules in GCP), add an inbound rule to allow traffic from Azure Database for PostgreSQL's public IP address/domain.

- **Private access**

  1. Establish a secure connection using ExpressRoute, IPSec VPN, or equivalent private connection services from the cloud provider (e.g., Azure Express route, AWS Direct Connect, GCP Interconnect) to Azure.
  1. In the source cloud provider's security settings (AWS security groups, GCP firewall rules), add an inbound rule to allow traffic from Azure Database for PostgreSQL's public IP address/domain or the IP range of the Azure virtual network on the PostgreSQL port (default 5432).
  1. Create an Azure Virtual Network where your Azure Database for PostgreSQL resides. Configure the Network Security Group (NSG) to allow outbound connections to the source cloud provider’s PostgreSQL instance’s IP address on port 5432.
  1. Set up NSG rules in Azure to permit incoming connections from the cloud provider (AWS, GCP) to the Azure PostgreSQL IP range.
  1. Test the connectivity between your PostgreSQL instance in the managed PostgreSQL service (AWS, GCP, Heroku, etc.) and Azure Database for PostgreSQL to ensure no network issues.

## Scenario 4: Azure VMs to Azure Database for PostgreSQL (in different virtual networks)

This scenario describes connectivity between an instance of Azure Virtual Machines and an instance of Azure Database for PostgreSQL that are in different virtual networks. Virtual network peering and appropriate NSG rules are required to facilitate traffic between the VNets.

:::image type="content" source="media/how-to-network-setup-migration-service/vm-to-azure-peering.png" alt-text="Screenshot of an Azure VM in one virtual network connects to the Azure Database for PostgreSQL in another virtual network." lightbox="media/how-to-network-setup-migration-service/vm-to-azure-peering.png":::

**Networking steps:**

1. Set up virtual network peering between the two VNets to enable direct network connectivity.
1. Configure NSG rules to allow traffic between the VNets on the PostgreSQL port.

## Scenario 5: Azure VMs to Azure PostgreSQL (in the same virtual network)

Configuration is straightforward when an Azure VM and Azure Database for PostgreSQL are within the same virtual network. NSG rules should be set to allow internal traffic on the PostgreSQL port, and no additional firewall rules are necessary for the Azure Database for PostgreSQL since the traffic remains within the virtual network.

:::image type="content" source="media/how-to-network-setup-migration-service/vm-to-azure-same-vnet.png" alt-text="Screenshot of an Azure VM in the same virtual network connects directly to the Azure Database for PostgreSQL." lightbox="media/how-to-network-setup-migration-service/vm-to-azure-same-vnet.png":::

**Networking steps:**

1. Ensure that the VM and the PostgreSQL server are in the same virtual network.
1. Configure NSG rules to allow traffic within the virtual network on the PostgreSQL port.
1. No other firewall rules are needed for the Azure Database for PostgreSQL since the traffic is internal to the virtual network.

## Scenario 6: Azure Database for PostgreSQL - Single server to VNet-Integrated Azure Database for PostgreSQL - Flexible Server

To facilitate connectivity between an instance of Azure Database for PostgreSQL - Single Server with public access and a VNet-integrated flexible server, you need to configure the Single Server to allow connections from the subnet where the Flexible Server is deployed. Here's a brief outline of the steps to set up this connectivity:

**Add a VNet rule to a single server:**

1. In the Azure portal, go your Azure Database for PostgreSQL - Single Server instance.
1. Go to the **Connection Security** settings.
1. In the **Virtual network rules** section, and select **Add existing virtual network**.

   This action lets you specify which virtual network can connect to your Single Server.

    :::image type="content" source="media/how-to-network-setup-migration-service/add-vnet-rule-single-server.png" alt-text="Screenshot of adding a virtual network rule in single server." lightbox="media/how-to-network-setup-migration-service/add-vnet-rule-single-server.png":::

**Configure Rule Settings:**

- Enter a name for the new virtual network rule in the configuration panel that appears.
- Select the subscription where your Flexible Server is located.
- Choose the virtual network (virtual network) and the specific subnet associated with your Flexible Server.
- Confirm the settings by selecting "OK".

    :::image type="content" source="media/how-to-network-setup-migration-service/allow-flexible-server-subnet.png" alt-text="Screenshot of allowing the flexible server subnet." lightbox="media/how-to-network-setup-migration-service/allow-flexible-server-subnet.png":::

After completing these steps, the Single Server will be configured to accept connections from the Flexible Server's subnet, enabling secure communication between the two servers.

## Scenario 7: Azure Database for PostgreSQL - Single Server with private endpoint to VNet-Integrated Azure Database for PostgreSQL - Flexible server

To facilitate connectivity from an Azure Database for PostgreSQL Single Server with a private endpoint to a VNet-integrated Flexible Server, follow these steps:

**Get private endpoint details:**

- In the Azure portal, navigate to the Single Server instance and select the private endpoint to view its virtual network and subnet details.
- Access the Networking page of the Flexible Server to note its virtual network and subnet information.

     :::image type="content" source="media/how-to-network-setup-migration-service/private-endpoint-single-server.png" alt-text="Screenshot of private endpoint connection in single server." lightbox="media/how-to-network-setup-migration-service/allow-flexible-server-subnet.png":::

    :::image type="content" source="media/how-to-network-setup-migration-service/vnet-details-single-server.png" alt-text="Screenshot showing virtual network and subnet details of single server's private endpoint." lightbox="media/how-to-network-setup-migration-service/vnet-details-single-server.png":::

**Assess VNet Peering Requirements**
- If both are in different VNets, you need to enable virtual network peering to connect one virtual network to another. Peering is optional if they are in the same virtual network but in different subnets. Ensure that no network security groups (NSGs) block the traffic from flexible server to single server.

**Private DNS Zone Configuration**
- Go to the **Networking** page on the flexible server and check if a private DNS zone is being used. If used, open this private DNS zone in the portal. In the left pane, select the **Virtual network links** and check if the virtual network of single server and flexible server is added to this list.

    :::image type="content" source="media/how-to-network-setup-migration-service/private-dns-zone-vnet-link.png" alt-text="Screenshot virtual network linked to a private DNS Zone." lightbox="media/how-to-network-setup-migration-service/private-dns-zone-vnet-link.png":::

If not, select the **Add** button and create a link to this private DNS zone for the VNets of single and flexible servers.

- Go to the private endpoint on your single server and select the **DNS configuration** page. Check if a private DNS zone is attached with this endpoint. If not, attach a private DNS zone by selecting on the **Add Configuration** button.

    :::image type="content" source="media/how-to-network-setup-migration-service/private-dns-zone-private-end-point.png" alt-text="Screenshot showing a private DNS Zone used in private end point." lightbox="media/how-to-network-setup-migration-service/private-dns-zone-private-end-point.png":::

- Select the Private DNS zone on your single server private endpoint and check if the Vnets of single server and flexible server are added to the Virtual network links. If not, follow the steps mentioned in the above step to add the links to the virtual networks of the single and flexible server to this private DNS zone.

- The final check would be to go the private DNS zone of the private endpoint on your single server and check if there exists an **A record** for your single server that points a private IP address.

    :::image type="content" source="media/how-to-network-setup-migration-service/private-dns-zone-record.png" alt-text="Screenshot showing a private IP address assigned to private end point." lightbox="media/how-to-network-setup-migration-service/private-dns-zone-record.png":::

Completing these steps enables the instance of Azure Database for PostgreSQL - Flexible Server to connect to the instance of Azure Database for PostgreSQL - Single Server.

## Scenario 8: Azure Database for PostgreSQL single server with private endpoint to Azure Database for PostgreSQL flexible server with private endpoint

Below are the essential networking steps for migrating from a Single Server with a private endpoint to a Flexible Server with a private endpoint in Azure PostgreSQL, including the integration of a runtime server's virtual network with private endpoint configurations. For more information about the Runtime Server, visit the [Migration Runtime Server](concepts-migration-service-runtime-server.md).

- **Gather Private Endpoint Details for Single Server**
    - Access the Azure portal and locate the Azure Database for PostgreSQL - Single Server instance.
    - Record the Virtual Network (virtual network) and subnet details listed under the private endpoint connection of the Single Server.

    :::image type="content" source="media/how-to-network-setup-migration-service/single-server-private-endpoint.png" alt-text="Screenshot of Single Server with PE." lightbox="media/how-to-network-setup-migration-service/single-server-private-endpoint.png":::

- **Gather Private Endpoint Details for Flexible Server**
    - Access the Azure portal and locate the Azure Database for PostgreSQL - Flexible Server instance.
    - Record the Virtual Network (virtual network) and subnet details listed under the private endpoint connection of the Flexible Server.

    :::image type="content" source="media/how-to-network-setup-migration-service/flexible-server-private-endpoint.png" alt-text="Screenshot of Flexible Server with PE." lightbox="media/how-to-network-setup-migration-service/flexible-server-private-endpoint.png":::

- **Gather VNET details for Migration Runtime Server**
    - Access the Azure portal and locate the migration runtime server, that is, Azure Database for PostgreSQL - Flexible Server (VNET Integrated) instance.
    - Record the Virtual Network (virtual network) and subnet details listed under the virtual network.

    :::image type="content" source="media/how-to-network-setup-migration-service/instance-vnet.png" alt-text="Screenshot of migration runtime server with virtual network." lightbox="media/how-to-network-setup-migration-service/instance-vnet.png":::

- **Assess VNet Peering Requirements**
    - Enable virtual network peering if the servers are in different VNets; no peering is needed in the same virtual network but with different subnets.
    - Ensure no NSGs block traffic between the source, migration runtime, and target servers.

- **Private DNS zone configuration**

  1. Verify the use of a private DNS zone on the networking page of the migration runtime server.
  1. Ensure that the VNets of both the source instance of Azure Database for PostgreSQL - Single Server and the target instance of Azure Database for PostgreSQL - Flexible Server are linked to the private DNS zone of the migration runtime server.

     :::image type="content" source="media/how-to-network-setup-migration-service/instance-dns-zone.png" alt-text="Screenshot of private DNS zone of runtime server." lightbox="media/how-to-network-setup-migration-service/instance-dns-zone.png":::

  1. Attach a private DNS zone to the Single Server's private endpoint if not already configured.
    - Add virtual network links for the Single Server and Migration Runtime Server to the private DNS zone.
    - Repeat the DNS zone attachment and virtual network linking process for the Flexible Server's private endpoint.

    :::image type="content" source="media/how-to-network-setup-migration-service/source-dns-zone.png" alt-text="Screenshot of private DNS zone of source/target server." lightbox="media/how-to-network-setup-migration-service/source-dns-zone.png":::

## Scenario 9: PostgreSQL source with private IPs to Azure Database for PostgreSQL flexible server with private endpoint

Below are the networking steps for migrating a PostgreSQL database from a cloud-based PostgreSQL service, an on-premises setup, or a virtual machine, all of which are configured with private IPs to an Azure Database for PostgreSQL Flexible Server that is secured with a private endpoint. The migration ensures secure data transfer within a private network space, using Azure's VPN or ExpressRoute for on-premises connections and virtual network peering or VPN for cloud-to-cloud migrations. For more information about the Runtime Server, visit the [Migration Runtime Server](concepts-migration-service-runtime-server.md).

- **Establish Network Connectivity:**
   - For on-premises sources, set up a Site-to-Site VPN or ExpressRoute to connect your local network to Azure's virtual network.
   - For Azure VM or Amazon instances, ensure virtual network peering or a VPN gateway or a ExpressRoute is in place for secure connectivity to Azure's virtual network.

- **Gather VNET details for Migration Runtime Server**
    - Access the Azure portal and locate the migration runtime server, that is, Azure Database for PostgreSQL - Flexible Server (VNET Integrated) instance.
    - Record the Virtual Network (virtual network) and subnet details listed under the virtual network.

- **Assess VNet Peering Requirements**
    - Enable virtual network peering if the servers are in different VNets; no peering is needed in the same virtual network but with different subnets.
    - Ensure no NSGs are blocking traffic between the source, migration runtime, and target servers.

- **Private DNS Zone Configuration**
    - Verify the use of a private DNS zone on the networking page of the Migration Runtime Server.
    - Ensure both source and target Azure Database for PostgreSQL - Flexible Server VNets are linked to the private DNS zone of the migration runtime server.
    - Attach a private DNS zone to the Flexible Server's private endpoint if not already configured.
    - Add virtual network links for the Flexible Server and Migration Runtime Server to the private DNS zone.

## Resources for network setup

- To establish an **ExpressRoute** connection, refer to the [What is Azure ExpressRoute?](/azure/expressroute/expressroute-introduction).
- For setting up an **IPsec VPN**, consult the guide on [About Point-to-Site VPN](/azure/vpn-gateway/point-to-site-about).
- For virtual network peering, [Virtual network peering](/azure/virtual-network/virtual-network-peering-overview)

## Related content

- [Migration service](concepts-migration-service-postgresql.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
- [Premigration validations](concepts-premigration-migration-service.md)

