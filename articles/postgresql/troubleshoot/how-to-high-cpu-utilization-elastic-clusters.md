---
title: Troubleshoot High CPU Utilization in Elastic Clusters
description: How to troubleshoot high CPU utilization across Azure Database for PostgreSQL Elastic Clusters.
author: GayathriPaderla
ms.author: gapaderla
ms.reviewer: jaredmeade, maghan
ms.date: 02/17/2026
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: troubleshooting-general
---

# Troubleshoot high CPU utilization in Azure Database for PostgreSQL Elastic Clusters

This article describes how to identify the root cause of high CPU utilization. It also provides possible remedial actions to control CPU utilization when using [Elastic clusters in Azure Database for PostgreSQL](../elastic-clusters/concepts-elastic-clusters.md).

In this article, you learn about:

- How to use tools like Azure Metrics, `pg_stat_statements`, `citus_stat_activity`, and `pg_stat_activity` to identify high CPU utilization.
- How to identify root causes, such as long running queries and total connections.
- How to resolve high CPU utilization by using `EXPLAIN ANALYZE` and vacuuming tables.

## Tools to identify high CPU utilization

Use the following tools to identify high CPU utilization:

### Azure Metrics

Azure Metrics is a good starting point to check the CPU utilization for a specific period. Metrics provide information about the resources utilized during the period in which you're monitoring. You can use the **Apply splitting** option and **Split by Server Name** to view the details of each individual node in your elastic cluster. You can then compare the performance of **Write IOPs, Read IOPs, Read Throughput Bytes/Sec**, and **Write Throughput Bytes/Sec** with **CPU percent**, to view the performance of individual nodes when you observe your workload consuming high CPU.

After you identify a particular node (or nodes) with higher than expected CPU utilization, you can connect directly to one or more nodes in question and perform a more in-depth analysis by using the following Postgres tools:

### pg_stat_statements

The `pg_stat_statements` extension helps identify queries that consume time on the server. For more information about this extension, see the detailed [documentation](https://www.postgresql.org/docs/current/pgstatstatements.html).

#### Calls/Mean and total execution time

The following query returns the top five SQL statements by highest total execution time:

```sql
SELECT userid::regrole, dbid, query, total_exec_time, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY total_exec_time
DESC LIMIT 5;
```

### pg_stat_activity

The `pg_stat_activity` view shows the queries that are currently running on the specific node. Use it to monitor active queries, sessions, and states on that node.

```sql
SELECT *, now() - xact_start AS duration
FROM pg_stat_activity
WHERE state IN ('idle in transaction', 'active') AND pid <> pg_backend_pid()
ORDER BY duration DESC;
```

### citus_stat_activity

The `citus_stat_activity` view is a superset of `pg_stat_activity`. It shows the distributed queries that are running on all nodes. It also shows tasks specific to subqueries dispatched to workers, task state, and worker nodes.

```sql
SELECT *, now() - xact_start AS duration
FROM citus_stat_activity
WHERE state IN ('idle in transaction', 'active') AND pid <> pg_backend_pid()
ORDER BY duration DESC;
```

## Identify root causes

If CPU consumption levels are high, the following scenarios might be the root causes:

### Long-running transactions on specific node

Long-running transactions consume CPU resources and lead to high CPU utilization.

The following query provides information on long-running transactions:

```sql
SELECT
    pid,
    datname,
    usename,
    application_name,
    client_addr,
    backend_start,
    query_start,
    now() - query_start AS duration,
    state,
    wait_event,
    wait_event_type,
    query
FROM pg_stat_activity
WHERE state != 'idle' AND pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY now() - query_start DESC;
```

### Long-running transactions on all nodes

Long-running transactions consume CPU resources and lead to high CPU utilization.

The following query provides information on long-running transactions across all nodes:

```sql
SELECT
    global_pid, pid,
    nodeid,
    datname,
    usename,
    application_name,
    client_addr,
    backend_start,
    query_start,
    now() - query_start AS duration,
    state,
    wait_event,
    wait_event_type,
    query
FROM citus_stat_activity
WHERE state != 'idle' AND pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY now() - query_start DESC;
```

### Slow query

Slow queries consume CPU resources and cause high CPU utilization.

The following query helps you identify queries that take longer run times:

```sql
SELECT
    query,
    calls,
    mean_exec_time,
    total_exec_time,
    rows,
    shared_blks_hit,
    shared_blks_read,
    shared_blks_dirtied,
    shared_blks_written,
    temp_blks_read,
    temp_blks_written,
    wal_records,
    wal_fpi,
    wal_bytes
FROM pg_stat_statements
WHERE query ILIKE '%select%' OR query ILIKE '%insert%' OR query ILIKE '%update%' OR query ILIKE '%delete%' OR queryid = <queryid>
ORDER BY total_exec_time DESC;
```

### Total number of connections and number of connections by state on a node

Many connections to the database lead to increased CPU utilization.

The following query provides information about the number of connections by state on a single node:

```sql
SELECT state, COUNT(*)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
GROUP BY state
ORDER BY state ASC;
```

### Total number of connections and number of connections by state on all nodes

Many connections to the database lead to increased CPU utilization.

The following query gives information about the number of connections by state across all nodes:

```sql
SELECT state, COUNT(*)
FROM citus_stat_activity
WHERE pid <> pg_backend_pid()
GROUP BY state
ORDER BY state ASC;
```

### Vacuum and table stats

Keeping table statistics up to date helps improve query performance. Monitor whether regular autovacuuming is happening.

The following query helps you identify the tables that need vacuuming:

```sql
SELECT *
FROM run_command_on_all_nodes($$
  SELECT json_agg(t)
  FROM (
    SELECT schemaname, relname
    ,n_live_tup, n_dead_tup
    ,n_dead_tup / (n_live_tup) AS bloat
    ,last_autovacuum, last_autoanalyze
    ,last_vacuum, last_analyze
    FROM pg_stat_user_tables
    WHERE n_live_tup > 0 AND relname LIKE '%orders%'
    ORDER BY n_dead_tup DESC
  ) t
$$);
```

The following image highlights the output from the preceding query. The `result` column is a JSON data type containing information on the stats.

:::image type="content" source="./media/how-to-high-cpu-utilization-elastic-clusters/elastic-clusters-cpu-utilization-result.png" alt-text="Results returned from query response - including `result` column as a json datatype " lightbox="./media/how-to-high-cpu-utilization-elastic-clusters/elastic-clusters-cpu-utilization-result.png":::

The `last_autovacuum` and `last_autoanalyze` columns provide the date and time when the table was last autovacuumed or analyzed. If the tables aren't autovacuumed regularly, take steps to tune autovacuum.

The following query provides information about the amount of bloat at the schema level:

```sql
SELECT *
FROM run_command_on_all_nodes($$
  SELECT json_agg(t) FROM (
    SELECT schemaname, sum(n_live_tup) AS live_tuples
    , sum(n_dead_tup) AS dead_tuples
    FROM pg_stat_user_tables
    WHERE n_live_tup > 0
    GROUP BY schemaname
    ORDER BY sum(n_dead_tup) DESC
  ) t
$$);
```

## Resolve high CPU utilization

Use EXPLAIN ANALYZE to examine any slow queries and terminate any improperly long running transactions. Consider using the built-in PgBouncer connection pooler and clear up excessive bloat to resolve high CPU utilization.

### Use EXPLAIN ANALYZE

After you identify the queries that consume more CPUs, use **EXPLAIN ANALYZE** to further investigate and tune them.

For more information about the **EXPLAIN ANALYZE** command, see its [documentation](https://www.postgresql.org/docs/current/sql-explain.html).

### Terminate long running transactions on a node

Consider terminating a long running transaction if the transaction runs longer than expected.

To terminate a session's PID, first find the PID by using the following query:

```sql
SELECT
    pid,
    datname,
    usename,
    application_name,
    client_addr,
    backend_start,
    query_start,
    now() - query_start AS duration,
    state,
    wait_event,
    wait_event_type,
    query
FROM pg_stat_activity WHERE state != 'idle' AND pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY now() - query_start DESC;
```

You can also filter by other properties like `usename` (user name), `datname` (database name), and more.

After you get the session's PID, terminate it by using the following query:

```sql
SELECT pg_terminate_backend(pid);
```

Terminating the PID ends the specific sessions related to a node.

### Terminate long running transactions on all nodes

Consider ending a long running transaction.

To terminate a session's PID, find its PID and global_pid by using the following query:

```sql
SELECT
    global_pid,
    pid,
    nodeid,
    datname,
    usename,
    application_name,
    client_addr,
    backend_start,
    query_start,
    now() - query_start AS duration,
    state,
    wait_event,
    wait_event_type,
    query
FROM citus_stat_activity WHERE state != 'idle' AND pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY now() - query_start DESC;
```

You can also filter by other properties like `usename` (user name), `datname` (database name), and more.

After you get the session's PID, terminate it by using the following query:

```sql
SELECT pg_terminate_backend(pid);
```
Terminating the pid ends the specific sessions related to a worker node.

The same query running on different worker nodes might have same global_pid's. In that case, you can end long running transaction on all worker nodes use global_pid.

The following screenshot shows the relativity of the global_pid's to session pid's.

:::image type="content" source="./media/how-to-high-cpu-utilization-elastic-clusters/global-pid-to-session-pid-example.png" alt-text="global pid to session pid reference example" lightbox="./media/how-to-high-cpu-utilization-elastic-clusters/global-pid-to-session-pid-example.png":::

```sql
SELECT pg_terminate_backend(global_pid);
```

> [!NOTE]  
> To terminate long running transactions, set server parameters `statement_timeout` or `idle_in_transaction_session_timeout`.

## Clearing bloat

A short-term solution is to manually vacuum and then analyze the tables where slow queries appear:

```sql
VACUUM ANALYZE <table>;
```

## Managing connections

If your application uses many short-lived connections or many connections that stay idle for most of their life, consider using a connection pooler like PgBouncer.

## PgBouncer, a built-in connection pooler

For more information about PgBouncer, see [connection pooler](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/not-all-postgres-connection-pooling-is-equal/ba-p/825717) and [connection handling best practices with PostgreSQL](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/connection-handling-best-practice-with-postgresql/ba-p/790883).

Azure Database for PostgreSQL Elastic Clusters offer PgBouncer as a built-in connection pooling solution. For more information, see [PgBouncer](../connectivity/concepts-pgbouncer.md).

## Related content

- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md)
- [Autovacuum tuning in Azure Database for PostgreSQL](how-to-autovacuum-tuning.md)
