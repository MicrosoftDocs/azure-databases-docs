---
title: "Migrate MySQL On-Premises to Azure Database for MySQL: Planning"
description: "An Azure landing zone is the target environment defined as the final resting place of a cloud migration project."
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: migration-guide
ms.topic: how-to
---

# Migrate MySQL on-premises to Azure Database for MySQL: Planning

Planning the migration of MySQL databases from on-premises environments to Azure Database for MySQL is a crucial phase that sets the foundation for a successful transition. This article explores the essential steps and considerations involved in the planning process. You can ensure a smooth and efficient migration by thoroughly analyzing your current database environment, defining clear migration goals, and developing a comprehensive migration strategy. This guide will provide you with the insights and best practices needed to effectively plan your migration, address potential challenges, and leverage Azure's robust features to optimize performance, scalability, and cost-efficiency. Whether you aim to modernize your infrastructure or enhance disaster recovery capabilities, this article equips you with the knowledge to make informed decisions and achieve a seamless migration.

## Prerequisites

[Migrate MySQL on-premises to Azure Database for MySQL: Assessment](03-assessment.md)

## Land zone

An [Azure Landing zone](/azure/cloud-adoption-framework/ready/landing-zone/) is the target environment defined as the final resting place of a cloud migration project. In most projects, the landing zone should be scripted via ARM templates for its initial setup. Finally, it should be customized with PowerShell or the Azure portal to fit the workloads needs.

Since WWI is based in San Francisco, all resources for the Azure landing zone were created in the `US West 2` region. The following resources were created to support the migration:

- [Azure Database for MySQL](../../quickstart-create-mysql-server-database-using-azure-portal.md)

- [Azure Database Migration Service (DMS)](../../../dms/quickstart-create-data-migration-service-portal.md)

- [Express Route](/azure/expressroute/expressroute-introduction)

- [Azure Virtual Network](/azure/virtual-network/quick-create-portal) with [hub and spoke design](/azure/architecture/reference-architectures/hybrid-networking/hub-spoke) with corresponding [virtual network peerings](/azure/virtual-network/virtual-network-peering-overview) establish.

- [App Service](/azure/app-service/overview)

- [Application Gateway](/azure/load-balancer/quickstart-load-balancer-standard-internal-portal?tabs=option-1-create-internal-load-balancer-standard)

- [Private endpoints](/azure/private-link/private-endpoint-overview) for the App Services and MySQL instance

> [!NOTE]  
> As part of this guide, two ARM templates (one with private endpoints, one without) were provided in order to deploy a potential Azure landing zone for a MySQL migration project. The private endpoints ARM template provides a more secure and production like scenario. Additional manual Azure landing zone configuration might be necessary, depending on the requirements.

## Networking

Getting data from the source system to Azure Database for MySQL in a fast and optimal way is a vital component to consider in a migration project. Small unreliable connections might require administrators to restart the migration several times until a successful result is achieved. Restarting migrations because of network issues can lead to wasted effort.

Take the time to understand and evaluate the network connectivity between the source, tool, and destination environments. In some cases, it might be appropriate to upgrade the internet connectivity or configure an ExpressRoute connection from the on-premises environment to Azure. Once on-premises to Azure connectivity has been created, the next step is to validate that the selected migration tool can connect from the source to the destination.

The migration tool location determines the network connectivity requirements. As shown in the table below, the selected migration tool must connect to both the on-premises machine and to Azure. Azure should be configured to only accept network traffic from the migration tool location.

| Migration Tool | Type | Location | Inbound Network Requirements | Outbound Network Requirements |
| --- | --- | --- | --- | --- |
| **Database Migration Service (DMS)** | Offline | Azure | Allow 3306 from external IP | A path to connect to the Azure MySQL database instance |
| **Import/Export (MySQL Workbench, mysqldump)** | Offline | On-premises | Allow 3306 from internal IP | A path to connect to the Azure MySQL database instance |
| **Import/Export (MySQL Workbench, mysqldump)** | Offline | Azure VM | Allow 3306 from external IP | A path to connect to the Azure MySQL database instance |
| **mydumper/myloader** | Offline | On-premises | Allow 3306 from internal IP | A path to connect to the Azure MySQL database instance |
| **mydumper/myloader** | Offline | Azure VM | Allow 3306 from external IP | A path to connect to the Azure MySQL database instance |
| **binlog** | Offline | On-premises | Allow 3306 from external IP or private IP via Private endpoints | A path for each replication server to the master |

Other networking considerations include:

- DMS located in a virtual network is assigned a [dynamic public IP](../../../dms/faq.yml) to the service. At creation time, you can place the service inside a virtual network that has connectivity via a [ExpressRoute](/azure/expressroute/expressroute-introduction) or over [a site to site VPN](/azure/vpn-gateway/tutorial-site-to-site-portal).

- When using an Azure Virtual Machine to run the migration tools, assign it a public IP address and then only allow it to connect to the on-premises MySQL instance.

- Outbound firewalls must ensure outbound connectivity to Azure Database for MySQL. The MySQL gateway IP addresses are available on the [Connectivity Architecture in Azure Database for MySQL](../../concepts-connectivity-architecture.md#azure-database-for-mysql-gateway-ip-addresses) page.

## SSL/TLS connectivity

In addition to the application implications of migrating to SSL-based communication, the SSL/TLS connection types are also something that needs to be considered. After creating the Azure Database for MySQL database, review the SSL settings, and read the [SSL/TLS connectivity in Azure Database for MySQL](../../concepts-ssl-connection-security.md) article to understand how the TLS settings can affect the security posture.

> [!IMPORTANT]  
> Pay attention to the disclaimer on the page. Enforcement of TLS version is not be enabled by default. Once TLS is enabled, the only way to disable it is to re-enable SSL.

## WWI scenario

WWI's cloud team has created the necessary Azure landing zone resources in a specific resource group for the Azure Database for MySQL. To create the landing zone, WWI decided to script the setup and deployment using ARM templates. By using ARM templates, they can quickly tear down and resetup the environment, if needed.

As part of the ARM template, all connections between virtual networks are configured with peering in a hub and spoke architecture. The database and application are placed into separate virtual networks. An Azure App Gateway is placed in front of the app service to allow the app service to be isolated from the Internet. The Azure App Service connects to the Azure Database for MySQL using a private endpoint.

WWI originally wanted to test an online migration, but the required network setup for DMS to connect to their on-premises environment made this infeasible. WWI chose to do an offline migration instead. The MySQL Workbench tool was used to export the on-premises data and then was used to import the data into the Azure Database for MySQL instance.

## Plan checklist

- Prepare the Azure landing zone. Consider using ARM template deployment in case the environment must be torn down and rebuilt quickly.

- Verify the networking setup. Verification should include: connectivity, bandwidth, latency, and firewall configurations.

- Determine if you're going to use the online or offline data migration strategy.

- Decide on the SSL certificate strategy.

## Next step

> [!div class="nextstepaction"]
> [Migrate MySQL on-premises to Azure Database for MySQL: Migration Methods](05-migration-methods.md)
