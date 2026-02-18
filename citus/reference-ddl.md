---
title: "Create and Modify Distributed Objects (DDL)"
description: This article describes how to create and modify distributed objects using the data definition language (DDL) in Citus.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Create and modify distributed objects (DDL)

The following sections describe how to create and modify distributed objects by using the data definition language (DDL) in Citus.

## Creating and distributing schemas

Citus 12.0 introduced `schema_based_sharding` that allows a schema to be distributed. Distributed schemas automatically associate with individual colocation groups. When you create tables in these schemas, the tables automatically become colocated distributed tables without a shard key.

You can distribute a schema in Citus in two ways:

1. Call the `citus_schema_distribute` function manually:

   ```sql
   SELECT citus_schema_distribute('user_service');
   ```

   This method also allows you to convert existing regular schemas into distributed schemas.

   > [!NOTE]  
   > You can only distribute schemas that don't contain distributed and reference tables.

1. Enable the `enable_schema_based_sharding` configuration variable:

   ```sql
   SET citus.enable_schema_based_sharding TO ON;

   CREATE SCHEMA AUTHORIZATION user_service;
   ```

   Change the variable for the current session or permanently in `postgresql.conf`. When you set the parameter to `ON`, all created schemas are distributed by default.

The process of distributing the schema automatically assigns and moves it to an existing node in the cluster. The background shard rebalancer takes these schemas and all tables within them when rebalancing the cluster. It then performs the optimal moves and migrates the schemas between the nodes in the cluster.

To convert a schema back into a regular PostgreSQL schema, use the `citus_schema_undistribute` function:

```sql
SELECT citus_schema_undistribute('user_service');
```

The tables and data in the `user_service` schema move from the current node back to the coordinator node in the cluster.

## Creating and distributing tables

To create a distributed table, first define the table schema. Define a table by using the [CREATE TABLE](http://www.postgresql.org/docs/current/static/sql-createtable.html) statement, just as you would for a regular PostgreSQL table.

```sql
CREATE TABLE github_events
(
    event_id bigint,
    event_type text,
    event_public boolean,
    repo_id bigint,
    payload jsonb,
    repo jsonb,
    actor jsonb,
    org jsonb,
    created_at timestamp
);
```

Next, use the `create_distributed_table()` function to specify the table distribution column and create the worker shards.

```sql
SELECT create_distributed_table('github_events', 'repo_id');
```

This function informs Citus that the `github_events` table should be distributed on the `repo_id` column by hashing the column value. The function also creates shards on the worker nodes by using the `citus.shard_count` configuration value.

This example creates a total of `citus.shard_count` number of shards where each shard owns a portion of a hash token space. After you create the shards, the function saves all distributed metadata on the coordinator.

Each created shard gets a unique shard ID. Each shard appears on the worker node as a regular PostgreSQL table with the name `tablename_shardid`. The `tablename` is the name of the distributed table, and the `shardid` is the unique ID assigned to that shard. You can connect to the worker PostgreSQL instances to view or run commands on individual shards.

You're now ready to insert data into the distributed table and run queries on it. To learn more about the user-defined functions used in this section, see [Citus utility functions](api-udf.md).

### Reference tables

The previous section describes distributing tables into multiple horizontal shards. Another option is distributing tables into a single shard and replicating the shard to every worker node. Tables distributed this way are *reference tables*. Use reference tables to store data that multiple nodes in a cluster need to access frequently.

Common candidates for reference tables include:

- Smaller tables, which need to join with larger distributed tables.
- Tables in multitenant apps, which lack a tenant ID column or which aren't associated with a tenant. In some cases, to reduce migration effort, users might even choose to make reference tables out of tables associated with a tenant that currently lack a tenant ID.
- Tables that need unique constraints across multiple columns and are small enough.

For instance, suppose a multitenant e-commerce site needs to calculate sales tax for transactions in any of its stores. Tax information isn't specific to any tenant. It makes sense to consolidate it in a shared table. A US-centric reference table might look like this:

```sql
-- a reference table

CREATE TABLE states (
  code char(2) PRIMARY KEY,
  full_name text NOT NULL,
  general_sales_tax numeric(4,3)
);

-- distribute it to all workers

SELECT create_reference_table('states');
```

Now queries such as one calculating tax for a shopping cart can join on the `states` table with no network overhead, and can add a foreign key to the state code for better validation.

In addition to distributing a table as a single replicated shard, the user-defined function `create_reference_table` marks it as a reference table in the Citus metadata tables. Citus automatically performs two-phase commits ([2PC](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)) for modifications to tables marked this way, which provides strong consistency guarantees.

If you have an existing distributed table, you can change it to a reference table by running:

```sql
SELECT undistribute_table('table_name');
SELECT create_reference_table('table_name');
```

For another example of using reference tables in a multitenant application, see `mt_ref_tables`.

### Distributing coordinator data

If you convert an existing PostgreSQL database into the coordinator node for a Citus cluster, you can efficiently distribute the data in its tables with minimal interruption to an application.

The `create_distributed_table` function described earlier works on both empty and nonempty tables. For nonempty tables, it automatically distributes table rows throughout the cluster. You can tell if it's distributing data by the presence of the message, "NOTICE: Copying data from local table..." For example:

```sql
CREATE TABLE series AS SELECT i FROM generate_series(1,1000000) i;
SELECT create_distributed_table('series', 'i');
NOTICE:  Copying data from local table...
NOTICE:  copying the data has completed
DETAIL:  The local data in the table is no longer visible, but is still on disk.
HINT:  To remove the local data, run: SELECT truncate_local_data_after_distributing_table($$public.series$$)
 create_distributed_table
 --------------------------

 (1 row)
```

Writes on the table are blocked while the data is migrated. The function handles pending writes as distributed queries once it commits. If the function fails, the queries become local again. Reads can continue as normal and become distributed queries once the function commits.

When distributing tables A and B, where A has a foreign key to B, distribute the key destination table B first. Doing it in the wrong order causes an error:

```output
ERROR: cannot create foreign key constraint
DETAIL: Referenced table must be a distributed table or a reference table.
```

If you can't distribute in the correct order, drop the foreign keys, distribute the tables, and recreate the foreign keys.

After you distribute the tables, use the `truncate_local_data_after_distributing_table` function to remove local data. Leftover local data in distributed tables is inaccessible to Citus queries and can cause irrelevant constraint violations on the coordinator.

When migrating data from an external database, such as from Amazon RDS to our `cloud_topic`, first create the Citus distributed tables by using `create_distributed_table`. Then, copy the data into the table. Copying into distributed tables avoids running out of space on the coordinator node.

## Colocating tables

Colocation is the practice of dividing data tactically, keeping related information on the same machines to enable efficient relational operations, while taking advantage of the horizontal scalability for the whole dataset. For more information and examples, see [Colocation group table](api-metadata.md#colocation-group-table).

Citus automatically colocate tables in groups. To manually control a table's colocation group assignment, use the optional `colocate_with` parameter of `create_distributed_table`. If you don't care about a table's colocation, omit this parameter. It defaults to the value `'default'`, which groups the table with any other default colocation table that has the same distribution column type and shard count. If you want to break or update this implicit colocation, use `update_distributed_table_colocation()`.

```sql
-- these tables are implicitly co-located by using the same
-- distribution column type and shard count with the default
-- co-location group

SELECT create_distributed_table('A', 'some_int_col');
SELECT create_distributed_table('B', 'other_int_col');
```

When a new table isn't related to others in its would-be implicit colocation group, specify `colocated_with => 'none'`.

```sql
-- not co-located with other tables

SELECT create_distributed_table('A', 'foo', colocate_with => 'none');
```

Splitting unrelated tables into their own colocation groups improves shard rebalancing performance, because shards in the same group move together.

When tables are related (for instance when they're joined), explicitly colocate them. The gains of appropriate colocation are more important than any rebalancing overhead.

To explicitly colocate multiple tables, distribute one table and then put the others into its colocation group. For example:

```sql
-- distribute stores
SELECT create_distributed_table('stores', 'store_id');

-- add to the same group as stores
SELECT create_distributed_table('orders', 'store_id', colocate_with => 'stores');
SELECT create_distributed_table('products', 'store_id', colocate_with => 'stores');
```

Information about colocation groups is stored in the `pg_dist_colocation` table, while `pg_dist_partition` reveals which tables are assigned to which groups.

## Dropping tables

Use the standard PostgreSQL DROP TABLE command to remove your distributed tables. As with regular tables, DROP TABLE removes any indexes, rules, triggers, and constraints that exist for the target table. In addition, it also drops the shards on the worker nodes and cleans up their metadata.

```sql
DROP TABLE github_events;
```

## Modifying tables

Citus automatically propagates many kinds of DDL statements. Modifying a distributed table on the coordinator node updates shards on the workers too. Other DDL statements require manual propagation, and certain others are prohibited such as those statements that would modify a distribution column. Attempting to run DDL that's ineligible for automatic propagation raises an error and leaves tables on the coordinator node unchanged.

Here's a reference of the categories of DDL statements, which propagate. You can enable or disable automatic propagation by using a configuration parameter.

### Adding or modifying columns

Citus automatically propagates most [ALTER TABLE](https://www.postgresql.org/docs/current/static/ddl-alter.html) commands. Adding columns or changing their default values works the same way as in a single-machine PostgreSQL database:

```sql
-- Adding a column

ALTER TABLE products ADD COLUMN description text;

-- Changing default value

ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

You can also make significant changes to an existing column, like renaming it or changing its data type. However, you can't alter the data type of the distribution column. This column determines how Citus distributes table data through the cluster, and modifying its data type would require moving the data.

If you attempt to alter the data type of the distribution column, you get an error:

```sql
-- assuming store_id is the distribution column
-- for products, and that it has type integer

ALTER TABLE products
ALTER COLUMN store_id TYPE text;

/*
ERROR:  cannot execute ALTER TABLE command involving partition column
*/
```

As a workaround, consider changing the distribution column `<alter_distributed_table>`, updating it, and changing it back.

### Adding or removing constraints

By using Citus, you can continue to enjoy the safety of a relational database, including database constraints. For more information, see the PostgreSQL [docs](https://www.postgresql.org/docs/current/static/ddl-constraints.html). Due to the nature of distributed systems, Citus doesn't cross-reference uniqueness constraints or referential integrity between worker nodes.

To set up a foreign key between colocated distributed tables, always include the distribution column in the key. This structure might involve making the key compound.

You can create foreign keys in these situations:

- between two local (nondistributed) tables,
- between two reference tables,
- between reference tables and local tables (by default enabled, via `enable_local_ref_fkeys`),
- between two colocated distributed tables when the key includes the distribution column, or
- as a distributed table referencing a reference table.

Foreign keys from reference tables to distributed tables aren't supported.

Citus supports all [referential actions](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK) on foreign keys from local to reference tables, but it doesn't support `ON DELETE/UPDATE CASCADE` in the reverse direction (reference to local).

> [!NOTE]  
> Primary keys and uniqueness constraints must include the distribution column. Adding them to a nondistribution column generates an error.

The following example shows how to create primary and foreign keys on distributed tables:

```sql
--
-- Adding a primary key
-- --------------------

-- We'll distribute these tables on the account_id. The ads and clicks
-- tables must use compound keys that include account_id.

ALTER TABLE accounts ADD PRIMARY KEY (id);
ALTER TABLE ads ADD PRIMARY KEY (account_id, id);
ALTER TABLE clicks ADD PRIMARY KEY (account_id, id);

-- Next distribute the tables

SELECT create_distributed_table('accounts', 'id');
SELECT create_distributed_table('ads',      'account_id');
SELECT create_distributed_table('clicks',   'account_id');

--
-- Adding foreign keys
-- -------------------

-- Note that this can happen before or after distribution, as long as
-- there exists a uniqueness constraint on the target column(s) which
-- can only be enforced before distribution.

ALTER TABLE ads ADD CONSTRAINT ads_account_fk
  FOREIGN KEY (account_id) REFERENCES accounts (id);
ALTER TABLE clicks ADD CONSTRAINT clicks_ad_fk
  FOREIGN KEY (account_id, ad_id) REFERENCES ads (account_id, id);
```

Similarly, include the distribution column in uniqueness constraints:

```sql
-- Suppose we want every ad to use a unique image. Notice we can
-- enforce it only per account when we distribute by account id.

ALTER TABLE ads ADD CONSTRAINT ads_unique_image
  UNIQUE (account_id, image_url);
```

You can apply not-null constraints to any column (distribution or not) because they require no lookups between workers.

```sql
ALTER TABLE ads ALTER COLUMN image_url SET NOT NULL;
```

### Using NOT VALID constraints

In some situations, it can be useful to enforce constraints for new rows while allowing existing nonconforming rows to remain unchanged. Citus supports this feature for CHECK constraints and foreign keys by using PostgreSQL's "NOT VALID" constraint designation.

For example, consider an application that stores user profiles in a reference table.

```sql
-- we're using the "text" column type here, but a real application
-- might use "citext" which is available in a PostgreSQL contrib module

CREATE TABLE users ( email text PRIMARY KEY );
SELECT create_reference_table('users');
```

Over time, some nonaddresses could get into the table.

```sql
INSERT INTO users VALUES
   ('foo@example.com'), ('hacker12@aol.com'), ('lol');
```

You want to validate the addresses, but PostgreSQL doesn't ordinarily allow you to add a CHECK constraint that fails for existing rows. However, it *does* allow a constraint marked not valid:

```sql
ALTER TABLE users
ADD CONSTRAINT syntactic_email
CHECK (email ~
   '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
) NOT VALID;
```

This strategy succeeds, and new rows are protected.

```sql
INSERT INTO users VALUES ('fake');

/*
ERROR:  new row for relation "users_102010" violates
        check constraint "syntactic_email_102010"
DETAIL:  Failing row contains (fake).
*/
```

Later, during nonpeak hours, a database administrator can attempt to fix the bad rows and revalidate the constraint.

```sql
-- later, attempt to validate all rows
ALTER TABLE users
VALIDATE CONSTRAINT syntactic_email;
```

The PostgreSQL documentation has more information about NOT VALID and VALIDATE CONSTRAINT in the [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) section.

### Adding and removing indices

Citus supports adding and removing [indices](https://www.postgresql.org/docs/current/static/sql-createindex.html):

```sql
-- Adding an index

CREATE INDEX clicked_at_idx ON clicks USING BRIN (clicked_at);

-- Removing an index

DROP INDEX clicked_at_idx;
```

Adding an index takes a write lock, which can be undesirable in a multitenant system of record. To minimize application downtime, create the index [concurrently](https://www.postgresql.org/docs/current/static/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY) instead. This method requires more total work than a standard index build and takes longer to complete. However, since it allows normal operations to continue while the index is built, this method is useful for adding new indexes in a production environment.

```sql
-- Adding an index without locking table writes

CREATE INDEX CONCURRENTLY clicked_at_idx ON clicks USING BRIN (clicked_at);
```

## Types and functions

When you create custom SQL types and user-defined functions, Citus automatically propagates them to worker nodes. However, creating these database objects in a transaction that includes distributed operations involves tradeoffs.

Citus parallelizes operations such as `create_distributed_table()` across shards by using multiple connections per worker. However, when you create a database object, Citus uses a single connection per worker to propagate the object to worker nodes. Combining these two operations in a single transaction might cause problems, because the parallel connections can't see an object created over a single connection but not yet committed.

Consider a transaction block that creates a type, a table, loads data, and distributes the table:

```sql
BEGIN;

-- type creation over a single connection:
CREATE TYPE coordinates AS (x int, y int);
CREATE TABLE positions (object_id text primary key, position coordinates);

-- data loading thus goes over a single connection:
SELECT create_distributed_table('positions', 'object_id');
\COPY positions FROM 'positions.csv'

COMMIT;
```

Before Citus 11.0, Citus deferred creating the type on the worker nodes, and committed it separately when creating the distributed table. This sequence of operations enabled the data copying in `create_distributed_table()` to happen in parallel. However, it also meant that the type wasn't always present on the Citus worker nodes. Or, if the transaction rolled back, the type remained on the worker nodes.

With Citus 11.0, the default behavior prioritizes schema consistency between coordinator and worker nodes. This behavior has a downside: if object propagation happens after a parallel command in the same transaction, the transaction can't be completed, as the ERROR in the following code block highlights:

```sql
BEGIN;
CREATE TABLE items (key text, value text);
-- parallel data loading:
SELECT create_distributed_table('items', 'key');
\COPY items FROM 'items.csv'
CREATE TYPE coordinates AS (x int, y int);

ERROR: cannot run type command because there was a parallel operation on a distributed table in the transaction
```

If you run into this problem, try one of these two workarounds:

1. Set `citus.create_object_propagation` to `deferred` to return to the old object propagation behavior. This option might cause some inconsistency between which database objects exist on different nodes.
1. Set `citus.multi_shard_modify_mode` to `sequential` to disable per-node parallelism. Data load in the same transaction might be slower.

### Database and role management DDL (Citus 13.1)

Citus 13.1 expands auto-propagation to ease role and database management. The coordinator now auto-propagates:

- `ALTER DATABASE .. SET ..`
- `ALTER USER RENAME`
- `COMMENT ON DATABASE` / `COMMENT ON ROLE`
- `CREATE DATABASE` / `DROP DATABASE`
- `GRANT/REVOKE` rights on table columns
- `REASSIGN OWNED BY`
- `SECURITY LABEL` on tables and columns

Additionally, Citus propagates some role and database management commands issued **from any node**:

- `CREATE DATABASE` / `DROP DATABASE`
- `SECURITY LABEL ON ROLE`
- General role management commands

See [citus.enable_ddl_propagation](api-guc.md#citusenable_ddl_propagation-boolean).

## Manual modification

Most DDL commands are autopropagated. For any others, you can propagate the changes manually, see [Manual query propagation](reference-propagation.md).

## Related content

- [Data modifying language (DML) operations reference](reference-dml.md)
- [SQL reference](reference-sql.md)
- [Citus SQL reference overview](reference.md)
