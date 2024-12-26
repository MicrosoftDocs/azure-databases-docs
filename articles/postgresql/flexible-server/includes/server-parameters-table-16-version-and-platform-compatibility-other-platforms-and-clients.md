---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 12/05/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### transform_null_equals

| Attribute      | Value                                                      |
|----------------|------------------------------------------------------------|
| Category       | Version and Platform Compatibility / Other Platforms and Clients |
| Description    | When on, expressions of the form expr = NULL (or NULL = expr) are treated as expr IS NULL, that is, they return true if expr evaluates to the null value, and false otherwise. |
| Data type      | boolean   |
| Default value  | `off`         |
| Allowed values | `on,off`       |
| Parameter type | dynamic        |
| Documentation  | [transform_null_equals](https://www.postgresql.org/docs/16/runtime-config-compatible.html#GUC-TRANSFORM-NULL-EQUALS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



