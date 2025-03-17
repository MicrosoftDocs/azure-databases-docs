---
title: Networking Overview
description: Connectivity and networking concepts for Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Connectivity and networking concepts for Azure Database for MySQL - Flexible Server

This article introduces the concepts to control connectivity to your Azure Database for MySQL Flexible Server instance. You learn in detail the networking concepts for Azure Database for MySQL Flexible Server to create and access a server securely in Azure.

Azure Database for MySQL Flexible Server supports three ways to configure connectivity to your servers:

   - **[Public Network Access for Azure Database for MySQL - Flexible Server](concepts-networking-public.md)** Your Flexible Server is accessed through a public endpoint. The public endpoint is a publicly resolvable DNS address. The phrase "allowed IP addresses" refers to a range of IPs you choose to give permission to access your server. These permissions are called **firewall rules**.

   - **[Private Endpoint](/azure/private-link/private-endpoint-overview)** You can use private endpoints to allow hosts on a virtual network [VNet](/azure/virtual-network/virtual-networks-overview) to securely access data over a [Private Link](/azure/private-link/private-link-overview).

   - **[Private Network Access using virtual network integration for Azure Database for MySQL - Flexible Server](concepts-networking-vnet.md)** You can deploy your Flexible Server into your [Azure Virtual Network](/azure/virtual-network/virtual-networks-overview). Azure virtual networks provide private and secure network communication. Resources in a virtual network can communicate through private IP addresses.

> [!NOTE]  
> After deploying a server with public or private access (via VNet integration), you cannot modify the connectivity mode. But in public access mode, you can enable or disable private endpoints as required and also disable public access if needed.

## Choose a networking option

Choose **Public access (allowed IP addresses) and Private endpoint** method if you want the following capabilities:
   - Connect from Azure resources without virtual network support
   - Connect from resources outside of Azure that aren't connected by VPN or ExpressRoute
   - The Flexible Server is accessible through a public endpoint and can be accessed via authorized internet resources. Public access can be disabled if needed.
   - Ability to configure Private endpoints to access the server from hosts on a virtual network (VNet)

Choose **Private access (VNet integration)** if you want the following capabilities:
   - Connect to your Flexible Server from Azure resources within the same virtual network or a [peered virtual network](/azure/virtual-network/virtual-network-peering-overview) without the need to configure a private endpoint
   - Use VPN or ExpressRoute to connect from non-Azure resources to your Flexible Server
   - No public endpoint

The following characteristics apply whether you choose to use the private access or the public access option:
- Connections from allowed IP addresses need to authenticate to the Azure Database for MySQL Flexible Server instance with valid credentials
- [Connection encryption](#tls-and-ssl) is available for your network traffic
- The server has a fully qualified domain name (fqdn). We recommend using the fqdn instead of an IP address for the hostname property in connection strings.
- Both options control access at the server-level, not at the database- or table-level. You would use MySQL's roles properties to control database, table, and other object access.

### Unsupported virtual network scenarios

- Public endpoint (or public IP or DNS) - A Flexible Server deployed to a virtual network can't have a public endpoint.
- After the Flexible Server is deployed to a virtual network and subnet, you can't move it to another virtual network or subnet.
- After the Flexible Server is deployed, you can't move the virtual network the Flexible Server uses into another resource group or subscription.
- Subnet size (address spaces) can't be increased once resources exist in the subnet.
- Change from Public to Private access isn't allowed after the server is created. The recommended way is to use point-in-time restore.

> [!NOTE]  
> If you are using the custom DNS server, you must use a DNS forwarder to resolve the FQDN of the Azure Database for MySQL Flexible Server instance. Refer to **[name resolution that uses your DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server)** to learn more.

## Hostname

Regardless of your networking option, we recommend you use the fully qualified domain name (FQDN) `<servername>.mysql.database.azure.com` in connection strings when connecting to your Azure Database for MySQL Flexible Server instance. The server's IP address is not guaranteed to remain static. Using the FQDN will help you avoid making changes to your connection string.

An example that uses an FQDN as a host name is hostname = servername.mysql.database.azure.com. Where possible, avoid using hostname = 10.0.0.4 (a private address) or hostname = 40.2.45.67 (a public address).

## TLS and SSL

Azure Database for MySQL Flexible Server supports connecting your client applications to the Azure Database for MySQL Flexible Server instance using Secure Sockets Layer (SSL) with Transport layer security (TLS) encryption. TLS is an industry-standard protocol that ensures encrypted network connections between your database server and client applications, allowing you to adhere to compliance requirements.

Azure Database for MySQL Flexible Server supports encrypted connections using Transport Layer Security (TLS 1.2) by default, and all incoming connections with TLS 1.0 and TLS 1.1 are denied by default. The encrypted connection enforcement or TLS version configuration on your Flexible Server can be configured and changed.

Following are the different configurations of SSL and TLS settings you can have for your Flexible Server:

> [!IMPORTANT]  
> According to [Removal of Support for the TLS 1.0 and TLS 1.1 Protocols](https://dev.mysql.com/doc/refman/8.0/en/encrypted-connection-protocols-ciphers.html#encrypted-connection-deprecated-protocols), we previously planned to fully deprecate TLS 1.0 and 1.1 by September 2024. However, due to dependencies identified by some customers, we have decided to extend the timeline.
> - Starting on August 31, 2025, we will begin the forced upgrade for all servers still using TLS 1.0 or 1.1. After this date, any connections relying on TLS 1.0 or 1.1 may stop working at any time. To avoid potential service disruptions, we strongly recommend that customers complete their migration to TLS 1.2 before August 31, 2025.
> - Beginning in September 2024, new servers will no longer be permitted to use TLS 1.0 or 1.1, and existing servers will not be allowed to downgrade to these versions.
> 
> We strongly recommend that customers update their applications to support TLS 1.2 as soon as possible to avoid service disruptions.

| Scenario | Server parameter settings | Description |
| --- | --- | --- |
| Disable SSL (encrypted connections) | require_secure_transport = OFF | If your legacy application doesn't support encrypted connections to the Azure Database for MySQL Flexible Server instance, you can disable enforcement of encrypted connections to your Flexible Server by setting require_secure_transport=OFF. |
| Enforce SSL with TLS version < 1.2 (Will be deprecated in September 2024) | require_secure_transport = ON and tls_version = TLS 1.0 or TLS 1.1 | If your legacy application supports encrypted connections but requires TLS version < 1.2, you can enable encrypted connections, but configure your Flexible Server to allow connections with the TLS version (v1.0 or v1.1) supported by your application |
| Enforce SSL with TLS version = 1.2(Default configuration) | require_secure_transport = ON and tls_version = TLS 1.2 | This is the recommended and default configuration for a Flexible Server. |
| Enforce SSL with TLS version = 1.3(Supported with MySQL v8.0 and above) | require_secure_transport = ON and tls_version = TLS 1.3 | This is useful and recommended for new applications development |

> [!NOTE]  
> Changes to SSL Cipher on the Flexible Server is not supported. FIPS cipher suites is enforced by default when tls_version is set to TLS version 1.2. For TLS versions other than version 1.2, SSL Cipher is set to default settings which comes with MySQL community installation.

Review [connect using SSL/TLS](how-to-connect-tls-ssl.md#verify-the-tlsssl-connection) to learn how to identify the TLS version you are using .

## Related content

- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-virtual-network-portal.md)
- [Create and manage virtual networks for Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-manage-virtual-network-cli.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-firewall-portal.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI](how-to-manage-firewall-cli.md)
- [configure private link for Azure Database for MySQL Flexible Server from Azure portal](how-to-networking-private-link-portal.md)
