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
### allow_in_place_tablespaces

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Allows tablespaces directly inside pg_tblspc, for testing. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [allow_in_place_tablespaces](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-ALLOW-IN-PLACE-TABLESPACES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### allow_system_table_mods

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Allows modifications of the structure of system tables. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [allow_system_table_mods](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-ALLOW-SYSTEM-TABLE-MODS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### backtrace_functions

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Log backtrace for errors in these functions. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [backtrace_functions](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-BACKTRACE-FUNCTIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### force_parallel_mode

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Forces use of parallel query facilities. |
| Data type | enumeration |
| Default value | `off` |
| Allowed values | `off,on,regress` |
| Parameter type | dynamic |
| Documentation | [force_parallel_mode](https://www.postgresql.org/docs/13/runtime-config-query.html#GUC-FORCE-PARALLEL-MODE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ignore_checksum_failure

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Continues processing after a checksum failure. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [ignore_checksum_failure](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-IGNORE-CHECKSUM-FAILURE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ignore_invalid_pages

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Continues recovery after an invalid pages failure. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [ignore_invalid_pages](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-IGNORE-INVALID-PAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ignore_system_indexes

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Disables reading from system indexes. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [ignore_system_indexes](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-IGNORE-SYSTEM-INDEXES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_debugging_support

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Register JIT compiled function with debugger. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [jit_debugging_support](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-JIT-DEBUGGING-SUPPORT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_dump_bitcode

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Write out LLVM bitcode to facilitate JIT debugging. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [jit_dump_bitcode](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-JIT-DUMP-BITCODE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_expressions

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Allow JIT compilation of expressions. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [jit_expressions](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-JIT-EXPRESSIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_profiling_support

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Register JIT compiled function with perf profiler. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [jit_profiling_support](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-JIT-PROFILING-SUPPORT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### jit_tuple_deforming

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Allow JIT compilation of tuple deforming. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [jit_tuple_deforming](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-JIT-TUPLE-DEFORMING) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### post_auth_delay

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Waits N seconds on connection startup after authentication. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [post_auth_delay](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-POST-AUTH-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pre_auth_delay

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Waits N seconds on connection startup before authentication. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [pre_auth_delay](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-PRE-AUTH-DELAY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### trace_notify

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Generates debugging output for LISTEN and NOTIFY. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [trace_notify](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-TRACE-NOTIFY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### trace_recovery_messages

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Enables logging of recovery-related debugging information. |
| Data type | enumeration |
| Default value | `log` |
| Allowed values | `log` |
| Parameter type | read-only |
| Documentation | [trace_recovery_messages](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-TRACE-RECOVERY-MESSAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### trace_sort

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Emit information about resource usage in sorting. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [trace_sort](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-TRACE-SORT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_consistency_checking

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Sets the WAL resource managers for which WAL consistency checks are done. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [wal_consistency_checking](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-WAL-CONSISTENCY-CHECKING) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### zero_damaged_pages

| Attribute | Value |
| --- | --- |
| Category | Developer Options |
| Description | Continues processing past damaged page headers. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [zero_damaged_pages](https://www.postgresql.org/docs/13/runtime-config-developer.html#GUC-ZERO-DAMAGED-PAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



