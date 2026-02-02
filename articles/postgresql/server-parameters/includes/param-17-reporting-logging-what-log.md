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
### application_name

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the application name to be reported in statistics and logs. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z0-9._-]*` |
| Parameter type | dynamic |
| Documentation | [application_name](https://www.postgresql.org/docs/17/libpq-connect.html#LIBPQ-CONNECT-APPLICATION-NAME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### debug_pretty_print

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Indents parse and plan tree displays. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [debug_pretty_print](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-DEBUG-PRETTY-PRINT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### debug_print_parse

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs each query's parse tree. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [debug_print_parse](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-DEBUG-PRINT-PARSE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### debug_print_plan

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs each query's execution plan. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [debug_print_plan](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-DEBUG-PRINT-PARSE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### debug_print_rewritten

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs each query's rewritten parse tree. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [debug_print_rewritten](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-DEBUG-PRINT-PARSE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_autovacuum_min_duration

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the minimum execution time above which autovacuum actions will be logged. Zero prints all actions. -1 turns autovacuum logging off. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [log_autovacuum_min_duration](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-AUTOVACUUM-MIN-DURATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_checkpoints

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs each checkpoint. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_checkpoints](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-CHECKPOINTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_connections

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs each successful connection. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_connections](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-CONNECTIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_disconnections

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs end of a session, including duration. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_disconnections](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-DISCONNECTIONS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_duration

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs the duration of each completed SQL statement. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_duration](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-DURATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_error_verbosity

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the verbosity of logged messages. |
| Data type | enumeration |
| Default value | `default` |
| Allowed values | `terse,default,verbose` |
| Parameter type | dynamic |
| Documentation | [log_error_verbosity](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-ERROR-VERBOSITY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_hostname

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs the host name in the connection logs. By default, connection logs only show the IP address of the connecting host. If you want them to show the host name you can turn this on, but depending on your host name resolution setup it might impose a non-negligible performance penalty. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_hostname](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-HOSTNAME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_line_prefix

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Controls information prefixed to each log line. If blank, no prefix is used. |
| Data type | string |
| Default value | `%t-%c-` |
| Allowed values | `[^']*` |
| Parameter type | dynamic |
| Documentation | [log_line_prefix](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_lock_waits

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs long lock waits. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_lock_waits](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-LOCK-WAITS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_parameter_max_length

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the maximum length in bytes of data logged for bind parameter values when logging statements. -1 to print values in full. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-1073741823` |
| Parameter type | dynamic |
| Documentation | [log_parameter_max_length](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-PARAMETER-MAX-LENGTH) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_parameter_max_length_on_error

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the maximum length in bytes of data logged for bind parameter values when logging statements, on error. -1 to print values in full. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `-1-1073741823` |
| Parameter type | dynamic |
| Documentation | [log_parameter_max_length_on_error](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-PARAMETER-MAX-LENGTH-ON-ERROR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_recovery_conflict_waits

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs standby recovery conflict waits. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_recovery_conflict_waits](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-RECOVERY-CONFLICT-WAITS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_replication_commands

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Logs each replication command. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [log_replication_commands](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-REPLICATION-COMMANDS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_statement

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the type of statements logged. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `none,ddl,mod,all` |
| Parameter type | dynamic |
| Documentation | [log_statement](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-STATEMENT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_temp_files

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Log the use of temporary files larger than this number of kilobytes. Zero logs all files. The default is -1 (turning this feature off). |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [log_temp_files](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-TEMP-FILES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_timezone

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / What to Log |
| Description | Sets the time zone to use in log messages. |
| Data type | string |
| Default value | `UTC` |
| Allowed values | `UTC` |
| Parameter type | read-only |
| Documentation | [log_timezone](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-TIMEZONE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



