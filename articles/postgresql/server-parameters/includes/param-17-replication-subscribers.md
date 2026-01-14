---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### max_logical_replication_workers

| Attribute | Value |
| --- | --- |
| Category | Replication / Subscribers |
| Description | Maximum number of logical replication worker processes. |
| Data type | integer |
| Default value | `4` |
| Allowed values | `0-262143` |
| Parameter type | static |
| Documentation | [max_logical_replication_workers](https://www.postgresql.org/docs/17/runtime-config-replication.html#GUC-MAX-LOGICAL-REPLICATION-WORKERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_parallel_apply_workers_per_subscription

| Attribute | Value |
| --- | --- |
| Category | Replication / Subscribers |
| Description | Maximum number of parallel apply workers per subscription. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `0-1024` |
| Parameter type | dynamic |
| Documentation | [max_parallel_apply_workers_per_subscription](https://www.postgresql.org/docs/17/runtime-config-replication.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_sync_workers_per_subscription

| Attribute | Value |
| --- | --- |
| Category | Replication / Subscribers |
| Description | Maximum number of table synchronization workers per subscription. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `0-262143` |
| Parameter type | dynamic |
| Documentation | [max_sync_workers_per_subscription](https://www.postgresql.org/docs/17/runtime-config-replication.html#GUC-MAX-SYNC-WORKERS-PER-SUBSCRIPTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



