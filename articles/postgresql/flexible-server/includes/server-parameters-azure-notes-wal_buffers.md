---
title: wal_buffers server parameter
description: wal_buffers server parameter for Azure Database for PostgreSQL - Flexible Server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `wal_buffers` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server won't have any effect on the default value for the `wal_buffers` server parameter of that instance.

In virtual machines with up to 4 vCores, the value computed for `wal_buffers` is `2048`.

In virtual machines with more than 4 vCores, the value computed for `wal_buffers` is `16384`.