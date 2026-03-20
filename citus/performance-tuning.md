---
title: Query Performance Tuning
description: Learn how to tune Citus query performance so you can optimize distributed PostgreSQL workloads and speed up queries.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: how-to
monikerRange: "citus-13 || citus-14"
---

# Query performance tuning

This article discusses how to tune your Citus cluster to get maximum performance and several performance related configuration parameters. Choosing the right distribution column affects performance. You can first tune your database for high performance on one PostgreSQL server and then scale it out across all the CPUs in the cluster.

## Table distribution and shards

The first step to creating a distributed table is choosing the right distribution column. This step helps Citus push down several operations directly to the worker shards and remove unrelated shards, which leads to significant query speedups.

Typically, you should pick that column as the distribution column, which is the most commonly used `join key` or on which most queries have filters. For filters, Citus uses the distribution column ranges to remove unrelated shards, ensuring that the query hits only those shards that overlap with the WHERE clause ranges. For joins, if the `join key` is the same as the distribution column, then Citus executes the join only between those shards that have matching/overlapping distribution column ranges. All these shards joins can be applied in parallel on the workers and therefore are more efficient.

In addition, Citus can push down several operations directly to the worker shards if they're based on the distribution column. This action greatly reduces both the amount of computation on each node and the network bandwidth involved in transferring data across nodes.

Once you choose the right distribution column, proceed to the next step, which is to tune worker node performance.

## PostgreSQL tuning

The Citus coordinator partitions an incoming query into fragment queries, and sends them to the workers for parallel processing. The workers are extended PostgreSQL servers and they apply PostgreSQL's standard planning and execution logic for these queries. The first step in tuning Citus is tuning the PostgreSQL configuration parameters on the workers for high performance.

Tuning the parameters is a matter of experimentation and often takes several attempts to achieve acceptable performance. It's best to load only a small portion of your data when tuning to make each iteration go faster.

To begin the tuning process, create a Citus cluster and load data into it. From the coordinator node, run the EXPLAIN command on representative queries to inspect performance. Citus extends the EXPLAIN command to provide information about distributed query execution. The EXPLAIN output shows how each worker processes the query and also a how the coordinator node combines their results.

The following example shows the plan for a particular example query. We use the VERBOSE flag to see the actual queries that were sent to the worker nodes.

```sql
EXPLAIN VERBOSE
 SELECT date_trunc('minute', created_at) AS minute,
        sum((payload->>'distinct_size')::int) AS num_commits
   FROM github_events
  WHERE event_type = 'PushEvent'
  GROUP BY minute
  ORDER BY minute;
```

```output
    Sort (cost=0.00..0.00 rows=0 width=0)
      Sort Key: remote_scan.minute
      -> HashAggregate (cost=0.00..0.00 rows=0 width=0)
        Group Key: remote_scan.minute
        -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
          Task Count: 32
          Tasks Shown: One of 32
          -> Task
            Query: SELECT date_trunc('minute'::text, created_at) AS minute, sum(((payload OPERATOR(pg_catalog.->>) 'distinct_size'::text))::integer) AS num_commits FROM github_events_102042 github_events WHERE (event_type OPERATOR(pg_catalog.=) 'PushEvent'::text) GROUP BY (date_trunc('minute'::text, created_at))
            Node: host=localhost port=5433 dbname=postgres
            -> HashAggregate (cost=93.42..98.36 rows=395 width=16)
              Group Key: date_trunc('minute'::text, created_at)
              -> Seq Scan on github_events_102042 github_events (cost=0.00..88.20 rows=418 width=503)
                Filter: (event_type = 'PushEvent'::text)
    (13 rows)
```

There are 32 shards, and the planner chose the Citus adaptive executor to execute this query:

```output
  -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
      Task Count: 32
```

Next, it picks one of the workers and shows you more about how the query behaves there. You see the host, port, database, and the query that were sent to the worker, so you can connect to the worker directly and try the query if desired:

```output
  Tasks Shown: One of 32
    -> Task
      Query: SELECT date_trunc('minute'::text, created_at) AS minute, sum(((payload OPERATOR(pg_catalog.->>) 'distinct_size'::text))::integer) AS num_commits FROM github_events_102042 github_events WHERE (event_type OPERATOR(pg_catalog.=) 'PushEvent'::text) GROUP BY (date_trunc('minute'::text, created_at))
      Node: host=localhost port=5433 dbname=postgres
```

Distributed EXPLAIN next shows the results of running a normal PostgreSQL EXPLAIN on that worker for the fragment query:

```output
  -> HashAggregate (cost=93.42..98.36 rows=395 width=16)
      Group Key: date_trunc('minute'::text, created_at)
      -> Seq Scan on github_events_102042 github_events (cost=0.00..88.20 rows=418 width=503)
        Filter: (event_type = 'PushEvent'::text)
```

You can now connect to the worker at `localhost`, port '5433' and tune query performance for the shard github_events_102042 by using standard PostgreSQL techniques. As you make changes, run EXPLAIN again from the coordinator or right on the worker.

The first set of such optimizations relates to configuration settings. PostgreSQL by default comes with conservative resource settings; and among these settings, `shared_buffers` and work_mem are probably the most important in optimizing read performance. We discuss these parameters later in this article. Apart from them, several other configuration settings affect query performance. These settings are covered in more detail in the [PostgreSQL manual](http://www.postgresql.org/docs/current/static/runtime-config.html) and are discussed in the [PostgreSQL 9.0 High Performance book](http://www.amazon.com/PostgreSQL-High-Performance-Gregory-Smith/dp/184951030X).

`shared_buffers` defines the amount of memory allocated to the database for caching data and defaults to 128 MB. If you have a worker node with 1GB or more RAM, a reasonable starting value for `shared_buffers` is 1/4 of the memory in your system. There are some workloads where even larger settings for `shared_buffers` are effective. Given the way PostgreSQL also relies on the operating system cache, you're unlikely to find more than 25% of RAM to work better than a smaller amount.

If you do many complex sorts, then increasing `work_mem` allows PostgreSQL to do larger in-memory sorts, which is faster than disk-based equivalents. If you see lot of disk activity on your worker node in spite of having a decent amount of memory, then increasing `work_mem` to a higher value can be useful. This process helps PostgreSQL choose more efficient query plans and allows for a greater number of operations to occur in memory.

Other than the configuration settings, the PostgreSQL query planner relies on statistical information about the contents of tables to generate good plans. These statistics are gathered when ANALYZE runs, which is enabled by default. You can learn more about the PostgreSQL planner and the ANALYZE command in greater detail in the [PostgreSQL documentation](http://www.postgresql.org/docs/current/static/sql-analyze.html).

Lastly, you can create indexes on your tables to enhance database performance. Indexes allow the database to find and retrieve specific rows faster than it could do without an index. To choose which indexes give the best performance, run the query with [EXPLAIN](http://www.postgresql.org/docs/current/static/sql-explain.html). You can run `EXPLAIN` to view query plans and optimize the slower parts of the query. After an index is created, the system has to keep it synchronized with the table that adds overhead to data manipulation operations. Therefore, indexes that are seldom or never used in queries should be removed.

For write performance, you can use general PostgreSQL configuration tuning to increase INSERT rates. We recommend increasing `checkpoint_timeout` and `max_wal_size` settings. Also, depending on the reliability requirements of your application, you can choose to change `fsync` or `synchronous_commit` values.

Once you tune a worker to your satisfaction, manually apply those changes to the other workers as well. To verify that they're all behaving properly, set this configuration variable on the coordinator:

```sql
SET citus.explain_all_tasks = 1;
```

EXPLAIN now shows the query plan for all tasks, not just one.

```sql
EXPLAIN
 SELECT date_trunc('minute', created_at) AS minute,
        sum((payload->>'distinct_size')::int) AS num_commits
   FROM github_events
  WHERE event_type = 'PushEvent'
  GROUP BY minute
  ORDER BY minute;
```

```output
    Sort (cost=0.00..0.00 rows=0 width=0)
      Sort Key: remote_scan.minute
      -> HashAggregate (cost=0.00..0.00 rows=0 width=0)
        Group Key: remote_scan.minute
        -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
          Task Count: 32
          Tasks Shown: All
          -> Task
            Node: host=localhost port=5433 dbname=postgres
            -> HashAggregate (cost=93.42..98.36 rows=395 width=16)
              Group Key: date_trunc('minute'::text, created_at)
              -> Seq Scan on github_events_102042 github_events (cost=0.00..88.20 rows=418 width=503)
                Filter: (event_type = 'PushEvent'::text)
          -> Task
            Node: host=localhost port=5434 dbname=postgres
            -> HashAggregate (cost=103.21..108.57 rows=429 width=16)
              Group Key: date_trunc('minute'::text, created_at)
              -> Seq Scan on github_events_102043 github_events (cost=0.00..97.47 rows=459 width=492)
                Filter: (event_type = 'PushEvent'::text)
          --
          -- ... repeats for all 32 tasks
          --     alternating between workers one and two
          --     (running in this case locally on ports 5433, 5434)
          --

    (199 rows)
```

Differences in worker execution can be caused by tuning configuration differences, uneven data distribution across shards, or hardware differences between the machines. To get more information about the time it takes the query to run on each shard, use EXPLAIN ANALYZE.

> [!NOTE]  
> When `citus.explain_all_tasks` is enabled, EXPLAIN plans are retrieved sequentially, which might take a long time for EXPLAIN ANALYZE.

Citus, by default, sorts tasks by execution time in descending order. If `citus.explain_all_tasks` is disabled, then Citus shows the single longest-running task. This functionality can be used only with EXPLAIN ANALYZE, since regular EXPLAIN doesn't execute the queries, and therefore doesn't know any execution times. To change the sort order, you can use `explain_analyze_sort_method`.

## Scale out performance

Once you achieve the desired performance for a single shard, you can set similar configuration parameters on all your workers. As Citus runs the fragment queries in parallel across the worker nodes, users can scale out the performance of their queries to be the cumulative of the computing power of all of the CPU cores in the cluster. The only limitation is the data that can fit within the memory.

You should try to fit as much of your working set in memory as possible to get best performance with Citus. If fitting the entire working set in memory isn't feasible, use solid state drives (SSDs) over hard disk drives (HDDs) as a best practice. HDDs are able to show decent performance when you have sequential reads over contiguous blocks of data but have lower random read/write performance. In cases where you have a high number of concurrent queries doing random reads and writes, the use of SSDs can improve query performance by several times as compared to HDDs. Also, if your queries are highly compute intensive, consider choosing machines with more powerful CPUs.

To measure the disk space usage of your database objects, you can log into the worker nodes and use [PostgreSQL administration functions](http://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE) for individual shards. The `pg_total_relation_size()` function can be used to get the total disk space used by a table. You can also use other functions mentioned in the PostgreSQL docs to get more specific size information. Based on these statistics for a shard and the shard count, users can compute the hardware requirements for their cluster.

The number of shards per worker node also affects performance. Citus partitions an incoming query into its fragment queries, which run on individual worker shards. Therefore, the number of shards the query hits governs the degree of parallelism for each query. To ensure maximum parallelism, create enough shards on each node so that there is at least one shard per CPU core. Citus prunes unrelated shards if the query has filters on the distribution column. Creating more shards than the number of cores might also be beneficial so that you can achieve greater parallelism even after shard pruning.

## Distributed query performance tuning

Once you distribute your data across the cluster, with each worker optimized for best performance, you should see high performance gains on your queries. The final step is to tune a few distributed performance tuning parameters.

Before you move to the specific configuration parameters, measure query times on your distributed cluster and compare them with the single shard performance. Enable, time, and run the query on the coordinator node, and run one of the fragment queries on the worker nodes. These actions help you determine the amount of time spent on the worker nodes and in fetching the data to the coordinator node. You can then figure out what the bottleneck is and optimize the database accordingly.

There are relevant parameters that help optimize the distributed query planner and executor: general and advanced. The general performance tuning section is sufficient for most use-cases and covers all the common configs. The advanced performance tuning section covers parameters that might provide performance gains in specific use cases.

### General

For higher INSERT performance, the level of concurrency affects insert rates the most. Try to run several concurrent INSERT statements in parallel. This way you can achieve high insert rates if you have a powerful coordinator node and are able to use all the CPU cores on that node together.

#### Subquery/CTE network overhead

In the best case, Citus can run queries containing subqueries and CTEs in a single step. This situation usually occurs because both the main query and subquery filter by tables' distribution column in the same way, and can be pushed down to worker nodes together. However, Citus is sometimes forced to execute subqueries before executing the main query, copying the intermediate subquery results to other worker nodes for use by the main query. This technique is called a "push-pull execution."

You should be aware when subqueries are enacted in a separate step and avoid sending too much data between worker nodes. The network overhead hurts performance. The EXPLAIN command allows you to discover how queries are run, including whether multiple steps are required. For more information, see [Subquery/CTE push-pull execution](reference-processing.md#subquery-and-cte-push-pull-execution).

Also, you can defensively set a safeguard against large intermediate results. Adjust the `max_intermediate_result_size` limit in a new connection to the coordinator node. By default the max intermediate result size is 1GB, which is large enough to allow some inefficient queries. Try turning it down and running your queries:

```sql
-- set a restrictive limit for intermediate results
SET citus.max_intermediate_result_size = '512kB';

-- attempt to run queries
-- SELECT ...
```

If the query has subqueries or CTEs that exceed this limit, the query is canceled and you see an error message:

ERROR: the intermediate result size exceeds citus.max_intermediate_result_size (currently 512 kB)
DETAIL: Citus restricts the size of intermediate results of complex subqueries and CTEs to avoid accidentally pulling large result sets into once place.
HINT: To run the current query, set citus.max_intermediate_result_size to a higher value or -1 to disable.

The size of intermediate results and their destination is available in EXPLAIN ANALYZE output:

```sql
EXPLAIN ANALYZE
WITH deleted_rows AS (
  DELETE FROM page_views WHERE tenant_id IN (3, 4) RETURNING *
), viewed_last_week AS (
  SELECT * FROM deleted_rows WHERE view_time > current_timestamp - interval '7 days'
)
SELECT count(*) FROM viewed_last_week;
```

```output
    Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0) (actual time=570.076..570.077 rows=1 loops=1)
      -> Distributed Subplan 31_1
            Subplan Duration: 6978.07 ms
            Intermediate Data Size: 26 MB
            Result destination: Write locally
            -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0) (actual time=364.121..364.122 rows=0 loops=1)
                  Task Count: 2
                  Tuple data received from nodes: 0 bytes
                  Tasks Shown: One of 2
                  -> Task
                        Tuple data received from node: 0 bytes
                        Node: host=localhost port=5433 dbname=postgres
                        -> Delete on page_views_102016 page_views (cost=5793.38..49272.28 rows=324712 width=6) (actual time=362.985..362.985 rows=0 loops=1)
                              -> Bitmap Heap Scan on page_views_102016 page_views (cost=5793.38..49272.28 rows=324712 width=6) (actual time=362.984..362.984 rows=0 loops=1)
                                    Recheck Cond: (tenant_id = ANY ('{3,4}'::integer[]))
                                    -> Bitmap Index Scan on view_tenant_idx_102016 (cost=0.00..5712.20 rows=324712 width=0) (actual time=19.193..19.193 rows=325733 loops=1)
                                          Index Cond: (tenant_id = ANY ('{3,4}'::integer[]))
                            Planning Time: 0.050 ms
                            Execution Time: 363.426 ms
            Planning Time: 0.000 ms
            Execution Time: 364.241 ms
     Task Count: 1
     Tuple data received from nodes: 6 bytes
     Tasks Shown: All
     -> Task
           Tuple data received from node: 6 bytes
           Node: host=localhost port=5432 dbname=postgres
           -> Aggregate (cost=33741.78..33741.79 rows=1 width=8) (actual time=565.008..565.008 rows=1 loops=1)
                 -> Function Scan on read_intermediate_result intermediate_result (cost=0.00..29941.56 rows=1520087 width=0) (actual time=326.645..539.158 rows=651466 loops=1)
                       Filter: (view_time > (CURRENT_TIMESTAMP - '7 days'::interval))
               Planning Time: 0.047 ms
               Execution Time: 569.026 ms
    Planning Time: 1.522 ms
    Execution Time: 7549.308 ms
```

In the EXPLAIN ANALYZE output, you see the following information about the intermediate results:

Intermediate Data Size: 26 MB
Result destination: Write locally

The output shows how large the intermediate results were, and where the intermediate results were written to. In this case, they were written to the node coordinating the query execution, as specified by "Write locally." For some other queries, it can also be of the following format:

Intermediate Data Size: 26 MB
Result destination: Send to 2 nodes

This response means the intermediate result was pushed to two worker nodes, and it involved more network traffic.

When you use CTEs, or join between CTEs and distributed tables, you can avoid push-pull execution by following these rules:

- Tables should be colocated.
- The CTE queries shouldn't require any merge steps (for example, LIMIT or GROUP BY on a nondistribution key).
- Tables and CTEs should be joined on distribution keys.

Also PostgreSQL 12 or above allows Citus to take advantage of *CTE inlining* to push CTEs down to workers in more circumstances. The inlining behavior can be controlled with the `MATERIALIZED` keyword. For more information, see [PostgreSQL docs](https://www.postgresql.org/docs/current/queries-with.html).

### Advanced

In this section, we discuss advanced performance tuning parameters. These parameters are applicable to specific use cases and might not be required for all deployments.

#### Connection management

When you run multi-shard queries, Citus must balance the gains from parallelism with the overhead from database connections. [Query Execution](https://docs.citusdata.com/en/stable/get_started/concepts.html#query-execution) explains the steps of turning queries into worker tasks and obtaining database connections to the workers.

- Set `max_adaptive_executor_pool_size` to a low value like 1 or 2 for transactional workloads with short queries (for example, \< 20ms of latency). For analytical workloads where parallelism is critical, leave this setting at its default value of 16.
- Set `executor_slow_start_interval` to a high value like 100ms for transactional workloads comprised of short queries that are bound on network latency rather than parallelism. For analytical workloads, leave this setting at its default value of 10ms.
- The default value of 1 for `max_cached_conns_per_worker` is reasonable. A larger value such as 2 might be helpful for clusters that use a few concurrent sessions, but it's not wise to go much further (for example, 16 would be too high). If set too high, sessions hold idle connections and use worker resources unnecessarily.
- Set `max_shared_pool_size` to match the [max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html#RUNTIME-CONFIG-CONNECTION-SETTINGS) setting of your *worker* nodes. This setting is mainly a fail-safe.

#### Task assignment policy

The Citus query planner assigns tasks to the worker nodes based on shard locations. The algorithm used while making these assignments can be chosen by setting the `citus.task_assignment_policy` configuration parameter. You can alter this configuration parameter to choose the policy that works best for their use case.

The **greedy** policy aims to distribute tasks evenly across the workers. This policy is the default and works well in most of the cases. The **round-robin** policy assigns tasks to workers in a round-robin fashion alternating between different replicas. Round-robin enables better cluster utilization when the shard count for a table is low compared to the number of workers. The third policy is the **first-replica** policy, which assigns tasks based on the insertion order of placements (replicas) for the shards. With this policy, users can be sure of which shards are accessed on each machine. This policy helps in providing stronger memory residency guarantees by allowing you to keep your working set in memory and use it for querying.

#### Intermediate data transfer format

On PostgreSQL 13 and lower, Citus defaults to transferring intermediate query data between workers in textual format. For certain data types, like hll or hstore arrays, the cost of serializing and deserializing data can be high. In such cases, the use of the binary format to transfer intermediate data can improve query performance. You can enable the `binary_worker_copy_format` configuration option to use the binary format.

#### Binary protocol

In some cases, a large part of query time is spent in sending query results from workers to the coordinator. These results happen when queries request many rows (such as `select * from table`), or when result columns use large types (like `hll` or `tdigest` from the postgresql-hll and tdigest extensions).

In those cases it can be beneficial to set `citus.enable_binary_protocol` to `true`, which changes the encoding of the results to binary, rather than by using text encoding. Binary encoding significantly reduces bandwidth for types that have a compact binary representation, such as `hll`, `tdigest`, `timestamp`, and `double precision`.

For PostgreSQL 14 and higher, the default for this setting is already `true`. Explicitly enabling it for those PostgreSQL versions has no effect.

## Scale out data ingestion

Citus lets you scale out data ingestion to high rates, but there are several trade-offs to consider in terms of application integration, throughput, and latency. In this section, we discuss different approaches to data ingestion, and provide guidelines for expected throughput and latency numbers.

### Real-time inserts and updates

On the Citus coordinator, you can perform INSERT, INSERT .. ON CONFLICT, UPDATE, and DELETE commands directly on distributed tables. When you issue one of these commands, the changes are immediately visible to the user.

When you run an INSERT (or another ingest command), Citus first finds the right shard placements based on the value in the distribution column. Citus then connects to the worker nodes storing the shard placements, and performs an INSERT on each of them. From the perspective of the user, the INSERT takes several milliseconds to process because of the network latency to worker nodes. The Citus coordinator node, however, can process concurrent INSERTs to reach high throughputs.

#### Insert throughput

To measure data ingest rates with Citus, we use a standard tool called pgbench and provide repeatable benchmarking steps.

To measure data ingest rates with Citus, you can use standard PostgreSQL benchmarking tools like pgbench. See repeatable benchmarking steps for detailed instructions.

Benchmark results vary based on your cluster configuration:

- Coordinator node resources (CPU cores, memory)
- Number and size of worker nodes
- Network latency between nodes
- pgbench concurrency settings (thread and client count)
- Database configuration tuning

For example, a basic Citus cluster with a dual-core coordinator and two single-core workers can handle thousands of INSERTs per second. Scaling to more powerful hardware with 4-8 cores and more workers can increase throughput significantly, potentially reaching tens of thousands of transactions per second.

Key observations from benchmarking:

- Entry-level clusters can deliver millions of transactional INSERT statements per day.
- More powerful clusters with 4x CPU capacity can handle billions of INSERT statements daily.
- Network latency and PostgreSQL connection handling often become the bottleneck.
- In production with many tables and indexes, bottlenecks might shift to other resources.

#### Update throughput

To measure UPDATE throughput with Citus, you can use the same benchmarking steps used for INSERT testing.

UPDATE performance follows similar patterns to INSERT performance. Throughput depends on cluster configuration, concurrency settings, and whether updates are distributed across shards or concentrated on specific partitions.

| Coordinator Node | Worker Nodes | Latency (ms) | Transactions per sec |
| --- | --- | --- | --- |
| 2 cores - 7.5GB RAM | 2 * (1 core - 15GB RAM) | 25.0 | 10,200 |
| 4 cores - 15GB RAM | 2 * (1 core - 15GB RAM) | 19.6 | 13,000 |
| 8 cores - 30GB RAM | 2 * (1 core - 15GB RAM) | 20.3 | 12,600 |
| 8 cores - 30GB RAM | 4 * (1 core - 15GB RAM) | 10.7 | 23,900 |

These benchmark numbers show that Citus's UPDATE throughput is slightly lower than the throughput of INSERTs. This difference is because pgbench creates a primary key index for UPDATE statements and an UPDATE incurs more work on the worker nodes.

UPDATE statements cause bloat in the database and VACUUM needs to run regularly to clean up this bloat. In Citus, since VACUUM runs in parallel across worker nodes, VACUUM is less likely to affect your workloads.

#### Insert and update: throughput checklist

When you run the previous pgbench benchmarks on a moderately sized Citus cluster, you can generally expect 10K-50K INSERTs per second. This action translates to approximately 1 to 4 billion INSERTs per day. If you aren't observing these throughputs numbers, remember the following checklist:

- Check the network latency between your application and your database. High latencies affect your write throughput.
- Ingest data by using concurrent threads. If the roundtrip latency during an INSERT is 4ms, you can process 250 INSERTs/second over one thread. If you run 100 concurrent threads, you see your write throughput increase with the number of threads.
- Check whether the nodes in your cluster have CPU or disk bottlenecks. Ingested data passes through the coordinator node, so check whether your coordinator is bottlenecked on CPU.
- Avoid closing connections between INSERT statements so that you also avoid the overhead of connection setup.
- Remember that column size affects insert speed. Rows with large JSON blobs take longer than rows with small columns like integers.

#### Insert and update: latency

The benefit of running INSERT or UPDATE commands, compared to issuing bulk COPY commands, is that changes are immediately visible to other queries. When you issue an INSERT or UPDATE command, the Citus coordinator node directly routes this command to related worker nodes. The coordinator node also keeps connections to the workers open within the same session, which means subsequent commands see lower response times.

``` psql
-- Set up a distributed table that keeps account history information
CREATE TABLE pgbench_history (tid int, bid int, aid int, delta int, mtime timestamp);
SELECT create_distributed_table('pgbench_history', 'aid');

-- Enable timing to see reponse times
\timing on

-- First INSERT requires connection set-up, second will be faster
INSERT INTO pgbench_history VALUES (10, 1, 10000, -5000, CURRENT_TIMESTAMP); -- Time: 10.314 ms
INSERT INTO pgbench_history VALUES (10, 1, 22000, 5000, CURRENT_TIMESTAMP); -- Time: 3.132 ms
```

### Stage data temporarily

When loading data for temporary staging, consider an [unlogged table](https://www.postgresql.org/docs/current/static/sql-createtable.html#SQL-CREATETABLE-UNLOGGED). The PostgreSQL write-ahead log doesn't back unlogged tables, which makes them faster for inserting rows but not suitable for long term data storage. You can use an unlogged table as a place to load incoming data before manipulating the data and moving it to permanent tables.

```sql
-- example unlogged table
CREATE UNLOGGED TABLE unlogged_table (
  key text,
  value text
);

-- its shards will be unlogged as well when
-- the table is distributed
SELECT create_distributed_table('unlogged_table', 'key');

-- ready to load data
```

### Bulk copy (250K - 2M/s)

Distributed tables support [COPY](http://www.postgresql.org/docs/current/static/sql-copy.html) from the Citus coordinator for bulk ingestion, which can achieve higher ingestion rates than INSERT statements.

COPY can be used to load data directly from an application by using COPY .. FROM STDIN, from a file on the server, or program executed on the server.

```sql
COPY pgbench_history FROM STDIN WITH (FORMAT CSV);
```

In psql, the \COPY command can be used to load data from the local machine. The \COPY command actually sends a COPY .. FROM STDIN command to the server before sending the local data. An application that loads data directly does so as well.

```bash
psql -c "\COPY pgbench_history FROM 'pgbench_history-2016-03-04.csv' (FORMAT CSV)"
```

A powerful feature of COPY for distributed tables is that it asynchronously copies data to the workers over many parallel connections, one for each shard placement. Data can be ingested by using multiple workers and multiple cores in parallel. Especially when there are expensive indexes such as a GIN, this feature can lead to major performance boosts over ingesting into a regular PostgreSQL table.

From a throughput standpoint, you can expect data ingest ratios of 250K - 2M rows per second when you use COPY. For more information, see [COPY into distributed PostgreSQL tables, up to 7M rows/sec](https://www.citusdata.com/blog/2016/06/15/copy-postgresql-distributed-tables).

> [!NOTE]  
> Make sure your benchmarking setup is well configured so you can observe optimal COPY performance. Follow these tips:
>
> - We recommend a large batch size (~ 50000-100000). You can benchmark with multiple files (1, 10, 1000, 10000 etc.), each of that batch size.
> - Use parallel ingestion. Increase the number of threads/ingestors to 2, 4, 8, 16 and run benchmarks.
> - Use a compute-optimized coordinator. For the workers choose memory-optimized boxes with a decent number of vcpus.
> - Go with a relatively small shard count, 32 should suffice but you could benchmark with 64, too.
> - Ingest data for a suitable amount of time (say 2, 4, 8, 24 hrs). Longer tests are more representative of a production setup.

## Related content

- [Diagnostic queries](diagnostic-queries.md)
- [Guides](guides.md)
- [What is Citus?](what-is-citus.md)
