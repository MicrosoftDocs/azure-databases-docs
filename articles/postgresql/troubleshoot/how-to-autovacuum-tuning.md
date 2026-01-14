---
title: Autovacuum Tuning
description: Troubleshooting guide for autovacuum in an Azure Database for PostgreSQL flexible server instance.
author: sarat-balijepalli
ms.author: sbalijepalli
ms.reviewer: maghan
ms.date: 11/06/2025
ms.service: azure-database-postgresql
ms.topic: how-to
---

# Autovacuum tuning in Azure Database for PostgreSQL

This article provides an overview of the autovacuum feature for [Azure Database for PostgreSQL](../overview.md) and the feature troubleshooting guides that are available to monitor the database bloat and autovacuum blockers. It also provides information about how far the database is from an emergency or wraparound situation.

> [!NOTE]
> This article covers autovacuum tuning for all supported PostgreSQL versions in Azure Database for PostgreSQL flexible server. Some features mentioned are version-specific (such as `vacuum_buffer_usage_limit` for PostgreSQL 16 and later, and `autovacuum_vacuum_max_threshold` for PostgreSQL 18 and later).

## What is autovacuum?

Autovacuum is a PostgreSQL background process that automatically cleans up dead tuples and updates statistics. It helps maintain the database performance by automatically running two key maintenance tasks:

- VACUUM - Reclaims space within the database's files by removing dead tuples and marking that space as reusable by PostgreSQL. It doesn't necessarily reduce the physical size of the database files on disk. To return space to the operating system, use operations that rewrite the table (for example, VACUUM FULL or pg_repack), which have additional considerations such as exclusive locks or maintenance windows.
- ANALYZE - Collects table and index statistics that the PostgreSQL query planner uses to choose efficient execution plans.

To ensure autovacuum works properly, set the autovacuum server parameter to `ON`. When enabled, PostgreSQL automatically decides when to run VACUUM or ANALYZE on a table, ensuring the database remains efficient and optimized.

## Autovacuum internals

Autovacuum reads pages looking for dead tuples. If it doesn't find any dead tuples, autovacuum discards the page. When autovacuum finds dead tuples, it removes them. The cost is based on the following parameters:

| Parameter                        | Description
| --- | --- |
| `vacuum_cost_page_hit` | Cost of reading a page that's already in shared buffers and doesn't need a disk read. The default value is 1. |
| `vacuum_cost_page_miss` | Cost of fetching a page that isn't in shared buffers. The default value is 10. |
| `vacuum_cost_page_dirty` | Cost of writing to a page when dead tuples are found in it. The default value is 20. |

The amount of work autovacuum performs depends on two parameters:

| Parameter                        | Description
| --- | --- |
| `autovacuum_vacuum_cost_limit` | The amount of work autovacuum does in one go. |
| `autovacuum_vacuum_cost_delay` | Number of milliseconds that autovacuum is asleep after it reaches the cost limit specified by the `autovacuum_vacuum_cost_limit` parameter. |

In all currently supported versions of PostgreSQL, the default value for `autovacuum_vacuum_cost_limit` is 200 (actually, set to -1, which makes it equal to the value of the regular `vacuum_cost_limit`, which by default, is 200).

The default value for `autovacuum_vacuum_cost_delay` is 2 milliseconds in PostgreSQL versions 12 and later (it was 20 milliseconds in version 11).

### Buffer usage limit (PostgreSQL 16+)

Starting with PostgreSQL version 16, you can use the `vacuum_buffer_usage_limit` parameter to control memory usage during VACUUM, ANALYZE, and autovacuum operations.

| Parameter                        | Description
| --- | --- |
| `vacuum_buffer_usage_limit` | Sets the buffer pool size for VACUUM, ANALYZE, and autovacuum operations. This parameter limits the amount of shared buffer cache that these operations can use, preventing them from consuming excessive memory resources. |

This parameter helps prevent VACUUM and autovacuum from evicting too many useful pages from shared buffers, which can improve overall database performance during maintenance operations. The default value is typically set based on `shared_buffers`, and you can configure it to balance vacuum performance with the needs of regular database operations.

### Maximum threshold for autovacuum (PostgreSQL 18+)

Starting with PostgreSQL version 18, you can use the `autovacuum_vacuum_max_threshold` parameter to set an upper limit on the number of tuple updates or deletes that trigger autovacuum.

| Parameter                        | Description
| --- | --- |
| `autovacuum_vacuum_max_threshold` | Sets a maximum number of tuple updates or deletes prior to vacuum. When set to `-1`, the maximum threshold is disabled. Use this parameter for fine-tuned control over autovacuum triggering on very large tables. |

This parameter is particularly useful for large tables where the default scale factor-based triggering might cause autovacuum to wait too long before running.

Autovacuum wakes up 50 times (50*20 ms=1000 ms) every second. Every time it wakes up, autovacuum reads 200 pages.

That means in one second autovacuum can do:

- ~80 MB/Sec [ (200 pages/`vacuum_cost_page_hit`) * 50 * 8 KB per page] if all pages with dead tuples are found in shared buffers.
- ~8 MB/Sec [ (200 pages/`vacuum_cost_page_miss`) * 50 * 8 KB per page] if all pages with dead tuples are read from disk.
- ~4 MB/Sec [ (200 pages/`vacuum_cost_page_dirty`) * 50 * 8 KB per page] autovacuum can write up to 4 MB/sec.

## Monitor autovacuum

Azure Database for PostgreSQL provides the following metrics for monitoring autovacuum.

[!INCLUDE [Autovacuum Metrics](includes/autovacuum-metrics-table.md)]

For more information, see [Autovacuum Metrics](../monitor/concepts-monitoring.md#autovacuum-metrics).

Use the following queries to monitor autovacuum:

```sql
select schemaname,relname,n_dead_tup,n_live_tup,round(n_dead_tup::float/n_live_tup::float*100) dead_pct,autovacuum_count,last_vacuum,last_autovacuum,last_autoanalyze,last_analyze from pg_stat_all_tables where n_live_tup >0;
```

The following columns help you determine if autovacuum is catching up to table activity:

| Parameter                        | Description
| --- | --- |
| `dead_pct` | Percentage of dead tuples when compared to live tuples. |
| `last_autovacuum` | The date of the last time the table was autovacuumed. |
| `last_autoanalyze` | The date of the last time the table was automatically analyzed. |

## Triggering autovacuum

An autovacuum action (*ANALYZE* or *VACUUM*) triggers when the number of dead tuples exceeds a particular number. This number depends on two factors: the total count of rows in a table, plus a fixed threshold. *ANALYZE* triggers by default when 10% of the table plus 50 row changes occur, while *VACUUM* triggers when 20% of the table plus 50 row changes occur. Since the *VACUUM* threshold is twice as high as the *ANALYZE* threshold, *ANALYZE* triggers earlier than *VACUUM*.

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

| Parameter                        | Description
| --- | --- |
| `autovacuum_analyze_scale_factor` | Percentage of inserts, updates, and deletes that triggers *ANALYZE* on the table. |
| `autovacuum_analyze_threshold` | Minimum number of tuples inserted, updated, or deleted to *ANALYZE* a table. |
| `autovacuum_vacuum_insert_scale_factor` | Percentage of inserts that triggers *ANALYZE* on the table. |
| `autovacuum_vacuum_insert_threshold` | Minimum number of tuples inserted to *ANALYZE* a table. |
| `autovacuum_vacuum_scale_factor` | Percentage of updates and deletes that triggers *VACUUM* on the table. |

Use the following query to list the tables in a database and identify the tables that qualify for the autovacuum process:

```sql
 SELECT *
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
      WHERE C.relkind IN (
          'r'
          ,'t'
          )
        AND N.nspname NOT IN (
          'pg_catalog'
          ,'information_schema'
          )
        AND N.nspname !~ '^pg_toast'
      ) AS av
    ORDER BY av_needed DESC ,n_dead_tup DESC;
```

> [!NOTE]  
> The query doesn't take into consideration that you can configure autovacuum on a per-table basis by using the "alter table" DDL command.

## Common autovacuum problems

Review the following list of common problems with the autovacuum process.

### Not keeping up with busy server

The autovacuum process estimates the cost of every I/O operation, accumulates a total for each operation it performs, and pauses once the upper limit of the cost is reached. The process uses two server parameters: `autovacuum_vacuum_cost_delay` and `autovacuum_vacuum_cost_limit`.

By default, `autovacuum_vacuum_cost_limit` is set to -1, which means the autovacuum cost limit uses the same value as the `vacuum_cost_limit` parameter. The default value for `vacuum_cost_limit` is 200. `vacuum_cost_limit` represents the cost of a manual vacuum.

If you set `autovacuum_vacuum_cost_limit` to -1, autovacuum uses the `vacuum_cost_limit` parameter. If you set `autovacuum_vacuum_cost_limit` to a value greater than -1, autovacuum uses the `autovacuum_vacuum_cost_limit` parameter.

If autovacuum isn't keeping up, consider changing the following parameters:

| Parameter                        | Description
| --- | --- |
| `autovacuum_vacuum_cost_limit` | Default: `200`. You can increase the cost limit. Monitor CPU and I/O utilization on the database before and after making changes. |
| `autovacuum_vacuum_cost_delay` | **PostgreSQL Version 12 and later** - Default: `2 ms`. You can decrease this value for more aggressive autovacuum. |
| `vacuum_buffer_usage_limit` | **PostgreSQL Versions 16 and later** - Sets the buffer pool size for VACUUM and autovacuum operations. Adjusting this parameter can help balance autovacuum performance with overall system performance by controlling how much shared buffer cache is used during vacuum operations. |

> [!NOTE]  
> - The `autovacuum_vacuum_cost_limit` value is distributed proportionally among the running autovacuum workers. If there's more than one worker, the sum of the limits for each worker doesn't exceed the value of the `autovacuum_vacuum_cost_limit` parameter.
> - `autovacuum_vacuum_scale_factor` is another parameter that can trigger vacuum on a table based on dead tuple accumulation. Default: `0.2`, Allowed range: `0.05 - 0.1`. The scale factor is workload-specific and should be set depending on the amount of data in the tables. Before changing the value, investigate the workload and individual table volumes.

### Autovacuum constantly running

If autovacuum runs continuously, it can affect CPU and I/O utilization on the server. Here are some possible reasons:

#### `maintenance_work_mem`

The autovacuum daemon uses `autovacuum_work_mem`, which is set to `-1` by default. This default setting means `autovacuum_work_mem` uses the same value as the `maintenance_work_mem` parameter. This article assumes `autovacuum_work_mem` is set to `-1` and the autovacuum daemon uses `maintenance_work_mem`.

If `maintenance_work_mem` is low, you can increase it up to 2 GB on an Azure Database for PostgreSQL flexible server instance. A general rule of thumb is to allocate 50 MB to `maintenance_work_mem` for every 1 GB of RAM.

#### Large number of databases

Autovacuum tries to start a worker on each database every `autovacuum_naptime` seconds.

For example, if a server has 60 databases and `autovacuum_naptime` is set to 60 seconds, then the autovacuum worker starts every second [autovacuum_naptime/Number of databases].

If there are more databases in a cluster, increase `autovacuum_naptime`. At the same time, make the autovacuum process more aggressive by increasing the `autovacuum_cost_limit` and decreasing the `autovacuum_cost_delay` parameters. You can also increase `autovacuum_max_workers` from the default of 3 to 4 or 5.

### Out of memory errors

Overly aggressive `maintenance_work_mem` values can periodically cause out-of-memory errors in the system. Understand the available RAM on the server before you change the `maintenance_work_mem` parameter.

### Autovacuum is too disruptive

If autovacuum consumes too many resources, try the following actions:

#### Autovacuum parameters

Evaluate the parameters `autovacuum_vacuum_cost_delay`, `autovacuum_vacuum_cost_limit`, and `autovacuum_max_workers`. Improperly setting autovacuum parameters might lead to scenarios where autovacuum becomes too disruptive.

If autovacuum is too disruptive, consider the following actions:

- Increase `autovacuum_vacuum_cost_delay` and reduce `autovacuum_vacuum_cost_limit` if you set it higher than the default of 200.
- Reduce the number of `autovacuum_max_workers` if you set it higher than the default of 3.

#### Too many autovacuum workers

Increasing the number of autovacuum workers doesn't increase the speed of vacuum. Don't use a high number of autovacuum workers.

Increasing the number of autovacuum workers results in more memory consumption. Depending on the value of `maintenance_work_mem`, it could cause performance degradation.

Each autovacuum worker process only gets (1/autovacuum_max_workers) of the total `autovacuum_cost_limit`, so having a high number of workers causes each one to go slower.

If you increase the number of workers, increase `autovacuum_vacuum_cost_limit` and/or decrease `autovacuum_vacuum_cost_delay` to make the vacuum process faster.

However, if you set the parameter at table level `autovacuum_vacuum_cost_delay` or `autovacuum_vacuum_cost_limit` parameters, the workers running on those tables are exempted from being considered in the balancing algorithm [autovacuum_cost_limit/autovacuum_max_workers].

### Autovacuum transaction ID (TXID) wraparound protection

When a database runs into transaction ID wraparound protection, you see an error message like the following error:

```
Database isn't accepting commands to avoid wraparound data loss in database 'xx'
Stop the postmaster and vacuum that database in single-user mode.
```

> [!NOTE]  
> This error message is a long-standing oversight. Usually, you don't need to switch to single-user mode. Instead, you can run the required VACUUM commands and perform tuning for VACUUM to run fast. While you can't run any data manipulation language (DML), you can still run VACUUM.

The wraparound problem occurs when the database isn't vacuumed or when autovacuum doesn't remove too many dead tuples.

Possible reasons for this issue include the following reasons:

#### Heavy workload

A heavy workload causes too many dead tuples in a brief period, making it difficult for autovacuum to catch up. The dead tuples in the system add up over a period leading to degradation of query performance and leading to wraparound situation. One reason for this situation to arise might be because autovacuum parameters aren't adequately set and it isn't keeping up with a busy server.

#### Long-running transactions

Any long-running transaction in the system doesn't allow autovacuum to remove dead tuples. They're a blocker to the vacuum process. Removing the long running transactions frees up dead tuples for deletion when autovacuum runs.

Long-running transactions can be detected using the following query:

```sql
    SELECT pid, age(backend_xid) AS age_in_xids,
    now () - xact_start AS xact_age,
    now () - query_start AS query_age,
    state,
    query
    FROM pg_stat_activity
    WHERE state != 'idle'
    ORDER BY 2 DESC
    LIMIT 10;
```

#### Prepared statements

If there are prepared statements that aren't committed, they prevent autovacuum from removing dead tuples.
The following query helps find noncommitted prepared statements:

```sql
    SELECT gid, prepared, owner, database, transaction
    FROM pg_prepared_xacts
    ORDER BY age(transaction) DESC;
```

Use `COMMIT` PREPARED or `ROLLBACK` PREPARED to commit or roll back these statements.

#### Unused replication slots

Unused replication slots prevent autovacuum from claiming dead tuples. The following query helps identify unused replication slots:

```sql
    SELECT slot_name, slot_type, database, xmin
    FROM pg_replication_slots
    ORDER BY age(xmin) DESC;
```

Use `pg_drop_replication_slot()` to delete unused replication slots.

When the database runs into transaction ID wraparound protection, check for any blockers as mentioned previously, and remove the blockers manually for autovacuum to continue and complete. You can also increase the speed of autovacuum by setting `autovacuum_cost_delay` to 0 and increasing the `autovacuum_cost_limit` to a value greater than 200. However, changes to these parameters don't apply to existing autovacuum workers. Either restart the database or kill existing workers manually to apply parameter changes.

### Table-specific requirements

You can set autovacuum parameters for individual tables. These settings are especially important for small and large tables. For example, for a small table that contains only 100 rows, autovacuum triggers the VACUUM operation when 70 rows change (as calculated previously). If you frequently update this table, you might see hundreds of autovacuum operations a day. These operations prevent autovacuum from maintaining other tables where the percentage of changes isn't as significant. Alternatively, a table containing a billion rows needs to change 200 million rows to trigger autovacuum operations. Setting autovacuum parameters appropriately prevents such scenarios.

To set autovacuum settings for each table, change the server parameters as shown in the following examples:

```sql
    ALTER TABLE <table name> SET (autovacuum_analyze_scale_factor = xx);
    ALTER TABLE <table name> SET (autovacuum_analyze_threshold = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_scale_factor = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_threshold = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_cost_delay = xx);
    ALTER TABLE <table name> SET (autovacuum_vacuum_cost_limit = xx);
    -- For PostgreSQL 16 and later:
    ALTER TABLE <table name> SET (vacuum_buffer_usage_limit = 'xx MB');
```

### Insert-only workloads

In PostgreSQL versions 13 and earlier, autovacuum doesn't run on tables with an insert-only workload, as there are no dead tuples and no free space that needs to be reclaimed. However, autoanalyze runs for insert-only workloads since there's new data. The disadvantages of this behavior are:

- The visibility map of the tables isn't updated, and thus query performance, especially where there are Index Only Scans, starts to suffer over time.
- The database can run into transaction ID wraparound protection.
- Hint bits aren't set.

#### Solutions

##### PostgreSQL versions 13 and earlier

By using the **pg_cron** extension, you can set up a cron job to schedule a periodic vacuum analyze on the table. The frequency of the cron job depends on the workload.

For guidance, see [special considerations about using pg_cron in Azure Database for PostgreSQL](../extensions/concepts-extensions-considerations.md#pg_cron).

##### PostgreSQL 13 and later versions

Autovacuum runs on tables with an insert-only workload. Two server parameters, `autovacuum_vacuum_insert_threshold` and `autovacuum_vacuum_insert_scale_factor`, help control when autovacuum can be triggered on insert-only tables.

## Troubleshooting guides

Azure Database for PostgreSQL flexible server provides troubleshooting guides in the portal that help you monitor bloat at the database or individual schema level and identify potential blockers to the autovacuum process. 

Two troubleshooting guides are available:

- **Autovacuum monitoring** - Use this guide to monitor bloat at the database or individual schema level.
- **Autovacuum blockers and wraparound** - This guide helps you identify potential autovacuum blockers and provides information on how far the databases on the server are from wraparound or emergency situations.

The troubleshooting guides also share recommendations to mitigate potential issues. For information about how to set up and use the troubleshooting guides, see [setup troubleshooting guides](how-to-troubleshooting-guides.md).

### Terminating autovacuum process: pg_signal_autovacuum_worker role

Autovacuum is an important background process because it helps with efficient storage and performance maintenance in the database. In the normal autovacuum process, it cancels itself after the `deadlock_timeout`. If a user executes a DDL statement on a table, the user might have to wait until the `deadlock_timeout` interval. Autovacuum doesn't allow executing reads or writes on the table requested by different connection requests, adding to latency in the transaction.

We introduced a new role `pg_signal_autovacuum_worker` from PostgreSQL, which allows nonsuperuser members to terminate an ongoing autovacuum task. The new role helps users get secure and controlled access to the autovacuum process. Non-superusers can cancel the autovacuum process once they're granted the `pg_signal_autovacuum_worker` role by using the `pg_terminate_backend` command. The role `pg_signal_autovacuum_worker` is available in Azure Database for PostgreSQL in PostgreSQL versions 15 and later.

#### Recommended approach for repetitive autovacuum workers

In rare scenarios, such as anti-wraparound autovacuum, workers might restart immediately after termination because they're critical for preventing transaction ID exhaustion. To minimize repeated conflicts, follow these steps:

- Queue the DDL operation prior to termination:
  - Session 1: Prepare and run the DDL statement.
  - Session 2: Terminate the autovacuum process.
  
    > [!Important]
    > These two steps must be executed back-to-back. If the DDL statement remains blocked for too long, it can hold locks and block other DML operations on the server.

- Terminate autovacuum and execute DDL: If the DDL must run immediately:
  - Terminate the autovacuum process using pg_terminate_backend().
  - Execute the DDL statement right after termination.

Steps to avoid repeated conflicts:

1. Grant role to user

    ```sql
    GRANT pg_signal_autovacuum_worker TO app_user;
    ```
    1. Identify autovacuum process ID
    
    ```sql
    SELECT pid, query FROM pg_stat_activity WHERE query LIKE '%autovacuum%' and pid!=pg_backend_pid();
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
> We don't recommend terminating ongoing autovacuum processes because doing so might lead to table and database bloat, which can further lead to performance regressions. However, in cases where there's a business-critical requirement involving the scheduled execution of a DDL statement that coincides with the autovacuum process, non-superusers can terminate the autovacuum in a controlled and secure manner by using the `pg_signal_autovacuum_worker` role.

## Azure Advisor recommendations

Azure Advisor recommendations proactively identify if a server has a high bloat ratio or if the server is approaching a transaction wraparound scenario. You can also [create Azure Advisor alerts for the recommendations](/azure/advisor/advisor-alerts-portal).

The recommendations are:

- **High bloat ratio**: A high bloat ratio can affect server performance in several ways. One significant issue is that the PostgreSQL Engine Optimizer might struggle to select the best execution plan, leading to degraded query performance. Therefore, a recommendation is triggered when the bloat percentage on a server reaches a certain threshold to avoid such performance issues.

- **Transaction wraparound**: This scenario is one of the most serious issues a server can encounter. Once your server is in this state, it might stop accepting any more transactions, causing the server to become read-only. Hence, a recommendation is triggered when the server crosses 1 billion transactions threshold.

## Related content

- [Full vacuum using pg_repack in Azure Database for PostgreSQL](how-to-perform-fullvacuum-pg-repack.md)
- [Troubleshoot high CPU utilization in Azure Database for PostgreSQL](how-to-high-cpu-utilization.md)
- [Troubleshoot high memory utilization in Azure Database for PostgreSQL](how-to-high-memory-utilization.md)
- [Troubleshoot high IOPS utilization in Azure Database for PostgreSQL](how-to-high-io-utilization.md)
- [Troubleshoot and identify slow-running queries in Azure Database for PostgreSQL](how-to-identify-slow-queries.md)
- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md)
