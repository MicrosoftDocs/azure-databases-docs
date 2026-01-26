---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### deadlock_timeout

| Attribute | Value |
| --- | --- |
| Category | Lock Management |
| Description | Sets the time to wait on a lock before checking for deadlock. |
| Data type | integer |
| Default value | `1000` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [deadlock_timeout](https://www.postgresql.org/docs/17/runtime-config-locks.html#GUC-DEADLOCK-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_locks_per_transaction

| Attribute | Value |
| --- | --- |
| Category | Lock Management |
| Description | Sets the maximum number of locks per transaction. The shared lock table is sized on the assumption that at most \"max_locks_per_transaction\" objects per server process or prepared transaction will need to be locked at any one time. |
| Data type | integer |
| Default value | `64` |
| Allowed values | `10-8388608` |
| Parameter type | static |
| Documentation | [max_locks_per_transaction](https://www.postgresql.org/docs/17/runtime-config-locks.html#GUC-MAX-LOCKS-PER-TRANSACTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_pred_locks_per_page

| Attribute | Value |
| --- | --- |
| Category | Lock Management |
| Description | Sets the maximum number of predicate-locked tuples per page. If more than this number of tuples on the same page are locked by a connection, those locks are replaced by a page-level lock. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [max_pred_locks_per_page](https://www.postgresql.org/docs/17/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-PAGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_pred_locks_per_relation

| Attribute | Value |
| --- | --- |
| Category | Lock Management |
| Description | Sets the maximum number of predicate-locked pages and tuples per relation. If more than this total of pages and tuples in the same relation are locked by a connection, those locks are replaced by a relation-level lock. |
| Data type | integer |
| Default value | `-2` |
| Allowed values | `-2147483648-2147483647` |
| Parameter type | dynamic |
| Documentation | [max_pred_locks_per_relation](https://www.postgresql.org/docs/17/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-RELATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_pred_locks_per_transaction

| Attribute | Value |
| --- | --- |
| Category | Lock Management |
| Description | Sets the maximum number of predicate locks per transaction. The shared predicate lock table is sized on the assumption that at most \"max_pred_locks_per_transaction\" objects per server process or prepared transaction will need to be locked at any one time. |
| Data type | integer |
| Default value | `64` |
| Allowed values | `64` |
| Parameter type | read-only |
| Documentation | [max_pred_locks_per_transaction](https://www.postgresql.org/docs/17/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-TRANSACTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



