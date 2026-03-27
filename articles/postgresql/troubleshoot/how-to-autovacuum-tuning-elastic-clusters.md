---
title: Autovacuum Tuning Elastic Clusters
description: Troubleshooting guide for autovacuum in an Azure Database for PostgreSQL Elastic Cluster.
author: GayathriPaderla
ms.author: gapaderla
ms.reviewer: jaredmeade, maghan
ms.date: 03/27/2026
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: troubleshooting-general
---

# Autovacuum tuning in elastic cluster in Azure Database for PostgreSQL

This article provides an overview of the autovacuum feature for [Azure Database for PostgreSQL Elastic Clusters](../elastic-clusters/concepts-elastic-clusters.md) and the troubleshooting guides that are available to monitor the database bloat and autovacuum blockers. It also provides information about how far the database is from an emergency or wraparound situation.

> [!NOTE]  
> This article covers autovacuum tuning for all supported PostgreSQL versions in an Azure Database for PostgreSQL Elastic Cluster. Some features mentioned are version-specific, such as `vacuum_buffer_usage_limit` for PostgreSQL 16 and later, and `autovacuum_vacuum_max_threshold` for PostgreSQL 18 and later.

## What is autovacuum?

Autovacuum is a PostgreSQL background process that automatically cleans up dead tuples and updates statistics. It helps maintain the database performance by automatically running two key maintenance tasks:

- VACUUM - Reclaims space within the database's files by removing dead tuples and marking that space as reusable by PostgreSQL. It doesn't necessarily reduce the physical size of the database files on the disk. To return space to the operating system, use operations that rewrite the table (for example, VACUUM FULL or `pg_repack`), which have additional considerations such as exclusive locks or maintenance windows.

The following query runs VACUUM on all the nodes.

```sql
VACUUM;
```

The following query runs VACUUM on orders tables in all the nodes.

```sql
VACUUM (VERBOSE, ANALYZE) public.orders;
```

- ANALYZE - Collects table and index statistics that the PostgreSQL query planner uses to choose efficient execution plans.
  To ensure autovacuum works properly, set the autovacuum server parameter to `ON`. When enabled, PostgreSQL automatically decides when to run VACUUM or ANALYZE on a table, ensuring the database remains efficient and optimized.

The following query runs ANALYZE on all the nodes.

```sql
ANALYZE;
```

The following query runs ANALYZE on orders tables in all the nodes.

```sql
ANALYZE public.orders;
```

## Autovacuum internals

Autovacuum reads pages looking for dead tuples. If it doesn't find any dead tuples, autovacuum discards the page. When autovacuum finds dead tuples, it removes them. The cost is based on the following parameters:

| Parameter | Description |
| --- | --- |
| `vacuum_cost_page_hit` | Cost of reading a page that's already in shared buffers and doesn't need a disk read. The default value is 1. |
| `vacuum_cost_page_miss` | Cost of fetching a page that isn't in shared buffers. The default value is 10. |
| `vacuum_cost_page_dirty` | Cost of writing to a page when dead tuples are found in it. The default value is 20. |

The amount of work autovacuum performs depends on two parameters:

| Parameter | Description |
| --- | --- |
| `autovacuum_vacuum_cost_limit` | The amount of work autovacuum does in one go. |
| `autovacuum_vacuum_cost_delay` | Number of milliseconds that autovacuum is asleep after it reaches the cost limit specified by the `autovacuum_vacuum_cost_limit` parameter |

In all currently supported versions of PostgreSQL, the default value for `autovacuum_vacuum_cost_limit` is 200 (actually, set to -1, which makes it equal to the value of the regular `vacuum_cost_limit`, which by default, is 200).

The default value for `autovacuum_vacuum_cost_delay` is 2 milliseconds in PostgreSQL versions 12 and later (it was 20 milliseconds in version 11).

### Buffer usage limit

Starting with PostgreSQL version 16, use the `vacuum_buffer_usage_limit` parameter to control memory usage during VACUUM, ANALYZE, and autovacuum operations.

| Parameter | Description |
| --- | --- |
| `vacuum_buffer_usage_limit` | Sets the buffer pool size for VACUUM, ANALYZE, and autovacuum operations. This parameter limits the amount of shared buffer cache that these operations can use, preventing them from consuming excessive memory resources. |

This parameter helps prevent VACUUM and autovacuum from evicting too many useful pages from shared buffers, which can improve overall database performance during maintenance operations. The default value is typically set based on `shared_buffers`. Configure it to balance vacuum performance with the needs of regular database operations.

### Maximum threshold for autovacuum (PostgreSQL 18+)

Starting with PostgreSQL version 18, use the `autovacuum_vacuum_max_threshold` parameter to set an upper limit on the number of tuple updates or deletes that trigger autovacuum.

| Parameter | Description |
| --- | --- |
| `autovacuum_vacuum_max_threshold` | Sets a maximum number of tuple updates or deletes before vacuum. When set to `-1`, the maximum threshold is disabled. Use this parameter for fine-tuned control over autovacuum triggering on very large tables. |

This parameter is particularly useful for large tables where the default scale factor-based triggering might cause autovacuum to wait too long before running.

Autovacuum wakes up 50 times (50*20 ms=1000 ms) every second. Every time it wakes up, autovacuum reads 200 pages.

That means in one second autovacuum can do:

- ~80 MB/s [ (200 pages/`vacuum_cost_page_hit`) * 50 * 8 KB per page] if all pages with dead tuples are found in shared buffers.
- ~8 MB/s [ (200 pages/`vacuum_cost_page_miss`) * 50 * 8 KB per page] if all pages with dead tuples are read from disk.
- ~4 MB/s [ (200 pages/`vacuum_cost_page_dirty`) * 50 * 8 KB per page] autovacuum can write up to 4 MB/s.

## Monitor autovacuum

Azure Database for PostgreSQL provides the following metrics for monitoring autovacuum.

[!INCLUDE [Autovacuum Metrics](includes/autovacuum-metrics-table.md)]

For more information, see [Autovacuum Metrics](../monitor/concepts-monitoring.md#autovacuum-metrics).

## Use the following queries to monitor autovacuum

The following query returns the bloat information for all the worker nodes.

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t)
FROM (SELECT schemaname, relname, n_live_tup, n_dead_tup, n_dead_tup/(n_live_tup)* 100 as Bloat, last_autovacuum, last_autoanalyze, last_vacuum, last_analyze,autovacuum_count
FROM pg_stat_all_tables WHERE n_live_tup > 0 ORDER BY n_dead_tup DESC ) t $$ );
```

The following columns help you determine if autovacuum is keeping up with table activity:

| Parameter | Description |
| --- | --- |
| `dead_pct` | Percentage of dead tuples compared to live tuples. |
| `last_autovacuum` | Date of the last autovacuum for the table. |
| `last_autoanalyze` | Date of the last automatic analysis for the table. |

## Trigger autovacuum

An autovacuum action (*ANALYZE* or *VACUUM*) starts when the number of dead tuples exceeds a certain number. This number depends on two factors: the total count of rows in a table, plus a fixed threshold. *ANALYZE* triggers by default when 10% of the table plus 50 row changes occur, while *VACUUM* triggers when 20% of the table plus 50 row changes occur. Since the *VACUUM* threshold is twice as high as the *ANALYZE* threshold, *ANALYZE* triggers earlier than *VACUUM*.

For PostgreSQL versions 13 and later, *ANALYZE* triggers by default when 20% of the table plus 1,000 row inserts occur.

The exact equations for each action are:

- **Autoanalyze** = autovacuum_analyze_scale_factor * tuples + autovacuum_analyze_threshold or
  autovacuum_vacuum_insert_scale_factor * tuples + autovacuum_vacuum_insert_threshold (For PostgreSQL versions 13 and later)
- **Autovacuum** = autovacuum_vacuum_scale_factor * tuples + autovacuum_vacuum_threshold

For example, if you have a table with 100 rows, the following equations show when the analyze and vacuum actions trigger:

For updates and deletes:
`Autoanalyze = 0.1 * 100 + 50 = 60`
`Autovacuum = 0.2 * 100 + 50 = 70`

*ANALYZE* triggers after 60 rows are changed on a table, and *VACUUM* triggers when 70 rows are changed on a table.

For inserts:
`Autoanalyze = 0.2 * 100 + 1000 = 1020`

*ANALYZE* triggers after 1,020 rows are inserted on a table.

Here's the description of the parameters used in the equation:

| Parameter | Description |
| --- | --- |
| `autovacuum_analyze_scale_factor` | Percentage of inserts, updates, and deletes that triggers *ANALYZE* on the table. |
| `autovacuum_analyze_threshold` | Minimum number of tuples inserted, updated, or deleted to *ANALYZE* a table. |
| `autovacuum_vacuum_insert_scale_factor` | Percentage of inserts that triggers *ANALYZE* on the table. |
| `autovacuum_vacuum_insert_threshold` | Minimum number of tuples inserted to *ANALYZE* a table. |
| `autovacuum_vacuum_scale_factor` | Percentage of updates and deletes that triggers *VACUUM* on the table. |

Use the following query to list the tables in a database on all worker nodes and identify the tables that qualify for the autovacuum process:

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t)
FROM (SELECT *
      ,n_dead_tup > av_threshold AS av_needed
      ,CASE
        WHEN reltuples > 0
          THEN round(100.0 * n_dead_tup / (reltuples))
        ELSE 0
        END AS pct_dead
    FROM (
      SELECT N.nspname
        ,C.relname
        ,pg_stat_get_tuples_inserted(C.oid) AS n_tup_ins
        ,pg_stat_get_tuples_updated(C.oid) AS n_tup_upd
        ,pg_stat_get_tuples_deleted(C.oid) AS n_tup_del
        ,pg_stat_get_live_tuples(C.oid) AS n_live_tup
        ,pg_stat_get_dead_tuples(C.oid) AS n_dead_tup
        ,C.reltuples AS reltuples
        ,round(current_setting('autovacuum_vacuum_threshold')::INTEGER + current_setting('autovacuum_vacuum_scale_factor')::NUMERIC * C.reltuples) AS av_threshold
        ,date_trunc('minute', greatest(pg_stat_get_last_vacuum_time(C.oid), pg_stat_get_last_autovacuum_time(C.oid))) AS last_vacuum
        ,date_trunc('minute', greatest(pg_stat_get_last_analyze_time(C.oid), pg_stat_get_last_autoanalyze_time(C.oid))) AS last_analyze
      FROM pg_class C
      LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
      WHERE C.relkind IN ('r', 't')
        AND N.nspname NOT IN ('pg_catalog', 'information_schema' )
        AND N.nspname !~ '^pg_toast'
      ) AS av
    ORDER BY av_needed DESC, n_dead_tup DESC) t $$ );
```

> [!NOTE]  
> The query doesn't take into consideration that you can configure autovacuum on a per-table basis by using the `ALTER TABLE` DDL command.

## Common autovacuum problems

Review the following list of common problems with the autovacuum process.

### Not keeping up with busy server

The autovacuum process estimates the cost of every I/O operation, accumulates a total for each operation it performs, and pauses once the upper limit of the cost is reached. The process uses two server parameters: `autovacuum_vacuum_cost_delay` and `autovacuum_vacuum_cost_limit`.

By default, `autovacuum_vacuum_cost_limit` is set to -1, which means the autovacuum cost limit uses the same value as the `vacuum_cost_limit` parameter. The default value for `vacuum_cost_limit` is 200. `vacuum_cost_limit` represents the cost of a manual vacuum.

If you set `autovacuum_vacuum_cost_limit` to -1, autovacuum uses the `vacuum_cost_limit` parameter. If you set `autovacuum_vacuum_cost_limit` to a value greater than -1, autovacuum uses the `autovacuum_vacuum_cost_limit` parameter.

If autovacuum isn't keeping up, consider changing the following parameters:

| Parameter | Description |
| --- | --- |
| `autovacuum_vacuum_cost_limit` | Default: `200`. You can increase the cost limit. Monitor CPU and I/O utilization on the database before and after making changes. |
| `autovacuum_vacuum_cost_delay` | **PostgreSQL Version 12 and later** - Default: `2 ms`. You can decrease this value for more aggressive autovacuum. |
| `vacuum_buffer_usage_limit` | **PostgreSQL Versions 16 and later** - Sets the buffer pool size for VACUUM and autovacuum operations. Adjusting this parameter can help balance autovacuum performance with overall system performance by controlling how much shared buffer cache is used during vacuum operations. |

> [!NOTE]  
> - The `autovacuum_vacuum_cost_limit` value is distributed proportionally among the running autovacuum workers. If there's more than one worker, the sum of the limits for each worker doesn't exceed the value of the `autovacuum_vacuum_cost_limit` parameter.
> - `autovacuum_vacuum_scale_factor` is another parameter that can trigger vacuum on a table based on dead tuple accumulation. Default: `0.2`, Allowed range: `0.05 - 0.1`. The scale factor is workload-specific and should be set depending on the amount of data in the tables. Before changing the value, investigate the workload and individual table volumes.

### Autovacuum runs constantly

If autovacuum runs continuously, it can affect CPU and I/O utilization on the server. Here are some possible reasons:

#### `maintenance_work_mem`

The autovacuum daemon uses `autovacuum_work_mem`, which is set to `-1` by default. This default setting means `autovacuum_work_mem` uses the same value as the `maintenance_work_mem` parameter. This article assumes `autovacuum_work_mem` is set to `-1` and the autovacuum daemon uses `maintenance_work_mem`.

If `maintenance_work_mem` is low, increase it up to 2 GB on an Azure Database for PostgreSQL flexible server instance. A general rule of thumb is to allocate 50 MB to `maintenance_work_mem` for every 1 GB of RAM.

### Out of memory errors

Overly aggressive `maintenance_work_mem` values can periodically cause out-of-memory errors in the system. Understand the available RAM on the server before you change the `maintenance_work_mem` parameter.

### Autovacuum disrupts performance

If autovacuum consumes too many resources, try the following actions:

#### Autovacuum parameters

Evaluate the parameters `autovacuum_vacuum_cost_delay`, `autovacuum_vacuum_cost_limit`, and `autovacuum_max_workers`. Improperly setting autovacuum parameters might lead to scenarios where autovacuum disrupts performance.

If autovacuum disrupts performance, consider the following actions:

- Increase `autovacuum_vacuum_cost_delay` and reduce `autovacuum_vacuum_cost_limit` if you set it higher than the default of 200.
- Reduce the number of `autovacuum_max_workers` if you set it higher than the default of 3.

#### Too many autovacuum workers

Increasing the number of autovacuum workers doesn't increase the speed of vacuum. Don't use a high number of autovacuum workers.

Increasing the number of autovacuum workers results in more memory consumption. Depending on the value of `maintenance_work_mem`, it could cause performance degradation.

Each autovacuum worker process only gets `(1/autovacuum_max_workers)` of the total `autovacuum_cost_limit`, so having a high number of workers causes each one to go slower.

If you increase the number of workers, increase `autovacuum_vacuum_cost_limit` and/or decrease `autovacuum_vacuum_cost_delay` to make the vacuum process faster.

However, if you set the parameter at table level `autovacuum_vacuum_cost_delay` or `autovacuum_vacuum_cost_limit` parameters, the workers running on those tables are exempted from being considered in the balancing algorithm `[autovacuum_cost_limit/autovacuum_max_workers]`.

### Autovacuum transaction ID (TXID) wraparound protection

When a database encounters transaction ID wraparound protection, you see an error message like the following error:

```bash
Database isn't accepting commands to avoid wraparound data loss in database 'xx'
Stop the postmaster and vacuum that database in single-user mode.
```

To check the percentage toward the wraparound on coordinator node and worker node, use these queries:

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (SELECT datname
    , age(datfrozenxid)
    , current_setting('autovacuum_freeze_max_age')
FROM pg_database where datname = 'postgres'
ORDER BY 2 DESC
) t $$ );

SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (WITH max_age AS (
    SELECT 2000000000 AS max_old_xid
        , setting AS autovacuum_freeze_max_age
        FROM pg_catalog.pg_settings
        WHERE name = 'autovacuum_freeze_max_age' )
, per_database_stats AS (
    SELECT datname
        , m.max_old_xid::int
        , m.autovacuum_freeze_max_age::int
        , age(d.datfrozenxid) AS oldest_current_xid
    FROM pg_catalog.pg_database d
    JOIN max_age m ON (true)
    WHERE d.datallowconn )
SELECT max(oldest_current_xid) AS oldest_current_xid
    , max(ROUND(100*(oldest_current_xid/max_old_xid::float))) AS percent_towards_wraparound
    , max(ROUND(100*(oldest_current_xid/autovacuum_freeze_max_age::float))) AS percent_towards_emergency_autovac
FROM per_database_stats) t $$ );
```

> [!NOTE]  
> This error message is a long-standing oversight. Usually, you don't need to switch to single-user mode. Instead, run the required VACUUM commands and perform tuning for VACUUM to run fast. While you can't run any data manipulation language (DML), you can still run VACUUM.

The wraparound problem occurs when the database isn't vacuumed or when autovacuum doesn't remove too many dead tuples.

Possible reasons for this problem include the following reasons:

#### Heavy workload

A heavy workload causes too many dead tuples in a brief period, making it difficult for autovacuum to catch up. The dead tuples in the system add up over time, leading to degradation of query performance and leading to wraparound situation. One reason for this situation might be that autovacuum parameters aren't adequately set and it isn't keeping up with a busy server.

#### Long-running transactions

Any long-running transaction in the system doesn't allow autovacuum to remove dead tuples. They're a blocker to the vacuum process. Removing the long running transactions frees up dead tuples for deletion when autovacuum runs.

You can detect long-running transactions by using the following query:

```sql
SELECT pg.nodeport,age(backend_xid) AS age_in_xids,
NOW() - xact_start AS xact_age,
NOW() - query_start AS query_age, cs.*
, state
, query
FROM citus_stat_activity cs
join pg_dist_node pg on cs.nodeid = pg.nodeid
WHERE state != 'idle'
AND pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY NOW() - query_start DESC
LIMIT 10;
```

#### Prepared statements

If there are prepared statements that aren't committed, they prevent autovacuum from removing dead tuples.
The following query helps find noncommitted prepared statements:

Run the following query to find any uncommitted prepared transactions on worker nodes.

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (
  SELECT * FROM pg_prepared_xacts
) t $$ );
```

Use `COMMIT PREPARED` or `ROLLBACK PREPARED` to commit or roll back these statements.

#### Unused replication slots

Unused replication slots prevent autovacuum from claiming dead tuples. The following query helps identify unused replication slots:

Run the following query to find any unused replication slots on worker nodes.

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (
  SELECT slot_name, slot_type, database, xmin,active FROM pg_replication_slots
) t $$ );
```

Use `pg_drop_replication_slot()` to delete unused replication slots.

When the database encounters transaction ID wraparound protection, check for any blockers as mentioned previously, and remove the blockers manually for autovacuum to continue and complete. You can also increase the speed of autovacuum by setting `autovacuum_cost_delay` to 0 and increasing the `autovacuum_cost_limit` to a value greater than 200. However, changes to these parameters don't apply to existing autovacuum workers. Either restart the database or kill existing workers manually to apply parameter changes.

### Table-specific requirements

Set autovacuum parameters for individual tables. These settings are especially important for small and large tables. For example, for a small table that contains only 100 rows, autovacuum triggers the VACUUM operation when 70 rows change (as calculated previously). If you frequently update this table, you might see hundreds of autovacuum operations a day. These operations prevent autovacuum from maintaining other tables where the percentage of changes isn't as significant. Alternatively, a table containing a billion rows needs to change 200 million rows to trigger autovacuum operations. Setting autovacuum parameters appropriately prevents such scenarios.

To set autovacuum settings for each table, change the server parameters as shown in the following examples:

```sql
    ALTER TABLE <table name> SET (autovacuum_analyze_scale_factor = xx);
    ALTER TABLE <table name> SET (autovacuum_analyze_threshold = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_scale_factor = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_threshold = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_cost_delay = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_cost_limit = xx);
    ALTER TABLE <table name> SET (vacuum_buffer_usage_limit = 'xx MB');
```
You can't set the parameter values for a table shard.

You can check the set value by using the following query on the coordinator node:

```sql
SELECT relname, reloptions FROM pg_class WHERE relname = <table name>;
```

You can check the query on all nodes:

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (
  SELECT relname, reloptions FROM pg_class WHERE relname = <tablename>
) t $$ );
```

#### Recommended approach for repetitive autovacuum workers

In rare scenarios, such as anti-wraparound autovacuum, workers might restart immediately after termination because they're critical for preventing transaction ID exhaustion. To minimize repeated conflicts, follow these steps:

- Queue the DDL operation prior to termination:
  - Session 1: Prepare and run the DDL statement on Coordinator nodes.
  - Session 2: Terminate the autovacuum process.

Execute the DDL statement on coordinator node right after termination.

Steps to avoid repeated conflicts:

1. Grant role to user

   ```sql
   GRANT pg_signal_autovacuum_worker TO app_user;
   ```
1. Identify autovacuum process ID

   ```sql
   SELECT pid, query FROM citus_stat_activity WHERE query LIKE '%autovacuum%' AND pid != pg_backend_pid();
   ```

1. Terminate autovacuum

   ```sql
   SELECT pg_terminate_backend(<pid>);
   ```

1. Execute DDL statement immediately

   ```sql
   ALTER TABLE my_table ADD COLUMN new_col TEXT;
   ```

> [!NOTE]  
> Don't terminate ongoing autovacuum processes. Doing so might lead to table and database bloat, which can further lead to performance regressions. However, in cases where there's a business-critical requirement involving the scheduled execution of a DDL statement that coincides with the autovacuum process, non-superusers can terminate the autovacuum in a controlled and secure manner by using the `pg_signal_autovacuum_worker` role.

## Related content

- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md)
