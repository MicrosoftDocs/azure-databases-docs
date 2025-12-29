---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 12/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### allow_alter_system

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Other Platforms and Clients |
| Description | Allows running the ALTER SYSTEM command. Can be set to off for environments where global configuration changes should be made using a different method. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [allow_alter_system](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-ALLOW-ALTER-SYSTEM) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### transform_null_equals

| Attribute | Value |
| --- | --- |
| Category | Version and Platform Compatibility / Other Platforms and Clients |
| Description | Treats \"expr=NULL\" as \"expr IS NULL\". When turned on, expressions of the form expr = NULL (or NULL = expr) are treated as expr IS NULL, that is, they return true if expr evaluates to the null value, and false otherwise. The correct behavior of expr = NULL is to always return null (unknown). |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [transform_null_equals](https://www.postgresql.org/docs/18/runtime-config-compatible.html#GUC-TRANSFORM-NULL-EQUALS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



