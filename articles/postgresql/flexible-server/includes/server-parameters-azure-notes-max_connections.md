---
title: max_connections server parameter
description: max_connections server parameter for Azure Database for PostgreSQL - Flexible Server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `max_connections` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server won't have any effect on the default value for the `max_connections` server parameter of that instance.

In virtual machines with up to 2GiB of memory, the formula used to compute the value of `max_connections` is `memoryGb * 25`.

In virtual machines with more than 2GiB, the formula used to compute the value of `max_connections` is `MIN(memoryGb * 0.1049164697034809, 5000)`.

For more information about `max_connections` in Azure Database for Flexible Server, refer to [Maximum connections](../concepts-limits.md#maximum-connections)