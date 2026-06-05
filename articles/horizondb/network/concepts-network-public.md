---
title: Networking Overview with Public Access (Allowed IP Addresses) in Azure HorizonDB
description: Learn about connectivity and networking with public access in Azure HorizonDB.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.topic: concept-article
ms.custom:
  - build-2026-public-preview
---

# Networking overview with public access (allowed IP addresses) and private endpoints in Azure HorizonDB

This article describes connectivity and networking concepts for Azure HorizonDB.

When you create an Azure HorizonDB instance, the only available connectivity method is **Public access (allowed IP addresses) and private endpoints**.

The following characteristics apply to this connectivity mode:

- Connections from allowed IP addresses need to authenticate to the Azure HorizonDB instance with valid credentials.
- Connection encryption is enforced for your network traffic.
- The server has a fully qualified domain name (FQDN). For the `hostname` property in connection strings, we recommend using the fully qualified domain name instead of an IP address.
- Both options control access at the server level, not at the database or table level. You would use PostgreSQL's role properties to control database, table, and other object access.

> [!NOTE]  
> Because the Azure HorizonDB service is a managed database service, users aren't provided host or operating system access to view or modify configuration files such as `pg_hba.conf`. The content of the files is automatically updated based on the network settings.

## Use public access networking with Azure HorizonDB

With public access connectivity method, your Azure HorizonDB cluster is accessed through a public endpoint over the internet. The public endpoint is a publicly resolvable DNS address. The phrase *allowed IP addresses* refers to a range of IP addresses that you choose to give permission to access the replicas of your cluster. These permissions are called *firewall rules*.

This connectivity method gives you the following capabilities:

- Connect from Azure resources that don't support virtual networks.
- Connect from resources outside Azure that aren't connected via VPN or Azure ExpressRoute.
- Ensure that the Azure HorizonDB cluster has a public endpoint that's accessible through the internet.

Characteristics of the public access connectivity method include:

- Only the IP addresses that you allow have permission to access the replicas of your Azure HorizonDB cluster. By default, no IP addresses are allowed. You can add IP addresses during server creation or afterwards.
- Your Azure HorizonDB cluster has a publicly resolvable DNS name.
- Your Azure HorizonDB cluster isn't in one of your Azure virtual networks.
- Network traffic to and from your cluster doesn't go over a private network. The traffic uses the general internet pathways.

### Firewall rules

Cluster-level firewall rules apply to all databases on the Azure HorizonDB cluster. If the source IP address of the request is within one of the ranges specified in the cluster-level firewall rules, the connection is granted. Otherwise, it's rejected. For example, if your application connects with the JDBC driver for PostgreSQL, you might encounter this error when you attempt to connect when the firewall is blocking the connection.

```java
java.util.concurrent.ExecutionException: java.lang.RuntimeException: org.postgresql.util.PSQLException: FATAL: no pg_hba.conf entry for host "123.45.67.890", user "administratorlogin", database "postgresql", SSL
```

> [!NOTE]  
> To access an Azure HorizonDB cluster from your local computer, ensure that the firewall on your network and local computer allow outgoing communication on TCP port 5432.

You can manage firewall rules using Azure portal, Azure CLI, SDKs or REST APIs. For more information, see [Networking in Azure HorizonDB (Preview)](how-to-network.md).

### Allow all Azure IP addresses

We recommend that you find the outgoing IP address of any application or service and explicitly allow access to the individual IP addresses or ranges it uses to route traffice on the internet. If a fixed outgoing IP address isn't available for your Azure service, you can consider enabling connections from all IP addresses for Azure datacenters.

To enable this setting, select your Azure HorizonDB cluster in Azure portal. In the resource menu, under **Settings**, select **Networking**. Finally, select the **Allow public access from any Azure service within Azure to this cluster**, and select **Save**.

> [!IMPORTANT]  
> The **Allow public access from Azure services and resources within Azure** option configures the firewall to allow all connections from Azure, including connections from the subscriptions of other customers. When you select this option, make sure that your sign-in and user permissions limit access to only authorized users.

### Troubleshoot public access issues

Consider the following points when trying to connect to your Azure HorizonDB cluster and failing to do so:

- **Recent changes to firewall rules might haven't taken effect yet**: There might be as much as a five-minute delay for changes to the firewall configuration of the Azure HorizonDB to take effect.
- **Connectivity works but authentication fails**. If a login doesn't have permissions on the Azure HorizonDB cluster or the password is incorrect, the connection to the Azure HorizonDB cluster is denied. Creating a firewall rule only provides clients connecting from a given IP address to route network packets to the cluster. Each client must still provide the necessary security credentials to be able to connect to the cluster.
- **Dynamically assigned client IP address might be the issue**. If you have an internet connection with dynamic IP addressing, it might be the case that your outgoing traffic IP address has changed from the one for which you configured a firewall rule to the one with which you're accessing the internet on current connection attempt. In that case, try one of the following solutions:
  - Ask your internet service provider (ISP) for the IP address range assigned to your client computers, with which you would be accessing the Azure HorizonDB cluster. Then add that IP address range as a firewall rule.
  - Get an static IP address instead for your client computers. Add that static IP address as a firewall rule.
- **Firewall rule isn't available for IPv6 format**. The firewall rules must be in IPv4 format. If you specify firewall rules in IPv6 format, you get a validation error.

## Host name

Regardless of the networking option that you choose, we recommend that you always use a fully qualified domain name as the name of the host, when connecting to your Azure HorizonDB cluster. The cluster's IP address isn't guaranteed to remain static. Using the fully qualified domain name helps you avoid making changes to your connection string.

An example that uses a fully qualified domain name as a host name is `hostname = clustername.clusteridentifier.location.horizondb.azure.com`. Where possible, avoid using `hostname = 40.2.45.67` (or whatever public address you have determined via DNS resolution that is assigned to your cluster at some point).

## Outbound IP addresses for firewall configuration

When your Azure HorizonDB cluster needs to make outbound connections to external services (for example, for logical replication, extensions that connect to external resources, or external data sources), you might need to configure firewall rules on those external services to allow traffic from your database server.

<a id="finding-the-servers-ip-address"></a>

### Find the IP address assigned to the cluster

To find the IP address currently assigned to your Azure HorizonDB cluster:

- **Using DNS resolution**: You can resolve the fully qualified domain name of your cluster's read-write (`clustername.clusteridentifier.location.horizondb.azure.com`) to get the current IP address. Use tools like `nslookup` or `dig`:

  ```bash
  nslookup clustername.clusteridentifier.location.horizondb.azure.com
  ```

- **Using Azure portal**: Navigate to your Azure HorizonDB cluster. In the resource menu, on the **Overview** page, copy the fully qualified domain name of your cluster from the value assigned to **Primary endpoint (read/write)**, and resolve its IP address.

<!--
- **Using Azure CLI**: You can use Azure CLI to get information about your server and then resolve the hostname:

  ```azurecli
  az postgres flexible-server show --resource-group myResourceGroup --name myServerName
  ```

### Important considerations for outbound connections

- **IP addresses can change**: The public IP address assigned to your Azure HorizonDB instance isn't static and can change during maintenance, updates, or other operational events. Always use the FQDN when possible, and regularly update external firewall rules if needed.

- **Azure datacenter IP ranges**: For more predictable firewall configuration, you can allow traffic from the entire Azure datacenter IP range for the region where your server is located. Azure publishes the IP ranges for each region in the [Azure IP Ranges and Service Tags](https://www.microsoft.com/download/details.aspx?id=56519) download.

- **Service Tags**: If the external service you're connecting to is also hosted in Azure, consider using [Azure Service Tags](/azure/virtual-network/service-tags-overview) for more dynamic and maintainable firewall rules.

- **Private endpoint alternative**: For more stable connectivity and to avoid public IP addresses, consider using [private endpoints](/azure/postgresql/flexible-server/concepts-networking-private) instead of public access.
-->
## Related content

- [Networking in Azure HorizonDB (Preview)](how-to-network.md)
