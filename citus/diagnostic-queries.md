---
title: Useful Diagnostic Queries
description: Learn about queries that are useful for finding diagnostic information about Citus nodes, shards, tables, and connections.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Useful diagnostic queries

## Finding which shard contains data for a specific tenant

The rows of a distributed table are grouped into shards, and each shard is placed on a worker node in the Citus cluster. In the multitenant Citus use case we can determine which worker node contains the rows for a specific tenant by putting together two pieces of information: the `shard id <get_shard_id>` associated with the tenant ID, and the shard placements on workers. The two can be retrieved together in a single query. Suppose our multitenant application's tenants are stores, and we want to find which worker node holds the data for Gap.com (for example, `id=4`).

To find the worker node holding the data for store `id=4`, ask for the placement of rows whose distribution column has the value 4:

```sql
SELECT shardid, shardstate, shardlength, nodename, nodeport, placementid
  FROM pg_dist_placement AS placement,
       pg_dist_node AS node
 WHERE placement.groupid = node.groupid
   AND node.noderole = 'primary'
   AND shardid = (
     SELECT get_shard_id_for_distribution_column('stores', 4)
   );
```

The output contains the host and port of the worker database.

```output
┌─────────┬────────────┬─────────────┬───────────┬──────────┬─────────────┐
│ shardid │ shardstate │ shardlength │ nodename  │ nodeport │ placementid │
├─────────┼────────────┼─────────────┼───────────┼──────────┼─────────────┤
│ 102009  │          1 │           0 │ localhost │     5433 │           2 │
└─────────┴────────────┴─────────────┴───────────┴──────────┴─────────────┘
```

## Finding which node hosts a distributed schema

Distributed schemas are automatically associated with individual colocation groups such that the tables created in those schemas are converted to colocated distributed tables without a shard key. You can find where a distributed schema resides by joining `citus_shards` with `citus_schemas`:

```sql
select schema_name, nodename, nodeport
  from citus_shards
  join citus_schemas cs
    on cs.colocation_id = citus_shards.colocation_id
 group by 1,2,3;
```

```output
schema_name | nodename  | nodeport
-------------+-----------+----------
a           | localhost |     9701
b           | localhost |     9702
with_data   | localhost |     9702
```

You can also query `citus_shards` directly filtering down to the *schema* table type to have a detailed listing for all tables.

```sql
select * from citus_shards where citus_table_type = 'schema';
```

## Finding the distribution column for a table

Each distributed table in Citus has a distribution column. For more information about what this column is and how it works, see Distributed Data Modeling. Many situations require knowing which column is the distribution column. Some operations require joining or filtering on the distribution column, and you might encounter error messages with hints like, "add a filter to the distribution column."

The `pg_dist_*` tables on the coordinator node contain diverse metadata about the distributed database. In particular, `pg_dist_partition` holds information about the distribution column (formerly called *partition* column) for each table. You can use a convenient utility function to look up the distribution column name from the low-level details in the metadata. Here's an example and its output:

```sql
-- create example table

CREATE TABLE products (
  store_id bigint,
  product_id bigint,
  name text,
  price money,

  CONSTRAINT products_pkey PRIMARY KEY (store_id, product_id)
);

-- pick store_id as distribution column

SELECT create_distributed_table('products', 'store_id');

-- get distribution column name for products table

SELECT column_to_column_name(logicalrelid, partkey) AS dist_col_name
  FROM pg_dist_partition
 WHERE logicalrelid='products'::regclass;
```

Example output:

```output
┌───────────────┐
│ dist_col_name │
├───────────────┤
│ store_id      │
└───────────────┘
```

## Detecting locks

This query runs across all worker nodes and identifies locks, how long they're open, and the offending queries:

```sql
SELECT * FROM citus_lock_waits;
```

For more information, see `dist_query_activity`.

## Querying the size of your shards

This query provides you with the size of every shard of a given distributed table, designated here by the placeholder `my_table`:

```sql
SELECT shardid, table_name, shard_size
FROM citus_shards
WHERE table_name = 'my_table';
```

Example output:

```output
 shardid | table_name | shard_size
---------+------------+------------
  102170 | my_table   |   90177536
  102171 | my_table   |   90177536
  102172 | my_table   |   91226112
  102173 | my_table   |   90177536
```

This query uses the `citus_shards`.

## Querying the size of all distributed tables

This query gets a list of the sizes for each distributed table plus the size of their indices.

```sql
SELECT table_name, table_size
  FROM citus_tables;
```

Example output:

```output
┌───────────────┬────────────┐
│ table_name    │ table_size │
├───────────────┼────────────┤
│ github_users  │ 39 MB      │
│ github_events │ 98 MB      │
└───────────────┴────────────┘
```

There are other ways to measure distributed table size. For more information, see `table_size`.

## Identifying unused indices

This query runs across all worker nodes and identifies any unused indexes for a given distributed table. Replace the placeholder `my_distributed_table` with the name of your distributed table.

```sql
SELECT *
FROM run_command_on_shards('my_distributed_table', $cmd$
  SELECT array_agg(a) as infos
  FROM (
    SELECT (
      schemaname || '.' || relname || '##' || indexrelname || '##'
                 || pg_size_pretty(pg_relation_size(i.indexrelid))::text
                 || '##' || idx_scan::text
    ) AS a
    FROM  pg_stat_user_indexes ui
    JOIN  pg_index i
    ON    ui.indexrelid = i.indexrelid
    WHERE NOT indisunique
    AND   idx_scan < 50
    AND   pg_relation_size(relid) > 5 * 8192
    AND   (schemaname || '.' || relname)::regclass = '%s'::regclass
    ORDER BY
      pg_relation_size(i.indexrelid) / NULLIF(idx_scan, 0) DESC nulls first,
      pg_relation_size(i.indexrelid) DESC
  ) sub
$cmd$);
```

Example output:

```output
┌─────────┬─────────┬───────────────────────────────────────────────────────────────────────┐
│ shardid │ success │                            result                                     │
├─────────┼─────────┼───────────────────────────────────────────────────────────────────────┤
│ 102008  │ t       │                                                                       │
│ 102009  │ t       │ {"public.my_distributed_table_102009##stupid_index_102009##28 MB##0"} │
│ 102010  │ t       │                                                                       │
│ 102011  │ t       │                                                                       │
└─────────┴─────────┴───────────────────────────────────────────────────────────────────────┘
```

## Monitoring client connection count

This query returns the connection count by each type for connections that are open on the coordinator.

```sql
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;
```

Example output:

```output
┌────────┬───────┐
│ state  │ count │
├────────┼───────┤
│ active │     3 │
│ ∅      │     1 │
└────────┴───────┘
```

## Viewing system queries

### Active queries

The `citus_stat_activity` view shows which queries are currently executing. You can filter the view to find the actively executing queries, along with the process ID of their backend:

```sql
SELECT global_pid, query, state
  FROM citus_stat_activity
 WHERE state != 'idle';
```

### Why queries are waiting

You can also query the view to see the most common reasons that non-idle queries are waiting. For an explanation of the reasons, see the [PostgreSQL documentation](https://www.postgresql.org/docs/current/monitoring-stats.html#WAIT-EVENT-TABLE).

```sql
SELECT wait_event || ':' || wait_event_type AS type, count(*) AS number_of_occurences
  FROM pg_stat_activity
 WHERE state != 'idle'
GROUP BY wait_event, wait_event_type
ORDER BY number_of_occurences DESC;
```

Here's example output when running `pg_sleep` in a separate query concurrently:

```output
┌─────────────────┬──────────────────────┐
│      type       │ number_of_occurences │
├─────────────────┼──────────────────────┤
│ ∅               │                    1 │
│ PgSleep:Timeout │                    1 │
└─────────────────┴──────────────────────┘
```

## Index hit rate

This query provides your index hit rate across all nodes. The index hit rate is useful in determining how often indices are used when querying:

```sql
-- on coordinator
SELECT 100 * (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) AS index_hit_rate
  FROM pg_statio_user_indexes;

-- on workers
SELECT nodename, result as index_hit_rate
FROM run_command_on_workers($cmd$
  SELECT 100 * (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) AS index_hit_rate
    FROM pg_statio_user_indexes;
$cmd$);
```

Example output:

```output
┌───────────┬────────────────┐
│ nodename  │ index_hit_rate │
├───────────┼────────────────┤
│ 10.0.0.16 │ 96.0           │
│ 10.0.0.20 │ 98.0           │
└───────────┴────────────────┘
```

## Cache hit rate

Most applications typically access a small fraction of their total data at once. PostgreSQL keeps frequently accessed data in memory to avoid slow reads from disk. You can see statistics about it in the [pg_statio_user_tables](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STATIO-ALL-TABLES-VIEW) view.

An important measurement is what percentage of data comes from the memory cache versus the disk in your workload:

```sql
-- on coordinator
SELECT
  sum(heap_blks_read) AS heap_read,
  sum(heap_blks_hit)  AS heap_hit,
  100 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_rate
FROM
  pg_statio_user_tables;

-- on workers
SELECT nodename, result as cache_hit_rate
FROM run_command_on_workers($cmd$
  SELECT
    100 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_rate
  FROM
    pg_statio_user_tables;
$cmd$);
```

Example output:

```output
┌───────────┬──────────┬─────────────────────┐
│ heap_read │ heap_hit │   cache_hit_rate    │
├───────────┼──────────┼─────────────────────┤
│         1 │      132 │ 99.2481203007518796 │
└───────────┴──────────┴─────────────────────┘
```

If you find a ratio significantly lower than 99%, consider increasing the cache available to your database.

## Related content

- [Cluster management in Citus](cluster-management.md)
- [Citus table management](table-management.md)
- [Performance tuning for Citus](performance-tuning.md)
- [What is Citus?](what-is-citus.md)
