---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### backend_flush_after

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Number of pages after which previously performed writes are flushed to disk. |
| Data type | integer |
| Default value | `256` |
| Allowed values | `0-256` |
| Parameter type | dynamic |
| Documentation | [backend_flush_after](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-BACKEND-FLUSH-AFTER) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### effective_io_concurrency

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Number of simultaneous requests that can be handled efficiently by the disk subsystem. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `0-1000` |
| Parameter type | dynamic |
| Documentation | [effective_io_concurrency](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### file_copy_method

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Selects the file copy method. |
| Data type | enumeration |
| Default value | `COPY` |
| Allowed values | `COPY` |
| Parameter type | read-only |
| Documentation | [file_copy_method](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC_FILE_COPY_METHOD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### maintenance_io_concurrency

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | A variant of \"effective_io_concurrency\" that is used for maintenance work. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `16` |
| Parameter type | read-only |
| Documentation | [maintenance_io_concurrency](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAINTENANCE-IO-CONCURRENCY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_notify_queue_pages

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Sets the maximum number of allocated pages for NOTIFY / LISTEN queue. |
| Data type | integer |
| Default value | `1048576` |
| Allowed values | `1048576` |
| Parameter type | read-only |
| Documentation | [max_notify_queue_pages](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAX-NOTIFY-QUEUE-PAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_parallel_maintenance_workers

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Sets the maximum number of parallel processes per maintenance operation. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `0-64` |
| Parameter type | dynamic |
| Documentation | [max_parallel_maintenance_workers](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_parallel_workers

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Sets the maximum number of parallel workers that can be active at one time. |
| Data type | integer |
| Default value | `8` |
| Allowed values | `0-1024` |
| Parameter type | dynamic |
| Documentation | [max_parallel_workers](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_parallel_workers_per_gather

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Sets the maximum number of parallel processes per executor node. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `0-1024` |
| Parameter type | dynamic |
| Documentation | [max_parallel_workers_per_gather](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS-PER-GATHER) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_worker_processes

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Maximum number of concurrent worker processes. |
| Data type | integer |
| Default value | `8` |
| Allowed values | `0-262143` |
| Parameter type | static |
| Documentation | [max_worker_processes](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### parallel_leader_participation

| Attribute | Value |
| --- | --- |
| Category | Resource Usage / Asynchronous Behavior |
| Description | Controls whether Gather and Gather Merge also run subplans. Should gather nodes also run subplans or just gather tuples?. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [parallel_leader_participation](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-PARALLEL-LEADER-PARTICIPATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



