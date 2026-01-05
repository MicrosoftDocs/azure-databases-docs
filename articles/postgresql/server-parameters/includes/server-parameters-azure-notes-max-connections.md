---
title: max_connections server parameter
description: max_connections server parameter for Azure Database for PostgreSQL flexible server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `max_connections` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server don't have any effect on the default value for the `max_connections` server parameter of that instance.

Every time you change the product assigned to an instance, you should also adjust the value for the `max_connections` parameter according to the values in the following formula.

In virtual machines with up to 2 GiB of memory, the formula used to compute the value of `max_connections` is `memoryGib * 25`.

In virtual machines with more than 2 GiB, the formula used to compute the value of `max_connections` is `MIN(memoryGib * 0.1049164697034809, 5000)`.

Based on the previous formula, the following table lists the values this server parameter would be set to depending on the amount of memory provisioned:

| Memory size | max_connections |
| ----------- | --------------- |
|       2 GiB |              50 |
|       4 GiB |             429 |
|       8 GiB |             859 |
|      16 GiB |            1718 |
|      32 GiB |            3437 |
|      48 GiB |            5000 |
|      64 GiB |            5000 |
|      80 GiB |            5000 |
|     128 GiB |            5000 |
|     160 GiB |            5000 |
|     192 GiB |            5000 |
|     256 GiB |            5000 |
|     384 GiB |            5000 |
|     432 GiB |            5000 |
|     672 GiB |            5000 |

Refer to [Maximum connections](../../configure-maintain/concepts-limits.md#maximum-connections) for more information about this parameter in Azure Database for PostgreSQL flexible server.