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
### autovacuum

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Starts the autovacuum subprocess. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [autovacuum](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_analyze_scale_factor

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Number of tuple inserts, updates, or deletes prior to analyze as a fraction of reltuples. |
| Data type | numeric |
| Default value | `0.1` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | [autovacuum_analyze_scale_factor](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_analyze_threshold

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Minimum number of tuple inserts, updates, or deletes prior to analyze. |
| Data type | integer |
| Default value | `50` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [autovacuum_analyze_threshold](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-ANALYZE-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_freeze_max_age

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Age at which to autovacuum a table to prevent transaction ID wraparound. |
| Data type | integer |
| Default value | `200000000` |
| Allowed values | `100000-2000000000` |
| Parameter type | static |
| Documentation | [autovacuum_freeze_max_age](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_max_workers

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Sets the maximum number of simultaneously running autovacuum worker processes. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-262143` |
| Parameter type | dynamic |
| Documentation | [autovacuum_max_workers](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-MAX-WORKERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_multixact_freeze_max_age

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Multixact age at which to autovacuum a table to prevent multixact wraparound. |
| Data type | integer |
| Default value | `400000000` |
| Allowed values | `10000-2000000000` |
| Parameter type | static |
| Documentation | [autovacuum_multixact_freeze_max_age](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_naptime

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Time to sleep between autovacuum runs. |
| Data type | integer |
| Default value | `60` |
| Allowed values | `1-2147483` |
| Parameter type | dynamic |
| Documentation | [autovacuum_naptime](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-NAPTIME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_cost_delay

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Vacuum cost delay in milliseconds, for autovacuum. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `-1-100` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_cost_delay](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_cost_limit

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Vacuum cost amount available before napping, for autovacuum. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-10000` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_cost_limit](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_insert_scale_factor

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Number of tuple inserts prior to vacuum as a fraction of reltuples. |
| Data type | numeric |
| Default value | `0.2` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_insert_scale_factor](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_insert_threshold

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Minimum number of tuple inserts prior to vacuum, or -1 to disable insert vacuums. |
| Data type | integer |
| Default value | `1000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_insert_threshold](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_max_threshold

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Maximum number of tuple updates or deletes prior to vacuum. -1 disables the maximum threshold. |
| Data type | integer |
| Default value | `100000000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_max_threshold](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_scale_factor

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Number of tuple updates or deletes prior to vacuum as a fraction of reltuples. |
| Data type | numeric |
| Default value | `0.2` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_scale_factor](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_threshold

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Minimum number of tuple updates or deletes prior to vacuum. |
| Data type | integer |
| Default value | `50` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_threshold](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_worker_slots

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Sets the number of backend slots to allocate for autovacuum workers. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `1-262143` |
| Parameter type | static |
| Documentation | [autovacuum_worker_slots](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-WORKER-SLOTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_max_eager_freeze_failure_rate

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Fraction of pages in a relation vacuum can scan and fail to freeze before disabling eager scanning. A value of 0.0 disables eager scanning and a value of 1.0 will eagerly scan up to 100 percent of the all-visible pages in the relation. If vacuum successfully freezes these pages, the cap is lower than 100 percent, because the goal is to amortize page freezing across multiple vacuums. |
| Data type | numeric |
| Default value | `0.03` |
| Allowed values | `0.0-1.0` |
| Parameter type | dynamic |
| Documentation | [vacuum_max_eager_freeze_failure_rate](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_truncate

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Enables vacuum to truncate empty pages at the end of the table. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [vacuum_truncate](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-VACUUM-TRUNCATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



