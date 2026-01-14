---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
### event_source

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the application name used to identify PostgreSQL messages in the event log. |
| Data type | string |
| Default value | `PostgreSQL` |
| Allowed values | `PostgreSQL` |
| Parameter type | read-only |
| Documentation | [event_source](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-EVENT-SOURCE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_destination

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the destination for server log output. Valid values are combinations of \"stderr\", \"syslog\", \"csvlog\", \"jsonlog\", and \"eventlog\", depending on the platform. |
| Data type | enumeration |
| Default value | `stderr` |
| Allowed values | `stderr,csvlog` |
| Parameter type | dynamic |
| Documentation | [log_destination](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-DESTINATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_directory

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the destination directory for log files. Can be specified as relative to the data directory or as absolute path. |
| Data type | string |
| Default value | `log` |
| Allowed values | `log` |
| Parameter type | read-only |
| Documentation | [log_directory](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-DIRECTORY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_file_mode

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the file permissions for log files. The parameter value is expected to be a numeric mode specification in the form accepted by the chmod and umask system calls. (To use the customary octal format the number must start with a 0 (zero).). |
| Data type | integer |
| Default value | `0600` |
| Allowed values | `0600` |
| Parameter type | read-only |
| Documentation | [log_file_mode](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-FILE-MODE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_filename

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the file name pattern for log files. |
| Data type | string |
| Default value | `postgresql-%Y-%m-%d_%H%M%S.log` |
| Allowed values | `postgresql-%Y-%m-%d_%H%M%S.log` |
| Parameter type | read-only |
| Documentation | [log_filename](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-FILENAME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### logging_collector

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Start a subprocess to capture stderr, csvlog and/or jsonlog into log files. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [logging_collector](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOGGING-COLLECTOR) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_rotation_age

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the amount of time to wait before forcing log file rotation. |
| Data type | integer |
| Default value | `60` |
| Allowed values | `60` |
| Parameter type | read-only |
| Documentation | [log_rotation_age](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-ROTATION-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_rotation_size

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the maximum size a log file can reach before being rotated. |
| Data type | integer |
| Default value | `102400` |
| Allowed values | `102400` |
| Parameter type | read-only |
| Documentation | [log_rotation_size](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-ROTATION-SIZE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_truncate_on_rotation

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Truncate existing log files of same name during log rotation. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [log_truncate_on_rotation](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-TRUNCATE-ON-ROTATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### md5_password_warnings

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Enables deprecation warnings for MD5 passwords. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [md5_password_warnings](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-MD5-PASSWORD-WARNINGS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### syslog_facility

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the syslog \"facility\" to be used when syslog enabled. |
| Data type | enumeration |
| Default value | `local0` |
| Allowed values | `local0` |
| Parameter type | read-only |
| Documentation | [syslog_facility](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-SYSLOG-FACILITY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### syslog_ident

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Sets the program name used to identify PostgreSQL messages in syslog. |
| Data type | string |
| Default value | `postgres` |
| Allowed values | `postgres` |
| Parameter type | read-only |
| Documentation | [syslog_ident](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-SYSLOG-IDENT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### syslog_sequence_numbers

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Add sequence number to syslog messages to avoid duplicate suppression. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [syslog_sequence_numbers](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-SYSLOG-SEQUENCE-NUMBERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### syslog_split_messages

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / Where to Log |
| Description | Split messages sent to syslog by lines and to fit into 1024 bytes. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [syslog_split_messages](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-SYSLOG-SPLIT-MESSAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



