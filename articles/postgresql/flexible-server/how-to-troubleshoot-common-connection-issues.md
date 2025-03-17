---
title: Troubleshoot connections
description: Learn how to troubleshoot connection issues to Azure Database for PostgreSQL flexible server.
author: assaff
ms.author: assaff
ms.reviewer: maghan
ms.date: 04/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Troubleshoot connection issues to Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Connection problems may be caused by various things, including:

* Firewall settings
* Connection time-out
* Incorrect login information
* Maximum limit reached on some Azure Database for PostgreSQL flexible server resources
* Issues with the infrastructure of the service
* Maintenance being performed in the service
* The compute allocation of the server is changed by scaling the number of vCores or moving to a different service tier

Generally, connection issues to Azure Database for PostgreSQL flexible server can be classified as follows:

* Transient errors (short-lived or intermittent)
* Persistent or non-transient errors (errors that regularly recur)

## Troubleshoot transient errors

Transient errors occur when maintenance is performed, the system encounters an error with the hardware or software, or you change the vCores or service tier of your server. Azure Database for PostgreSQL flexible server has built-in high availability and is designed to mitigate these types of problems automatically. However, your application loses its connection to the server for a short period of time of typically less than 60 seconds at most. Some events can occasionally take longer to mitigate, such as when a large transaction causes a long-running recovery.

### Steps to resolve transient connectivity issues

1. Check the [Microsoft Azure Service Dashboard](https://azure.microsoft.com/status) for any known outages that occurred during the time in which the errors were reported by the application.
2. Applications that connect to a cloud service such as Azure Database for PostgreSQL flexible server should expect transient errors and implement retry logic to handle these errors instead of surfacing these as application errors to users. Review [Handling of transient connectivity errors - Azure Database for PostgreSQL flexible server](concepts-connectivity.md) for best practices and design guidelines for handling transient errors.
3. As a server approaches its resource limits, errors can seem to be transient connectivity issue. See [Limitations - Azure Database for PostgreSQL flexible server](concepts-limits.md).
4. If connectivity problems continue, or if the duration for which your application encounters the error exceeds 60 seconds or if you see multiple occurrences of the error in a given day, file an Azure support request by selecting **Get Support** on the [Azure Support](https://azure.microsoft.com/support/options) site.

## Troubleshoot persistent errors

If the application persistently fails to connect to Azure Database for PostgreSQL flexible server, it usually indicates an issue with one of the following:

- Server firewall configuration: Make sure that the Azure Database for PostgreSQL flexible server firewall is configured to allow connections from your client, including proxy servers and gateways.
- Client firewall configuration: The firewall on your client must allow connections to your database server. IP addresses and ports of the server that you can't connect to must be allowed and the application names such as PostgreSQL in some firewalls.
- If you see the error _Server isn't configured to allow ipv6 connections_, note that the Basic tier doesn't support VNet service endpoints. You have to remove the Microsoft.Sql endpoint from the subnet that is attempting to connect to the Basic server.
- If you see the connection error _sslmode value "\*\*" invalid when SSL support isn't compiled in_ error, it means your PostgreSQL client doesn't support SSL. Most probably, the client-side libpq hasn't been compiled with the "--with-openssl" flag. Try connecting with a PostgreSQL client that has SSL support.

### Steps to resolve persistent connectivity issues

1. Set up [firewall rules](concepts-firewall-rules.md) to allow the client IP address. For temporary testing purposes only, set up a firewall rule using 0.0.0.0 as the starting IP address and using 255.255.255.255 as the ending IP address. This will open the server to all IP addresses. If this resolves your connectivity issue, remove this rule and create a firewall rule for an appropriately limited IP address or address range.
2. On all firewalls between the client and the internet, make sure that port 5432 is open for outbound connections.
3. Verify your connection string and other connection settings.
4. Check the service health in the dashboard. If you think there’s a regional outage, see [Overview of business continuity - Azure Database for PostgreSQL flexible server](concepts-business-continuity.md) for steps to recover to a new region.

## Related content

- [Handling transient connectivity errors in Azure Database for PostgreSQL flexible server](concepts-connectivity.md).
