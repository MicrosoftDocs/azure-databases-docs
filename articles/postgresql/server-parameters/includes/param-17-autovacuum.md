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
### autovacuum

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Starts the autovacuum subprocess. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [autovacuum](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM) |


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
| Documentation | [autovacuum_analyze_scale_factor](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR) |


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
| Documentation | [autovacuum_analyze_threshold](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-THRESHOLD) |


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
| Documentation | [autovacuum_freeze_max_age](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_max_workers

| Attribute | Value |
| --- | --- |
| Category | Autovacuum |
| Description | Sets the maximum number of simultaneously running autovacuum worker processes. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-262143` |
| Parameter type | static |
| Documentation | [autovacuum_max_workers](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MAX-WORKERS) |


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
| Documentation | [autovacuum_multixact_freeze_max_age](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MULTIXACT-FREEZE-MAX-AGE) |


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
| Documentation | [autovacuum_naptime](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME) |


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
| Documentation | [autovacuum_vacuum_cost_delay](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY) |


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
| Documentation | [autovacuum_vacuum_cost_limit](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT) |


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
| Documentation | [autovacuum_vacuum_insert_scale_factor](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR) |


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
| Documentation | [autovacuum_vacuum_insert_threshold](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD) |


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
| Documentation | [autovacuum_vacuum_scale_factor](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR) |


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
| Documentation | [autovacuum_vacuum_threshold](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



