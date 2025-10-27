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
### constraint_exclusion

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Controls the query planner's use of table constraints to optimize queries. |
| Data type | enumeration |
| Default value | `partition` |
| Allowed values | `partition,on,off` |
| Parameter type | dynamic |
| Documentation | [constraint_exclusion](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-CONSTRAINT-EXCLUSION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cursor_tuple_fraction

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the planner's estimate of the fraction of a cursor's rows that will be retrieved. |
| Data type | numeric |
| Default value | `0.1` |
| Allowed values | `0-1` |
| Parameter type | dynamic |
| Documentation | [cursor_tuple_fraction](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-CURSOR-TUPLE-FRACTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_statistics_target

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the default statistics target for table columns without a column-specific target. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `1-10000` |
| Parameter type | dynamic |
| Documentation | [default_statistics_target](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### from_collapse_limit

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | The planner will merge sub-queries into upper queries upto this limit in FROM clause. Smaller values reduce planning time but might yield inferior query plans. |
| Data type | integer |
| Default value | `8` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [from_collapse_limit](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-FROM-COLLAPSE-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Determines whether JIT compilation may be used by PostgreSQL. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [jit](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-JIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### join_collapse_limit

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the FROM-list size beyond which JOIN constructs are not flattened. |
| Data type | integer |
| Default value | `8` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [join_collapse_limit](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-JOIN-COLLAPSE-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### plan_cache_mode

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Controls the planner's selection of custom or generic plan. |
| Data type | enumeration |
| Default value | `auto` |
| Allowed values | `auto,force_generic_plan,force_custom_plan` |
| Parameter type | dynamic |
| Documentation | [plan_cache_mode](https://www.postgresql.org/docs/13/runtime-config-query.html#id-1.6.6.10.5.2.9.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



