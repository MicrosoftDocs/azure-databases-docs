---
title: shared_buffers server parameter
description: shared_buffers server parameter for Azure Database for PostgreSQL - Flexible Server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Description

The `shared_buffers` configuration parameter determines the amount of system memory allocated to the PostgreSQL database for buffering data. It serves as a centralized memory pool that's accessible to all database processes.

When data is needed, the database process first checks the shared buffer. If the required data is present, it's quickly retrieved and bypasses a more time-consuming disk read. Shared buffers serve as an intermediary between the database processes and the disk, and effectively reduces the number of required I/O operations.

#### Azure-specific notes
The default value for the `shared_buffers` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server don't have any effect on the default value for the `shared_buffers` server parameter of that instance.

Every time you change the product assigned to an instance, you should also adjust the value for the `shared_buffers` parameter according to the values in the following formulas.

For virtual machines with up to 2 GiB of memory, the formula used to compute the value of `shared_buffers` is `memoryGb * 16`.

For virtual machines with more than 2 GiB, the formula used to compute the value of `shared_buffers` is `memoryGb * 32`.