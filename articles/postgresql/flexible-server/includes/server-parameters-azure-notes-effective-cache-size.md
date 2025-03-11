---
title: effective_cache_size server parameter
description: effective_cache_size server parameter for Azure Database for PostgreSQL flexible server.
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

The formula used to compute the value of `effective_cache_size` is dependent on the value of `shared_buffers`, and looks like `(memoryGib * 131072) - shared_buffers`.

| Memory size | shared_buffers | effective_cache_size |
| ----------- | -------------- | -------------------- |
|       2 GiB |         32768  |               229376 |
|       4 GiB |        131072  |               393216 |
|       8 GiB |        262144  |               786432 |
|      16 GiB |        524288  |              1572864 |
|      32 GiB |       1048576  |              3145728 |
|      48 GiB |       1572864  |              4718592 |
|      64 GiB |       2097152  |              6291456 |
|      80 GiB |       2621440  |              7864320 |
|     128 GiB |       4194304  |             12582912 |
|     160 GiB |       5242880  |             15728640 |
|     192 GiB |       6291456  |             18874368 |
|     256 GiB |       8388608  |             25165824 |
|     384 GiB |      12582912  |             37748736 |
|     432 GiB |      14155776  |             42467328 |
|     672 GiB |      22020096  |             66060288 |