---
title: shared_buffers server parameter
description: shared_buffers server parameter for Azure Database for PostgreSQL flexible server.
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

For virtual machines with up to 2 GiB of memory, the formula used to compute the value of `shared_buffers` is `memoryGib * 16384`.

For virtual machines with more than 2 GiB, the formula used to compute the value of `shared_buffers` is `memoryGib * 32768`.

Based on the previous formula, the following table lists the values this server parameter would be set to depending on the amount of memory provisioned:

| Memory size | shared_buffers |
| ----------- | -------------- |
|       2 GiB |         32768  |
|       4 GiB |        131072  |
|       8 GiB |        262144  |
|      16 GiB |        524288  |
|      32 GiB |       1048576  |
|      48 GiB |       1572864  |
|      64 GiB |       2097152  |
|      80 GiB |       2621440  |
|     128 GiB |       4194304  |
|     160 GiB |       5242880  |
|     192 GiB |       6291456  |
|     256 GiB |       8388608  |
|     384 GiB |      12582912  |
|     432 GiB |      14155776  |
|     672 GiB |      22020096  |