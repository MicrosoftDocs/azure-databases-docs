---
title: "azure_storage.blob_block_size_mb Server Parameter"
description: azure_storage.blob_block_size_mb server parameter for Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.topic: include
---

#### Azure-specific notes

The default value for the `azure_storage.blob_block_size_mb` server parameter is calculated when you provision the instance of Azure HorizonDB, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the flexible server won't have any effect on the default value for the `azure_storage.blob_block_size_mb` server parameter of that instance.

As of today, if you change the product assigned to an instance, you won't be able to adjust the value of `azure_storage.blob_block_size_mb` parameter because the parameter is declared as read-only.

The formula used to compute the value of `azure_storage.blob_block_size_mb` is `MIN(3072, MAX(128, memoryGiB * 32))`.

Based on the previous formula, the following table lists the values this server parameter would be set to depending on the amount of memory provisioned:

| Memory size | azure_storage.blob_block_size_mb |
| --- | --- |
| 2 GiB | 128 MiB |
| 4 GiB | 128 MiB |
| 8 GiB | 256 MiB |
| 16 GiB | 512 MiB |
| 32 GiB | 1024 MiB |
| 48 GiB | 1536 MiB |
| 64 GiB | 2048 MiB |
| 80 GiB | 2560 MiB |
| 128 GiB | 3072 MiB |
| 160 GiB | 3072 MiB |
| 192 GiB | 3072 MiB |
| 256 GiB | 3072 MiB |
| 384 GiB | 3072 MiB |
| 432 GiB | 3072 MiB |
| 672 GiB | 3072 MiB |
