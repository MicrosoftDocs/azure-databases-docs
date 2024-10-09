---
title: effective_cache_size server parameter
description: effective_cache_size server parameter for Azure Database for PostgreSQL - Flexible Server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `effective_cache_size` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server won't have any effect on the default value for the `effective_cache_size` server parameter of that instance.

Every time you change the product assigned to an instance, you should also adjust the value for the `effective_cache_size` parameter according to the values in the following formula.

The formula used to compute the value of `effective_cache_size` is dependent on the value of `shared_buffers`, and looks like `(memoryMb - (shared_buffers * 8 / 1024)) * 1024 / 8`.