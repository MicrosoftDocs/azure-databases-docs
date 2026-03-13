---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### cpu_index_tuple_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of processing each index entry during an index scan. |
| Data type | numeric |
| Default value | `0.005` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [cpu_index_tuple_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-CPU-INDEX-TUPLE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cpu_operator_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of processing each operator or function call. |
| Data type | numeric |
| Default value | `0.0025` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [cpu_operator_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-CPU-OPERATOR-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cpu_tuple_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of processing each tuple (row). |
| Data type | numeric |
| Default value | `0.01` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [cpu_tuple_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-CPU-TUPLE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### effective_cache_size

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's assumption about the total size of the data caches. That is, the total size of the caches (kernel cache and shared buffers) used for PostgreSQL data files. This is measured in disk pages, which are normally 8 kB each. |
| Data type | integer |
| Default value | Depends on resources (vCores, RAM, or disk space) allocated to the server. |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [effective_cache_size](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE) |


[!INCLUDE [server-parameters-azure-notes-effective-cache-size](./server-parameters-azure-notes-effective-cache-size.md)]



### jit_above_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Perform JIT compilation if query is more expensive. -1 disables JIT compilation. |
| Data type | integer |
| Default value | `100000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [jit_above_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-JIT-ABOVE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_inline_above_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Perform JIT inlining if query is more expensive. -1 disables inlining. |
| Data type | integer |
| Default value | `500000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [jit_inline_above_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-JIT-INLINE-ABOVE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_optimize_above_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Optimize JIT-compiled functions if query is more expensive. -1 disables optimization. |
| Data type | integer |
| Default value | `500000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [jit_optimize_above_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-JIT-OPTIMIZE-ABOVE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### min_parallel_index_scan_size

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the minimum amount of index data for a parallel scan. If the planner estimates that it will read a number of index pages too small to reach this limit, a parallel scan will not be considered. |
| Data type | integer |
| Default value | `64` |
| Allowed values | `0-715827882` |
| Parameter type | dynamic |
| Documentation | [min_parallel_index_scan_size](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-MIN-PARALLEL-INDEX-SCAN-SIZE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### min_parallel_table_scan_size

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the minimum amount of table data for a parallel scan. If the planner estimates that it will read a number of table pages too small to reach this limit, a parallel scan will not be considered. |
| Data type | integer |
| Default value | `1024` |
| Allowed values | `0-715827882` |
| Parameter type | dynamic |
| Documentation | [min_parallel_table_scan_size](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-MIN-PARALLEL-TABLE-SCAN-SIZE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### parallel_setup_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of starting up worker processes for parallel query. |
| Data type | numeric |
| Default value | `1000` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [parallel_setup_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-PARALLEL-SETUP-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### parallel_tuple_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of passing each tuple (row) from worker to leader backend. |
| Data type | numeric |
| Default value | `0.1` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [parallel_tuple_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-PARALLEL-TUPLE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### random_page_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of a nonsequentially fetched disk page. |
| Data type | numeric |
| Default value | `2` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [random_page_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-RANDOM-PAGE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### seq_page_cost

| Attribute | Value |
| --- | --- |
| Category | Query Tuning / Planner Cost Constants |
| Description | Sets the planner's estimate of the cost of a sequentially fetched disk page. |
| Data type | numeric |
| Default value | `1` |
| Allowed values | `0-1.79769e+308` |
| Parameter type | dynamic |
| Documentation | [seq_page_cost](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-SEQ-PAGE-COST) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



