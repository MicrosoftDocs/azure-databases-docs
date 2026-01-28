---
title: Networking Overview
description: Connectivity and networking concepts for Azure Database for MySQL - Flexible Server.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Connectivity and networking concepts for Azure Database for MySQL - Flexible Server

This article introduces the concepts to control connectivity to your Azure Database for MySQL Flexible Server instance. You learn in detail the networking concepts for Azure Database for MySQL Flexible Server to create and access a server securely in Azure.

Azure Database for MySQL Flexible Server supports three ways to configure connectivity to your servers:

- **[Public Network Access for Azure Database for MySQL - Flexible Server](concepts-networking-public.md)** Your Flexible Server is accessed through a public endpoint. The public endpoint is a publicly resolvable DNS address. The phrase "allowed IP addresses" refers to a range of IPs you choose to give permission to access your server. These permissions are called **firewall rules**.

- **[Private Endpoint](/azure/private-link/private-endpoint-overview)** You can use private endpoints to allow hosts on a [virtual network](/azure/virtual-network/virtual-networks-overview) to securely access data over a [Private Link](/azure/private-link/private-link-overview).

- **[Private Network Access using virtual network integration for Azure Database for MySQL - Flexible Server](concepts-networking-vnet.md)** You can deploy your Flexible Server into your [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview). Azure virtual networks provide private and secure network communication. Resources in a virtual network can communicate through private IP addresses.

> [!NOTE]  
> After deploying a server with public or private access (via virtual network integration), you can't modify the connectivity mode. But in public access mode, you can enable or disable private endpoints as required and also disable public access if needed.

## Choose a networking option

Choose **Public access (allowed IP addresses) and Private endpoint** method if you want the following capabilities:

- Connect from Azure resources without virtual network support
- Connect from resources outside of Azure that aren't connected by VPN or ExpressRoute
- The Flexible Server is accessible through a public endpoint and can be accessed via authorized internet resources. Public access can be disabled if needed.
- Ability to configure Private endpoints to access the server from hosts on a virtual network

Choose **Private access (virtual network integration)** if you want the following capabilities:

- Connect to your Flexible Server from Azure resources within the same virtual network or a [peered virtual network](/azure/virtual-network/virtual-network-peering-overview) without the need to configure a private endpoint
- Use VPN or ExpressRoute to connect from non-Azure resources to your Flexible Server
- No public endpoint

The following characteristics apply whether you choose to use the private access or the public access option:

- Connections from allowed IP addresses need to authenticate to the Azure Database for MySQL Flexible Server instance with valid credentials
- [Connection encryption](#tls-and-ssl) is available for your network traffic
- The server has a fully qualified domain name (fqdn). We recommend using the fqdn instead of an IP address for the hostname property in connection strings.
- Both options control access at the server-level, not at the database- or table-level. You would use MySQL's roles properties to control database, table, and other object access.

### Custom port support

Azure MySQL now supports the ability to specify a custom port between 250001 and 26000 during server creation to connect to the server. The default port to connect is 3306.

- Only one custom port per server is supported.
- Supported scenarios for custom port: server creation, restore (cross-port restore supported), read replica creation, high availability enablement.
- Current limitations:
  - Custom port can't be updated post server creation.
  - Geo-restore and geo-replica creation with custom port aren't supported.

### Unsupported virtual network scenarios

- Public endpoint (or public IP or DNS) - A Flexible Server deployed to a virtual network can't have a public endpoint.
- After the Flexible Server is deployed to a virtual network and subnet, you can't move it to another virtual network or subnet.
- After the Flexible Server is deployed, you can't move the virtual network the Flexible Server uses into another resource group or subscription.
- Subnet size (address spaces) can't be increased once resources exist in the subnet.
- Change from Public to Private access isn't allowed after the server is created. The recommended way is to use point-in-time restore.

> [!NOTE]  
> If you're using the custom DNS server, you must use a DNS forwarder to resolve the FQDN of the Azure Database for MySQL Flexible Server instance. Refer to **[name resolution that uses your DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server)** to learn more.

## Hostname

Regardless of your networking option, we require that you use the fully qualified domain name (FQDN) `<servername>.mysql.database.azure.com` in connection strings. The server's IP address isn't guaranteed to remain static.

An example that uses an FQDN as a host name is hostname = servername.mysql.database.azure.com. Where possible, avoid using hostname = 10.0.0.4 (a private address) or hostname = 40.2.45.67 (a public address).

## TLS and SSL

This documentation has moved to [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md).

## Related content

- [Transport Layer Security (TLS) in Azure Database for MySQL](security-tls.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-virtual-network-cli.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](security-how-to-manage-firewall-portal.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI](security-how-to-manage-firewall-cli.md)
- [configure private link for Azure Database for MySQL Flexible Server from Azure portal](how-to-networking-private-link-portal.md)
