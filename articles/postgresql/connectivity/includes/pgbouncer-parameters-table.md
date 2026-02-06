---
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/03/2026
ms.service: azure-database-postgresql
ms.topic: include
---

| Parameter name | Description | Default |
| --- | --- | --- |
| `pgbouncer.default_pool_size` | Set this parameter value to the number of connections per user and database pair. | 50 |
| `pgbouncer.ignore_startup_parameters` | Enter a comma-separated list of parameters that PgBouncer can ignore. For example, you can let PgBouncer ignore the `extra_float_digits` parameter. Some parameters are allowed; all others raise an error. This ability is needed to tolerate overenthusiastic Java Database Connectivity (JDBC) wanting to unconditionally set `extra_float_digits=2` in startup packets. Use this option if the library that you use reports errors such as `pq: unsupported startup parameter: extra_float_digits`. | |
| `pgbouncer.max_client_conn` | Set this parameter value to the maximum number of client connections to PgBouncer that you want to support. The default is 5,000, with an allowable range from 1 to 50,000. | 5000 |
| `pgbouncer.max_prepared_statements` | When this value is nonzero, PgBouncer tracks protocol-level named prepared statements related commands that the client sends in transaction and statement pooling mode. | 0 |
| `pgbouncer.min_pool_size` | Add more server connections to the pool if the number of connections falls below this value. | 0 |
| `pgbouncer.pool_mode` | Set this parameter value to TRANSACTION for transaction pooling (which is the recommended setting for most workloads). | transaction |
| `pgbouncer.query_wait_timeout` | Maximum time in seconds that queries are allowed to spend waiting for execution. If the query isn't assigned to a server during that time, the client is disconnected. | 120 |
| `pgbouncer.server_idle_timeout` | If a server connection is idle for more than this many seconds, PgBouncer drops the connection. If 0, the timeout is disabled. | 600 |
| `pgbouncer.stats_users` | Comma-separated list of database users that are allowed to connect and run read-only queries on the pgBouncer console. | |
