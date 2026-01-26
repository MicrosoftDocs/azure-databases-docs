---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/26/2026
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### constraint_exclusion

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Enables the planner to use constraints to optimize queries. Table scans will be skipped if their constraints guarantee that no rows match the query. |
| Data type | enumeration |
| Default value | `partition` |
| Allowed values | `partition,on,off` |
| Parameter type | dynamic |
| Documentation | [constraint_exclusion](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-CONSTRAINT-EXCLUSION) |


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
| Documentation | [cursor_tuple_fraction](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-CURSOR-TUPLE-FRACTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_statistics_target

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the default statistics target. This applies to table columns that have not had a column-specific target set via ALTER TABLE SET STATISTICS. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `1-10000` |
| Parameter type | dynamic |
| Documentation | [default_statistics_target](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### from_collapse_limit

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the FROM-list size beyond which subqueries are not collapsed. The planner will merge subqueries into upper queries if the resulting FROM list would have no more than this many items. |
| Data type | integer |
| Default value | `8` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [from_collapse_limit](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-FROM-COLLAPSE-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Allow JIT compilation. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on, off` |
| Parameter type | dynamic |
| Documentation | [jit](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-JIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### join_collapse_limit

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the FROM-list size beyond which JOIN constructs are not flattened. The planner will flatten explicit JOIN constructs into lists of FROM items whenever a list of no more than this many items would result. |
| Data type | integer |
| Default value | `8` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [join_collapse_limit](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-JOIN-COLLAPSE-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### plan_cache_mode

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Controls the planner's selection of custom or generic plan. Prepared statements can have custom and generic plans, and the planner will attempt to choose which is better. This can be set to override the default behavior. |
| Data type | enumeration |
| Default value | `auto` |
| Allowed values | `auto,force_generic_plan,force_custom_plan` |
| Parameter type | dynamic |
| Documentation | [plan_cache_mode](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-PLAN-CACHE-MODE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### recursive_worktable_factor

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Other Planner Options |
| Description | Sets the planner's estimate of the average size of a recursive query's working table. |
| Data type | numeric |
| Default value | `10` |
| Allowed values | `10` |
| Parameter type | read-only |
| Documentation | [recursive_worktable_factor](https://www.postgresql.org/docs/17/runtime-config-query.html#GUC-RECURSIVE-WORKTABLE-FACTOR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



