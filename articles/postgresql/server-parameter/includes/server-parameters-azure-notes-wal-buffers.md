---
title: wal_buffers server parameter
description: wal_buffers server parameter for Azure Database for PostgreSQL flexible server.
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

Every time you change the product assigned to an instance, you should also adjust the value for the `wal_buffers` parameter according to the values in the following formula.

In virtual machines with up to 4 vCores, the value computed for `wal_buffers` is `2048`.

In virtual machines with more than 4 vCores, the value computed for `wal_buffers` is `16384`.

Based on the previous formula, the following table lists the values this server parameter would be set to depending on the amount of memory provisioned:

| vCores | wal_buffers |
| ------ | ----------- |
|      1 |        2048 |
|      2 |        2048 |
|      4 |        2048 |
|      8 |       16384 |
|     12 |       16384 |
|     16 |       16384 |
|     20 |       16384 |
|     32 |       16384 |
|     48 |       16384 |
|     64 |       16384 |
|     96 |       16384 |