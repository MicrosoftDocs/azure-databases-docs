---
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 04/06/2026
ms.service: azure-database-postgresql
ms.topic: include
ms.custom: automatically generated
---
| Parameter name | Description | Default |
| --- | --- | --- |
| `pgbouncer.default_pool_size` | How many server connections to allow per user/database pair. | 50 |
| `pgbouncer.ignore_startup_parameters` | Comma-separated list of parameters that PgBouncer can ignore because they are going to be handled by the admin. | |
| `pgbouncer.max_client_conn` | Maximum number of client connections allowed. | 5000 |
| `pgbouncer.max_prepared_statements` | When this is set to a non-zero value PgBouncer tracks protocol-level named prepared statements related commands sent by the client in transaction and statement pooling mode. | 0 |
| `pgbouncer.min_pool_size` | Add more server connections to pool if below this number. | 0 |
| `pgbouncer.pool_mode` | Specifies when a server connection can be reused by other clients. | transaction |
| `pgbouncer.query_wait_timeout` | Maximum time (in seconds) queries are allowed to spend waiting for execution. If the query is not assigned to a server during that time, the client is disconnected. | 120 |
| `pgbouncer.server_idle_timeout` | If a server connection has been idle more than this many seconds it will be dropped. If 0 then timeout is disabled. | 600 |
| `pgbouncer.stats_users` | Comma-separated list of database users that are allowed to connect and run read-only queries on the pgBouncer console. | |
