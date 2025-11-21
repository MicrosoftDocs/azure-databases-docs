---
title: max_wal_size server parameter
description: max_wal_size server parameter for Azure Database for PostgreSQL flexible server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/07/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `max_wal_size` server parameter is calculated when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server won't have any effect on the default value for the `max_wal_size` server parameter of that instance.

Every time you change the size of the disk assigned to the instance, you should also adjust the value for the `max_wal_size` parameter according to the values listed in the following table.

The value is computed based on the size of the disk chosen for the instance, as indicated in the following table:

| Disks size | max_wal_size |
| ---------- | ------------ |
|     32 GiB |    2048  MiB |
|     64 GiB |    4096  MiB |
|    128 GiB |   12288  MiB |
|    256 GiB |   20480  MiB |
|    512 GiB |   25600  MiB |
|    512 GiB |   25600  MiB |
|      1 TiB |   30720  MiB |
|      2 TiB |   40960  MiB |
|      4 TiB |   40960  MiB |
|      8 TiB |   65536  MiB |
|     16 TiB |   65536  MiB |
|     32 TiB |   65536  MiB |