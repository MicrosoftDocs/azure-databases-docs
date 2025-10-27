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
### pgbouncer.default_pool_size

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | How many server connections to allow per user/database pair. |
| Data type | integer |
| Default value | `50` |
| Allowed values | `1-4950` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.default_pool_size](https://www.pgbouncer.org/config.html#default_pool_size) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-default-pool-size](./server-parameters-azure-notes-pgbouncer-default-pool-size.md)]



### pgbouncer.enabled

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Denotes if pgBouncer service is enabled. |
| Data type | boolean |
| Default value | `false` |
| Allowed values | `true, false` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.enabled](https://www.pgbouncer.org/config.html#enabled) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-enabled](./server-parameters-azure-notes-pgbouncer-enabled.md)]



### pgbouncer.ignore_startup_parameters

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Comma-separated list of parameters that PgBouncer can ignore because they are going to be handled by the admin. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z0-9_\\.,]*` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.ignore_startup_parameters](https://www.pgbouncer.org/config.html#ignore_startup_parameters) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-ignore-startup-parameters](./server-parameters-azure-notes-pgbouncer-ignore-startup-parameters.md)]



### pgbouncer.max_client_conn

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Maximum number of client connections allowed. |
| Data type | integer |
| Default value | `5000` |
| Allowed values | `1-50000` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.max_client_conn](https://www.pgbouncer.org/config.html#max_client_conn) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-max-client-conn](./server-parameters-azure-notes-pgbouncer-max-client-conn.md)]



### pgbouncer.max_prepared_statements

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | When this is set to a non-zero value PgBouncer tracks protocol-level named prepared statements related commands sent by the client in transaction and statement pooling mode. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-5000` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.max_prepared_statements](https://www.pgbouncer.org/config.html#max_prepared_statements) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-max-prepared-statements](./server-parameters-azure-notes-pgbouncer-max-prepared-statements.md)]



### pgbouncer.min_pool_size

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Add more server connections to pool if below this number. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-4950` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.min_pool_size](https://www.pgbouncer.org/config.html#min_pool_size) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-min-pool-size](./server-parameters-azure-notes-pgbouncer-min-pool-size.md)]



### pgbouncer.pool_mode

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Specifies when a server connection can be reused by other clients. |
| Data type | enumeration |
| Default value | `transaction` |
| Allowed values | `session,transaction,statement` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.pool_mode](https://www.pgbouncer.org/config.html#pool_mode) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-pool-mode](./server-parameters-azure-notes-pgbouncer-pool-mode.md)]



### pgbouncer.query_wait_timeout

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Maximum time (in seconds) queries are allowed to spend waiting for execution. If the query is not assigned to a server during that time, the client is disconnected. |
| Data type | integer |
| Default value | `120` |
| Allowed values | `0-86400` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.query_wait_timeout](https://www.pgbouncer.org/config.html#query_wait_timeout) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-query-wait-timeout](./server-parameters-azure-notes-pgbouncer-query-wait-timeout.md)]



### pgbouncer.server_idle_timeout

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | If a server connection has been idle more than this many seconds it will be dropped. If 0 then timeout is disabled. |
| Data type | integer |
| Default value | `600` |
| Allowed values | `0-86400` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.server_idle_timeout](https://www.pgbouncer.org/config.html#server_idle_timeout) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-server-idle-timeout](./server-parameters-azure-notes-pgbouncer-server-idle-timeout.md)]



### pgbouncer.stats_users

| Attribute | Value |
| --- | --- |
| Category | PgBouncer |
| Description | Comma-separated list of database users that are allowed to connect and run read-only queries on the pgBouncer console. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z0-9,@_\\-\\.]*` |
| Parameter type | dynamic |
| Documentation | [pgbouncer.stats_users](https://www.pgbouncer.org/config.html#stats_users) |


[!INCLUDE [server-parameters-azure-notes-pgbouncer-stats-users](./server-parameters-azure-notes-pgbouncer-stats-users.md)]



