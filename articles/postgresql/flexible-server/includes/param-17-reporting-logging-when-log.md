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
### log_min_duration_sample

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Sets the minimum execution time above which a sample of statements will be logged. Sampling is determined by log_statement_sample_rate. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [log_min_duration_sample](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-MIN-DURATION-SAMPLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_min_duration_statement

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Sets the minimum execution time (in milliseconds) above which statements will be logged. -1 disables logging statement durations. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [log_min_duration_statement](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-MIN-DURATION-STATEMENT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_min_error_statement

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Causes all statements generating error at or above this level to be logged. |
| Data type | enumeration |
| Default value | `error` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,info,notice,warning,error,log,fatal,panic` |
| Parameter type | dynamic |
| Documentation | [log_min_error_statement](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-MIN-ERROR-STATEMENT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_min_messages

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Controls which message levels are written to the server log. |
| Data type | enumeration |
| Default value | `warning` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,info,notice,warning,error,log,fatal,panic` |
| Parameter type | dynamic |
| Documentation | [log_min_messages](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-MIN-MESSAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_startup_progress_interval

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Time between progress updates for long-running startup operations. |
| Data type | integer |
| Default value | `10000` |
| Allowed values | `10000` |
| Parameter type | read-only |
| Documentation | [log_startup_progress_interval](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-STARTUP-PROGRESS-INTERVAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_statement_sample_rate

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Fraction of statements exceeding log_min_duration_sample to be logged. |
| Data type | numeric |
| Default value | `1` |
| Allowed values | `0-1` |
| Parameter type | dynamic |
| Documentation | [log_statement_sample_rate](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-STATEMENT-SAMPLE-RATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_transaction_sample_rate

| Attribute | Value |
| --- | --- |
| Category | Reporting and Logging / When to Log |
| Description | Sets the fraction of transactions from which to log all statements. |
| Data type | numeric |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [log_transaction_sample_rate](https://www.postgresql.org/docs/17/runtime-config-logging.html#GUC-LOG-TRANSACTION-SAMPLE-RATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



