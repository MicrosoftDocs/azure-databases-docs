---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### vacuum_defer_cleanup_age

| Attribute | Value |
| --- | --- |
| Category | Replication / Primary Server |
| Description | Specifies the number of transactions by which VACUUM and HOT updates will defer cleanup of dead row versions. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-1000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_defer_cleanup_age](https://www.postgresql.org/docs/13/runtime-config-replication.html#GUC-VACUUM-DEFER-CLEANUP-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



