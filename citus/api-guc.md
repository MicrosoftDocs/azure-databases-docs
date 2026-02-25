---
title: "Configure Citus: GUC Parameters Reference"
description: In the Citus configuration reference, you find information about Citus specific configuration parameters and standard PostgreSQL parameters that affect the behavior of Citus.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
ai-usage: ai-assisted
---

# Configure Citus: GUC parameters reference

Various configuration parameters affect the behavior of Citus. These parameters include both standard PostgreSQL parameters and Citus-specific parameters. To learn more about PostgreSQL configuration parameters, see the [run time configuration](http://www.postgresql.org/docs/current/static/runtime-config.html) section of the PostgreSQL documentation.

The rest of this reference discusses Citus-specific configuration parameters. Set these parameters similar to PostgreSQL parameters by modifying `postgresql.conf` or [by using the SET command](http://www.postgresql.org/docs/current/static/config-setting.html).

For example, you can update a setting by using the following command:

```sql
ALTER DATABASE citus SET citus.multi_task_query_log_level = 'log';
```

## General configuration

### citus.max_background_task_executors_per_node (integer)

Determines how many background tasks can run in parallel at a given time. For instance, these tasks are for shard moves from or to a node. When you increase this value, consider increasing `citus.max_background_task_executors` and [max_worker_processes](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES).

- Default: 1
- Minimum: 1
- Maximum: 128

### citus.max_worker_nodes_tracked (integer)

Citus tracks worker nodes' locations and their membership in a shared hash table on the coordinator node. This configuration value limits the size of the hash table, and thus the number of worker nodes that can be tracked. The default for this setting is 2,048. Set this parameter only at server start. It's effective on the coordinator node.

### citus.use_secondary_nodes (enum)

Sets the policy to use when choosing nodes for `SELECT` queries. If you set this policy to `always`, the planner queries only nodes that `pg_dist_node` marks as secondary nodes.

The supported values for this enum are:

- **never**: (default) All reads happen on primary nodes.
- **always**: Reads run against secondary nodes instead, and insert/update statements are disabled.

### citus.cluster_name (text)

Informs the coordinator node planner which cluster it coordinates. Once you set `cluster_name`, the planner queries worker nodes in that cluster alone.

### citus.enable_version_checks (boolean)

Upgrading the Citus version requires a server restart (to pick up the new shared-library) and running an `ALTER EXTENSION UPDATE` command. Failure to execute both steps could potentially cause errors or crashes. Citus thus validates that the version of the code and that of the extension match, and errors out if they don't.

This value defaults to *true* and is effective on the coordinator. In rare cases, complex upgrade processes might require setting this parameter to *false*, thus disabling the check.

### citus.log_distributed_deadlock_detection (boolean)

Whether to log distributed deadlock detection related processing in the server log. It defaults to false.

### citus.distributed_deadlock_detection_factor (floating point)

Sets the time to wait before checking for distributed deadlocks. This value is multiplied by PostgreSQL's [deadlock_timeout](https://www.postgresql.org/docs/current/static/runtime-config-locks.html) setting. The default value is *2*. A value of *-1* disables distributed deadlock detection.

### citus.node_connection_timeout (integer)

The `citus.node_connection_timeout` global user configuration (GUC) sets the maximum duration in milliseconds to wait for connection establishment. Citus raises an error if the timeout elapses before at least one worker connection is established. This GUC affects connections from the coordinator to workers, and workers to each other.

- Default: 30 seconds
- Minimum: 10 milliseconds
- Maximum: one hour

```sql
-- set to 60 seconds
ALTER DATABASE foo
SET citus.node_connection_timeout = 60000;
```

### citus.node_conninfo (text)

The `citus.node_conninfo` GUC sets nonsensitive [libpq connection parameters](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS) for all inter-node connections.

```sql
-- key=value pairs separated by spaces.
-- For example, ssl options:

ALTER DATABASE foo
SET citus.node_conninfo =
  'sslrootcert=/path/to/citus.crt sslmode=verify-full';
```

Citus honors only a specific subset of the allowed options, namely:

- connect_timeout
- gsslib†
- host
- keepalives
- keepalives_count
- keepalives_idle
- keepalives_interval
- krbsrvname†
- sslcompression
- sslcrl
- sslmode (defaults to "require" as of Citus 8.1)
- sslnegotiation
- sslrootcert
- tcp_user_timeout

*(† = subject to the runtime presence of optional PostgreSQL features)*

The `node_conninfo` setting takes effect only on newly opened connections. To force all connections to use the new settings, make sure to reload the PostgreSQL configuration:

```sql
SELECT pg_reload_conf();
```

> [!WARNING]  
> Citus versions prior to 9.2.4 require a full database restart to force all connections to use the new setting.

### citus.local_hostname (text)

Citus nodes sometimes need to connect to themselves for system operations. By default, they use the address `localhost` to refer to themselves, but this address can cause problems. For example, when a host requires `sslmode=verify-full` for incoming connections, adding `localhost` as an alternative hostname on the SSL certificate isn't always desirable or feasible.

`citus.local_hostname` sets the hostname a node uses to connect to itself. The default value is *localhost*.

```sql
ALTER SYSTEM SET citus.local_hostname TO 'mynode.example.com';
```

### citus.show_shards_for_app_name_prefixes (text)

By default, Citus hides shards from the list of tables PostgreSQL gives to SQL clients. Citus has this default because there are multiple shards per distributed table, and the shards can be distracting to the SQL client.

The `citus.show_shards_for_app_name_prefixes` GUC allows shards to be displayed for selected clients that want to see them. Its default value is `''`.

``` psql
-- show shards to psql only (hide in other clients, like pgAdmin)

SET citus.show_shards_for_app_name_prefixes TO 'psql';

-- also accepts a comma separated list

SET citus.show_shards_for_app_name_prefixes TO 'psql,pg_dump';
```

### citus.rebalancer_by_disk_size_base_cost (integer)

When you use the by_disk_size rebalance strategy, each shard group gets this cost in bytes added to its actual disk size. Use this strategy to avoid creating a bad balance when there's minimal data in some of the shards. The assumption is that even empty shards have some cost, because of parallelism and because empty shard groups will likely grow in the future.

The default value is `100MB`.

### citus.shard_transfer_mode (enum)

Controls the default method for moving shards and distributed schemas (used by shard rebalancing, `citus_move_shard_placement`, `rebalance_table_shards`, and `citus_schema_move`). When available, logical replication avoids blocking writes; otherwise, Citus falls back to a blocking copy.

Possible values:

- **auto** (default): Use logical replication when replica identity exists; otherwise fall back to legacy behavior (COPY with blocking writes).
- **force_logical**: Force logical replication even when tables lack a replica identity. Concurrent UPDATE/DELETEs on those tables fail during replication.
- **block_writes**: Always use COPY while blocking writes for tables lacking a primary key or replica identity.

This GUC takes effect on the coordinator. Use it to set a cluster-wide default for data movement operations.

```sql
-- force logical replication for shard moves
SET citus.shard_transfer_mode = 'force_logical';
SELECT rebalance_table_shards('orders');
```

## Query Statistics

### citus.stat_statements_purge_interval (integer)

> [!NOTE]  
> As of version 11.0, this GUC is part of the Citus Community edition.

Sets how often the maintenance daemon removes records from `citus_stat_statements` that don't match any records in `pg_stat_statements`. Set the time interval between purges in seconds. The default value is *10*. Set the value to *0* to disable the purges.

``` psql
SET citus.stat_statements_purge_interval TO 5;
```

This parameter works on the coordinator and you can change it at runtime.

### citus.stat_statements_max (integer)

> [!NOTE]  
> As of version 11.0, this GUC is part of the Citus Community edition.

Sets the maximum number of rows to store in `citus_stat_statements`. The default value is *50000*. You can change it to any value in the range *1000* - *10000000*. Each row requires 140 bytes of storage, so setting `stat_statements_max` to its maximum value of 10M uses 1.4 GB of memory.

You need to restart PostgreSQL for this change to take effect.

### citus.stat_statements_track (enum)

> [!NOTE]  
> As of version 11.0, this GUC is part of the Citus Community edition.

Recording statistics for `citus_stat_statements` uses extra CPU resources. When the database is under load, the administrator might want to disable statement tracking. The `citus.stat_statements_track` GUC turns tracking on or off.

- **all**: Track all statements.
- **none**: (default) Disable tracking.

### citus.stat_tenants_untracked_sample_rate (floating point)

Sampling rate for new tenants in `citus_stat_tenants`. The rate can be of range between *0.0* and *1.0*. The default is *1.0*, which means 100% of untracked tenant queries are sampled. Set to a lower value to sample tenants that are currently untracked at the provided rate, while already tracked tenants have 100% queries sampled.

### citus.enable_stat_counters (boolean)

When enabled, Citus collects connection and query execution counters that you can query via the `citus_stat_counters` view and `citus_stat_counters()` function, and reset with `citus_stat_counters_reset()`.

> [!IMPORTANT]  
> - Default: **false** (disabled).
> - Requires superuser to change.
> - Counters are not persisted; they reset on server restart.
> - Disabling stops collection but existing counters remain queryable.

```sql
-- enable stat counters collection
ALTER SYSTEM SET citus.enable_stat_counters = true;
SELECT pg_reload_conf();
```

## Data Loading

### citus.multi_shard_commit_protocol (enum)

Sets the commit protocol to use when performing COPY on a hash distributed table. On each individual shard placement, the process performs the COPY in a transaction block to ensure that no data is ingested if an error occurs during the COPY. However, there's a particular failure case in which the COPY succeeds on all placements, but a (hardware) failure occurs before all transactions commit. You can use this parameter to prevent data loss in that case by choosing between the following commit protocols:

- **2pc**: (default) The transactions that COPY data on the shard placements first prepare PostgreSQL's [two-phase commit](http://www.postgresql.org/docs/current/static/sql-prepare-transaction.html) and then commit it. You can manually recover or abort failed commits by using COMMIT PREPARED or ROLLBACK PREPARED, respectively. When you use `2pc`, increase [max_prepared_transactions](http://www.postgresql.org/docs/current/static/runtime-config-resource.html) on all the workers, typically to the same value as max_connections.
- **1pc**: The transactions that COPY data on the shard placements commit in a single round. Data might be lost if a commit fails after COPY succeeds on all placements (rare).

### citus.shard_count (integer)

Sets the shard count for hash-partitioned tables and defaults to *32*. The user-defined function `create_distributed_table <create_distributed_table>` uses this value when creating hash-partitioned tables. Set this parameter at run-time. It takes effect on the coordinator.

### citus.replicate_reference_tables_on_activate (boolean)

Reference table shards must be placed on all nodes that have distributed tables. By default, the system copies reference table shards to a node at node activation time, that is, when such functions as `citus_add_node` or `citus_activate_node` are called. However, node activation might be an inconvenient time to copy the placements, because it can take a long time when there are large reference tables.

You can defer reference table replication by setting the `citus.replicate_reference_tables_on_activate` GUC to `off`. With this setting, reference table replication happens when the system creates new shards on the node. For instance, when calling `create_distributed_table`, `create_reference_table`, or when the shard rebalancer moves shards to the new node.

The default value for this GUC is *on*.

### citus.metadata_sync_mode (enum)

> [!NOTE]  
> Requires superuser access to change.

This GUC determines how Citus synchronizes metadata across nodes. By default Citus updates all metadata in a single transaction for consistency. However, PostgreSQL has a hard memory limit related to cache invalidations, and Citus metadata syncing for a large cluster can fail from memory exhaustion.

As a workaround, Citus provides an optional nontransactional sync mode that uses a series of smaller transactions. While this mode works in limited memory, there's a possibility of transactions failing and leaving metadata in an inconsistency state. To help with this potential problem, nontransactional metadata sync is designed as an idempotent action, so you can rerun it repeatedly if needed.

There are two values for this GUC:

- **transactional**: (Default) Synchronize all metadata in a single transaction.
- **nontransactional**: Synchronize metadata using multiple small transactions.

Examples:

```sql
-- to add a new node and sync nontransactionally

SET citus.metadata_sync_mode TO 'nontransactional';
SELECT citus_add_node(<ip>, <port>);

-- to manually (re)sync

SET citus.metadata_sync_mode TO 'nontransactional';
SELECT start_metadata_sync_to_all_nodes();
```

We advise trying transactional mode first, and switching to nontransactional only if a memory failure occurs.

## Planner Configuration

### citus.enable_local_fast_path_query_optimization (boolean)

Enables delayed fast path planning optimization for local single-shard router queries. When on, Citus delays building the fast-path placeholder plan until shard identification; if the shard is local (MX mode), Citus replans with the shard OID and reuses a cached plan, avoiding deparse/parse/planning overhead.

- Default: true

### citus.enable_recurring_outer_join_pushdown (boolean)

Controls whether Citus pushes down eligible LEFT/RIGHT outer joins (recurring outer joins) to workers by injecting shard-interval constraints on reference/intermediate results. Enabled by default in Citus 13.2. Disable if you want to force such joins to execute on the coordinator.

- Default: true

### citus.local_table_join_policy (enum)

This GUC determines how Citus moves data when joining local and distributed tables. Customizing the join policy can help reduce the amount of data sent between worker nodes.

Citus sends either the local or distributed tables to nodes as necessary to support the join. Copying table data is referred to as a *conversion*. If a local table is converted, the Citus planner sends it to any workers that need its data to perform the join. If a distributed table is converted, the coordinator collects it and uses it to support the join. The Citus planner sends only the necessary rows during a conversion.

Four modes express conversion preference:

- **auto**: (Default) Citus converts either all local or all distributed tables to support local and distributed table joins. Citus decides which to convert using a heuristic. It converts distributed tables if they're joined by using a constant filter on a unique index (such as a primary key). This behavior ensures that less data moves between workers.
- **never**: Citus doesn't allow joins between local and distributed tables.
- **prefer-local**: Citus prefers converting local tables to support local and distributed table joins.
- **prefer-distributed**: Citus prefers converting distributed tables to support local and distributed table joins. If the distributed tables are huge, using this option might result in moving lots of data between workers.

For example, assume `citus_table` is a distributed table distributed by the column `x`, and that `postgres_table` is a local table:

```sql
CREATE TABLE citus_table(x int primary key, y int);
SELECT create_distributed_table('citus_table', 'x');

CREATE TABLE postgres_table(x int, y int);

-- even though the join is on primary key, there isn't a constant filter
-- hence postgres_table will be sent to worker nodes to support the join
SELECT * FROM citus_table JOIN postgres_table USING (x);

-- there is a constant filter on a primary key, hence the filtered row
-- from the distributed table will be pulled to coordinator to support the join
SELECT * FROM citus_table JOIN postgres_table USING (x) WHERE citus_table.x = 10;

SET citus.local_table_join_policy to 'prefer-distributed';
-- since we prefer distributed tables, citus_table will be pulled to coordinator
-- to support the join. Note that citus_table can be huge.
SELECT * FROM citus_table JOIN postgres_table USING (x);

SET citus.local_table_join_policy to 'prefer-local';
-- even though there is a constant filter on primary key for citus_table
-- postgres_table will be sent to necessary workers because we are using 'prefer-local'.
SELECT * FROM citus_table JOIN postgres_table USING (x) WHERE citus_table.x = 10;
```

### citus.limit_clause_row_fetch_count (integer)

Sets the number of rows to fetch per task for limit clause optimization. In some cases, select queries with limit clauses might need to fetch all rows from each task to generate results. In those cases, and where an approximation would produce meaningful results, this configuration value sets the number of rows to fetch from each shard. Limit approximations are disabled by default and this parameter is set to *-1*. Set this value at run-time. It takes effect on the coordinator.

### citus.count_distinct_error_rate (floating point)

Citus can calculate count(distinct) approximations by using the postgresql-hll extension. This configuration entry sets the desired error rate when calculating count(distinct). *0.0*, which is the default, disables approximations for count(distinct). *1.0* provides no guarantees about the accuracy of results. Set this parameter to *0.005* for best results. Set this value at run-time. It takes effect on the coordinator.

### citus.task_assignment_policy (enum)

> [!NOTE]  
> This GUC applies to queries against `reference_tables`.

Set the policy to use when assigning tasks to workers. The coordinator assigns tasks to workers based on shard locations. This configuration value specifies the policy to use when making these assignments. Currently, you can use three task assignment policies.

- **greedy**: The greedy policy is the default and aims to evenly distribute tasks across workers.
- **round-robin**: The round-robin policy assigns tasks to workers in a round-robin fashion, alternating between different replicas. This policy enables better cluster utilization when the shard count for a table is low compared to the number of workers.
- **first-replica**: The first-replica policy assigns tasks based on the insertion order of placements (replicas) for the shards. In other words, the fragment query for a shard is assigned to the worker, which has the first replica of that shard. This method allows you to have strong guarantees about which shards are used on which nodes (that is, stronger memory residency guarantees).

Set this parameter at run-time. It takes effect on the coordinator.

### enable_non_colocated_router_query_pushdown (boolean)

Enables router planner for the queries that reference non-colocated distributed tables.

Normally, router planner is only enabled for the queries that reference colocated distributed tables because it isn't guaranteed to have the target shards always on the same node. For example, after rebalancing the shards. For this reason, while enabling this flag allows some degree of optimization for the queries that reference non-colocated distributed tables, it isn't guaranteed that the same query works after rebalancing the shards or altering the shard count of one of those distributed tables.

The default is `off`.

## Intermediate Data Transfer

### citus.binary_worker_copy_format (boolean)

Use the binary copy format to transfer intermediate data between workers. During large table joins, Citus might have to dynamically repartition and shuffle data between different workers. For PostgreSQL 13 and lower, the default for this setting is `false`, which means text encoding is used to transfer this data. For PostgreSQL 14 and higher, the default is `true`. Set this parameter to `true` to instruct the database to use PostgreSQL's binary serialization format to transfer data. The parameter takes effect on the workers and you need to change it in the postgresql.conf file. After you edit the config file, you can send a SIGHUP signal or restart the server for this change to take effect.

### citus.max_intermediate_result_size (integer)

The maximum size in KB of intermediate results for common table expressions (CTEs) that can't be pushed down to worker nodes for execution, and for complex subqueries. The default value is 1 GB, and a value of *-1* means no limit. Queries that exceed the limit are canceled and produce an error message.

## Data definition language (DDL)

### citus.enable_ddl_propagation (boolean)

Specifies whether to automatically propagate DDL changes from the coordinator to all workers. The default value is *true*. Because some schema changes require an access exclusive lock on tables, and because the automatic propagation applies to all workers sequentially, it can make a Citus cluster temporarily less responsive. You might choose to disable this setting and propagate changes manually.

> [!NOTE]  
> For a list of DDL propagation support, see [reference-ddl](reference-ddl.md).

### citus.enable_local_reference_table_foreign_keys (boolean)

This setting, enabled by default, allows foreign keys to be created between reference and local tables. For the feature to work, the coordinator node must be registered with itself, using `citus_add_node`.

Foreign keys between reference tables and local tables come at a slight cost. When you create the foreign key, Citus must add the plain table to Citus' metadata, and track it in `partition_table`. Local tables that are added to metadata inherit the same limitations as reference tables (see `ddl` and `citus_sql_reference`).

If you drop the foreign keys, Citus automatically removes such local tables from metadata, which eliminates such limitations on those tables.

### citus.enable_change_data_capture (boolean)

This setting, disabled by default, causes Citus to alter the `wal2json` and `pgoutput` logical decoders to work with distributed tables. Specifically, it rewrites the names of shards (for example, `foo_102027`) in decoder output to the base names of the distributed tables (for example, `foo`). It also avoids publishing duplicate events during tenant isolation and shard split, move, or rebalance operations.

For an example of using this GUC, see `cdc`.

### citus.enable_schema_based_sharding (boolean)

When you set this parameter to `ON`, all created schemas are distributed by default. Distributed schemas automatically associate with individual colocation groups, so tables you create in these schemas automatically become colocated distributed tables without a shard key. You can change this setting for individual sessions.

For an example of using this GUC, see `microservices_tutorial`.

## Executor Configuration

### General

#### citus.all_modifications_commutative

Citus enforces commutativity rules and acquires appropriate locks for modify operations to guarantee correct behavior. For example, it assumes that an INSERT statement commutes with another INSERT statement, but not with an UPDATE or DELETE statement. Similarly, it assumes that an UPDATE or DELETE statement doesn't commute with another UPDATE or DELETE statement. This behavior means that UPDATEs and DELETEs require Citus to acquire stronger locks.

If you have UPDATE statements that are commutative with your INSERTs or other UPDATEs, you can relax these commutativity assumptions by setting this parameter to true. When you set this parameter to true, all commands are considered commutative and claim a shared lock, which can improve overall throughput. Set this parameter at runtime. It's effective on the coordinator.

#### citus.multi_task_query_log_level (enum)

Sets a log level for any query that generates more than one task (that is, any query that hits more than one shard). This setting is useful during a multitenant application migration, as you can choose to error or warn for such queries, to find them and add a tenant_id filter to them. Set this parameter at runtime. It's effective on the coordinator. The default value for this parameter is *off*.

The supported values for this enum are:

- **off**: Turn off logging for any queries that generate multiple tasks (that is, span multiple shards).
- **debug**: Logs statement at DEBUG severity level.
- **log**: Logs statement at LOG severity level. The log line includes the SQL query that was run.
- **notice**: Logs statement at NOTICE severity level.
- **warning**: Logs statement at WARNING severity level.
- **error**: Logs statement at ERROR severity level.

It might be useful to use `error` during development testing, and a lower log level like `log` during actual production deployment. Choosing `log` causes multi-task queries to appear in the database logs with the query itself shown after "STATEMENT."

```output
LOG:  multi-task query about to be executed
HINT:  Queries are split to multiple tasks if they have to be split into several queries on the workers.
STATEMENT:  select * from foo;
```

#### citus.propagate_set_commands (enum)

Determines which SET commands the coordinator propagates to workers. The default value for this parameter is *none*.

The supported values are:

- **none**: no SET commands are propagated.
- **local**: only SET LOCAL commands are propagated.

#### citus.enable_repartition_joins (boolean)

Ordinarily, attempting to perform `repartition_joins` with the adaptive executor fails with an error message. However, setting `citus.enable_repartition_joins` to *true* allows Citus to perform the join. The default value is *false*.

#### citus.enable_repartitioned_insert_select (boolean)

By default, an `INSERT INTO ... SELECT` statement that can't be pushed down, attempts to repartition rows from the SELECT statement and transfer them between workers for insertion. However, if the target table has too many shards, repartitioning probably doesn't perform well. The overhead of processing the shard intervals when determining how to partition the results is too great. You can disable repartitioning manually by setting `citus.enable_repartitioned_insert_select` to *false*.

#### citus.enable_binary_protocol (boolean)

Set this parameter to true to instruct the coordinator node to use PostgreSQL's binary serialization format (when applicable) to transfer data with workers. Some column types don't support binary serialization.

Enabling this parameter is mostly useful when the workers must return large amounts of data. For example, when many rows are requested, the rows have many columns, or they use large types such as `hll` from the postgresql-hll extension.

The default value is *true*. When set to *false*, all results are encoded and transferred in text format.

#### citus.max_shared_pool_size (integer)

Specifies the maximum number of connections that the coordinator node, across all simultaneous sessions, is allowed to make per **remote** node. PostgreSQL must allocate fixed resources for every connection and this GUC helps ease connection pressure on remote nodes.

Without connection throttling, every multi-shard query creates connections on each remote node proportional to the number of shards it accesses (in particular, up to \#shards/#workers). Running dozens of multi-shard queries at once can easily hit remote nodes' `max_connections` limit, causing queries to fail.

By default, the value is automatically set equal to the coordinator's own `max_connections`, which isn't guaranteed to match that of the remote nodes (see the following note). The value *-1* disables throttling.

> [!NOTE]  
> Certain operations don't obey `citus.max_shared_pool_size`, most importantly repartition joins. For that reason, it can be prudent to increase the `max_connections` on the remote nodes a bit higher than `max_connections` on the coordinator. This larger value gives extra space for the connections required for repartition queries on the workers.

#### citus.local_shared_pool_size (integer)

Specifies the maximum number of connections, across all simultaneous sessions, that the coordinator is allowed to make to the **local** node. This setting is relevant when the local node has shards (for example, [Single-Node Citus](single-node.md)).

By default, the value is automatically set to half of the node's own `max_connections`. The goal is to keep headroom for client backends (such as `psql` or application connections) rather than letting internal Citus connections consume all available slots. The value *-1* disables throttling.

This GUC provides similar throttling as `citus.max_shared_pool_size`, but only for the local node.

#### citus.max_adaptive_executor_pool_size (integer)

While `max_shared_pool_size` limits worker connections across all sessions, `max_adaptive_executor_pool_size` limits worker connections from just the *current* session. This GUC is useful for:

- Preventing a single backend from getting all the worker resources
- Providing priority management: designate low priority sessions with low `max_adaptive_executor_pool_size`, and high priority sessions with higher values

The default value is *16*.

#### citus.executor_slow_start_interval (integer)

Time to wait in milliseconds between opening connections to the same worker node.

When the individual tasks of a multishard query take little time, they can often be finished over a single (often already cached) connection. To avoid redundantly opening more connections, the executor waits between connection attempts for the configured number of milliseconds. At the end of the interval, it increases the number of connections it can open.

For long queries (those taking more than 500 ms), slow start might add latency, but for short queries it's faster. The default value is *10 ms*.

#### citus.max_cached_conns_per_worker (integer)

Each backend opens connections to the workers to query the shards. At the end of the transaction, the configured number of connections stays open to speed up subsequent commands. Increasing this value reduces the latency of multishard queries, but also increases overhead on the workers.

The default value is *1*. A larger value such as *2* might be helpful for clusters that use a few concurrent sessions, but it's not wise to go much further (for example, *16* would be too high).

#### citus.force_max_query_parallelization (boolean)

Simulates the deprecated and now nonexistent real-time executor. Use this setting to open as many connections as possible to maximize query parallelization.

When you enable this GUC, Citus forces the adaptive executor to use as many connections as possible while executing a parallel distributed query. If not enabled, the executor might choose to use fewer connections to optimize overall query execution throughput. Internally, setting this value to *true* uses one connection per task.

One place where this setting is useful is in a transaction whose first query is lightweight and requires few connections, while a subsequent query would benefit from more connections. Citus decides how many connections to use in a transaction based on the first statement, which can throttle other queries unless you use the GUC to provide a hint.

```sql
BEGIN;
-- add this hint
SET citus.force_max_query_parallelization TO ON;

-- a lightweight query that doesn't require many connections
SELECT count(*) FROM table WHERE filter = x;

-- a query that benefits from more connections, and can obtain
-- them since we forced max parallelization above
SELECT ... very .. complex .. SQL;
COMMIT;
```

The default value is *false*.

### Explain output

#### citus.explain_all_tasks (boolean)

By default, Citus shows the output of a single, arbitrary task when running [EXPLAIN](http://www.postgresql.org/docs/current/static/sql-explain.html) on a distributed query. In most cases, the output of EXPLAIN is similar across tasks. Occasionally, some of the tasks are planned differently or have considerably higher execution times. In those cases, it can be useful to enable this parameter. After you enable this parameter, the EXPLAIN output includes all tasks. This setting might cause the EXPLAIN to take longer.

#### citus.explain_analyze_sort_method (enum)

Determines the sort method of the tasks in the output of EXPLAIN ANALYZE. The default value of `citus.explain_analyze_sort_method` is `execution-time`.

The supported values are:

- **execution-time**: sort by execution time.
- **taskId**: sort by task ID.

## Related content

- [User defined functions](api-udf.md)
- [Metadata tables and views](api-metadata.md)
- [What is Azure Cosmos DB for PostgreSQL?](what-is-citus.md)
