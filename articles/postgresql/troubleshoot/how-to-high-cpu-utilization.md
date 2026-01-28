---
title: High CPU utilization
description: Troubleshooting guide for high CPU utilization.
author: sarat0681
ms.author: sbalijepalli
ms.reviewer: maghan
ms.date: 12/10/2024
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: troubleshooting-general
---

# Troubleshoot high CPU utilization in Azure Database for PostgreSQL 

This article describes how to identify the root cause of high CPU utilization. It also provides possible remedial actions to control CPU utilization when using [Azure Database for PostgreSQL](../overview.md).

In this article, you can learn:

- About troubleshooting guides to identify and get recommendations to mitigate root causes.
- About tools to identify high CPU utilization such as Azure Metrics, query store, and pg_stat_statements.
- How to identify root causes, such as long running queries and total connections.
- How to resolve high CPU utilization by using EXPLAIN ANALYZE, connection pooling, and vacuuming tables.

## Troubleshooting guides

Using the **Troubleshooting guides** you can identify the probable root cause of a high CPU scenario, and can read through recommendations to mitigate the problem found.

To learn how to set up and use the troubleshooting guides, follow [setup troubleshooting guides](how-to-troubleshooting-guides.md).

## Tools to identify high CPU utilization

Consider the use of the following list of tools to identify high CPU utilization.

### Azure Metrics

Azure Metrics is a good starting point to check the CPU utilization for a specific period. Metrics provide information about the resources utilized during the period in which CPU utilization is high. Compare the graphs of **Write IOPs**, **Read IOPs**, **Read Throughput Bytes/Sec**, and **Write Throughput Bytes/Sec** with **CPU percent**, to find out times when the workload caused high CPU.

For proactive monitoring, you can configure alerts on the metrics. For step-by-step guidance, see [Azure Metrics](../monitor/how-to-alert-on-metrics.md).

### Query store

Query store automatically captures the history of queries and runtime statistics, and it retains them for your review. It slices the data by time, so that you can see temporal usage patterns. Data for all users, databases, and queries is stored in a database named `azure_sys` in the Azure Database for PostgreSQL flexible server instance.

Query store can correlate wait event information with query run time statistics. Use query store to identify queries that have high CPU consumption during the period of interest.

For more information, see [query store](../monitor/concepts-query-store.md).

### pg_stat_statements

The `pg_stat_statements` extension helps identify queries that consume time on the server. For more information about this extension, see its [documentation](https://www.postgresql.org/docs/current/pgstatstatements.html).

#### Mean or average execution time

##### [Postgres v13 & higher](#tab/mean-postgres13)

For Postgres versions 13 and above, use the following statement to view the top five SQL statements by mean or average execution time:

```sql
SELECT userid::regrole, dbid, query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 5;
```

##### [Postgres v12](#tab/mean-postgres12)

For Postgres version 12, use the following statement to view the top five SQL statements by mean or average execution time:

```sql
SELECT userid::regrole, dbid, query
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 5;
```
---

#### Total execution time

Execute the following statements to view the top five SQL statements by total execution time.

##### [Postgres v13 & higher](#tab/total-postgres13)

For Postgres versions 13 and above, use the following statement to view the top five SQL statements by total execution time:

```sql
SELECT userid::regrole, dbid, query
FROM pg_stat_statements
ORDER BY total_exec_time
DESC LIMIT 5;
```

##### [Postgres v12](#tab/total-postgres12)

For Postgres version 12, use the following statement to view the top five SQL statements by total execution time:

```sql
SELECT userid::regrole, dbid, query,
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 5;
```

---

## Identify root causes

If CPU consumption levels are high in general, the following ones could be possible root causes:

### Long-running transactions

Long-running transactions can consume CPU resources that can lead to high CPU utilization.

The following query helps identify connections running for the longest time:

```sql
SELECT pid, usename, datname, query, now() - xact_start as duration
FROM pg_stat_activity
WHERE pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY duration DESC;
```

### Total number of connections and number of connections by state

A large number of connections to the database might also lead to increased CPU and memory utilization.

The following query gives information about the number of connections by state:

```sql
SELECT state, count(*)
FROM  pg_stat_activity
WHERE pid <> pg_backend_pid()
GROUP BY state
ORDER BY state ASC;
```

## Resolve high CPU utilization

Use EXPLAIN ANALYZE, consider using the built-in PgBouncer connection pooler, and terminate long running transactions to resolve high CPU utilization.

### Use EXPLAIN ANALYZE

Once you know the queries that are consuming more CPU, use **EXPLAIN ANALYZE** to further investigate and tune them.

For more information about the **EXPLAIN ANALYZE** command, review its [documentation](https://www.postgresql.org/docs/current/sql-explain.html).

### PgBouncer, a built-in connection pooler

In situations where there are many short-lived connections, or many connections that remain idle for most of their life, consider using a connection pooler like PgBouncer.

For more information about PgBouncer, see [connection pooler](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/not-all-postgres-connection-pooling-is-equal/ba-p/825717) and [connection handling best practices with PostgreSQL](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/connection-handling-best-practice-with-postgresql/ba-p/790883)

Azure Database for PostgreSQL offers PgBouncer as a built-in connection pooling solution. For more information, see [PgBouncer](../connectivity/concepts-pgbouncer.md).

### Terminate long running transactions

You could consider killing a long running transaction as an option.

To terminate a session's PID, you need to find its PID by using the following query:

```sql
SELECT pid, usename, datname, query, now() - xact_start as duration
FROM pg_stat_activity
WHERE pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active')
ORDER BY duration DESC;
```

You can also filter by other properties like `usename` (user name), `datname` (database name), etc.

Once you have the session's PID, you can terminate it using the following query:

```sql
SELECT pg_terminate_backend(pid);
```

### Monitor vacuum and table stats

Keeping table statistics up to date helps improve query performance. Monitor whether regular autovacuuming is being carried out.

The following query helps to identify the tables that need vacuuming:

```sql
SELECT schemaname,relname,n_dead_tup,n_live_tup,last_vacuum,last_analyze, last_autovacuum,last_autoanalyze
FROM pg_stat_all_tables
WHERE n_live_tup > 0;
```

`last_autovacuum` and `last_autoanalyze` columns give the date and time when the table was last autovacuumed or analyzed. If the tables aren't being vacuumed regularly, take steps to tune autovacuum.

For more information about autovacuum troubleshooting and tuning, see [Autovacuum Troubleshooting](how-to-autovacuum-tuning.md).

A short-term solution would be to do a manual vacuum analyze of the tables where slow queries are seen:

```sql
VACUUM ANALYZE <table>;
```

## Related content

- [Troubleshoot high memory utilization in Azure Database for PostgreSQL](how-to-high-memory-utilization.md).
- [Troubleshoot high IOPS utilization in Azure Database for PostgreSQL](how-to-high-io-utilization.md).
- [Troubleshoot and identify slow-running queries in Azure Database for PostgreSQL](how-to-identify-slow-queries.md).
- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md).
- [Autovacuum tuning in Azure Database for PostgreSQL](how-to-autovacuum-tuning.md).
