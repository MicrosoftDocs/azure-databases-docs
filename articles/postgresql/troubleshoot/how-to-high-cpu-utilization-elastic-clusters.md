---
title: High CPU Utilization Across Azure Database for PostgreSQL Elastic Clusters
description: Troubleshoot high CPU utilization across Azure Database for PostgreSQL elastic clusters.
author: GayathriPaderla
ms.author: gapaderla
ms.reviewer: jaredmeade
ms.date: 01/28/2026
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: troubleshooting-general
---

# Troubleshoot High CPU Utilization in Azure Database for PostgreSQL Elastic Clusters

This article describes how to identify the root cause of high CPU utilization. It also provides possible remedial actions to control CPU utilization when using [Elastic clusters in Azure Database for PostgreSQL](../elastic-clusters/concepts-elastic-clusters.md).

In this article, you learn about:

- How to use tools like Azure Metrics, pg_stat_statements, citus_stat_activity, and pg_stat_activity to identify high CPU utilization.
- How to identify root causes, such as long running queries and total connections
- How to resolve high CPU utilization by using EXPLAIN ANALYZE and vacuuming tables.

## Tools to Identify High CPU Utilization

Consider the use of the following list of tools to identify high CPU utilization:

### Azure Metrics

Azure Metrics is a good starting point to check the CPU utilization for a specific period. Metrics provide information about the resources utilized during the period in which you are monitoring. You can use the **Apply splitting** option and **Split by Server Name** to view the details of each individual node in your elastic cluster. You can then compare the performance of **Write IOPs, Read IOPs, Read Throughput Bytes/Sec**, and **Write Throughput Bytes/Sec** with **CPU percent**, to view the performance of individual nodes when you observe your workload consuming high CPU. 

Once you have identified a particular node (or nodes) with higher than expected CPU utilization, you can connect directly to one more nodes in question and perform a more in-depth analysis using the following Postgres tools:

### pg_stat_statements

The `pg_stat_statements` extension helps identify queries that consume time on the server. For more information about this extension, see the detailed [documentation](https://www.postgresql.org/docs/current/pgstatstatements.html).

#### Calls/Mean & Total Execution Time 

The following query returns the top five SQL statements by highest total execution time:

```sql
SELECT userid::regrole, dbid, query, total_exec_time, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY total_exec_time
DESC LIMIT 5;
```

### pg_stat_activity

The `pg_stat_activity` view shows the queries that are currently being executed on the specific node. Monitor active queries, sessions, and states on that node.

```sql
SELECT *, now() - xact_start AS duration
FROM pg_stat_activity
WHERE state IN ('idle in transaction', 'active') AND pid <> pg_backend_pid()
ORDER BY duration DESC;
```

### citus_stat_activity

The `citus_stat_activity` view shows the distributed queries that are executing on all nodes, and is a superset of `pg_stat_activity`. This view also shows tasks specific to subqueries dispatched to workers, task state, and worker nodes.

```sql
SELECT *, now() - xact_start AS duration
FROM citus_stat_activity
WHERE state IN ('idle in transaction', 'active') AND pid <> pg_backend_pid()
ORDER BY duration DESC;
```

## Identify Root Causes

If CPU consumption levels are high in general, the following scenarios could be possible root causes:

### Long-running transactions on specific node

Long-running transactions can consume CPU resources that lead to high CPU utilization.

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

Long-running transactions can consume CPU resources that lead to high CPU utilization.

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

Slow queries can consume CPU resources that lead to high CPU utilization.

The following query helps identify queries taking longer run times:

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

Many connections to the database might also lead to increased CPU utilization.

The following query provides information about the number of connections by state on a single node:

```sql
SELECT state, COUNT(*) 
FROM pg_stat_activity 
WHERE pid <> pg_backend_pid() 
GROUP BY state 
ORDER BY state ASC;
```

### Total number of connections and number of connections by state on all nodes

Many connections to the database might also lead to increased CPU utilization.

The following query gives information about the number of connections by state across all nodes:

```sql
SELECT state, COUNT(*) 
FROM citus_stat_activity 
WHERE pid <> pg_backend_pid() 
GROUP BY state 
ORDER BY state ASC;
```

### Vacuum and Table Stats

Keeping table statistics up to date helps improve query performance. Monitor whether regular auto vacuuming is being carried out.

The following query helps to identify the tables that need vacuuming:
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

The following image highlights the output resulting from the above query. The "result" column is a json datatype containing information on the stats.

:::image type="content" source="./media/how-to-high-cpu-utilization-elastic-clusters/elastic-clusters-cpu-utilization-result.png" alt-text="Results returned from query response - including `result` column as a json datatype " lightbox="./media/how-to-high-cpu-utilization-elastic-clusters/elastic-clusters-cpu-utilization-result.png":::

The last_autovacuum and last_autoanalyze columns provide the date and time when the table was last auto vacuumed or analyzed. If the tables aren't being vacuumed regularly, take steps to tune autovacuum.

The following query provides information regarding the amount of bloat at the schema level:

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

## Resolve High CPU Utilization

Use EXPLAIN ANALYZE to examine any slow queries and terminate any improperly long running transactions. Consider using the built-in PgBouncer connection pooler and clear up excessive bloat to resolve high CPU utilization.

### Use EXPLAIN ANALYZE

Once you know the queries that are consuming more CPU, use **EXPLAIN ANALYZE** to further investigate and tune them.

For more information about the **EXPLAIN ANALYZE** command, review its [documentation](https://www.postgresql.org/docs/current/sql-explain.html).

### Terminate long running transactions on a nodes

You can consider terminating a long running transaction as an option if the transaction is running longer than expected.

To terminate a session's PID, you need to find its PID by using the following query:

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

You can also filter by other properties like usename (user name), datname (database name), etc.

Once you have the session's PID, you can terminate it using the following query:

```sql
SELECT pg_terminate_backend(pid);
```

Terminating the pid ends the specific sessions related to a node.

### Terminate long running transactions on all nodes

You could consider ending a long running transaction as an option.

To terminate a session's PID, you need to find its PID, global_pid by using the following query:

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

You can also filter by other properties like usename (user name), datname (database name), etc.

Once you have the session's PID, you can terminate it using the following query:

```sql
SELECT pg_terminate_backend(pid);
```
Terminating the pid ends the specific sessions related to a worker node.

The same query running on different worker nodes might have same global_pid’s. In that case, you can end long running transaction on all worker nodes use global_pid. 

The following screenshot shows the relativity of the global_pid’s to session pid’s.

:::image type="content" source="./media/how-to-high-cpu-utilization-elastic-clusters/global-pid-to-session-pid-example.png" alt-text="global pid to session pid reference example" lightbox="./media/how-to-high-cpu-utilization-elastic-clusters/global-pid-to-session-pid-example.png":::

```sql
SELECT pg_terminate_backend(global_pid);
```

> [!NOTE]  
> To terminate long running transactions, it is advised to set server parameters `statement_timeout` or `idle_in_transaction_session_timeout`.

## Clearing bloat

A short-term solution would be to manually vacuum and then analyze the tables where slow queries are seen:

```sql
VACUUM ANALYZE <table>;
```

## Managing Connections

In situations where there are many short-lived connections, or many connections that remain idle for most of their life, consider using a connection pooler like PgBouncer.

## PgBouncer, a built-in connection pooler

For more information about PgBouncer, see [connection pooler](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/not-all-postgres-connection-pooling-is-equal/ba-p/825717) and [connection handling best practices with PostgreSQL](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/connection-handling-best-practice-with-postgresql/ba-p/790883)

Azure Database for PostgreSQL Elastic Clusters offer PgBouncer as a built-in connection pooling solution. For more information, see [PgBouncer](../connectivity/concepts-pgbouncer.md).

## Related content

- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md).
- [Autovacuum tuning in Azure Database for PostgreSQL](how-to-autovacuum-tuning.md).
