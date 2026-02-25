---
title: Manage Your Citus Cluster
description: Learn how to manage a Citus cluster, add or remove nodes, scale and rebalance a cluster, and handle node failures.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
ai-usage: ai-assisted
---

# Manage your Citus cluster

In this article, you learn how to add or remove nodes from your Citus cluster and how to handle node failures.

> [!NOTE]  
> To make moving shards across nodes or re-replicating shards on failed nodes easier, Citus Community edition 11.0+ supports fully online shard rebalancing. When relevant, the following sections briefly discuss the functions provided by the shard rebalancer. For more information about these functions, their arguments, and usage, see the `cluster_management_functions` reference section.

## Choosing cluster size

This section explores configuration settings for running a cluster in production.

### Shard count

Choosing the shard count for each distributed table is a balance between the flexibility of having more shards and the overhead for query planning and execution across them. If you decide to change the shard count of a table after distributing it, use the `alter_distributed_table` function.

#### Multitenant SaaS use case

The optimal choice varies depending on your access patterns for the data. For instance, in the `mt_blurb` use case, choose between **32 - 128 shards**. For smaller workloads (less than 100 GB), start with 32 shards. For larger workloads, choose 64 or 128. This choice gives you the leeway to scale from 32 to 128 worker machines.

#### Real-time analytics use case

In the `rt_blurb` use case, shard count should relate to the total number of cores on the workers. To ensure maximum parallelism, create enough shards on each node so that there's at least one shard per CPU core. Typically, create a high number of initial shards, such as **2x or 4x the number of current CPU cores**. This setup allows for future scaling if you add more workers and CPU cores.

However, keep in mind that for each query, Citus opens one database connection per shard, and these connections are limited. Be careful to keep the shard count small enough that distributed queries don't often wait for a connection. Put another way, the connections needed, `(max concurrent queries * shard count)`, shouldn't exceed the total connections possible in the system, `(number of workers * max_connections per worker)`.

## Initial hardware size

You can easily change the size of a cluster in terms of the number of nodes and their hardware capacity. (Scaling on our `cloud_topic` is especially easy.) However, you still need to choose an initial size for a new cluster. Here are some tips for a reasonable initial cluster size.

### Multitenant SaaS use case

If you're migrating to Citus from an existing single-node database instance, choose a cluster where the total number of worker cores and RAM matches your original instance. In these scenarios, you can see two to three times better performance because sharding improves resource utilization, which lets you use smaller indexes.

The coordinator node needs less memory than the worker nodes, so you can choose a compute-optimized machine for running the coordinator. The number of cores you need depends on your existing workload, such as write and read throughput.

### Real-time analytics use case

**Total cores:** When your working data fits in RAM, you can expect a linear performance improvement on Citus that's proportional to the number of worker cores. To determine the right number of cores for your needs, consider the current latency for queries in your single-node database and the required latency in Citus. Divide current latency by desired latency, and round the result.

**Worker RAM:** The best case is providing enough memory so that most the working set fits in memory. The type of queries your application uses affects memory requirements. You can run `EXPLAIN ANALYZE` on a query to determine how much memory it requires.

## Scaling the cluster

Citus's logical sharding-based architecture lets you scale out your cluster without any downtime. This section describes how you can add more nodes to your Citus cluster to improve query performance and scalability.

### Add a worker

Citus stores all the data for distributed tables on the worker nodes. If you want to scale out your cluster by adding more computing power, add a worker node.

To add a new node to the cluster, first add the DNS name or IP address of that node and the port (on which PostgreSQL is running) in the `pg_dist_node` catalog table. Use the `citus_add_node` UDF to add the new node. Example:

```sql
SELECT * from citus_add_node('node-name', 5432);
```

The new node is available for shards of new distributed tables. Existing shards stay where they are unless you redistribute them, so adding a new worker might not help performance without further steps.

> [!NOTE]  
> If your cluster has large reference tables, they can slow down the addition of a node. In this case, consider the `replicate_reference_tables_on_activate` GUC.
>
> Also, new nodes synchronize Citus' metadata upon creation. By default, the sync happens inside a single transaction for consistency. However, in a large cluster with large amounts of metadata, the transaction can run out of memory and fail. If you encounter this situation, you can choose a nontransactional metadata sync mode by using the `metadata_sync_mode` GUC.

#### Snapshot-based node addition (Citus 13.2)

Citus 13.2 introduces a faster scale-out path using snapshot-based node addition. Instead of moving data over the network to a fresh worker, you promote a streaming replica (clone) of an existing worker and then split shards between the source and the clone, avoiding full data copy.

**Workflow (high level):**

1. Create a physical replica of a worker (for example, `pg_basebackup`) and configure it as a streaming replica of the source worker.
1. Register the clone and optionally preview the plan.
1. Promote the clone to a worker and rebalance shards between the source and clone.

**Benefits:**

- Eliminates full data copy during scale-out
- Rebalance scope limited to the source worker and its clone
- Reduced write blocking and faster node addition for large datasets

For UDF details and examples, see the snapshot-based node addition functions in the utility reference: [citus_add_clone_node](api-udf.md#citus_add_clone_node), [citus_add_clone_node_with_nodeid](api-udf.md#citus_add_clone_node_with_nodeid), [get_snapshot_based_node_split_plan](api-udf.md#get_snapshot_based_node_split_plan), and [citus_promote_clone_and_rebalance](api-udf.md#citus_promote_clone_and_rebalance).

### Rebalance shards without downtime

> [!NOTE]  
> Starting in version 11.0, Citus Community edition supports nonblocking reads *and* writes during rebalancing.

If you want to move existing shards to a newly added worker, use the `citus_rebalance_start` function. This function distributes shards evenly among the workers.

> [!NOTE]  
> Citus 13.2 improves rebalancing throughput by enabling parallel moves within colocation groups and parallel reference table copying, removes the global replication lock, and uses per-shard advisory locks with relaxed colocation locks. Enable the `parallel_transfer_colocated_shards` and `parallel_transfer_reference_tables` parameters (default *false*) when calling `citus_rebalance_start`, and tune `max_worker_processes`, `citus.max_background_task_executor`, and `citus.max_background_task_executors_per_node` to use parallelism.

You can configure the function to rebalance shards according to different strategies to best match your database workload. See the function reference to learn which strategy to choose. Here's an example of rebalancing shards by using the default strategy:

```sql
SELECT citus_rebalance_start();
```

Many products, like multitenant SaaS applications, can't tolerate downtime. On our managed service, rebalancing honors this requirement on PostgreSQL 10 or above. This feature means reads and writes from the application can continue with minimal interruption while data is being moved.

#### Parallel rebalancing

This operation carries out multiple shard moves in a sequential order by default. In some cases, you might prefer to rebalance faster at the expense of using more resources, such as network bandwidth. In those situations, you can configure a rebalance operation to perform many shard moves in parallel.

The `citus.max_background_task_executors_per_node` GUC allows tasks such as shard rebalancing to operate in parallel. Increase it from its default value (1) as desired to boost parallelism. For higher concurrency, also increase `max_worker_processes` and `citus.max_background_task_executor` (global pool). To parallelize moves within a colocation group and reference table copies, pass `parallel_transfer_colocated_shards := true` and/or `parallel_transfer_reference_tables := true` to `citus_rebalance_start`.

```sql
ALTER SYSTEM SET citus.max_background_task_executors_per_node = 2;
ALTER SYSTEM SET citus.max_background_task_executor = 8;
ALTER SYSTEM SET max_worker_processes = 32;
SELECT pg_reload_conf();

SELECT citus_rebalance_start(parallel_transfer_colocated_shards := true,
                             parallel_transfer_reference_tables := true);
```

**What are the typical use cases?**

- Scaling out faster when adding new nodes to the cluster
- Rebalancing the cluster faster to even out the utilization of nodes

**Corner cases and gotchas**

`citus.max_background_task_executors_per_node` value limits the number of parallel task executors in general. By default, shards in the same colocation group move sequentially; enable `parallel_transfer_colocated_shards` to parallelize within a colocation group. Reference table copies can parallelize when `parallel_transfer_reference_tables` is enabled.

#### How it works

Citus's shard rebalancing uses PostgreSQL logical replication to move data from the old shard (called the "publisher" in replication terms) to the new shard (the "subscriber"). Logical replication allows application reads and writes to continue uninterrupted while copying shard data. Citus puts a brief write-lock on a shard only during the time it takes to update metadata to promote the subscriber shard as active.

As the PostgreSQL docs [explain](https://www.postgresql.org/docs/current/static/logical-replication-publication.html), the source needs a *replica identity* configured:

A published table must configure a "replica identity" in order to replicate UPDATE and DELETE operations, so that appropriate rows to update or delete can be identified on the subscriber side. By default, this identity is the primary key, if there is one. Another unique index (with certain additional requirements) can also be set to be the replica identity.

In other words, if your distributed table has a primary key defined, then it's ready for shard rebalancing with no extra work. However, if it doesn't have a primary key or an explicitly defined replica identity, then attempting to rebalance it causes an error. Here's how to fix it.

**First, does the table have a unique index?**

If the table to be replicated already has a unique index that includes the distribution column, then choose that index as a replica identity:

```sql
-- supposing my_table has unique index my_table_idx
-- which includes distribution column

ALTER TABLE my_table REPLICA IDENTITY
  USING INDEX my_table_idx;
```

> [!NOTE]  
> While `REPLICA IDENTITY USING INDEX` is fine, we recommend **against** adding `REPLICA IDENTITY FULL` to a table. This setting results in each update or delete doing a full-table-scan on the subscriber side to find the tuple with those rows. In our testing, we found this setting results in worse performance than even solution four in the following section.

**Otherwise, can you add a primary key?**

Add a primary key to the table. If the desired key is the distribution column, then it's easy - just add the constraint. Otherwise, a primary key with a nondistribution column must be composite and contain the distribution column too.

### Adding a coordinator

The Citus coordinator only stores metadata about the table shards and doesn't store any data. This architecture pushes all of the computation to the workers, and the coordinator performs only the final aggregations on the results from the workers. Therefore, it's unlikely that the coordinator becomes a bottleneck for read performance. Also, you can easily boost the coordinator's performance by shifting to a more powerful machine.

However, in some write-heavy use cases where the coordinator becomes a performance bottleneck, you can add another node as described in the following section and load balance the client connections.

```sql
SELECT * FROM citus_add_node(second_coordinator_hostname, second_coordinator_port);
SELECT * FROM citus_set_node_property(second_coordinator_hostname, second_coordinator_port, 'shouldhaveshards', false);
```

> [!NOTE]  
> You can run DDL queries only through the first coordinator node. See [database and role DDL propagation](reference-ddl.md).

## Dealing with node failures

In this subsection, you discuss how to deal with node failures without incurring any downtime on your Citus cluster.

### Worker node failures

Citus uses PostgreSQL streaming replication, which allows it to tolerate worker-node failures. This option replicates entire worker nodes by continuously streaming their WAL records to a standby. You can configure streaming replication on-premises yourself by consulting the [PostgreSQL replication documentation](https://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION) or use our `cloud_topic`, which is preconfigured for replication and high availability.

### Coordinator node failures

The Citus coordinator maintains metadata tables to track all of the cluster nodes and the locations of the database shards on those nodes. The metadata tables are small (typically a few MBs in size) and don't change often. This architecture means that you can replicate and quickly restore these tables if the node ever experiences a failure. You have several options for dealing with coordinator failures.

1. **Use PostgreSQL streaming replication:** You can use PostgreSQL's streaming replication feature to create a hot standby of the coordinator. Then, if the primary coordinator node fails, the standby can be promoted to the primary automatically to serve queries to your cluster. For details on setting up this feature, see the [PostgreSQL wiki](https://wiki.postgresql.org/wiki/Streaming_Replication).
1. **Use backup tools:** Since the metadata tables are small, you can use EBS volumes or [PostgreSQL backup tools](https://www.postgresql.org/docs/current/static/backup.html) to back up the metadata. Then, you can easily copy over that metadata to new nodes to resume operation.

## Tenant isolation

### Row-based sharding

> [!NOTE]  
> Starting in version 11.0, Citus Community edition includes tenant isolation functionality!

Citus places table rows into worker shards based on the hashed value of the rows' distribution column. Multiple distribution column values often fall into the same shard. In the Citus multitenant use case, this behavior means that tenants often share shards.

However, sharing shards can cause resource contention when tenants differ drastically in size. This situation is common for systems with a large number of tenants. As the number of tenants increases, the size of tenant data tends to follow a Zipfian distribution. This distribution means there are a few large tenants and many smaller ones. To improve resource allocation and make guarantees of tenant QoS, move large tenants to dedicated nodes.

Citus provides the tools to isolate a tenant on a specific node. This process happens in two phases: 1) isolating the tenant's data to a new dedicated shard, then 2) moving the shard to the desired node. To understand the process, you need to know precisely how rows of data are assigned to shards.

Every shard is marked in Citus metadata with the range of hashed values it contains (more info in the reference for `pg_dist_shard <pg_dist_shard>`). The Citus UDF `isolate_tenant_to_new_shard(table_name, tenant_id)` moves a tenant into a dedicated shard in three steps:

1. Creates a new shard for `table_name` that (a) includes rows whose distribution column has value `tenant_id` and (b) excludes all other rows.
1. Moves the relevant rows from their current shard to the new shard.
1. Splits the old shard into two with hash ranges that abut the excision above and below.

Furthermore, the UDF takes a `CASCADE` option that isolates the tenant rows of not just `table_name` but of all tables colocated with it. Here's an example:

```sql
-- This query creates an isolated shard for the given tenant_id and
-- returns the new shard id.

-- General form:

SELECT isolate_tenant_to_new_shard('table_name', tenant_id);

-- Specific example:

SELECT isolate_tenant_to_new_shard('lineitem', 135);

-- If the given table has co-located tables, the query above errors out and
-- advises to use the CASCADE option

SELECT isolate_tenant_to_new_shard('lineitem', 135, 'CASCADE');
```

Output:

```output
┌─────────────────────────────┐
│ isolate_tenant_to_new_shard │
├─────────────────────────────┤
│                      102240 │
└─────────────────────────────┘
```

The new shards are created on the same node as the shards from which the tenant was removed. For true hardware isolation, you can move them to a separate node in the Citus cluster. As mentioned, the `isolate_tenant_to_new_shard` function returns the newly created shard ID. You can use this ID to move the shard:

Now that you have the shard identifier, you can use `move_shard`.

### Schema-based sharding

In schema-based sharding, you don't need to isolate a tenant because each tenant already resides in its own schema. To perform a move, you need to get a shard identifier for a schema.

First, find the colocation ID of the schema you want to move.

```sql
select * from citus_schemas;
```

```output
schema_name  | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             1 | 0 bytes     | user_service
time_service |             2 | 0 bytes     | time_service
ping_service |             3 | 0 bytes     | ping_service
a            |             4 | 128 kB      | citus
b            |             5 | 32 kB       | citus
with_data    |            11 | 6408 kB     | citus
(6 rows)
```

Next, query `citus_shards`. Use colocation identifier 11 from the preceding output:

```sql
select * from citus_shards where colocation_id = 11;
```

```output
table_name    | shardid |       shard_name       | citus_table_type | colocation_id | nodename  | nodeport | shard_size
-----------------+---------+------------------------+------------------+---------------+-----------+----------+------------
with_data.test  |  102180 | with_data.test_102180  | schema           |            11 | localhost |     9702 |     647168
with_data.test2 |  102183 | with_data.test2_102183 | schema           |            11 | localhost |     9702 |    5914624
(2 rows)
```

You can pick any <span class="title-ref">sharded</span> from the output. When you make the move, it also propagates to all colocated tables. In schema-based sharding, this action moves all tables within the schema.

Now that you have the shard identifier, you can use `move_shard`.

### Make the move

When you know the shard identifier that denotes the tenant, you can execute the move:

```sql
-- find the node currently holding the new shard
SELECT nodename, nodeport
  FROM citus_shards
 WHERE shardid = 102240;

-- list the available worker nodes that could hold the shard
SELECT * FROM master_get_active_worker_nodes();

-- move the shard to your choice of worker
-- (it will also move any shards created with the CASCADE option)
SELECT citus_move_shard_placement(
  102240,
  'source_host', source_port,
  'dest_host', dest_port);
```

`citus_move_shard_placement` also moves any shards that colocate with the specified shard, so it preserves their colocation.

## Viewing query statistics

> [!NOTE]  
> Starting in version 11.0, Citus Community edition includes the `citus_stat_statements` view.

When you administer a Citus cluster, it's useful to know what queries users run, which nodes are involved, and which execution method Citus uses for each query. Citus records query statistics in a metadata view called `citus_stat_statements`, named analogously to PostgreSQL's [pg_stat_statements](https://www.postgresql.org/docs/current/static/pgstatstatements.html). Whereas `pg_stat_statements` stores info about query duration and I/O, `citus_stat_statements` stores info about Citus execution methods and shard partition keys (when applicable).

Citus requires the `pg_stat_statements` extension to be installed to track query statistics. On our `cloud_topic` this extension is preactivated, but on a self-hosted PostgreSQL instance you must load the extension in `postgresql.conf` via `shared_preload_libraries`, then create the extension in SQL:

```sql
CREATE EXTENSION pg_stat_statements;
```

Let's see how this works. Assume you have a table called `foo` that is hash-distributed by its `id` column.

```sql
-- create and populate distributed table
create table foo ( id int );
select create_distributed_table('foo', 'id');

insert into foo select generate_series(1,100);
```

You run two more queries, and `citus_stat_statements` shows how Citus chooses to execute them.

```sql
-- counting all rows executes on all nodes, and sums
-- the results on the coordinator
SELECT count(*) FROM foo;

-- specifying a row by the distribution column routes
-- execution to an individual node
SELECT * FROM foo WHERE id = 42;
```

To find how these queries were executed, ask the stats table:

```sql
SELECT * FROM citus_stat_statements;
```

Results:

```output
-[ RECORD 1 ]-+----------------------------------------------
queryid       | -6844578505338488014
userid        | 10
dbid          | 13340
query         | SELECT count(*) FROM foo;
executor      | adaptive
partition_key |
    calls         | 1
    -[ RECORD 2 ]-+----------------------------------------------
    queryid       | 185453597994293667
    userid        | 10
    dbid          | 13340
    query         | insert into foo select generate_series($1,$2)
    executor      | insert-select
    partition_key |
    calls         | 1
    -[ RECORD 3 ]-+----------------------------------------------
    queryid       | 1301170733886649828
    userid        | 10
    dbid          | 13340
    query         | SELECT * FROM foo WHERE id = $1
    executor      | adaptive
    partition_key | 42
    calls         | 1
```

You can see that Citus uses the adaptive executor most commonly to run queries. This executor fragments the query into constituent queries to run on relevant nodes, and combines the results on the coordinator node. In the second query (filtering by the distribution column `id = $1`), Citus determined that it needed the data from just one node. Lastly, you can see that the `insert into foo select...` statement ran with the insert-select executor, which provides flexibility to run this kind of queries.

### citus_stats view (Citus 13.2)

For cluster-wide column statistics, see the views reference: [citus_stats](api-metadata.md#citus_stats-view).

### Tenant-level statistics

So far, the information in this view doesn't give us anything we couldn't already learn by running the `EXPLAIN` command for a given query. However, in addition to getting information about individual queries, the `citus_stat_statements` view allows us to answer questions such as "what percentage of queries in the cluster are scoped to a single tenant?"

```sql
SELECT sum(calls),
       partition_key IS NOT NULL AS single_tenant
FROM citus_stat_statements
GROUP BY 2;
```

```output
    .
     sum | single_tenant
    -----+---------------
       2 | f
       1 | t
```

In a multitenant database, for instance, you expect most queries to be single tenant. Seeing too many multitenant queries might indicate that queries don't have the proper filters to match a tenant, and are using unnecessary resources.

To investigate which tenants are most active, use the `citus_stat_tenants` view.

### Statistics expiration

The `pg_stat_statements` view limits the number of statements it tracks and the duration of its records. Because `citus_stat_statements` tracks a strict subset of the queries in `pg_stat_statements`, choosing equal limits for the two views causes a mismatch in their data retention. Mismatched records can cause joins between the views to behave unpredictably.

Three ways help synchronize the views, and you can use all three methods together.

1. Have the maintenance daemon periodically sync the Citus and PostgreSQL stats. The GUC `citus.stat_statements_purge_interval` sets time in seconds for the sync. A value of 0 disables periodic syncs.
1. Adjust the number of entries in `citus_stat_statements`. The `citus.stat_statements_max` GUC removes old entries when new ones cross the threshold. The default value is 50K, and the highest allowable value is 10M. Each entry costs about 140 bytes in shared memory so set the value wisely.
1. Increase `pg_stat_statements.max`. Its default value is 5,000, and you can increase it to 10K, 20K, or even 50K without much overhead. This option is most beneficial when there's more local (that is, coordinator) query workload.

> [!NOTE]  
> Restart the PostgreSQL service after changing `pg_stat_statements.max` or `citus.stat_statements_max`. A call to [pg_reload_conf()](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL) makes changing `citus.stat_statements_purge_interval` take effect.

## Resource conservation

### Limiting long-running queries

Long-running queries can hold locks, queue up WAL, or consume a lot of system resources. In a production environment, prevent them from running too long. To cancel queries that run too long, set the [statement_timeout](https://www.postgresql.org/docs/current/static/runtime-config-client.html#GUC-STATEMENT-TIMEOUT) parameter on the coordinator and workers.

```sql
-- limit queries to five minutes
ALTER DATABASE citus
  SET statement_timeout TO 300000;
SELECT run_command_on_workers($cmd$
  ALTER DATABASE citus
    SET statement_timeout TO 300000;
$cmd$);
```

Specify the timeout in milliseconds.

To customize the timeout for each query, use `SET LOCAL` in a transaction:

``` postgres
```sql

BEGIN;
-- this limit applies to just the current transaction
SET LOCAL statement_timeout TO 300000;

-- ...
COMMIT;

```
## Security

### Connection management

> [!NOTE]
> Since Citus version 8.1.0 (released 2018-12-17), the traffic between the different nodes in the cluster is encrypted for new installations. This encryption uses TLS with self-signed certificates. This encryption **doesn't protect against man-in-the-middle attacks.** It only protects against passive eavesdropping on the network.
>
> Clusters originally created with a Citus version before 8.1.0 don't have any network encryption enabled between nodes, even if you upgrade later. To set up self-signed TLS on this type of installation, follow the steps in the [official PostgreSQL documentation](https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-CERTIFICATE-CREATION) together with the Citus-specific settings described here, such as changing `citus.node_conninfo` to `sslmode=require`. You should apply this setup on both the coordinator and worker nodes.

When Citus nodes communicate with one another, they consult a table with connection credentials. This approach gives the database administrator flexibility to adjust parameters for security and efficiency.

To set nonsensitive libpq connection parameters for all node connections, update the `citus.node_conninfo` GUC:
```sql

-- key=value pairs separated by spaces.
-- For example, ssl options:

ALTER SYSTEM SET citus.node_conninfo =
  'sslrootcert=/path/to/citus-ca.crt sslcrl=/path/to/citus-ca.crl sslmode=verify-full';

```
The GUC accepts an allowed list of parameters. For details, see the `node_conninfo <node_conninfo>` reference. As of Citus 8.1, the default value for `node_conninfo` is `sslmode=require`, which prevents unencrypted communication between nodes. If you originally created your cluster before Citus 8.1, the value is `sslmode=prefer`. After setting up self-signed certificates on all nodes, change this setting to `sslmode=require`.

After changing this setting, reload the PostgreSQL configuration. Even though the changed setting might be visible in all sessions, Citus only consults the setting when new connections are established. When a reload signal is received, Citus marks all existing connections to be closed, which causes a reconnect after running transactions are completed.
```sql

SELECT pg_reload_conf();

```
> [!WARNING]
> Citus versions before 9.2.4 require a restart for existing connections to be closed.
>
> For these versions, a reload of the configuration doesn't trigger connection ending and subsequent reconnecting. Instead, restart the server to enforce all connections to use the new settings.
```sql

-- only superusers can access this table

-- add a password for user jdoe
INSERT INTO pg_dist_authinfo
  (nodeid, rolename, authinfo)
VALUES
  (123, 'jdoe', 'password=abc123');

```
After this `INSERT`, any query needing to connect to node 123 as the user jdoe uses the supplied password. The documentation for `pg_dist_authinfo <pg_dist_authinfo>` has more info.
```sql

-- update user jdoe to use certificate authentication
UPDATE pg_dist_authinfo
SET authinfo = 'sslcert=/path/to/user.crt sslkey=/path/to/user.key'
WHERE nodeid = 123 AND rolename = 'jdoe';

```
This change switches the user from using a password to using a certificate and keyfile while connecting to node 123. Make sure the user certificate is signed by a certificate that the worker you are connecting to trusts and that the authentication settings on the worker allow for certificate-based authentication. For full documentation on how to use client certificates, see [the PostgreSQL libpq documentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-CLIENTCERT).

Changing `pg_dist_authinfo` doesn't force any existing connection to reconnect.

### Setup Certificate Authority signed certificates

This section assumes you have a trusted Certificate Authority that can issue server certificates to you for all nodes in your cluster. Work with the security department in your organization to prevent key material from being handled incorrectly. This guide covers only Citus specific configuration that you need to apply, not best practices for PKI management.

For all nodes in the cluster, you need to get a valid certificate signed by the *same Certificate Authority*. The following **machine specific** files are available on every machine:

- `/path/to/server.key`: Server Private Key
- `/path/to/server.crt`: Server Certificate or Certificate Chain for Server Key, signed by trusted Certificate Authority.

Next to these machine specific files, you need these cluster or CA wide files:

- `/path/to/ca.crt`: Certificate of the Certificate Authority
- `/path/to/ca.crl`: Certificate Revocation List of the Certificate Authority

> [!NOTE]
> The Certificate Revocation List is likely to change over time. Work with your security department to set up a mechanism to update the revocation list on to all nodes in the cluster in a timely manner. A reload of every node in the cluster is required after the revocation list has been updated.

Once all files are in place on the nodes, configure the following settings in the PostgreSQL configuration file:
``` ini

# the following settings allow the PostgreSQL server to enable ssl, and

# configure the server to present the certificate to clients when

# connecting over tls/ssl

ssl = on
ssl_key_file = '/path/to/server.key'
ssl_cert_file = '/path/to/server.crt'

# this will tell citus to verify the certificate of the server it is connecting to

citus.node_conninfo = 'sslmode=verify-full sslrootcert=/path/to/ca.crt sslcrl=/path/to/ca.crl'

```
After you change these settings, either restart the database or reload the configuration to apply these changes. A restart is required if you use a Citus version earlier than 9.2.4. Also, you might need to adjust `local_hostname` for proper functioning with `sslmode=verify-full`.

Depending on the policy of the Certificate Authority used, you might need or want to change `sslmode=verify-full` in `citus.node_conninfo` to `sslmode=verify-ca`. For the difference between the two settings, consult [the official PostgreSQL documentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS).

Lastly, to prevent any user from connecting via an unencrypted connection, make changes to `pg_hba.conf`. Many PostgreSQL installations have entries allowing `host` connections, which allow SSL/TLS connections and plain TCP connections. By replacing all `host` entries with `hostssl` entries, only encrypted connections are allowed to authenticate to PostgreSQL. For full documentation on these settings, take a look at [the pg_hba.conf file](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) documentation on the official PostgreSQL documentation.

> [!NOTE]
> When a trusted Certificate Authority isn't available, you can create your own via a self-signed root certificate. This process is nontrivial and you should seek guidance from your security team.

To verify the connections from the coordinator to the workers are encrypted, run the following query. It shows the SSL/TLS version used to encrypt the connection that the coordinator uses to talk to the worker:
```sql

SELECT run_command_on_workers($$
  SELECT version FROM pg_stat_ssl WHERE pid = pg_backend_pid()
$$);

```
```output

    ┌────────────────────────────┐
    │   run_command_on_workers   │
    ├────────────────────────────┤
    │ (localhost,9701,t,TLSv1.2) │
    │ (localhost,9702,t,TLSv1.2) │
    └────────────────────────────┘
    (2 rows)

```
### Increasing worker security

For your convenience, the multi-node installation instructions direct you to set up the `pg_hba.conf` on the workers with its [authentication method](https://www.postgresql.org/docs/current/static/auth-methods.html) set to "trust" for local network connections. However, you might want more security.

To require that all connections supply a hashed password, update the PostgreSQL `pg_hba.conf` on every worker node with something like this:
```bash

# Require password access and a ssl/tls connection to nodes in the local

# network. The following ranges correspond to 24, 20, and 16-bit blocks

# in Private IPv4 address spaces.

hostssl    all             all             10.0.0.0/8              md5

# Require passwords and ssl/tls connections when the host connects to

# itself as well.

hostssl    all             all             127.0.0.1/32            md5
hostssl    all             all             ::1/128                 md5

```
The coordinator node needs to know roles' passwords to communicate with the workers. Our `cloud_topic` keeps track of that kind of information for you. However, in Citus Community Edition, you have to maintain the authentication information in a [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html) file. Edit .pgpass in the postgres user's home directory, with a line for each combination of worker address and role:

*hostname:port:database:username:password*

Sometimes workers need to connect to one another, such as during `repartition joins <repartition_joins>`. Thus each worker node requires a copy of the .pgpass file as well.

### Row-level security

> [!NOTE]
> Starting in version 11.0, Citus Community edition supports row-level security for distributed tables.

PostgreSQL [row-level security](https://www.postgresql.org/docs/current/static/ddl-rowsecurity.html) policies restrict, on a per-user basis, which rows normal queries can return or data modification commands can insert, update, or delete. This feature is especially useful in a multitenant Citus cluster because it allows individual tenants to have full SQL access to the database while hiding each tenant's information from other tenants.

You can implement the separation of tenant data by using a naming convention for database roles that ties into table row-level security policies. Assign each tenant a database role in a numbered sequence: `tenant_1`, `tenant_2`, and so on. Tenants connect to Citus by using these separate roles. Row-level security policies compare the role name to values in the `tenant_id` distribution column to decide whether to allow access.

The following example shows how to apply this approach on a simplified events table distributed by `tenant_id`. First, create the roles `tenant_1` and `tenant_2`. Then run the following commands as an administrator:
```sql

``` sql
CREATE TABLE events(
  tenant_id int,
  id int,
  type text
);

SELECT create_distributed_table('events','tenant_id');

INSERT INTO events VALUES (1,1,'foo'), (2,2,'bar');

-- assumes that roles tenant_1 and tenant_2 exist
GRANT select, update, insert, delete
  ON events TO tenant_1, tenant_2;
```

As it stands, anyone with select permissions for this table can see both rows. Users from either tenant can see and update the row of the other tenant. You can solve this issue with row-level table security policies.

Each policy consists of two clauses: `USING` and `WITH CHECK`. When a user tries to read or write rows, the database evaluates each row against these clauses. Existing table rows are checked against the expression specified in `USING`, while new rows that would be created via `INSERT` or `UPDATE` are checked against the expression specified in `WITH CHECK`.

```sql
-- first a policy for the system admin "citus" user
CREATE POLICY admin_all ON events
  TO citus           -- apply to this role
  USING (true)       -- read any existing row
  WITH CHECK (true); -- insert or update any row

-- next a policy which allows role "tenant_<n>" to
-- access rows where tenant_id = <n>
CREATE POLICY user_mod ON events
  USING (current_user = 'tenant_' || tenant_id::text);
  -- lack of CHECK means same condition as USING

-- enforce the policies
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
```

Now roles `tenant_1` and `tenant_2` get different results for their queries:

**Connected as tenant_1:**

``` sql
SELECT * FROM events;
```

```output
┌───────────┬────┬──────┐
│ tenant_id │ id │ type │
├───────────┼────┼──────┤
│         1 │ 1  │ foo  │
└───────────┴────┴──────┘
```

**Connected as tenant_2:**

``` sql
SELECT * FROM events;
```

```output
┌───────────┬────┬──────┐
│ tenant_id │ id │ type │
├───────────┼────┼──────┤
│         2 │ 2  │ bar  │
└───────────┴────┴──────┘
```

```sql
-- connected as tenant_1INSERT INTO events VALUES (3,3,'surprise');
/*
ERROR: new row violates row-level security policy for table "events_102055"
*/
```

## PostgreSQL extensions

Citus provides distributed functionality by extending PostgreSQL through the hook and extension APIs. This approach lets you benefit from the features in the rich PostgreSQL ecosystem. These features include, but aren't limited to, support for a wide range of [data types](http://www.postgresql.org/docs/current/static/datatype.html) (including semi-structured data types like jsonb and hstore), [operators and functions](http://www.postgresql.org/docs/current/static/functions.html), full text search, and other extensions such as [PostGIS](http://postgis.net/) and [HyperLogLog](https://github.com/aggregateknowledge/postgresql-hll). Proper use of the extension APIs enables compatibility with standard PostgreSQL tools such as [pgAdmin](http://www.pgadmin.org/) and [pg_upgrade](http://www.postgresql.org/docs/current/static/pgupgrade.html).

Because Citus is an extension you can install on any PostgreSQL instance, you can directly use other extensions such as hstore, hll, or PostGIS with Citus. However, keep in mind that when you include other extensions in `shared_preload_libraries`, Citus must be the first extension.

> [!NOTE]  
> Sometimes, Citus doesn't support some features of an extension out of the box. For example, a few aggregates in an extension might need to be modified to be parallelized across multiple nodes. [Contact us](https://www.citusdata.com/about/contact_us) if some feature from your favorite extension doesn't work as expected with Citus.

In addition to our core Citus extension, we also maintain several others:

- [cstore_fdw](https://github.com/citusdata/cstore_fdw) - Columnar store for analytics. The columnar nature delivers performance by reading only relevant data from disk, and it might compress data by a factor of six to 10 times to reduce space requirements for data archival.
- [pg_cron](https://github.com/citusdata/pg_cron) - Run periodic jobs directly from the database.
- [postgresql-topn](https://github.com/citusdata/postgresql-topn) - Returns the top values in a database according to some criteria. Uses an approximation algorithm to provide fast results with modest compute and memory resources.
- [postgresql-hll](https://github.com/citusdata/postgresql-hll) - HyperLogLog data structure as a native data type. It's a fixed-size, set-like structure used for distinct value counting with tunable precision.

## Creating a new database

Each PostgreSQL server can hold [multiple databases](https://www.postgresql.org/docs/current/static/manage-ag-overview.html). However, new databases don't inherit the extensions of any other databases; you must add all desired extensions. To run Citus on a new database, you need to create the database on the coordinator and workers, create the Citus extension within that database, and register the workers in the coordinator database.

Connect to each of the worker nodes and run:

``` psql
-- on every worker node

CREATE DATABASE newbie;
\c newbie
CREATE EXTENSION citus;
```

Then, on the coordinator:

``` psql
CREATE DATABASE newbie;
\c newbie
CREATE EXTENSION citus;

SELECT * from citus_add_node('node-name', 5432);
SELECT * from citus_add_node('node-name2', 5432);
-- ... for all of them
```

Now the new database operates as another Citus cluster.

## Related content

- [Citus table management](table-management.md)
- [Upgrading Citus](upgrade-citus.md)
- [Diagnostic queries for Citus](diagnostic-queries.md)
- [What is Citus?](what-is-citus.md)
