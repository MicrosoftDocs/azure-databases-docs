---
title: Citus Utility Functions Reference
description: In the Citus utility functions reference, you find information about the user defined functions that give Citus extra functionality beyond the standard SQL commands.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
ai-usage: ai-assisted
---

# Citus utility functions reference

This section contains reference information for the user-defined functions that Citus provides. These functions help provide further distributed functionality to Citus beyond the standard SQL commands.

## Table and shard DDL

In Citus, the following data definition language (DDL) commands for creating and modifying distributed tables and shards are essential for managing distributed databases.

### citus_schema_distribute

Use this function to convert existing regular schemas into distributed schemas. These distributed schemas automatically associate with individual colocation groups. When you create tables in these schemas, they automatically become colocated distributed tables without a shard key. The process of distributing the schema automatically assigns and moves it to an existing node in the cluster.

#### Arguments

**schemaname**: Name of the schema that you want to distribute.

#### Return value

None

#### Example

Distribute three schemas named `tenant_a`, `tenant_b`, and `tenant_c`.

```sql
SELECT citus_schema_distribute('tenant_a');
SELECT citus_schema_distribute('tenant_b');
SELECT citus_schema_distribute('tenant_c');
```

For more examples, see the [Citus microservices tutorial](tutorial-micro-services.md).

### citus_schema_undistribute

Converts an existing distributed schema back into a regular schema. This process moves the tables and data from the current node back to the coordinator node in the cluster.

#### Arguments

**schemaname**: Name of the schema that you want to undistribute.

#### Return value

None

#### Example

Converts three different distributed schemas back into regular schemas.

```sql
SELECT citus_schema_undistribute('tenant_a');
SELECT citus_schema_undistribute('tenant_b');
SELECT citus_schema_undistribute('tenant_c');
```

For more examples, see the [Citus microservices tutorial](tutorial-micro-services.md).

### citus_schema_move

Use this function to move a distributed schema from one node to another.

You can move a distributed schema in two ways: blocking or nonblocking. The blocking approach pauses all modifications to the tables in the schema during the move. The second way, which avoids blocking writes, relies on PostgreSQL 10 logical replication.

#### Arguments

**schema_id**: Oid of the distributed schema to move. If you provide the name of the schema as a string literal, the name is automatically cast to the oid.

**target_node_name**: The domain name system (DNS) name of the node on which to move the distributed schema ("target" node).

**target_node_port**: The port on the target worker node on which the database server listens.

**shard_transfer_mode**: (Optional) Specify the replication method, whether to use PostgreSQL logical replication or a cross-worker COPY command. Possible values are:

- *auto*: Require replica identity if logical replication is possible, otherwise use legacy behavior. The default value.
- *force_logical*: Use logical replication even if all the tables in the schema don't have a replica identity. Any concurrent update or delete statements to the tables in the schema fail during replication.
- *block_writes*: Use COPY (blocking writes) for the tables in the schema lacking primary key or replica identity.

#### Return value

None

#### Example

```sql
SELECT citus_schema_move('schema-name', 'to_host', 5432);
```

### create_distributed_table

Use the `create_distributed_table()` function to define a distributed table and create its shards if it's a hash-distributed table. Provide a table name, the distribution column, and an optional distribution method. The function inserts metadata to mark the table as distributed. If you don't specify a distribution method, the function defaults to hash distribution. If the table is hash-distributed, the function creates worker shards based on the shard count configuration value. If the table contains any rows, the function automatically distributes them to worker nodes, but doesn't delete them from the table on the coordinator. Leftover local data in distributed tables is inaccessible to Citus queries, and can cause irrelevant constraint violations on the coordinator. To remove the leftover data, use the `truncate_local_data_after_distributing_table` function.

#### Arguments

**table_name**: Name of the table that you want to distribute.

**distribution_column**: The column on which to distribute the table.

**colocate_with**: (Optional) Include the current table in the colocation group of another table. By default, tables are colocated when they're distributed by columns of the same type with the same shard count. If you want to break this colocation later, you can use `update_distributed_table_colocation`. Possible values for `colocate_with` are *default*, *none* to start a new colocation group, or the name of another table to colocate with that table. (See `colocation_groups`.)

The *default* value of `colocate_with` does implicit colocation. The *default* value can be a great thing when tables are related or are joined. However, when two tables are unrelated but happen to use the same data type for their distribution columns, accidentally colocating them can decrease performance during shard rebalancing. The table shards are moved together unnecessarily in a "cascade." If you want to break this implicit colocation, you can use `update_distributed_table_colocation`.

If a new distributed table isn't related to other tables, specify `colocate_with => 'none'`.

**shard_count**: (Optional) The number of shards to create for the new distributed table. When you specify `shard_count`, you can't specify a value for `colocate_with` other than *none*. To change the shard count of an existing table or colocation group, use the `alter_distributed_table` function.

Possible values for `shard_count` are between *1* and *64000*. For guidance on choosing the optimal value, see `prod_shard_count`.

#### Return value

None

#### Example

This example informs the database that the *github_events* table should be distributed by hash on the *repo_id* column.

```sql
SELECT create_distributed_table('github_events', 'repo_id');

-- alternatively, to be more explicit:
SELECT create_distributed_table('github_events', 'repo_id',
                                colocate_with => 'github_repo');
```

For more examples, see `ddl`.

### truncate_local_data_after_distributing_table

Truncate all local rows after distributing a table, and prevent constraints from failing due to outdated local records. The truncation cascades to tables that have a foreign key to the designated table. If the referring tables aren't themselves distributed, then truncation is forbidden until they are, to protect referential integrity:

`ERROR: cannot truncate a table referenced in a foreign key constraint by a local table`

Truncating local coordinator node table data is safe for distributed tables because their rows, if they have any, are copied to worker nodes during distribution.

#### Arguments

**table_name**: Name of the distributed table whose local counterpart on the coordinator node you want to truncate.

#### Return value

None

#### Example

```sql
-- requires that argument is a distributed table
SELECT truncate_local_data_after_distributing_table('public.github_events');
```

### undistribute_table

The `undistribute_table()` function reverses the action of `create_distributed_table` or `create_reference_table`. When you undistribute a table, Citus moves all data from the shards back into a local table on the coordinator node (assuming the data fits), and then deletes the shards.

Citus doesn't undistribute tables that have foreign keys or are referenced by foreign keys, unless you set the `cascade_via_foreign_keys` argument to *true*. If this argument is *false* or omitted, you must manually drop the foreign key constraints before undistributing.

#### Arguments

**table_name**: Name of the distributed or reference table to undistribute.

**cascade_via_foreign_keys**: (Optional) When this argument is *true*, `undistribute_table` also undistributes all tables that are related to `table_name` through foreign keys. Use caution with this parameter, because it can potentially affect many tables.

#### Return value

None

#### Example

This example distributes a `github_events` table and then undistributes it.

```sql
-- first distribute the table
SELECT create_distributed_table('github_events', 'repo_id');

-- undo that and make it local again
SELECT undistribute_table('github_events');
```

### alter_distributed_table

Use the `alter_distributed_table()` function to change the distribution column, shard count, or colocation properties of a distributed table.

#### Arguments

**table_name**: Name of the distributed table that you want to alter.

**distribution_column**: (Optional) Name of the new distribution column.

**shard_count**: (Optional) The new shard count.

**colocate_with**: (Optional) The table that you want to colocate the current distributed table with. Possible values are *default*, *none* to start a new colocation group, or the name of another table with which to colocate.

**cascade_to_colocated**: (Optional) When you set this argument to *true*, `shard_count`, and `colocate_with` changes are also applied to all of the tables that were previously colocated with the table, and the colocation is preserved. If you set it to *false*, the current colocation of this table is broken.

#### Return value

None

#### Example

```sql
-- change distribution column
SELECT alter_distributed_table('github_events', distribution_column:='event_id');

-- change shard count of all tables in colocation group
SELECT alter_distributed_table('github_events', shard_count:=6, cascade_to_colocated:=true);

-- change colocation
SELECT alter_distributed_table('github_events', colocate_with:='another_table');
```

### alter_table_set_access_method

Use the `alter_table_set_access_method()` function to change the access method of a table (for example, heap or columnar).

#### Arguments

- **table_name**: Name of the table whose access method you want to change.

- **access_method**: Name of the new access method.

#### Return value

None

#### Example

```sql
SELECT alter_table_set_access_method('github_events', 'columnar');
```

### remove_local_tables_from_metadata

Use the `remove_local_tables_from_metadata()` function to remove local tables from Citus metadata when you no longer need them. For more information, see `enable_local_ref_fkeys`.

Usually, you include a local table in Citus metadata for a reason. For example, foreign keys exist between the table and a reference table. However, if you disable `enable_local_reference_foreign_keys`, Citus stops managing metadata in that situation. Unnecessary metadata can persist until you manually clean it.

#### Arguments

None

#### Return value

None

### create_reference_table

Use the `create_reference_table()` function to define a small reference or dimension table. Provide a table name to create a distributed table with one shard that's replicated to every worker node.

#### Arguments

**table_name**: Name of the small dimension or reference table to distribute.

#### Return value

None

#### Example

This example informs the database that the nation table should be defined as a reference table.

```sql
SELECT create_reference_table('nation');
```

### citus_add_local_table_to_metadata

Use the `citus_add_local_table_to_metadata()` function to add a local PostgreSQL table into Citus metadata. A major use case for this function is to make local tables on the coordinator accessible from any node in the cluster. This structure is mostly useful when running queries from other nodes. The data associated with the local table stays on the coordinator, and only its schema and metadata are sent to the workers.

Adding local tables to the metadata comes at a slight cost. When you add the table, Citus must track it in the `partition_table`. Local tables that you add to metadata inherit the same limitations as reference tables (see `ddl` and `citus_sql_reference`).

If you `undistribute_table`, Citus automatically removes the resulting local tables from metadata, which eliminates such limitations on those tables.

#### Arguments

**table_name**: Name of the table on the coordinator to add to Citus metadata.

**cascade_via_foreign_keys**: (Optional) When you set this argument to *true*, `citus_add_local_table_to_metadata` adds other tables that are in a foreign key relationship with given table into metadata automatically. Use caution with this parameter, because it can potentially affect many tables.

#### Return value

None

#### Example

This example informs the database that the nation table should be defined as a coordinator-local table, accessible from any node:

```sql
SELECT citus_add_local_table_to_metadata('nation');
```

### update_distributed_table_colocation

Use the `update_distributed_table_colocation()` function to update the colocation of a distributed table. You can also use this function to break the colocation of a distributed table. Citus implicitly colocates two tables if the distribution column is the same type. This colocation is useful if the tables are related and perform some joins. If tables A and B are colocated, and table A gets rebalanced, table B is also rebalanced. If table B doesn't have a replica identity, the rebalance fails. Therefore, this function is useful for breaking the implicit colocation in that case.

This function doesn't move any data around physically.

#### Arguments

**table_name**: Name of the table for which colocation is updated.

**colocate_with**: The table to which the table should be colocated.

To break the colocation of a table, specify `colocate_with => 'none'`.

#### Return value

None

#### Example

This example shows that colocation of `table A` is updated as colocation of `table B`.

```sql
SELECT update_distributed_table_colocation('A', colocate_with => 'B');
```

Assume that `table A` and `table B` are implicitly colocated. To break the colocation:

```sql
SELECT update_distributed_table_colocation('A', colocate_with => 'none');
```

Now, assume that `table A`, `table B`, `table C`, and `table D` are colocated and you want to colocate `table A` and `table B` together, and `table C` and `table D` together:

```sql
SELECT update_distributed_table_colocation('C', colocate_with => 'none');
SELECT update_distributed_table_colocation('D', colocate_with => 'C');
```

If you have a hash distributed table named `none` and you want to update its colocation, run:

```sql
SELECT update_distributed_table_colocation('"none"', colocate_with => 'some_other_hash_distributed_table');
```

### create_distributed_function

Propagate a function from the coordinator node to workers, and mark it for distributed execution. When you call a distributed function on the coordinator, Citus uses the value of `distribution_arg_name` to pick a worker node to run the function. When you execute this function on workers, it increases parallelism and can bring the code closer to data in shards for lower latency.

The PostgreSQL search path doesn't propagate from the coordinator to workers during distributed function execution, so distributed function code should fully qualify the names of database objects. Also, notices that the functions emit aren't displayed to the user.

#### Arguments

**function_name**: Name of the function to distribute. The name must include the function's parameter types in parentheses, because multiple functions can have the same name in PostgreSQL. For example, `'foo(int)'` is different from `'foo(int, text)'`.

**distribution_arg_name**: (Optional) The argument name by which to distribute. For convenience (or if the function arguments don't have names), a positional placeholder is allowed, such as `'$1'`. If you don't specify this parameter, the function named by `function_name` is created on the workers.

**colocate_with**: (Optional) When the distributed function reads or writes to a distributed table (or more generally `colocation_groups`), be sure to name that table using the `colocate_with` parameter. This setting ensures that each invocation of the function runs on the worker node containing relevant shards.

#### Return value

None

#### Example

```sql
-- an example function which updates a hypothetical
-- event_responses table which itself is distributed by event_id
CREATE OR REPLACE FUNCTION
  register_for_event(p_event_id int, p_user_id int)
RETURNS void LANGUAGE plpgsql AS $fn$
BEGIN
  INSERT INTO event_responses VALUES ($1, $2, 'yes')
  ON CONFLICT (event_id, user_id)
  DO UPDATE SET response = EXCLUDED.response;
END;
$fn$;

-- distribute the function to workers, using the p_event_id argument
-- to determine which shard each invocation affects, and explicitly
-- colocating with event_responses which the function updates
SELECT create_distributed_function(
  'register_for_event(int, int)', 'p_event_id',
  colocate_with := 'event_responses'
);
```

### alter_columnar_table_set

Use the `alter_columnar_table_set()` function to change settings on a `columnar table <columnar>`. If you call this function on a noncolumnar table, you get an error. All arguments except the table name are optional.

To view current options for all columnar tables, consult this table:

```sql
SELECT * FROM columnar.options;
```

Override the default values for columnar settings for newly created tables by using these global user configurations (GUCa):

- columnar.compression
- columnar.compression_level
- columnar.stripe_row_count
- columnar.chunk_row_count

#### Arguments

**table_name**: Name of the columnar table.

**chunk_row_count**: (Optional) The maximum number of rows per chunk for newly inserted data. The operation doesn't change existing chunks of data, which might have more rows than this maximum value. The default value is *10000*.

**stripe_row_count**: (Optional) The maximum number of rows per stripe for newly inserted data. The operation doesn't change existing stripes of data, which might have more rows than this maximum value. The default value is *150000*.

**compression**: (Optional) Valid settings are *none*, *pglz*, *zstd*, *lz4*, and *z4hc*. The compression type for newly inserted data. The operation doesn't recompress or decompress existing data. The suggested default value is *zstd* (if support is compiled in).

**compression_level**: (Optional) Valid settings are from *1* through *19*. If the compression method doesn't support the level you choose, the closest level is selected instead.

#### Return value

None

#### Example

```sql
SELECT alter_columnar_table_set(
  'my_columnar_table',
  compression => 'none',
  stripe_row_count => 10000);
```

### create_time_partitions

The `create_time_partitions()` function creates partitions of a given interval to cover a given range of time.

#### Arguments

**table_name**: The table of type `regclass` for which to create new partitions. The table must be partitioned on one column, of type `date`, `timestamp`, or `timestamptz`.

**partition_interval**: An interval of time, such as `'2 hours'` or `'1 month'`, to use when setting ranges on new partitions.

**end_at**: (`timestamptz`) Create partitions up to this time. The last partition contains the point `end_at`, and no later partitions are created.

**start_from**: (`timestamptz`, optional) Pick the first partition so that it contains the point `start_from`. The default value is `now()`.

#### Return value

*True* if the function needs to create new partitions. *False* if all partitions already exist.

#### Example

```sql
-- create a year's worth of monthly partitions
-- in table foo, starting from the current time

SELECT create_time_partitions(
  table_name         := 'foo',
  partition_interval := '1 month',
  end_at             := now() + '12 months'
);
```

### drop_old_time_partitions

The `drop_old_time_partitions()` function removes all partitions whose intervals fall before a given timestamp. In addition to using this function, you might consider using `alter_old_partitions_set_access_method` to compress the old partitions by using columnar storage.

#### Arguments

**table_name**: The table of type `regclass` to remove partitions from. The table must be partitioned on one column, of type `date`, `timestamp`, or `timestamptz`.

**older_than**: (`timestamptz`) Drop partitions whose upper range is less than or equal to `older_than`.

#### Return value

None

#### Example

```sql
-- drop partitions that are over a year old

CALL drop_old_time_partitions('foo', now() - interval '12 months');
```

### alter_old_partitions_set_access_method

In a `timeseries` use case, partition tables by time, and compress old partitions into read-only columnar storage.

#### Arguments

**parent_table_name**: The table of type `regclass` for which to change partitions. The table must be partitioned on one column, of type `date`, `timestamp`, or `timestamptz`.

**older_than**: (`timestamptz`) Change partitions whose upper range is less than or equal to `older_than`.

**new_access_method**: (`name`) Either *heap* for row-based storage, or *columnar* for columnar storage.

#### Return value

None

#### Example

```sql
CALL alter_old_partitions_set_access_method(
  'foo', now() - interval '6 months',
  'columnar'
);
```

## Metadata / Configuration Information

### citus_add_node

> [!NOTE]  
> You need database superuser access to run this function.

The `citus_add_node()` function registers a new node in the cluster by adding it to the Citus metadata table `pg_dist_node`. It also copies reference tables to the new node.

If you run `citus_add_node` on a single-node cluster, make sure to run `set_coordinator_host` first.

#### Arguments

**nodename**: DNS name or IP address of the new node to add.

**nodeport**: The port on the worker node that PostgreSQL listens on.

**groupid**: A group of one primary server and its secondary servers, relevant only for streaming replication. Set `groupid` to a value greater than zero, since zero is reserved for the coordinator node. The default is *-1*.

**noderole**: Specifies whether the node is *primary* or *secondary*. Default *primary*.

- **nodecluster**: The cluster name. Default *default*.

#### Return value

The `nodeid` column from the newly inserted row in `pg_dist_node`.

#### Example

```sql
select * from citus_add_node('new-node', 12345);
 citus_add_node
-----------------
               7
(1 row)
```

### citus_update_node

> [!NOTE]  
> You need database superuser access to run this function.

Use the `citus_update_node()` function to change the hostname and port for a node registered in the Citus metadata table `pg_dist_node`.

#### Arguments

- **node_id**: An ID from the `pg_dist_node` table.

- **node_name**: Updated DNS name or IP address for the node.

- **node_port**: The worker node port on which PostgreSQL is listening.

#### Return value

None

#### Example

```sql
select * from citus_update_node(123, 'new-address', 5432);
```

### citus_set_node_property

The `citus_set_node_property()` function changes properties in the Citus metadata table `pg_dist_node`. Currently, it can change only the `shouldhaveshards` property.

#### Arguments

**node_name**: DNS name or IP address for the node.

- **node_port**: The worker node port on which PostgreSQL is listening.

**property**: The column to change in `pg_dist_node`, currently only `shouldhaveshards` is supported.

**value**: The new value for the column.

#### Return value

None

#### Example

```sql
SELECT * FROM citus_set_node_property('localhost', 5433, 'shouldhaveshards', false);
```

### citus_add_inactive_node

> [!NOTE]  
> You need database superuser access to run this function.

The `citus_add_inactive_node` function works like `citus_add_node`. It registers a new node in `pg_dist_node`. However, this function marks the new node as inactive, so it doesn't hold any shards. Also, it doesn't copy reference tables to the new node.

#### Arguments

**nodename**: DNS name or IP address of the new node to add.

**nodeport**: The port on the worker node that PostgreSQL listens on.

**groupid**: A group of one primary server and zero or more secondary servers, relevant only for streaming replication. Default *-1*.

**noderole**: Specifies whether the node is *primary* or *secondary*. Default *primary*.

- **nodecluster**: The cluster name. Default *default*.

#### Return value

The `nodeid` column from the newly inserted row in `pg_dist_node`.

#### Example

```sql
select * from citus_add_inactive_node('new-node', 12345);
 citus_add_inactive_node
--------------------------
                        7
(1 row)
```

### citus_activate_node

> [!NOTE]  
> You need database superuser access to run this function.

Use the `citus_activate_node` function to mark a node as active in the Citus metadata table `pg_dist_node` and copy reference tables to the node. This function is useful for nodes you add by using `citus_add_inactive_node`.

#### Arguments

**nodename**: DNS name or IP address of the new node to add.

**nodeport**: The port on the worker node that PostgreSQL listens on.

#### Return value

The `nodeid` column from the newly inserted row in `pg_dist_node`.

#### Example

```sql
select * from citus_activate_node('new-node', 12345);
 citus_activate_node
----------------------
                    7
(1 row)
```

### citus_disable_node

> [!NOTE]  
> You need database superuser access to run this function.

The `citus_disable_node` function works opposite to `citus_activate_node`. It marks a node as inactive in the Citus metadata table `pg_dist_node`, so the node is temporarily removed from the cluster. The function also deletes all reference table placements from the disabled node. To reactivate the node, run `citus_activate_node` again.

#### Arguments

**nodename**: DNS name or IP address of the node to disable.

**nodeport**: The port on the worker node that PostgreSQL listens on.

#### Return value

None

#### Example

```sql
select * from citus_disable_node('new-node', 12345);
```

### citus_add_secondary_node

> [!NOTE]  
> You need database superuser access to run this function.

Use the `citus_add_secondary_node()` function to register a new secondary node in the cluster for an existing primary node. This function updates the Citus metadata table `pg_dist_node`.

#### Arguments

**nodename**: DNS name or IP address of the new node to add.

**nodeport**: The port on the worker node that PostgreSQL listens on.

- **primaryname**: DNS name or IP address of the primary node for this secondary node.

- **primaryport**: The port on the primary node that PostgreSQL listens on.

- **nodecluster**: The cluster name. Default *default*.

#### Return value

The `nodeid` column for the secondary node, inserted row in `pg_dist_node`.

#### Example

```sql
select * from citus_add_secondary_node('new-node', 12345, 'primary-node', 12345);
 citus_add_secondary_node
---------------------------
                         7
(1 row)
```

### citus_remove_node

> [!NOTE]  
> You need database superuser access to run this function.

Use the `citus_remove_node()` function to remove a node from the `pg_dist_node` metadata table. This function returns an error if the node has existing shard placements. Before using this function, move the shards off the node.

#### Arguments

**nodename**: DNS name of the node to remove.

**nodeport**: The port on the worker node that PostgreSQL listens on.

#### Return value

None

#### Example

```sql
select citus_remove_node('new-node', 12345);
 citus_remove_node
--------------------

(1 row)
```

### citus_get_active_worker_nodes

The `citus_get_active_worker_nodes()` function returns a list of active worker host names and port numbers.

#### Arguments

None

#### Return value

List of tuples where each tuple contains the following information:

- **node_name**: DNS name of the worker node.

- **node_port**: Port on the worker node on which the database server is listening.

#### Example

```sql
SELECT * from citus_get_active_worker_nodes();
```

```output
 node_name | node_port
-----------+-----------
 localhost |      9700
 localhost |      9702
 localhost |      9701

(3 rows)
```

### citus_backend_gpid

The `citus_backend_gpid()` function returns the global process identifier (GPID) for the PostgreSQL backend that serves the current session. A GPID encodes both a node in the Citus cluster and the operating system process ID of PostgreSQL on that node.

Citus extends the PostgreSQL [server signaling functions](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL-TABLE) `pg_cancel_backend()` and `pg_terminate_backend()` so that they accept GPIDs. In Citus, calling these functions on one node can affect a backend running on another node.

#### Arguments

None

#### Return value

An integer GPID, of the form `(NodeId * 10,000,000,000) + ProcessId`.

#### Example

```sql
SELECT citus_backend_gpid();
```

```output
  citus_backend_gpid
--------------------
  10000002055
```

### citus_check_cluster_node_health

Checks connectivity between all nodes. If there are N nodes, this function checks all N<sup>2</sup> connections between them.

#### Arguments

None

#### Return value

List of tuples where each tuple contains the following information:

- **from_nodename**: DNS name of the source worker node.

- **from_nodeport**: Port on the source worker node where the database server listens.

- **to_nodename**: DNS name of the destination worker node.

- **to_nodeport**: Port on the destination worker node where the database server listens.

- **result**: Indicates whether a connection is established.

#### Example

```sql
SELECT * FROM citus_check_cluster_node_health();
```

```output
 from_nodename │ from_nodeport │ to_nodename │ to_nodeport │ result
---------------+---------------+-------------+-------------+--------
 localhost     |          1400 | localhost   |        1400 | t
 localhost     |          1400 | localhost   |        1401 | t
 localhost     |          1400 | localhost   |        1402 | t
 localhost     |          1401 | localhost   |        1400 | t
 localhost     |          1401 | localhost   |        1401 | t
 localhost     |          1401 | localhost   |        1402 | t
 localhost     |          1402 | localhost   |        1400 | t
 localhost     |          1402 | localhost   |        1401 | t
 localhost     |          1402 | localhost   |        1402 | t

 (9 rows)
```

### citus_set_coordinator_host

Use this function when you add worker nodes to a Citus cluster that you originally created as a single-node cluster. When the coordinator registers a new worker, it adds a coordinator hostname from the value of `local_hostname`, which is *localhost* by default. The worker tries to connect to *localhost* to talk to the coordinator, which is obviously wrong.

Call `citus_set_coordinator_host` before calling `citus_add_node` in a single-node cluster.

#### Arguments

**host**: DNS name of the coordinator node.

**port**: (Optional) The port on which the coordinator listens for PostgreSQL connections. Defaults to `current_setting('port')`.

**node_role**: (Optional) Defaults to *primary*.

**node_cluster**: (Optional) Defaults to *default*.

#### Return value

None

#### Example

```sql
-- assuming we're in a single-node cluster

-- first establish how workers should reach us
SELECT citus_set_coordinator_host('coord.example.com', 5432);

-- then add a worker
SELECT * FROM citus_add_node('worker1.example.com', 5432);
```

### get_shard_id_for_distribution_column

Citus assigns every row of a distributed table to a shard based on the value of the row's distribution column and the table's method of distribution. In most cases, the database administrator doesn't need to know the precise mapping. However, it can be useful to determine a row's shard, either for manual database maintenance tasks or just to satisfy curiosity. The `get_shard_id_for_distribution_column` function provides this info for hash-distributed tables and reference tables.

#### Arguments

- **table_name**: The distributed table.

- **distribution_value**: The value of the distribution column.

#### Return value

The ID of the shard that Citus associates with the distribution column value for the given table.

#### Example

```sql
SELECT get_shard_id_for_distribution_column('my_table', 4);
```

```output
 get_shard_id_for_distribution_column
--------------------------------------
                               540007
(1 row)
```

### column_to_column_name

Translates the `partkey` column of `pg_dist_partition` into a textual column name. This name is useful to determine the distribution column of a distributed table.

For a more detailed discussion, see `finding_dist_col`.

#### Arguments

- **table_name**: The distributed table.

- **column_var_text**: The value of `partkey` in the `pg_dist_partition` table.

#### Return value

The name of the distribution column for **table_name**.

#### Example

```sql
-- get distribution column name for products table

SELECT column_to_column_name(logicalrelid, partkey) AS dist_col_name
  FROM pg_dist_partition
 WHERE logicalrelid='products'::regclass;
```

Output:

```output
┌───────────────┐
│ dist_col_name │
├───────────────┤
│ company_id    │
└───────────────┘
```

### citus_relation_size

Gets the disk space used by all the shards of the specified distributed table. This value includes the size of the *main fork*, but excludes the visibility map and free space map for the shards.

#### Arguments

**logicalrelid**: the name of a distributed table.

#### Return value

Size in bytes as a bigint.

#### Example

```sql
SELECT pg_size_pretty(citus_relation_size('github_events'));
```

```output
    pg_size_pretty
    --------------
    23 MB
```

### citus_table_size

Gets the disk space used by all the shards of the specified distributed table, excluding indexes but including TOAST, free space map, and visibility map.

#### Arguments

**logicalrelid**: The name of a distributed table.

#### Return value

Size in bytes as a bigint.

#### Example

```sql
SELECT pg_size_pretty(citus_table_size('github_events'));
```

```output
    pg_size_pretty
    --------------
    37 MB
```

### citus_total_relation_size

Gets the total disk space used by all the shards of the specified distributed table, including all indexes and TOAST data.

#### Arguments

**logicalrelid**: The name of a distributed table.

#### Return value

Size in bytes as a bigint.

#### Example

```sql
SELECT pg_size_pretty(citus_total_relation_size('github_events'));
```

```output
    pg_size_pretty
    --------------
    73 MB
```

### citus_stat_statements_reset

Removes all rows from `citus_stat_statements`. This function works independently from `pg_stat_statements_reset()`. To reset all stats, call both functions.

#### Arguments

None

#### Return value

None

### citus_stat_counters_reset

Resets the Citus statistics counters to zero for a specific database. The counters are visible in the [`citus_stat_counters` view](api-metadata.md#citus-stat-counters-view) and via the [`citus_stat_counters()`](#citus_stat_counters) function. Requires superuser privileges.

#### Arguments

**database_id**: (Optional) OID of the database whose statistics you want to reset. Use `NULL` or `0` (or omit the argument) to reset stats for the current database.

#### Return value

None

#### Examples

```sql
-- reset stats for the current database
SELECT citus_stat_counters_reset();

-- explicitly pass 0 for current database
SELECT citus_stat_counters_reset(0);

-- reset stats for a specific database by OID; no-op if it doesn't exist
SELECT citus_stat_counters_reset(12345);
```

> [!CAUTION]  
> Due to concurrent access, there's a small chance not all active backends reset their counters immediately. The `stats_reset` column in `citus_stat_counters` shows the last reset timestamp.

### citus_stat_counters

Returns Citus statistics counters for one or more databases. This function provides the same metrics as the [`citus_stat_counters` view](api-metadata.md#citus-stat-counters-view), but can also return stats for dropped databases (the view filters those out).

#### Arguments

**database_id**: (Optional) OID of the database to query. Use `NULL` or `0` (or omit) to return stats for all databases.

#### Return value

A set of rows with these columns:

| Column | Type | Description |
| --- | --- | --- |
| `database_id` | oid | Database OID. |
| `connection_establishment_succeeded` | bigint | Successful inter-node connections. |
| `connection_establishment_failed` | bigint | Failed connection attempts. |
| `connection_reused` | bigint | Cached connections reused. |
| `query_execution_single_shard` | bigint | Queries/subplans that accessed a single shard. |
| `query_execution_multi_shard` | bigint | Queries/subplans that accessed multiple shards. |
| `stats_reset` | timestamptz | Last reset timestamp (NULL if never reset). |

#### Examples

```sql
-- get stats for all databases
SELECT * FROM citus_stat_counters();

-- get stats for a specific database
SELECT * FROM citus_stat_counters(12345);

-- get stats for the current database only
SELECT *
FROM citus_stat_counters(
  (SELECT oid FROM pg_database WHERE datname = current_database())
);
```

> [!NOTE]  
> - Statistics are collected only when `citus.enable_stat_counters` is enabled (default is false). Existing stats remain queryable even if you disable it.  
> - Stats are stored in memory and reset on server restart.  
> - Providing a database OID that has never been used returns an empty result set.

## Cluster Management And Repair Functions

### citus_move_shard_placement

This function moves a shard and its colocated shards from one node to another node. Typically, you use this function indirectly during shard rebalancing instead of calling it directly.

You can move the data in two ways: blocking or nonblocking. The blocking approach pauses all modifications to the shard during the move. The second way, which avoids blocking shard writes, relies on PostgreSQL 10 logical replication.

After a successful move operation, the function deletes the source node shards. If the move fails at any point, the function throws an error and leaves the source and target nodes unchanged.

#### Arguments

**shard_id**: ID of the shard to move.

**source_node_name**: DNS name of the node with the healthy shard placement (the "source" node).

**source_node_port**: The port on the source worker node where the database server listens.

**target_node_name**: DNS name of the node with the invalid shard placement (the "target" node).

**target_node_port**: The port on the target worker node on which the database server listens.

**shard_transfer_mode**: (Optional) Specify the replication method, whether to use PostgreSQL logical replication or a cross-worker COPY command. Possible values are:

- *auto*: Require replica identity if logical replication is possible, otherwise use legacy behavior. For example, for shard repair *PostgreSQL 9.6*, which is the default value.
- *force_logical*: Use logical replication even if the table doesn't have a replica identity. Any concurrent update or delete statements to the table fail during replication.
- *block_writes*: Use COPY (blocking writes) for tables lacking primary key or replica identity.

> [!NOTE]  
> Citus Community edition supports all shard transfer modes starting in version 11.0!

#### Return value

None

#### Example

```sql
SELECT citus_move_shard_placement(12345, 'from_host', 5432, 'to_host', 5432);
```

### citus_rebalance_start

The `citus_rebalance_start()` function moves table shards to more evenly distribute them among the workers. It starts a background job to do the rebalancing, and returns immediately.

The rebalancing process first calculates the list of moves it needs to make to ensure that the cluster is balanced within the given threshold. Then, it moves shard placements one by one from the source node to the destination node and updates the corresponding shard metadata to reflect the move.

When determining whether shards are *evenly distributed*, every shard is assigned a cost. The default rebalancing strategy is *by_disk_size*, which derives cost from shard sizes. The *by_shard_count* strategy assigns cost 1 per shard and is appropriate under these circumstances:

1. The shards are roughly the same size.
1. The shards get roughly the same amount of traffic.
1. All worker nodes are the same size and type.
1. The shards aren't pinned to particular workers.

If any of these assumptions don't hold, then rebalancing *by_shard_count* can result in a bad plan.

You can always customize the strategy by using the `rebalance_strategy` parameter.

To see and verify the actions to perform, call `get_rebalance_table_shards_plan` before running `citus_rebalance_start`.

> [!NOTE]  
> Citus 13.2 improves rebalance performance:
>
> - Enable `parallel_transfer_colocated_shards` to move colocated shards in parallel while preserving dependency order.
> - Enable `parallel_transfer_reference_tables` to copy reference table shards in separate background tasks.
> - Increase `max_worker_processes`, `citus.max_background_task_executor`, and `citus.max_background_task_executors_per_node` to use parallelism.
> - Locking now uses per-shard advisory locks and relaxed colocation locks (RowExclusiveLock), eliminating the global replication lock.

#### Arguments

**threshold**: (Optional) A float number between 0.0 and 1.0 that indicates the maximum difference ratio of node utilization from average utilization. For example, specifying *0.1* causes the shard rebalancer to attempt to balance all nodes to hold the same number of shards ±10%. Specifically, the shard rebalancer tries to converge utilization of all worker nodes to the (1 - threshold) \* average_utilization ... (1 + threshold) \* average_utilization range.

**drain_only**: (Optional) When *true*, move shards off worker nodes that have `shouldhaveshards` set to *false* in `pg_dist_node`; move no other shards.

**rebalance_strategy**: (Optional) The name of a strategy in [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table). If you omit this argument, the function chooses the default strategy, as indicated in the table.

**parallel_transfer_colocated_shards**: (Optional, default *false*) When *true*, colocated shards can be moved in parallel while preserving dependency order.

**parallel_transfer_reference_tables**: (Optional, default *false*) When *true*, each reference table shard is copied in its own background task.

#### Return value

None

#### Example

The following example attempts to rebalance shards within the default threshold.

```sql
SELECT citus_rebalance_start();
NOTICE:  Scheduling...
NOTICE:  Scheduled as job 1337.
DETAIL:  Rebalance scheduled as background job 1337.
HINT:  To monitor progress, run: SELECT details FROM citus_rebalance_status();
```

### citus_rebalance_status

The `citus_rebalance_start` function returns immediately, while the rebalance continues as a background job. Use the `citus_rebalance_status()` function to monitor the progress of this rebalance.

#### Example

To get general information about the rebalance, select all columns from the status. This command shows the basic state of the job:

```sql
SELECT * FROM citus_rebalance_status();
```

```output
 job_id | state   | job_type  |           description           |          started_at           |          finished_at          | details
--------+---------+-----------+---------------------------------+-------------------------------+-------------------------------+-----------
      4 | running | rebalance | Rebalance colocation group 1    | 2022-08-09 21:57:27.833055+02 | 2022-08-09 21:57:27.833055+02 | { ... }
```

Rebalancer specifics live in the `details` column, in JSON format:

```sql
SELECT details FROM citus_rebalance_status();
```

``` json
{
    "phase": "copy",
    "phase_index": 1,
    "phase_count": 3,
    "last_change":"2022-08-09 21:57:27",
    "colocations": {
        "1": {
            "shard_moves": 30,
            "shard_moved": 29,
            "last_move":"2022-08-09 21:57:27"
        },
        "1337": {
            "shard_moves": 130,
            "shard_moved": 0
        }
    }
}
```

### citus_rebalance_stop

This function cancels a rebalance in progress, if any.

#### Arguments

None

#### Return value

None

### citus_rebalance_wait

This function blocks until a running rebalance is complete. If no rebalance is in progress when you call `citus_rebalance_wait()`, the function returns immediately.

This function can be useful for scripts or benchmarking.

#### Arguments

None

#### Return value

None

### rebalance_table_shards

> [!WARNING]  
> The `rebalance_table_shards()` function is deprecated. As of Citus v11.2, use `citus_rebalance_start` instead.

### get_rebalance_table_shards_plan

Returns the planned shard movements for `citus_rebalance_start` without performing them. While it's unlikely, `get_rebalance_table_shards_plan` can return a slightly different plan than a `citus_rebalance_start` call with the same arguments. This difference can occur because the two functions don't execute at the same time. Facts about the cluster, such as disk space, might differ between the calls.

#### Arguments

A superset of the arguments for `citus_rebalance_start`: `relation`, `threshold`, `max_shard_moves`, `excluded_shard_list`, and `drain_only`. See the documentation of that function for the arguments' meaning.

#### Return value

Tuples with these columns:

- **table_name**: The table whose shards move.
- **shardid**: The shard in question.
- **shard_size**: Size in bytes.
- **sourcename**: Hostname of the source node.
- **sourceport**: Port of the source node.
- **targetname**: Hostname of the destination node.
- **targetport**: Port of the destination node.

### get_rebalance_progress

> [!NOTE]  
> Citus v11.2 introduces the `citus_rebalance_status` function, whose output is easier to understand than the output of `get_rebalance_progress`.

When you start a shard rebalance, the `get_rebalance_progress()` function shows the progress for every shard involved. It tracks the moves that `citus_rebalance_start()` plans and executes.

#### Arguments

None

#### Return value

Tuples with these columns:

- **sessionid**: PostgreSQL PID of the rebalance monitor.
- **table_name**: The table whose shards are moving.
- **shardid**: The shard in question.
- **shard_size**: Size of the shard in bytes.
- **sourcename**: Hostname of the source node.
- **sourceport**: Port of the source node.
- **targetname**: Hostname of the destination node.
- **targetport**: Port of the destination node.
- **progress**: 0 = waiting to be moved; 1 = moving; 2 = complete.
- **source_shard_size**: Size of the shard on the source node in bytes.
- **target_shard_size**: Size of the shard on the target node in bytes.

#### Example

```sql
SELECT * FROM get_rebalance_progress();
```

```output
┌───────────┬────────────┬─────────┬────────────┬───────────────┬────────────┬───────────────┬────────────┬──────────┬───────────────────┬───────────────────┐
│ sessionid │ table_name │ shardid │ shard_size │ sourcename    │ sourceport │ targetname    │ targetport │ progress │ source_shard_size │ target_shard_size │
├───────────┼────────────┼─────────┼────────────┼───────────────┼────────────┼───────────────┼────────────┼──────────┼───────────────────┼───────────────────┤
│      7083 │ foo        │ 102008  │    1204224 │ n1.foobar.com │       5432 │ n4.foobar.com │       5432 │        0 │           1204224 │                 0 │
│      7083 │ foo        │ 102009  │    1802240 │ n1.foobar.com │       5432 │ n4.foobar.com │       5432 │        0 │           1802240 │                 0 │
│      7083 │ foo        │ 102018  │     614400 │ n2.foobar.com │       5432 │ n4.foobar.com │       5432 │        1 │            614400 │            354400 │
│      7083 │ foo        │ 102019  │       8192 │ n3.foobar.com │       5432 │ n4.foobar.com │       5432 │        2 │                 0 │              8192 │
└───────────┴────────────┴─────────┴────────────┴───────────────┴────────────┴───────────────┴────────────┴──────────┴───────────────────┴───────────────────┘
```

### citus_add_rebalance_strategy

Adds a row to the [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table) table.

#### Arguments

For more information about these arguments, see the corresponding column values in [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table).

- **name**: Identifier for the new strategy.

- **shard_cost_function**: Identifies the function used to determine the "cost" of each shard.

- **node_capacity_function**: Identifies the function to measure node capacity.

- **shard_allowed_on_node_function**: Identifies the function that determines which shards can be placed on which nodes.

- **default_threshold**: A floating point threshold that tunes how precisely the cumulative shard cost should be balanced between nodes.

- **minimum_threshold**: (Optional) A safeguard column that holds the minimum value allowed for the threshold argument of `citus_rebalance_start()`. Its default value is *0*.

#### Return value

None

### citus_set_default_rebalance_strategy

Updates the [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table) table. Sets the strategy named by its argument as the default strategy for rebalancing shards.

#### Arguments

**name**: The name of the strategy in [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table).

#### Return value

None

#### Example

```sql
SELECT citus_set_default_rebalance_strategy('by_disk_size');
```

### citus_remote_connection_stats

The `citus_remote_connection_stats()` function returns the number of active connections to each remote node.

#### Arguments

None

#### Example

```sql
SELECT * from citus_remote_connection_stats();
```

```output
    hostname    | port | database_name | connection_count_to_node
----------------+------+---------------+--------------------------
 citus_worker_1 | 5432 | postgres      |                        3
(1 row)
```

### citus_drain_node

The `citus_drain_node()` function moves shards off the designated node and onto other nodes that have `shouldhaveshards` set to *true* in `pg_dist_node`. Call this function before removing a node from the cluster, such as when turning off the node's physical server.

#### Arguments

**nodename**: The hostname of the node to drain.

**nodeport**: The port number of the node to drain.

**shard_transfer_mode**: (Optional) Specify the replication method, whether to use PostgreSQL logical replication or a cross-worker COPY command. Possible values are:

- *auto*: Require replica identity if logical replication is possible, otherwise use legacy behavior. For example, for shard repair, *PostgreSQL 9.6*, which is the default value.
- *force_logical*: Use logical replication even if the table doesn't have a replica identity. Any concurrent update or delete statements to the table fail during replication.
- *block_writes*: Use COPY (blocking writes) for tables lacking primary key or replica identity.

> [!NOTE]  
> Citus Community edition supports all shard transfer modes starting in version 11.0!

**rebalance_strategy**: (Optional) the name of a strategy in [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table). If you omit this argument, the function chooses the default strategy, as indicated in the table.

#### Return value

None

#### Example

Here are the typical steps to remove a single node (for example, '10.0.0.1' on a standard PostgreSQL port):

1. Drain the node.

   ```sql
   SELECT * from citus_drain_node('10.0.0.1', 5432);
   ```

1. Wait until the command finishes.

1. Remove the node.

When draining multiple nodes, use `citus_rebalance_start` instead. By using this function, Citus can plan ahead and move shards the minimum number of times.

1. Run this code for each node that you want to remove:

   ```sql
   SELECT * FROM citus_set_node_property(node_hostname, node_port, 'shouldhaveshards', false);
   ```

1. Drain them all at once by using `citus_rebalance_start`:

   ```sql
   SELECT * FROM citus_rebalance_start(drain_only := true);
   ```

1. Wait until the draining rebalance finishes.

1. Remove the nodes.

As of Citus 13.2, the following functions enable snapshot-based node addition by registering a clone (asynchronous streaming replica) and promoting it to a worker with minimal data movement.

### citus_add_clone_node

Use this function to register a streaming replica as a clone of an existing worker node.

#### Arguments

**clone_host**: Hostname of the clone node.

**clone_port**: Port of the clone node.

**primary_host**: Hostname of the source worker node.

**primary_port**: Port of the source worker node.

#### Return value

Node ID of the registered clone.

#### Example

```sql
SELECT citus_add_clone_node('clone-node', 5432, 'primary-node', 5432);
```

### citus_add_clone_node_with_nodeid

Use this function to register a clone by source worker node ID.

#### Arguments

**clone_host**: Hostname of the clone node.

**clone_port**: Port of the clone node.

**primary_node_id**: Node ID of the source worker node.

#### Return value

Node ID of the registered clone.

#### Example

```sql
SELECT citus_add_clone_node_with_nodeid('clone-node', 5432, 7);
```

### citus_remove_clone_node

Use this function to remove a clone node from the cluster.

#### Arguments

**clone_host**: Hostname of the clone node.

**clone_port**: Port of the clone node.

#### Return value

None

#### Example

```sql
SELECT citus_remove_clone_node('clone-node', 5432);
```

### citus_remove_clone_node_with_nodeid

Use this function to remove a clone node by node ID.

#### Arguments

**clone_node_id**: Node ID of the clone to remove.

#### Return value

None

#### Example

```sql
SELECT citus_remove_clone_node_with_nodeid(9);
```

### get_snapshot_based_node_split_plan

Use this function to preview the shard distribution plan between a source worker and its clone before promotion.

#### Arguments

**primary_host**: Hostname of the source worker node.

**primary_port**: Port of the source worker node.

**clone_host**: Hostname of the clone node.

**clone_port**: Port of the clone node.

**rebalance_strategy**: (Optional) Strategy name in [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table).

#### Return value

A set of rows showing the planned shard distribution (for example, table_name, shardid, shard_size, sourcename, sourceport, targetname, targetport).

#### Example

```sql
SELECT * FROM get_snapshot_based_node_split_plan('primary-node', 5432, 'clone-node', 5432);
```

### citus_promote_clone_and_rebalance

Use this function to promote a clone to a worker node and rebalance shards between the source worker and the promoted clone.

> [!IMPORTANT]  
> - Rebalancing affects only the source worker and its clone; other workers are unaffected.
> - The clone must be an asynchronous streaming replica actively replicating from the source.
> - The function briefly blocks writes for consistency and serializes placement changes.

#### Arguments

**clone_node_id**: Node ID of the clone to promote.

**rebalance_strategy**: (Optional, default *by_disk_size*) Strategy name in [pg_dist_rebalance_strategy](api-metadata.md#rebalancer-strategy-table).

**catchup_timeout_seconds**: (Optional, default *300*) Timeout for replica catch-up.

#### Return value

Boolean success status.

#### Example

```sql
SELECT citus_promote_clone_and_rebalance(9);
```

### isolate_tenant_to_new_shard

> [!NOTE]  
> Starting with version 11.0, Citus Community edition includes the `isolate_tenant_to_new_shard` function.

This function creates a new shard to hold rows with a specific single value in the distribution column. It's especially handy for the multitenant Citus use case, where you can place a large tenant alone on its own shard and ultimately its own physical node.

For a more in-depth discussion, see `tenant_isolation`.

#### Arguments

- **table_name**: The name of the table to get a new shard.

- **tenant_id**: The value of the distribution column, which you assign to the new shard.

- **cascade_option**: (Optional) When set to *CASCADE*, also isolates a shard from all tables in the current table's `colocation_groups`.

#### Return value

- **shard_id**: The function returns the unique ID assigned to the newly created shard.

#### Examples

Create a new shard to hold the lineitems for tenant *135*:

```sql
SELECT isolate_tenant_to_new_shard('lineitem', 135);
```

```output
┌─────────────────────────────┐
│ isolate_tenant_to_new_shard │
├─────────────────────────────┤
│                      102240 │
└─────────────────────────────┘
```

### citus_create_restore_point

This function temporarily blocks any writes to the cluster and creates a named restore point on all nodes. This function is similar to [pg_create_restore_point](https://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADMIN-BACKUP), but it applies to all nodes and makes sure the restore point is consistent across them.

Use this function for point-in-time recovery and cluster forking.

:::moniker range=">=citus-14"

> [!TIP]
> **MX-safe restore points.** In Citus 14, `citus_create_restore_point()` is safe for MX (multi-writer) clusters. The function now:
>
> - Opens connections to all nodes (metadata and non-metadata)
> - Begins coordinated transactions on remote nodes
> - Locks `pg_dist_transaction` with `ExclusiveLock` on **all metadata nodes** (blocks 2PC commit decisions)
> - Locks `pg_dist_node` and `pg_dist_partition` on the coordinator (blocks topology/DDL changes)
> - Creates restore points on all nodes in parallel
> - Releases locks when connections are closed (implicit ROLLBACK)
>
> Because the commit decision in Citus 2PC is recorded in `pg_dist_transaction`, holding `ExclusiveLock` provides a clean cut-over point without draining transactions. Prepared transactions that already logged commit records will complete; others will block.
>
> **Backward compatibility:** The function signature and return type are unchanged. Coordinator-only mode behavior is unchanged.

:::moniker-end

#### Arguments

**name**: The name of the restore point to create.

#### Return value

**coordinator_lsn**: Log sequence number of the restore point in the coordinator node write-ahead logging (WAL).

#### Examples

```sql
select citus_create_restore_point('foo');
```

```output
┌────────────────────────────┐
│ citus_create_restore_point │
├────────────────────────────┤
│ 0/1EA2808                  │
└────────────────────────────┘
```

## Related content

- [Metadata tables and views](api-metadata.md)
- [Configuration parameters](api-guc.md)
- [What is Azure Cosmos DB for PostgreSQL?](what-is-citus.md)
