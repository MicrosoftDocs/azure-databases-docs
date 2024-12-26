---
title: Public Network Access Overview
description: Learn about public access networking option in Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Public Network Access for Azure Database for MySQL - Flexible Server

This article describes the public connectivity option for Azure Database for MySQL Flexible Server. You learn in detail the concepts to create an Azure Database for MySQL Flexible Server instance that is accessible securely through the internet.

## Public access (allowed IP addresses)

Configuring public access on your Azure Database for MySQL Flexible Server instance allows the server access through a public endpoint. That is, the server is accessible through the internet. The public endpoint is a publicly resolvable DNS address. The phrase *allowed IP addresses* refers to a range of IPs you choose to permit access to your server. These permissions are called firewall rules.

Characteristics of the public access method include:

- Only the IP addresses you allow have permission to access your Azure Database for MySQL Flexible Server instance. By default, no IP addresses are allowed. You can add IP addresses when initially setting up your server or after your server has been created.
- Your Azure Database for MySQL Flexible Server instance has a publicly resolvable DNS name.
- Your Azure Database for MySQL Flexible Server instance isn't in one of your Azure virtual networks.
- Network traffic to and from your server doesn't go over a private network. The traffic uses the general internet pathways.

### Firewall rules

Granting permission to an IP address is called a firewall rule. If a connection attempt comes from an IP address you haven't allowed, the originating client sees an error.

### Allow all Azure IP addresses

You can consider enabling connections from all Azure data center IP addresses if a fixed outgoing IP address isn't available for your Azure service.

> [!IMPORTANT]  
> - The **Allow public access from Azure services and resources within Azure** option configures the firewall to allow all connections from Azure, including connections from the subscriptions of other customers. When selecting this option, ensure your login and user permissions limit access to only authorized users.
> - You can create a maximum of 500 IP firewall rules.
>

Learn how to enable and manage public access (allowed IP addresses) using the [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-firewall-portal.md) or [Manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI](how-to-manage-firewall-cli.md).

### Troubleshoot public access issues

Consider the following points when access to Azure Database for MySQL Flexible Server doesn't behave as you expect:

- **Changes to the allowlist have yet to take effect:** There might be as much as a five-minute delay for changes to the Azure Database for MySQL Flexible Server firewall configuration to take effect.

- **Authentication failed:** If a user doesn't have permissions on the Azure Database for MySQL Flexible Server instance or the password used is incorrect, the connection to the Azure Database for MySQL Flexible Server instance is denied. Creating a firewall setting only allows clients to attempt to connect to your server. Each client must still provide the necessary security credentials.

- **Dynamic client IP address:** If you have an Internet connection with dynamic IP addressing and you're having trouble getting through the firewall, you could try one of the following solutions:
    - Ask your internet service provider (ISP) for the IP address range assigned to your client computers that access the Azure Database for MySQL Flexible Server instance, and then add the IP address range as a firewall rule.
    - Get static IP addressing instead for your client computers, and then add the static IP address as a firewall rule.

- **Firewall rule is not available for IPv6 format:** The firewall rules must be in IPv4 format. If you specify firewall rules in IPv6 format, it shows the validation error.

> [!NOTE]  
> We recommend you use the fully qualified domain name (FQDN) `<servername>.mysql.database.azure.com` in connection strings when connecting to your Flexible Server. The server's IP address is not guaranteed to remain static. Using the FQDN will help you avoid making changes to your connection string.

## Related content

- [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-firewall-portal.md)
- [Manage firewall rules for Azure Database for MySQL - Flexible Server using Azure CLI](how-to-manage-firewall-cli.md)
- [use TLS](how-to-connect-tls-ssl.md)
