---
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 10/22/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include

---

You can use PgBouncer metrics to monitor the performance of the PgBouncer process, including details for active connections, idle connections, total pooled connections, and the number of connection pools. Each metric is emitted at a *1-minute* interval and has up to *93 days* of history. Customers can configure alerts on the metrics and also access the new metrics dimensions to split and filter metrics data by database name.

#### How to enable PgBouncer metrics

- To monitor PgBouncer metrics, ensure that **pgbouncer** feature is enabled via the server parameter `pgbouncer.enabled` and metrics parameter `metrics.pgbouncer_diagnostics` is enabled.
- These parameters are dynamic and don't require an instance restart.
- PgBouncer metrics are disabled by default.

#### List of PgBouncer metrics

|Display name|Metric ID|Unit|Description|Dimension|Default enabled|
|---|---|---|---|---|---|
|**Active client connections** |`client_connections_active` |Count|Connections from clients that are associated with an Azure Database for PostgreSQL flexible server connection. |DatabaseName|No |
|**Waiting client connections** |`client_connections_waiting`|Count|Connections from clients that are waiting for an Azure Database for PostgreSQL flexible server connection to service them.|DatabaseName|No |
|**Active server connections** |`server_connections_active` |Count|Connections to Azure Database for PostgreSQL flexible server that are in use by a client connection. |DatabaseName|No |
|**Idle server connections** |`server_connections_idle` |Count|Connections to Azure Database for PostgreSQL flexible server that are idle and ready to service a new client connection. |DatabaseName|No |
|**Total pooled connections** |`total_pooled_connections`|Count|Current number of pooled connections. |DatabaseName|No |
|**Number of connection pools** |`num_pools` |Count|Total number of connection pools. |DatabaseName|No |

#### Considerations for using the PgBouncer metrics

- PgBouncer metrics that use the DatabaseName dimension have a *30-database* limit.
- On the *Burstable* SKU, the limit is 10 databases that have the DatabaseName dimension.
- The DatabaseName dimension limit is applied to the OID column, which reflects the order of creation for the database.