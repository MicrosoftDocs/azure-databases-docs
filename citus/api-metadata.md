---
title: Citus Cluster Metadata Reference
description: In the Citus tables and views reference, you find descriptions of the metadata tables and schemas created by the Citus coordinator to track statistics and information about logical shards.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
ai-usage: ai-assisted
---

# Citus cluster metadata reference

Citus extends PostgreSQL with distributed database capabilities. This extension includes metadata tables and views that help you manage and monitor your distributed cluster. This article provides a reference for the tables and views that Citus creates to track information about distributed tables, shards, node configuration, and query statistics. Understanding these metadata structures helps you monitor cluster health, troubleshoot problems, and optimize distributed query performance.

## Coordinator metadata

Citus divides each distributed table into multiple logical shards based on the distribution column. The coordinator node maintains metadata tables to track statistics and information about the health and location of these shards. This section describes each of these metadata tables and their schema. You can view and query these tables by using SQL after signing in to the coordinator node.

### Partition table

The `pg_dist_partition` table stores metadata about which tables in the database are distributed. For each distributed table, it also stores information about the distribution method and detailed information about the distribution column.

```sql
SELECT * from pg_dist_partition;
```

```output
 logicalrelid  | partmethod | partkey | colocationid | repmodel
---------------+------------+---------+--------------+----------
 github_events | h          | {VAR...}  |            2 | s
(1 row)
```

### Shard table

The `pg_dist_shard` table stores metadata about individual shards of a table. This metadata includes information about which distributed table the shard belongs to and statistics about the distribution column for that shard. For hash distributed tables, the metadata consists of hash token ranges assigned to that shard. The coordinator uses these statistics to prune away unrelated shards during `SELECT` queries.

```sql
SELECT * from pg_dist_shard;
```

```output
  logicalrelid | shardid | shardstorage | shardminvalue | shardmaxvalue
 --------------+---------+--------------+---------------+---------------
  github_events | 102026 | t            | 268435456     | 402653183
  github_events | 102027 | t            | 402653184     | 536870911
  github_events | 102028 | t            | 536870912     | 671088639
  github_events | 102029 | t            | 671088640     | 805306367
  (4 rows)
```

#### Shard storage types

The `shardstorage` column in `pg_dist_shard` indicates the type of storage used for the shard. The following table provides a brief overview of the different shard storage types and their representation.

| Storage Type | `shardstorage` value | Description |
| --- | --- | --- |
| TABLE | `t` | Indicates that the shard stores data belonging to a regular distributed table. |
| COLUMNAR | `c` | Indicates that the shard stores columnar data. Used by distributed `cstore_fdw` tables. |
| FOREIGN | `f` | Indicates that the shard stores foreign data. Used by distributed `file_fdw` tables. |

### Shard information view

In addition to the low-level shard metadata table described previously, Citus provides a `citus_shards` view to easily check:

- Where each shard is (node and port),
- What kind of table it belongs to, and
- Its size.

This view helps you inspect shards to find, among other things, any size imbalances across nodes.

```sql
SELECT * FROM citus_shards;
```

```output
 table_name | shardid | shard_name   | citus_table_type | colocation_id | nodename | nodeport | shard_size
------------+---------+--------------+------------------+---------------+----------+----------+------------
 dist       | 102170  | dist_102170  | distributed      |            34 | localhost |     9701 |   90677248
 dist       | 102171  | dist_102171  | distributed      |            34 | localhost |     9702 |   90619904
 dist       | 102172  | dist_102172  | distributed      |            34 | localhost |     9701 |   90701824
 dist       | 102173  | dist_102173  | distributed      |            34 | localhost |     9702 |   90693632
 ref        | 102174  | ref_102174   | reference        |             2 | localhost |     9701 |       8192
 ref        | 102174  | ref_102174   | reference        |             2 | localhost |     9702 |       8192
 dist2      | 102175  | dist2_102175 | distributed      |            34 | localhost |     9701 |     933888
 dist2      | 102176  | dist2_102176 | distributed      |            34 | localhost |     9702 |     950272
 dist2      | 102177  | dist2_102177 | distributed      |            34 | localhost |     9701 |     942080
 dist2      | 102178  | dist2_102178 | distributed      |            34 | localhost |     9702 |     933888
```

The `colocation_id` refers to the colocation group. For more info about `citus_table_type` and colocation groups, see the [Citus tables view](#citus-tables-view) and [Colocation group table](#colocation-group-table) sections.

### Shard placement table

The `pg_dist_placement` table tracks the location of shards on worker nodes. Each shard assigned to a specific node is a *shard placement*. This table stores information about the health and location of each shard placement.

| Name | Type | Description |
| --- | --- | --- |
| `placementid` | bigint | Unique autogenerated identifier for each individual placement. |
| `shardid` | bigint | Shard identifier associated with this placement. This value references the `shardid` column in the `pg_dist_shard` catalog table. |
| `shardstate` | int | Describes the state of this placement. Different shard states are discussed in the following section. |
| `shardlength` | bigint | For hash distributed tables, zero. |
| `groupid` | int | Identifier used to denote a group of one primary server and zero or more secondary servers. |

```sql
SELECT * from pg_dist_placement;
```

```output
 placementid | shardid | shardstate | shardlength | groupid
-------------+---------+------------+-------------+---------
           1 | 102008  |          1 |           0 |       1
           2 | 102008  |          1 |           0 |       2
           3 | 102009  |          1 |           0 |       2
           4 | 102009  |          1 |           0 |       3
           5 | 102010  |          1 |           0 |       3
           6 | 102010  |          1 |           0 |       4
           7 | 102011  |          1 |           0 |       4
```

> [!NOTE]  
> As of Citus 7.0, the analogous table `pg_dist_shard_placement` is deprecated. It included the node name and port for each placement:
>
> ```sql
> SELECT * from pg_dist_shard_placement;
> ```
>
> You can now get that information by joining `pg_dist_placement` with `pg_dist_node <pg_dist_node>` on the `groupid`. For compatibility, Citus still provides `pg_dist_shard_placement` as a view. However, use the new, more normalized, tables when possible.

### Worker node table

The `pg_dist_node` table contains information about the worker nodes in the cluster.

| Name | Type | Description |
| --- | --- | --- |
| `nodeid` | int | Autogenerated identifier for an individual node. |
| `groupid` | int | Identifier used to denote a group of one primary server and zero or more secondary servers. By default, it's the same as the `nodeid`. |
| `nodename` | text | Host name or IP address of the PostgreSQL worker node. |
| `nodeport` | int | Port number on which the PostgreSQL worker node is listening. |
| `noderack` | text | (Optional) Rack placement information for the worker node. |
| `hasmetadata` | boolean | Reserved for internal use. |
| `isactive` | boolean | Indicates whether the node is active and accepting shard placements. |
| `noderole` | text | Indicates whether the node is a primary or secondary. |
| `nodecluster` | text | (Optional) Rack placement information for the worker node. |
| `metadatasynced` | boolean | Reserved for internal use. |
| `shouldhaveshards` | boolean | If this value is `false`, move shards off node (drained) when rebalancing. Also, don't place shards from new distributed tables on the node, unless they're colocated with shards that are already there. |

```sql
SELECT * from pg_dist_node;
```

```output
 nodeid | groupid | nodename | nodeport | noderack | hasmetadata | isactive | noderole | nodecluster | metadatasynced | shouldhaveshards
--------+---------+-----------+----------+----------+-------------+----------+----------+-------------+----------------+------------------
      1 |       1 | localhost |    12345 | default | f           | t        | primary | default     | f              | t
      2 |       2 | localhost |    12346 | default | f           | t        | primary | default     | f              | t
      3 |       3 | localhost |    12347 | default | f           | t        | primary | default     | f              | t
(3 rows)
```

### Citus nodes view

The `citus_nodes` view shows node information from `pg_dist_node` without needing superuser access.

| Name | Type | Description |
| --- | --- | --- |
| `nodename` | text | Host name or IP address of the node. |
| `nodeport` | int | Port number that the node uses to listen. |
| `role` | text | Role of the node: `coordinator` or `worker`. |
| `active` | boolean | Shows whether the node is active. |

```sql
SELECT * from citus_nodes;
```

```output
 nodename  | nodeport |    role     | active
-----------+----------+-------------+--------
 localhost |    57637 | worker      | t
 localhost |    57638 | worker      | f
 localhost |    57636 | coordinator | t
(3 rows)
```

### Distributed object table

The `citus.pg_dist_object` table contains a list of objects such as types and functions that you create on the coordinator node and propagate to worker nodes. When an administrator adds new worker nodes to the cluster, Citus automatically creates copies of the distributed objects on the new nodes in the correct order to satisfy object dependencies.

| Name | Type | Description |
| --- | --- | --- |
| `classid` | oid | Class of the distributed object |
| `objid` | oid | Object ID of the distributed object |
| `objsubid` | integer | Object sub ID of the distributed object, for example, attnum |
| `type` | text | Part of the stable address used during pg upgrades |
| `object_names` | text\[\] | Part of the stable address used during pg upgrades |
| `object_args` | text\[\] | Part of the stable address used during pg upgrades |
| `distribution_argument_index` | integer | Only valid for distributed functions/procedures |
| `colocationid` | integer | Only valid for distributed functions/procedures |

"Stable addresses" uniquely identify objects independently of a specific server. Citus tracks objects during a PostgreSQL upgrade by using stable addresses created by the [pg_identify_object_as_address()](https://www.postgresql.org/docs/current/functions-info.html#FUNCTIONS-INFO-OBJECT-TABLE) function.

Here's an example of how `create_distributed_function()` adds entries to the `citus.pg_dist_object` table:

``` psql
CREATE TYPE stoplight AS enum ('green', 'yellow', 'red');

CREATE OR REPLACE FUNCTION intersection()
RETURNS stoplight AS $$
DECLARE
        color stoplight;
BEGIN
        SELECT *
          FROM unnest(enum_range(NULL::stoplight)) INTO color
         ORDER BY random() LIMIT 1;
        RETURN color;
END;
$$ LANGUAGE plpgsql VOLATILE;

SELECT create_distributed_function('intersection()');

-- will have two rows, one for the TYPE and one for the FUNCTION
TABLE citus.pg_dist_object;
```

```output
-[ RECORD 1 ]---------------+------
classid                     | 1247
objid                       | 16780
objsubid                    | 0
type                        |
object_names                |
object_args                 |
distribution_argument_index |
colocationid                |
-[ RECORD 2 ]---------------+------
classid                     | 1255
objid                       | 16788
objsubid                    | 0
type                        |
object_names                |
object_args                 |
distribution_argument_index |
colocationid                |
```

### Citus schemas view

Citus 12.0 introduces the concept of `schema_based_sharding` and the `citus_schemas` view. This view shows which schemas are distributed in the system. The view only lists distributed schemas. Local schemas aren't displayed.

| Name | Type | Description |
| --- | --- | --- |
| schema_name | regnamespace | Name of the distributed schema |
| colocation_id | integer | Colocation ID of the distributed schema |
| schema_size | text | Human readable size summary of all objects within the schema |
| schema_owner | name | Role that owns the schema |

Here's an example:

```sql
schema_name  | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             1 | 0 bytes     | user_service
time_service |             2 | 0 bytes     | time_service
ping_service |             3 | 632 kB      | ping_service
```

### Citus tables view

The `citus_tables` view shows a summary of all tables managed by Citus (distributed and reference tables). The view combines information from Citus metadata tables for an easy, human-readable overview of these table properties:

- Table type
- Distribution column
- Colocation group ID
- Human-readable size
- Shard count
- Owner (database user)
- Access method (heap or columnar)

Here's an example:

```sql
SELECT * FROM citus_tables;
```

```output
┌────────────┬──────────────────┬─────────────────────┬───────────────┬────────────┬─────────────┬─────────────┬───────────────┐
│ table_name │ citus_table_type │ distribution_column │ colocation_id │ table_size │ shard_count │ table_owner │ access_method │
├────────────┼──────────────────┼─────────────────────┼───────────────┼────────────┼─────────────┼─────────────┼───────────────┤
│ foo.test   │ distributed      │ test_column         │             1 │ 0 bytes    │          32 │ citus       │ heap          │
│ ref        │ reference        │ <none>              │             2 │ 24 GB      │           1 │ citus       │ heap          │
│ test       │ distributed      │ id                  │             1 │ 248 TB     │          32 │ citus       │ heap          │
└────────────┴──────────────────┴─────────────────────┴───────────────┴────────────┴─────────────┴─────────────┴───────────────┘
```

### Time partitions view

Citus provides user-defined functions to manage partitions for the `timeseries` use case. It also maintains a `time_partitions` view to inspect the partitions it manages.

Columns:

- **parent_table** The table that is partitioned.
- **partition_column** The column on which the parent table is partitioned.
- **partition** The name of a partition table.
- **from_value** The lower bound in time for rows in this partition.
- **to_value** The upper bound in time for rows in this partition.
- **access_method** `heap` for row-based storage, and `columnar` for columnar storage.

```sql
SELECT * FROM time_partitions;
```

```output
┌────────────────────────┬──────────────────┬─────────────────────────────────────────┬─────────────────────┬─────────────────────┬───────────────┐
│      parent_table      │ partition_column │                partition                │     from_value      │      to_value       │ access_method │
├────────────────────────┼──────────────────┼─────────────────────────────────────────┼─────────────────────┼─────────────────────┼───────────────┤
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0000 │ 2015-01-01 00:00:00 │ 2015-01-01 02:00:00 │ columnar      │
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0200 │ 2015-01-01 02:00:00 │ 2015-01-01 04:00:00 │ columnar      │
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0400 │ 2015-01-01 04:00:00 │ 2015-01-01 06:00:00 │ columnar      │
│ github_columnar_events │ created_at       │ github_columnar_events_p2015_01_01_0600 │ 2015-01-01 06:00:00 │ 2015-01-01 08:00:00 │ heap          │
└────────────────────────┴──────────────────┴─────────────────────────────────────────┴─────────────────────┴─────────────────────┴───────────────┘
```

### Colocation group table

The `pg_dist_colocation` table contains information about which tables' shards should be placed together, or colocated. When two tables are in the same colocation group, Citus ensures shards with the same partition values are on the same worker nodes. This setup enables join optimizations, certain distributed rollups, and foreign key support. Shard colocation is inferred when the shard counts and partition column types all match between two tables. However, you can specify a custom colocation group when creating a distributed table.

| Name | Type | Description |
| --- | --- | --- |
| `colocationid` | int | Unique identifier for the colocation group this row corresponds to. |
| `shardcount` | int | Shard count for all tables in this colocation group. |
| `replicationfactor` | int | Replication factor for all tables in this colocation group. |
| `distributioncolumntype` | oid | The type of the distribution column for all tables in this colocation group. |
| `distributioncolumncollation` | oid | The collation of the distribution column for all tables in this colocation group. |

```sql
SELECT * from pg_dist_colocation;
```

```output
 colocationid | shardcount | replicationfactor | distributioncolumntype | distributioncolumncollation
--------------+------------+-------------------+------------------------+-----------------------------
            2 |         32 |                 1 |                     20 |                           0
(1 row)
```

### Rebalancer strategy table

This table defines strategies that `citus_rebalance_start` can use to determine where to move shards.

| Name | Type | Description |
| --- | --- | --- |
| `name` | name | Unique name for the strategy. |
| `default_strategy` | boolean | Specifies whether `citus_rebalance_start` should choose this strategy by default. Use `citus_set_default_rebalance_strategy` to update this column. |
| `shard_cost_function` | regproc | Identifier for a cost function, which must take a `shardid` as bigint, and return its notion of a cost, as type real. |
| `node_capacity_function` | regproc | Identifier for a capacity function, which must take a `nodeid` as int, and return its notion of node capacity as type real. |
| `shard_allowed_on_node_function` | regproc | Identifier for a function that when given a `shardid` bigint, and `nodeidarg` int, returns a boolean that indicates whether the shard is allowed to be stored on the node. |
| `default_threshold` | float4 | Threshold for deeming a node too full or too empty, which determines when the `citus_rebalance_start` should try to move shards. |
| `minimum_threshold` | float4 | A safeguard to prevent the threshold argument of `citus_rebalance_start()` from being set too low. |
| `improvement_threshold` | float4 | Determines when moving a shard is worth it during a rebalance. The rebalancer moves a shard when the ratio of the improvement with the shard move to the improvement without crosses the threshold. This value is most useful with the `by_disk_size strategy`. |

A Citus installation ships with these strategies in the table:

```sql
SELECT * FROM pg_dist_rebalance_strategy;
```

```output
-[ RECORD 1 ]------------------+---------------------------------
name                           | by_shard_count
default_strategy               | f
shard_cost_function            | citus_shard_cost_1
node_capacity_function         | citus_node_capacity_1
shard_allowed_on_node_function | citus_shard_allowed_on_node_true
default_threshold              | 0
minimum_threshold              | 0
improvement_threshold          | 0
-[ RECORD 2 ]------------------+---------------------------------
name                           | by_disk_size
default_strategy               | t
shard_cost_function            | citus_shard_cost_by_disk_size
node_capacity_function         | citus_node_capacity_1
shard_allowed_on_node_function | citus_shard_allowed_on_node_true
default_threshold              | 0.1
minimum_threshold              | 0.01
improvement_threshold          | 0.5
```

The `by_shard_count` strategy assigns every shard the same cost. Its effect is to equalize the shard count across nodes. The default strategy, `by_disk_size`, assigns a cost to each shard matching its disk size in bytes plus that of the shards that are colocated with it. The disk size is calculated using `pg_total_relation_size`, so it includes indices. This strategy attempts to achieve the same disk space on every node. Note the default threshold of 0.1. It prevents unnecessary shard movement caused by insignificant differences in disk space.

#### Creating custom rebalancer strategies

The following examples show functions that you can use within new shard rebalancer strategies. Register these functions in the `pg_dist_rebalance_strategy` table by using the `citus_add_rebalance_strategy` function.

- Setting a node capacity exception by hostname pattern:

  ```sql
  -- example of node_capacity_function

  CREATE FUNCTION v2_node_double_capacity(nodeidarg int)
      RETURNS real AS $$
      SELECT
          (CASE WHEN nodename LIKE '%.v2.worker.citusdata.com' THEN 2.0::float4 ELSE 1.0::float4 END)
      FROM pg_dist_node where nodeid = nodeidarg
      $$ LANGUAGE sql;
  ```

- Rebalancing by number of queries that go to a shard, as measured by the `citus_stat_statements`:

  ```sql
  -- example of shard_cost_function

  CREATE FUNCTION cost_of_shard_by_number_of_queries(shardid bigint)
      RETURNS real AS $$
      SELECT coalesce(sum(calls)::real, 0.001) as shard_total_queries
      FROM citus_stat_statements
      WHERE partition_key is not null
          AND get_shard_id_for_distribution_column('tab', partition_key) = shardid;
  $$ LANGUAGE sql;
  ```

- Isolating a specific shard (10000) on a node (address '10.0.0.1'):

  ```sql
  -- example of shard_allowed_on_node_function

  CREATE FUNCTION isolate_shard_10000_on_10_0_0_1(shardid bigint, nodeidarg int)
      RETURNS boolean AS $$
      SELECT
          (CASE WHEN nodename = '10.0.0.1' THEN shardid = 10000 ELSE shardid != 10000 END)
      FROM pg_dist_node where nodeid = nodeidarg
      $$ LANGUAGE sql;

  -- The next two definitions are recommended in combination with the above function.
  -- This way the average utilization of nodes is not impacted by the isolated shard.
  CREATE FUNCTION no_capacity_for_10_0_0_1(nodeidarg int)
      RETURNS real AS $$
      SELECT
          (CASE WHEN nodename = '10.0.0.1' THEN 0 ELSE 1 END)::real
      FROM pg_dist_node where nodeid = nodeidarg
      $$ LANGUAGE sql;
  CREATE FUNCTION no_cost_for_10000(shardid bigint)
      RETURNS real AS $$
      SELECT
          (CASE WHEN shardid = 10000 THEN 0 ELSE 1 END)::real
      $$ LANGUAGE sql;
  ```

### Query statistics table

> [!NOTE]  
> Starting with version 11.0, the `citus_stat_statements` view is part of Citus Community edition.

Citus provides `citus_stat_statements` for stats about how queries are executed and who runs them. It's similar to the [pg_stat_statements](https://www.postgresql.org/docs/current/static/pgstatstatements.html) view in PostgreSQL, which tracks statistics about query speed. You can join `citus_stat_statements` with `pg_stat_statements`.

| Name | Type | Description |
| --- | --- | --- |
| `queryid` | bigint | identifier (good for pg_stat_statements joins) |
| `userid` | oid | user who ran the query |
| `dbid` | oid | database instance of coordinator |
| `query` | text | anonymized query string |
| `executor` | text | Citus `executor <distributed_query_executor>` used: adaptive, or insert-select |
| `partition_key` | text | value of distribution column in router-executed queries, else NULL |
| `calls` | bigint | number of times the query was run |

```sql
-- create and populate distributed table
create table foo ( id int );
select create_distributed_table('foo', 'id');
insert into foo select generate_series(1,100);

-- enable stats
-- pg_stat_statements must be in shared_preload libraries
create extension pg_stat_statements;

select count(*) from foo;
select * from foo where id = 42;

select * from citus_stat_statements;
```

Results:

```output
-[ RECORD 1 ]-+----------------------------------------------
queryid       | -909556869173432820
userid        | 10
dbid          | 13340
query         | insert into foo select generate_series($1,$2)
executor      | insert-select
partition_key |
calls         | 1
-[ RECORD 2 ]-+----------------------------------------------
queryid       | 3919808845681956665
userid        | 10
dbid          | 13340
query         | select count(*) from foo;
executor      | adaptive
partition_key |
calls         | 1
-[ RECORD 3 ]-+----------------------------------------------
queryid       | 5351346905785208738
userid        | 10
dbid          | 13340
query         | select * from foo where id = $1
executor      | adaptive
partition_key | 42
calls         | 1
```

Caveats:

- The stats data isn't replicated, so it doesn't survive database crashes or failover.
- The table tracks a limited number of queries, set by the `pg_stat_statements.max` global user configuration (GUC). The default value is 5,000.
- To truncate the table, use the `citus_stat_statements_reset()` function.

### citus_stats view

> [!NOTE]  
> The `citus_stats` view is available starting in Citus 13.2.

The `citus_stats` view aggregates `pg_stats` across workers for distributed, reference, and Citus local tables. It provides cluster-wide column statistics.

| Name | Type | Description |
| --- | --- | --- |
| `tablename` | text | Citus table name |
| `attname` | name | Column name |
| `null_frac` | real | Fraction of NULL values (0.0–1.0) |
| `most_common_vals` | anyarray | Array of most common values |
| `most_common_freqs` | real[] | Frequencies corresponding to `most_common_vals` |

> [!TIP]  
> Run `ANALYZE` on tables to populate `pg_stats` on workers before querying `citus_stats`.

Example:

```sql
SELECT tablename, attname, null_frac, most_common_vals, most_common_freqs
FROM citus_stats
WHERE tablename = 'dist_user_payloads';
```

### Citus stat counters view

The `citus_stat_counters` view reports aggregate statistics for each database on the local node, including both connection management and distributed query execution metrics. It also returns rows for databases without Citus (their counters are zero).

| Name | Type | Description |
| --- | --- | --- |
| `database_id` | oid | Database OID. |
| `name` | name | Database name (NULL if the database was dropped). |
| `connection_establishment_succeeded` | bigint | Successful inter-node connections initiated by this node. |
| `connection_establishment_failed` | bigint | Failed connection attempts (for example, unreachable nodes, timeouts, configuration errors). Optional connections skipped due to throttling (`citus.max_shared_pool_size`, `citus.local_shared_pool_size`) aren't counted as failures. See the throttling GUCs in [api-guc](api-guc.md#citusmax_shared_pool_size-integer). |
| `connection_reused` | bigint | Cached connections reused instead of opening a new one (`citus.max_cached_conns_per_worker`, `citus.max_cached_connection_lifetime`). |
| `query_execution_single_shard` | bigint | Single-shard queries and subplans executed. |
| `query_execution_multi_shard` | bigint | Multi-shard queries and subplans executed. |
| `stats_reset` | timestamptz | Timestamp when stats were last reset (NULL if never reset). |

**Connection management metrics**

- `connection_establishment_succeeded`: counts successfully established inter-node connections from this node.
- `connection_establishment_failed`: counts failed connection attempts (includes timeouts; see `citus.node_connection_timeout`).
- `connection_reused`: counts times an existing cached connection was reused instead of opening a new one.

**Query execution metrics**

These counters increment for top-level queries *and* subplans/subqueries (for example, `INSERT ... SELECT`, `MERGE`, recursive planning steps).

- `query_execution_single_shard`: queries that accessed a single shard.
- `query_execution_multi_shard`: queries that accessed multiple shards.

```sql
SELECT * FROM citus_stat_counters;
```

```output
 database_id |    name    | connection_establishment_succeeded | connection_establishment_failed | connection_reused | query_execution_single_shard | query_execution_multi_shard |          stats_reset
-------------+------------+------------------------------------+---------------------------------+-------------------+------------------------------+-----------------------------+-------------------------------+
       16384 | dist_db_1  |                               1897 |                               2 |              6213 |                         4449 |                         292 |
       17216 | dist_db_2  |                                422 |                               0 |              2060 |                          731 |                         256 | 2025-09-12 11:44:39.186173+03
           5 | postgres   |                                  0 |                               0 |                 0 |                            0 |                           0 |
(3 rows)
```

Notes:

- Stats aren't persisted; they're cleared on server restart.
- `citus.enable_stat_counters` controls collection. Default is **false**. Set it globally in `postgresql.conf`, or per role/database using `ALTER ROLE ... SET` or `ALTER DATABASE ... SET`.
- Use `citus_stat_counters(<db_oid>)` to query a specific database (or omit/`0` to get all databases). The function can return stats for dropped databases; the view filters them out (name is NULL).
- Use `citus_stat_counters_reset(<db_oid>)` to reset counters for a specific database (or omit/`0` for the current database).

### Tenant-level query statistics view

The `citus_stat_tenants` view augments the `citus_stat_statements` view with information about how many queries each tenant is running. Tracing queries to originating tenants helps you decide when to use `tenant_isolation`.

This view counts recent single-tenant queries that happen during a configurable time period. The tally of read-only and total queries for the period increases until the current period ends. After that, the counts move to last period's statistics, which stays constant until expiration. Set the period length in seconds by using `citus.stats_tenants_period`. The default is 60 seconds.

The view displays up to `citus.stat_tenants_limit` rows. The default is 100. It counts only queries filtered to a single tenant, ignoring queries that apply to multiple tenants at once.

| Name | Type | Description |
| --- | --- | --- |
| `nodeid` | int | Node ID from `pg_dist_node` |
| `colocation_id` | int | ID of `colocation group <colocation_group_table>` |
| `tenant_attribute` | text | Value in the distribution column identifying tenant |
| `read_count_in_this_period` | int | Number of read (SELECT) queries for tenant in period |
| `read_count_in_last_period` | int | Number of read queries one period of time ago |
| `query_count_in_this_period` | int | Number of read/write queries for tenant in time period |
| `query_count_in_last_period` | int | Number of read/write queries one period of time ago |
| `cpu_usage_in_this_period` | double | Seconds of CPU time spent for this tenant in period |
| `cpu_usage_in_last_period` | double | Seconds of CPU time spent for this tenant in last period |

Tracking tenant level statistics adds overhead, so it's disabled by default. To enable it, set `citus.stat_tenants_track` to `'all'`.

**Example:**

Suppose you have a distributed table called `dist_table`, with distribution column `tenant_id`. Then you make some queries:

```sql
INSERT INTO dist_table(tenant_id) VALUES (1);
INSERT INTO dist_table(tenant_id) VALUES (1);
INSERT INTO dist_table(tenant_id) VALUES (2);

SELECT count(*) FROM dist_table WHERE tenant_id = 1;
```

The tenant-level statistics reflect the queries you just made:

```sql
SELECT tenant_attribute, read_count_in_this_period,
       query_count_in_this_period, cpu_usage_in_this_period
  FROM citus_stat_tenants;
```

```output
 tenant_attribute | read_count_in_this_period | query_count_in_this_period | cpu_usage_in_this_period
------------------+---------------------------+----------------------------+--------------------------
 1                |                         1 |                          3 |                 0.000883
 2                |                         0 |                          1 |                 0.000144
```

### Distributed query activity

In some situations, queries block on row-level locks on one of the shards on a worker node. If that situation happens, those queries don't show up in [pg_locks](https://www.postgresql.org/docs/current/static/view-pg-locks.html) on the Citus coordinator node.

Citus provides special views to watch queries and locks throughout the cluster, including shard-specific queries used internally to build results for distributed queries.

- **citus_stat_activity**: shows the distributed queries that are executing on all nodes. A superset of `pg_stat_activity`, usable wherever the latter is.
- **citus_dist_stat_activity**: the same as `citus_stat_activity` but restricted to distributed queries only, and excluding Citus fragment queries.
- **citus_lock_waits**: Blocked queries throughout the cluster.

The first two views include all columns of [pg_stat_activity](https://www.postgresql.org/docs/current/static/monitoring-stats.html#PG-STAT-ACTIVITY-VIEW) plus the global PID of the worker that initiated the query.

For example, consider counting the rows in a distributed table:

```sql
-- run in one session
-- (with a pg_sleep so we can see it)

SELECT count(*), pg_sleep(3) FROM users_table;
```

You can see the query appear in `citus_dist_stat_activity`:

```sql
-- run in another session

SELECT * FROM citus_dist_stat_activity;

-[ RECORD 1 ]----+-------------------------------------------
global_pid       | 10000012199
nodeid           | 1
is_worker_query  | f
datid            | 13724
datname          | postgres
pid              | 12199
leader_pid       |
usesysid         | 10
usename          | postgres
application_name | psql
client_addr      |
client_hostname  |
client_port      | -1
backend_start    | 2022-03-23 11:30:00.533991-05
xact_start       | 2022-03-23 19:35:28.095546-05
query_start      | 2022-03-23 19:35:28.095546-05
state_change     | 2022-03-23 19:35:28.09564-05
wait_event_type  | Timeout
wait_event       | PgSleep
state            | active
backend_xid      |
backend_xmin     | 777
query_id         |
query            | SELECT count(*), pg_sleep(3) FROM users_table;
backend_type     | client backend
```

The `citus_dist_stat_activity` view hides internal Citus fragment queries. To see those queries, use the more detailed `citus_stat_activity` view. For instance, the previous `count(*)` query requires information from all shards. Some of the information is in shard `users_table_102039`, which is visible in the following query.

```sql
SELECT * FROM citus_stat_activity;

-[ RECORD 1 ]----+-----------------------------------------------------------------------
global_pid       | 10000012199
nodeid           | 1
is_worker_query  | f
datid            | 13724
datname          | postgres
pid              | 12199
leader_pid       |
usesysid         | 10
usename          | postgres
application_name | psql
client_addr      |
client_hostname  |
client_port      | -1
backend_start    | 2022-03-23 11:30:00.533991-05
xact_start       | 2022-03-23 19:32:18.260803-05
query_start      | 2022-03-23 19:32:18.260803-05
state_change     | 2022-03-23 19:32:18.260821-05
wait_event_type  | Timeout
wait_event       | PgSleep
state            | active
backend_xid      |
backend_xmin     | 777
query_id         |
query            | SELECT count(*), pg_sleep(3) FROM users_table;
backend_type     | client backend
-[ RECORD 2 ]----------+-----------------------------------------------------------------------------------------
global_pid       | 10000012199
nodeid           | 1
is_worker_query  | t
datid            | 13724
datname          | postgres
pid              | 12725
leader_pid       |
usesysid         | 10
usename          | postgres
application_name | citus_internal gpid=10000012199
client_addr      | 127.0.0.1
client_hostname  |
client_port      | 44106
backend_start    | 2022-03-23 19:29:53.377573-05
xact_start       |
query_start      | 2022-03-23 19:32:18.278121-05
state_change     | 2022-03-23 19:32:18.278281-05
wait_event_type  | Client
wait_event       | ClientRead
state            | idle
backend_xid      |
backend_xmin     |
query_id         |
query            | SELECT count(*) AS count FROM public.users_table_102039 users WHERE true
backend_type     | client backend
```

The `query` field shows rows being counted in shard 102039.

Here are examples of useful queries you can build using `citus_stat_activity`:

```sql
-- active queries' wait events

SELECT query, wait_event_type, wait_event
  FROM citus_stat_activity
 WHERE state='active';

-- active queries' top wait events

SELECT wait_event, wait_event_type, count(*)
  FROM citus_stat_activity
 WHERE state='active'
 GROUP BY wait_event, wait_event_type
 ORDER BY count(*) desc;

-- total internal connections generated per node by Citus

SELECT nodeid, count(*)
  FROM citus_stat_activity
 WHERE is_worker_query
 GROUP BY nodeid;
```

The next view is `citus_lock_waits`. To see how it works, generate a locking situation manually. First, set up a test table from the coordinator:

```sql
CREATE TABLE numbers AS
  SELECT i, 0 AS j FROM generate_series(1,10) AS i;
SELECT create_distributed_table('numbers', 'i');
```

Then, using two sessions on the coordinator, run this sequence of statements:

```sql
-- session 1                           -- session 2
-------------------------------------  -------------------------------------
BEGIN;
UPDATE numbers SET j = 2 WHERE i = 1;
                                       BEGIN;
                                       UPDATE numbers SET j = 3 WHERE i = 1;
                                       -- (this blocks)
```

The `citus_lock_waits` view shows the situation.

```sql
SELECT * FROM citus_lock_waits;

-[ RECORD 1 ]-------------------------+--------------------------------------
waiting_gpid                          | 10000011981
blocking_gpid                         | 10000011979
blocked_statement                     | UPDATE numbers SET j = 3 WHERE i = 1;
current_statement_in_blocking_process | UPDATE numbers SET j = 2 WHERE i = 1;
waiting_nodeid                        | 1
blocking_nodeid                       | 1
```

In this example the queries originated on the coordinator, but the view can also list locks between queries originating on workers.

## Tables on all nodes

Citus has other informational tables and views that you can access on all nodes, not just the coordinator.

### Connection credentials table

> [!NOTE]  
> This table is part of Citus Community edition as of version 11.0.

The `pg_dist_authinfo` table holds authentication parameters that Citus nodes use to connect to one another.

| Name | Type | Description |
| --- | --- | --- |
| `nodeid` | integer | Node ID from `pg_dist_node`, or 0, or -1 |
| `rolename` | name | PostgreSQL role |
| `authinfo` | text | Space-separated libpq connection parameters |

When a connection starts, a node checks the table to see if a row with the destination `nodeid` and desired `rolename` exists. If it does, the node includes the corresponding `authinfo` string in its libpq connection. A common example is to store a password, like `'password=abc123'`. You can review the [full list](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS) of possibilities.

The parameters in `authinfo` are space-separated, in the form `key=val`. To write an empty value or a value containing spaces, surround it with single quotes, for example, `keyword='a value'`. Single quotes and backslashes within the value must be escaped by using a backslash. For example, `\'` and `\\`.

The `nodeid` column can also take the special values 0 and -1, which mean *all nodes* or *loopback connections*, respectively. If, for a given node, both specific and all-node rules exist, the specific rule takes precedence.

``` postgres
SELECT * FROM pg_dist_authinfo;

 nodeid | rolename | authinfo
--------+----------+-----------------
    123 | jdoe     | password=abc123
(1 row)
```

### Connection pooling credentials

> [!NOTE]  
> This table is part of Citus Community edition as of version 11.0.

To use a connection pooler to connect to a node, specify the pooler options by using `pg_dist_poolinfo`. This metadata table holds the host, port, and database name for Citus to use when connecting to a node through a pooler.

If you add pool information, Citus tries to use these values instead of setting up a direct connection. The `pg_dist_poolinfo` information supersedes `pg_dist_node`.

| Name | Type | Description |
| --- | --- | --- |
| `nodeid` | integer | Node ID from `pg_dist_node` |
| `poolinfo` | text | Space-separated parameters: host, port, or dbname |

> [!NOTE]  
> In some situations, Citus ignores the settings in `pg_dist_poolinfo`. For example, shard rebalancing isn't compatible with connection poolers such as PgBouncer. In these scenarios, Citus uses a direct connection.

```sql
-- how to connect to node 1 (as identified in pg_dist_node)

INSERT INTO pg_dist_poolinfo (nodeid, poolinfo)
     VALUES (1, 'host=127.0.0.1 port=5433');
```

## Related content

- [User defined functions](api-udf.md)
- [Configuration parameters](api-guc.md)
- [What is Azure Cosmos DB for PostgreSQL?](what-is-citus.md)
