---
title: Server parameters in Azure Database for PostgreSQL - Flexible Server
description: Learn about the server parameters in Azure Database for PostgreSQL - Flexible Server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 12/08/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Server parameters in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL provides a set of configurable parameters for each server.

These parameters can correspond to:

- Parameters defined by the PostgreSQL database engine or by binary libraries that implement functionality of extensions. Some examples of database engine built-in parameters are `autovacuum_max_workers`, `DateStyle`, `client_min_messages`, `password_encryption`, `max_connections`, `geqo`, `from_collapse_limit`, `cpu_tuple_cost`, `cpu_tuple_cost`, `max_standby_streaming_delay`, `log_connections`, `log_min_duration_statement`, `max_parallel_workers`, `bgwriter_delay`, and `shared_buffers`. Some examples of parameters defined by extensions are `pg_qs.max_query_text_length` (pg_qs extension, implementing functionality for [query store](concepts-query-store.md)), `pg_stat_statements.max` ([pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) extension), `pgaudit.log_catalog` ([pgaudit](https://github.com/pgaudit/pgaudit) extension), and `cron.database_name` ([cron](https://github.com/citusdata/pg_cron) extension).
- Parameters that control some built-in functionality, which is core to the Azure Database for PostgreSQL Flexible Server service, but is not part of the database engine or any of its extensions. Some examples of these are `metrics.collector_database_activity` (controls whether or not the service should collect the list of metrics which are considered [enhanced metrics](concepts-monitoring.md#enhanced-metrics) and aren't collected by default), `pgbouncer.enabled` (allows the user to activate the instance of [PgBouncer](concepts-pgbouncer.md) which is built into the service), `index_tuning.analysis_interval` (sets the frequency at which [automatic index tuning](concepts-index-tuning.md) should wake up to produce recommendations)

You can explore the specific documentation of each of these parameters in the following list of supported server parameters.

## Supported server parameters

[!INCLUDE [server-parameters-table](./includes/server-parameters-table.md)]


[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [configure server parameters](./how-to-configure-server-parameters.md).