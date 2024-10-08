---
title: azure_storage.blob_block_size_mb server parameter
description: azure_storage.blob_block_size_mb server parameter for Azure Database for PostgreSQL - Flexible Server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `azure_storage.blob_block_size_mb` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server won't have any effect on the default value for the `azure_storage.blob_block_size_mb` server parameter of that instance.

Every time you change the product assigned to an instance, you should also adjust the value for the `azure_storage.blob_block_size_mb` parameter according to the values in the following formula.

The formula used to compute the value of `azure_storage.blob_block_size_mb` is `MIN(3072, MAX(128, memoryMb / 32))`.
