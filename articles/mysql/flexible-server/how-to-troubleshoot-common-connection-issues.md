---
title: Troubleshoot Connection Issues
description: Learn how to troubleshoot connection issues to Azure Database for MySQL - Flexible Server.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: troubleshooting
---

# Troubleshoot connection issues to Azure Database for MySQL - Flexible Server

Causes for connection problems include:

- Firewall settings
- Connection time-out
- Incorrect login information
- Maximum limit reached on some Azure Database for MySQL Flexible Server resources

In this article, we discuss how you can troubleshoot some of the common errors and steps to resolve these errors.

## Troubleshoot common errors

If the application persistently fails to connect to Azure Database for MySQL Flexible Server, it usually indicates:

- Encrypted connection using TLS/SSL: Azure Database for MySQL Flexible Server supports encrypted connections using Transport Layer Security (TLS 1.2) and all **incoming connections with TLS 1.0 and TLS 1.1 will be denied by default**. You can disable enforcement of encrypted connections or change the TLS version. Learn more about [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](security-tls-how-to-connect.md).
- Azure Database for MySQL Flexible Server in *Private access (virtual network integration)*: Make sure you're connecting from within the same virtual network as the Azure Database for MySQL Flexible Server instance. Refer to [virtual network in Azure Database for MySQL Flexible Server]<!--(./concepts-networking-virtual-network.md)-->
- Azure Database for MySQL Flexible Server with *Public access (allowed IP addresses)*, make sure that the firewall is configured to allow connections from your client. Refer to [Manage firewall rules for Azure Database for MySQL - Flexible Server using the Azure portal](security-how-to-manage-firewall-portal.md).
- Client firewall configuration: The firewall on your client must allow connections to your Azure Database for MySQL Flexible Server instance. IP addresses and ports of the server that you connect to must be allowed as well as application names such as MySQL in some firewalls.
- User error: You might have mistyped connection parameters, such as the server name in the connection string.

### Resolve connectivity issues

- Refer to [encrypted connectivity using Transport Layer Security (TLS 1.2) in Azure Database for MySQL Flexible Server](security-tls-how-to-connect.md) --> to learn more about encrypted connections.
- If you're using **Public access (allowed IP addresses)**, then set up [firewall rules](security-how-to-manage-firewall-portal.md) to allow the client IP address. For temporary testing purposes only, set up a firewall rule allowing access from any IP address using 0.0.0.0 as the starting IP address and using 255.255.255.255 as the ending IP address. If this firewall rule resolves your connectivity issue, remove this rule and create a firewall rule for an appropriately limited IP address or address range.
- On all firewalls between the client and the internet, make sure that port 3306 is open for outbound connections.
- Verify your connection string and other connection settings. Refer to the predefined connection strings in the **Connection Strings** page available for your server in the Azure portal for common languages.

## Related content

- [Use MySQL Workbench with Azure Database for MySQL - Flexible Server](connect-workbench.md)
- [Use PHP with Azure Database for MySQL - Flexible Server](connect-php.md)
- [Quickstart: Use Python to connect and query data in Azure Database for MySQL - Flexible Server](connect-python.md)
