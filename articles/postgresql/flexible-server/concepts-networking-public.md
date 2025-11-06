---
title: "Networking Overview with Public Access (Allowed IP Addresses)"
description: Learn about connectivity and networking with public access for an Azure Database for PostgreSQL flexible server instance.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 11/06/2025
ms.service: azure-database-postgresql
ms.topic: concept-article
ms.custom:
  - ignite-2023
---

# Networking overview for Azure Database for PostgreSQL with public access (allowed IP addresses)

This article describes connectivity and networking concepts for Azure Database for PostgreSQL flexible server instances.

When you create an Azure Database for PostgreSQL flexible server instance, you must choose one of the following networking options:

- Private access (virtual network integration)
- Public access (allowed IP addresses) and private endpoint

The following characteristics apply whether you choose to use the private access or the public access option:

- Connections from allowed IP addresses need to authenticate to the Azure Database for PostgreSQL flexible server instance with valid credentials.
- Connection encryption is enforced for your network traffic.
- The server has a fully qualified domain name (FQDN). For the `hostname` property in connection strings, we recommend using the FQDN instead of an IP address.
- Both options control access at the server level, not at the database or table level. You would use PostgreSQL's role properties to control database, table, and other object access.

> [!NOTE]  
> Because the Azure Database for PostgreSQL service is a managed database service, users aren't provided host or operating system access to view or modify configuration files such as `pg_hba.conf`. The content of the files is automatically updated based on the network settings.

## Use public access networking with Azure Database for PostgreSQL

When you choose the public access method, your Azure Database for PostgreSQL flexible server instance is accessed through a public endpoint over the internet. The public endpoint is a publicly resolvable DNS address. The phrase *allowed IP addresses* refers to a range of IP addresses that you choose to give permission to access your server. These permissions are called *firewall rules*.

Choose this networking option if you want the following capabilities:

- Connect from Azure resources that don't support virtual networks.
- Connect from resources outside Azure that aren't connected by VPN or Azure ExpressRoute.
- Ensure that the Azure Database for PostgreSQL flexible server instance has a public endpoint that's accessible through the internet.

Characteristics of the public access method include:

- Only the IP addresses that you allow have permission to access your Azure Database for PostgreSQL flexible server instance. By default, no IP addresses are allowed. You can add IP addresses during server creation or afterward.

- Your Azure Database for PostgreSQL flexible server instance has a publicly resolvable DNS name.

- Your Azure Database for PostgreSQL flexible server instance isn't in one of your Azure virtual networks.

- Network traffic to and from your server doesn't go over a private network. The traffic uses the general internet pathways.

### Firewall rules

Server-level firewall rules apply to all databases on the same an Azure Database for PostgreSQL flexible server instance. If the source IP address of the request is within one of the ranges specified in the server-level firewall rules, the connection is granted. Otherwise, it's rejected. For example, if your application connects with the JDBC driver for PostgreSQL, you might encounter this error when you attempt to connect when the firewall is blocking the connection.

```java
java.util.concurrent.ExecutionException: java.lang.RuntimeException: org.postgresql.util.PSQLException: FATAL: no pg_hba.conf entry for host "123.45.67.890", user "adminuser", database "postgresql", SSL
```

> [!NOTE]  
> To access an Azure Database for PostgreSQL flexible server instance from your local computer, ensure that the firewall on your network and local computer allow outgoing communication on TCP port 5432.

### Programmatically managed firewall rules

In addition using to the Azure portal, you can manage firewall rules programmatically by using the Azure CLI. For more information, see [Networking](how-to-manage-firewall-cli.md).

### Allow all Azure IP addresses

We recommend that you find the outgoing IP address of any application or service and explicitly allow access to those individual IP addresses or ranges. If a fixed outgoing IP address isn't available for your Azure service, you can consider enabling connections from all IP addresses for Azure datacenters.

To enable this setting from the Azure portal, on the **Networking** pane, select the **Allow public access from any Azure service within Azure to this server** checkbox and then select **Save**.

> [!IMPORTANT]  
> The **Allow public access from Azure services and resources within Azure** option configures the firewall to allow all connections from Azure, including connections from the subscriptions of other customers. When you select this option, make sure that your sign-in and user permissions limit access to only authorized users.

### Troubleshoot public access issues

Consider the following points when access to an Azure Database for PostgreSQL flexible server instance doesn't behave as you expect:

- **Changes to the allowlist haven't taken effect yet**. There might be as much as a five-minute delay for changes to the firewall configuration of the Azure Database for PostgreSQL flexible server to take effect.

- **Authentication failed**. If a user doesn't have permissions on the Azure Database for PostgreSQL flexible server instance or the password is incorrect, the connection to the Azure Database for PostgreSQL flexible server instance is denied. Creating a firewall setting only provides clients with an opportunity to try connecting to your server. Each client must still provide the necessary security credentials.

- **Dynamic client IP address is preventing access**. If you have an internet connection with dynamic IP addressing and you're having trouble getting through the firewall, try one of the following solutions:

  - Ask your internet service provider (ISP) for the IP address range assigned to your client computers that access the Azure Database for PostgreSQL flexible server instance. Then add the IP address range as a firewall rule.
  - Get static IP addressing instead for your client computers. Then add the static IP address as a firewall rule.

- **Firewall rule isn't available for IPv6 format**. The firewall rules must be in IPv4 format. If you specify firewall rules in IPv6 format, you get a validation error.

## Host name

Regardless of the networking option that you choose, we recommend that you always use an FQDN as host name when connecting to your Azure Database for PostgreSQL flexible server instance. The server's IP address isn't guaranteed to remain static. Using the FQDN helps you avoid making changes to your connection string.

An example that uses an FQDN as a host name is `hostname = servername.postgres.database.azure.com`. Where possible, avoid using `hostname = 10.0.0.4` (a private address) or `hostname = 40.2.45.67` (a public address).

## Outbound IP addresses for firewall configuration

When your Azure Database for PostgreSQL flexible server instance needs to make outbound connections to external services (for example, for logical replication, extensions that connect to external resources, or external data sources), you might need to configure firewall rules on those external services to allow traffic from your database server.

### Finding the server's IP address

To find the IP address currently assigned to your Azure Database for PostgreSQL flexible server instance:

- **Using DNS resolution**: You can resolve the server's FQDN (`servername.postgres.database.azure.com`) to get the current IP address. Use tools like `nslookup` or `dig`:

    ```bash
    nslookup servername.postgres.database.azure.com
    ```

- **Using the Azure portal**: Navigate to your Azure Database for PostgreSQL flexible server instance in the Azure portal. The server's public IP address isn't directly displayed, but you can find it by resolving the server's FQDN.

- **Using Azure CLI**: You can use Azure CLI to get information about your server and then resolve the hostname:

    ```azurecli
    az postgres flexible-server show --resource-group myResourceGroup --name myServerName
    ```

### Important considerations for outbound connections

- **IP addresses can change**: The public IP address assigned to your Azure Database for PostgreSQL flexible server instance isn't static and can change during maintenance, updates, or other operational events. Always use the FQDN when possible, and regularly update external firewall rules if needed.

- **Azure datacenter IP ranges**: For more predictable firewall configuration, you can allow traffic from the entire Azure datacenter IP range for the region where your server is located. Azure publishes the IP ranges for each region in the [Azure IP Ranges and Service Tags](https://www.microsoft.com/download/details.aspx?id=56519) download.

- **Service Tags**: If the external service you're connecting to is also hosted in Azure, consider using [Azure Service Tags](/azure/virtual-network/service-tags-overview) for more dynamic and maintainable firewall rules.

- **Private endpoint alternative**: For more stable connectivity and to avoid public IP addresses, consider using [private endpoints](/azure/postgresql/flexible-server/concepts-networking-private) instead of public access.

## Related content

- [Azure portal](how-to-manage-firewall-portal.md)
- [Azure CLI](how-to-manage-firewall-cli.md)
