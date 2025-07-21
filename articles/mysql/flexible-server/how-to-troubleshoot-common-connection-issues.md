---
title: Troubleshoot Connection Issues
description: Learn how to troubleshoot connection issues to Azure Database for MySQL - Flexible Server.author: aditivgupta
ms.author: adig

ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: troubleshooting
---

# Troubleshoot connection issues to Azure Database for MySQL - Flexible Server

Connection problems might be caused by a variety of things, including:

- Firewall settings
- Connection time-out
- Incorrect login information
- Maximum limit reached on some Azure Database for MySQL Flexible Server resources

In this article, we will discuss how you can troubleshoot some of the common errors and steps to resolve these errors.

## Troubleshoot common errors

If the application persistently fails to connect to Azure Database for MySQL Flexible Server, it usually indicates an issue with one of the following:

- Encrypted connection using TLS/SSL: Azure Database for MySQL Flexible Server supports encrypted connections using Transport Layer Security (TLS 1.2) and all **incoming connections with TLS 1.0 and TLS 1.1 will be denied by default**. You can disable enforcement of encrypted connections or change the TLS version. Learn more about [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md).
- Azure Database for MySQL Flexible Server in *Private access (VNet Integration)*: Make sure you are connecting from within the same virtual network as the Azure Database for MySQL Flexible Server instance. Refer to [virtual network in Azure Database for MySQL Flexible Server]<!--(./concepts-networking-virtual-network.md)-->
- Azure Database for MySQL Flexible Server with *Public access (allowed IP addresses)*, make sure that the firewall is configured to allow connections from your client. Refer to [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](how-to-manage-firewall-portal.md).
- Client firewall configuration: The firewall on your client must allow connections to your Azure Database for MySQL Flexible Server instance. IP addresses and ports of the server that you connect to must be allowed as well as application names such as MySQL in some firewalls.
- User error: You might have mistyped connection parameters, such as the server name in the connection string.

### Resolve connectivity issues

- Refer to [encrypted connectivity using Transport Layer Security (TLS 1.2) in Azure Database for MySQL Flexible Server](how-to-connect-tls-ssl.md) --> to learn more about encrypted connections.
- If you are using **Public access (allowed IP addresses)**, then set up [firewall rules](how-to-manage-firewall-portal.md) to allow the client IP address. For temporary testing purposes only, set up a firewall rule using 0.0.0.0 as the starting IP address and using 255.255.255.255 as the ending IP address. This will open the server to all IP addresses. If this resolves your connectivity issue, remove this rule and create a firewall rule for an appropriately limited IP address or address range.
- On all firewalls between the client and the internet, make sure that port 3306 is open for outbound connections.
- Verify your connection string and other connection settings. Refer to the pre-defined connection strings in the **Connection Strings** page available for your server in the Azure portal for common languages.

## Related content

- [Use MySQL Workbench with Azure Database for MySQL - Flexible Server](connect-workbench.md)
- [Use PHP with Azure Database for MySQL - Flexible Server](connect-php.md)
- [Quickstart: Use Python to connect and query data in Azure Database for MySQL - Flexible Server](connect-python.md)
