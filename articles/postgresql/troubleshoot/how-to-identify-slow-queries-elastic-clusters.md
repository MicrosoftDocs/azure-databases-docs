---
title: Identify Slow Running Queries on elastic clusters
description: Troubleshooting guide for identifying slow running queries in Azure Database for PostgreSQL elastic clusters.
author: GayathriPaderla
ms.author: gapaderla
ms.reviewer: jaredmeade, maghan
ms.date: 03/23/2026
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: troubleshooting-general
---

# Troubleshoot and identify slow-running queries in Azure Database for PostgreSQL Elastic Clusters

This article describes how to identify and diagnose the root cause of slow-running queries, which can consume CPU resources and lead to high CPU utilization.

## Identifying the slow query

You could identify the slow query using `pg_stat_statments`. Below is the query which would help us identify the top 5 slow queries.

```sql
SELECT userid::regrole, dbid, query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 5;
```

## Inspect current active/long-running queries:

The following query helps identify queries running for greater than 15 minutes.

```sql
SELECT 
    global_pid,pid,
    nodeid,
    datname,
    usename,
    application_name,
    client_addr,
    backend_start,
    query_start,
    NOW() - query_start AS duration,
    state,
    wait_event,
    wait_event_type,
    query
FROM citus_stat_activity 
WHERE state != 'idle' 
AND pid <> pg_backend_pid() 
AND state IN ('idle in transaction', 'active') 
AND NOW() - query_start > '15 minutes'
ORDER BY NOW() - query_start  DESC;
```

:::image type="content" source="./media/how-to-identify-slow-queries-elastic-clusters/long-running-queries.png" alt-text="Screenshot of long-running queries result." lightbox="./media/how-to-identify-slow-queries-elastic-clusters/long-running-queries.png":::

This tells us there is one query on the server which has been running slow and taking longer execution times.

The `global_pid` associated to the long running query is the same, which means the same query is running the longest on all the worker nodes.

### Identifying the tables and their distribution type in the query:

   1.	The distributed tables
   2.	The reference tables
   3.	The colocation tables

If any tables are regular, make them either reference tables or colocation tables.  You can find that information using the query below.

```sql
SELECT table_name,
       distribution_type,
       distribution_column,
       shard_count,
       colocation_id
FROM citus_tables
ORDER BY table_name;
```

What to look for in the above query:

   -	distribution_type = reference → broadcast joins
   -	Missing or wrong distribution_column

### Solution:

Change the regular table to a reference or colocation table, this enables reducing the network latency going back and forth the different nodes.

```sql
SELECT create_reference_table('products');
```

## Detect Non-Colocated tables used in joins:

One of the topmost causes for slow queries could be non-colocated table. Here is the query below to identify any such non-colocated tables.

```sql
SELECT a.table_name AS table_a,
       b.table_name AS table_b,
       a.colocation_id AS colocation_a,
       b.colocation_id AS colocation_b
FROM citus_tables a
JOIN citus_tables b
  ON a.table_name <> b.table_name
WHERE a.colocation_id <> b.colocation_id;
```

What to look for in the above query:

   1.	If your tables from query join are listed here, which means they are not collocated causing the below.
      a.	Data reshuffling across nodes
      b.	Network overhead
      c.	Temp file spills

You can identify this from query plans of the query. If you notice the nodes below:

   1.	Distributed Repartition Join
   2.	Distributed Subplan/Union

### Solution:
   •	Distribute tables on the join key.
   •	Make sure the distributed table and reference table are joined correctly
   •	Index the join keys
   •	Fix colocation of the table by pointing the table to the right distribution key.
    o	For which you might need to undistributed the table and then distribute the table using the right distribution key.

```sql
SELECT undistribute_table('orders');
SELECT create_distributed_table('orders', 'customer_id');
```

## Check for the Skewness of data across shards/nodes

The below query provides which shard/Node the query is running longer on and shard size.

```sql
SELECT
    shardid,
    cs.shard_size/1024/1024 AS shard_size_mb,
    nodeid,
    nodename,
    global_pid,
    pid,
    state,
    query,
    NOW() - query_start AS duration
FROM citus_shards cs
JOIN citus_stat_activity ON citus_stat_activity.query LIKE '%' || cs.shardid || '%' AND pid <> pg_backend_pid() AND state IN ('idle in transaction', 'active') AND NOW() - query_start > '15 minutes'
ORDER BY duration DESC;
```

From the output we see the queries are accessing 4 specific shards in each of the worker nodes. 

If you see the data sitting on just few worker nodes and the remaining worker nodes have no data. Then this points out to distribution key selection issue.

You can further troubleshoot but get into the details of the distributed table by shards using the below query

```sql
SELECT * FROM run_command_on_shards('orders', $$ SELECT json_build_object( 'shard_name', '%1$s', 'size', pg_size_pretty(pg_table_size('%1$s')) ); $$); 
```

### Solution:

Based on the above output, if the data is skewed on few shards and not on all, that might point us to the distribution key causing the skewness in which case rearchitecting the distribution key would be a good solution. 

Here is a talk on choosing the right shard key. [Efficiently distributing Postgres with Citus – How to choose the right shard key? | Citus Con 2022](https://www.youtube.com/watch?v=t0EXeWk3lAk)

## Diagnose any lock contention

Check for any locking and blocking happening using the below query.

```sql
SELECT
    lw.waiting_gpid AS blocked_gpid,
    lw.blocking_gpid AS blocking_gpid,
    wa.query AS blocked_query,
    wa.state AS blocked_state,
    wa.wait_event AS blocked_wait_event,
    wa.wait_event_type AS blocked_wait_event_type,
    NOW() - wa.query_start AS blocked_duration,
    ba.query AS blocking_query,
    ba.state AS blocking_state,
    ba.wait_event AS blocking_wait_event,
    ba.wait_event_type AS blocking_wait_event_type,
    lw.waiting_nodeid,
    lw.blocking_nodeid
FROM citus_lock_waits lw
LEFT JOIN citus_stat_activity wa ON lw.waiting_gpid = wa.global_pid
LEFT JOIN citus_stat_activity ba ON lw.blocking_gpid = ba.global_pid
ORDER BY blocked_duration DESC NULLS LAST;
```

### Solution:
Terminate the blocking_gpid using the command below.

```sql
SELECT pg_terminate_backend(blocking_gpid);
```

## Check for the Bloat for the tables involved in the slow query

Get the stats details by executing the below query from the customer server to see the vacuum and analyze statistics of the tables involved in the slow query.

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM ( 
   SELECT * FROM pg_stat_user_tables WHERE relname LIKE '%orders%' ORDER BY n_dead_tup DESC LIMIT 5 
) t $$) ;
```

This query provides the output in the below format. The result column is a json column with all the information of the stats related to the table.

:::image type="content" source="./media/how-to-identify-slow-queries-elastic-clusters/bloat.png" alt-text="Screenshot of bloat check query result." lightbox="./media/how-to-identify-slow-queries-elastic-clusters/bloat.png":::
 
### Solution:

If you observe the `n_dead_tup/n_live_tup` proceed to run `VACUUM` on the table.

## Check the query plan for missing indexes

Get the query plan of the query by running the below

```sql
EXPLAIN (ANALYZE,BUFFERS) <query>;
```

Look for sequential scan nodes in the query plan and the number of row processed, if number of rows are huge taking up the maximum execution time.

### Solution:

Add appropriate indexes to the table to improve the query performance.

## Check for Cache/IO efficiency

To check for cache hit rate using the below query.

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (
   SELECT sum(heap_blks_read) AS Reads, sum(heap_blks_hit) AS Hits, 100 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_rate
   FROM pg_statio_user_tables
) t $$ );
```

## Index cache hit rate:

```sql
SELECT * FROM run_command_on_all_nodes( $$ SELECT json_agg(t) FROM (
   SELECT sum(idx_blks_read) AS index_reads, sum(idx_blks_hit) AS index_hits, 100 * sum(idx_blks_hit) / (sum(idx_blks_hit) + sum(idx_blks_read)) AS index_cache_hit_rate
   FROM pg_statio_user_indexes
) t $$ );
```

### Solution:
   •	All the above solutions should fix this too
   •	This might happen when server restarted or scaled recently; in which cases waiting out would help.

## Related content

- [Troubleshoot high CPU utilization in Azure Database for PostgreSQL](how-to-high-cpu-utilization.md).
- [Troubleshoot high IOPS utilization in Azure Database for PostgreSQL](how-to-high-io-utilization.md).
- [Troubleshoot high memory utilization in Azure Database for PostgreSQL](how-to-high-memory-utilization.md).
- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md).
- [Autovacuum tuning in Azure Database for PostgreSQL elastic clusters](how-to-autovacuum-tuning-elastic-clusters.md).
