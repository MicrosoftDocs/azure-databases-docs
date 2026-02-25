---
title: Choosing Distribution Column
description: Learn how to choose distribution columns in Citus so you can build fast, scalable distributed applications.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Choose a distribution column

Citus uses the distribution column in distributed tables to assign table rows to shards. Choosing the distribution column for each table is **one of the most important** modeling decisions because it determines how data spreads across nodes.

If you choose the distribution columns correctly, related data joins on the same physical nodes. This choice makes queries fast and adds support for all SQL features. If you choose the columns incorrectly, the system runs slowly and can't support all SQL features across nodes.

This section gives distribution column tips for the two most common Citus scenarios. It concludes by going in-depth on "colocation," the desirable grouping of data on nodes.

## Multitenant apps

The multitenant architecture uses a form of hierarchical database modeling to distribute queries across nodes in the distributed cluster. The top of the data hierarchy is known as the *tenant ID*, and you need to store it in a column on each table. Citus inspects queries to see which tenant ID they involve. Citus then routes the query to a single worker node for processing, specifically the node. The node holds the data shards associated with the tenant ID. Running a query with all relevant data placed on the same node is called `colocation`.

The following diagram illustrates colocation in the multitenant data model. It contains two tables, Accounts and Campaigns, each distributed by `account_id`. The shaded boxes represent shards, each of whose color represents which worker node contains it. Green shards are stored together on one worker node, and blue on another. Notice how a join query between Accounts and Campaigns would have all the necessary data together on one node when restricting both tables to the same account_id.

:::image type="content" source="./media/data-modeling/multi-tenant-colocation.png" alt-text="Diagram about Node differences.":::

To apply this design in your own schema, first identify what constitutes a tenant in your application. Common instances include company, account, organization, or customer. The column name is something like `company_id` or `customer_id`. Examine each of your queries and ask yourself: would it work if it had extra WHERE clauses to restrict all tables involved to rows with the same tenant ID? Queries in the multitenant model are scoped to a tenant, for instance queries on sales or inventory are scoped within a certain store.

### Best practices

- **Partition distributed tables by a common tenant_id column.** For instance, in a SaaS application where tenants are companies, the tenant_id is likely `company_id`.
- **Convert small cross-tenant tables to reference tables.** When multiple tenants share a small table of information, distribute it as a reference table.
- **Restrict filter all application queries by tenant_id.** Each query should request information for one tenant at a time.

Read the [Use cases](use-cases.md) guide for a detailed example of building this kind of application.

## Real-time apps

While the multitenant architecture introduces a hierarchical structure and uses data colocation to route queries per tenant, real-time architectures depend on specific distribution properties of their data to achieve highly parallel processing.

We use "entity ID" as a term for distribution columns in the real-time model, as opposed to tenant IDs in the multitenant model. Typical entities are users, hosts, or devices.

Real-time queries typically ask for numeric aggregates grouped by date or category. Citus sends these queries to each shard for partial results and assembles the final answer on the coordinator node. Queries run fastest when as many nodes contribute as possible, and when no single node must do a disproportionate amount of work.

### Best practices

- **Choose a column with high cardinality as the distribution column.** For comparison, a "status" field on an order table with values "new," "paid," and "shipped" is a poor choice of distribution column because it assumes only those three values. The number of distinct values limits the number of shards that can hold the data and the number of nodes that can process it. Among columns with high cardinality, choose values that are frequently used in group-by clauses or as join keys.
- **Choose a column with even distribution.** If you distribute a table on a column skewed to certain common values, then data in the table tends to accumulate in certain shards. The nodes holding those shards end up doing more work than other nodes.
- **Distribute fact and dimension tables on their common columns.** Your fact table can have only one distribution key. Tables that join on another key aren't colocated with the fact table. Choose one dimension to colocate based on how frequently it joins and the size of the joining rows.
- **Change some dimension tables into reference tables.** If a dimension table can't be colocated with the fact table, you can improve query performance by distributing copies of the dimension table to the nodes in the form of a reference table.

Read the [Use cases](use-cases.md) guide for a detailed example of building this kind of application.

## Time series data

In a time-series workload, applications query recent information while archiving old information.

The most common mistake in modeling time series information in Citus is by using the timestamp itself as a distribution column. A hash distribution based on time distributes times seemingly at random into different shards rather than keeping ranges of time together in shards. However, queries involving time generally reference ranges of time (for example the most recent data), so such a hash distribution leads to network overhead.

### Best practices

- **Don't choose a timestamp as the distribution column.** Choose a different distribution column. In a multitenant app, use the tenant ID, or in a real-time app use the entity ID.
- **Use PostgreSQL table partitioning for time instead.** Use table partitioning to break a large table of time-ordered data into multiple inherited tables with each containing different time ranges. Distributing a PostgreSQL-partitioned table in Citus creates shards for the inherited tables.

See [Time series data](tutorial-time-series.md) for a detailed example of building this kind of application.

## Table colocation

Relational databases are the first choice of data store for many applications due to their enormous flexibility and reliability. Historically, the one criticism of relational databases is that they can run on only a single machine, which creates inherent limitations when data storage needs outpace server improvements. The solution to rapidly scaling databases is to distribute them, but this solution creates a performance problem of its own: relational operations such as joins then need to cross the network boundary. Colocation is the practice of dividing data tactically. You keep related information on the same machines to enable efficient relational operations, but you take advantage of the horizontal scalability for the whole dataset.

The principle of data colocation is that all tables in the database have a common distribution column and are sharded across machines in the same way. The way they're shared is such that rows with the same distribution column value are always on the same machine, even across different tables. As long as the distribution column provides a meaningful grouping of data, relational operations can be performed within the groups.

### Data colocation in Citus for hash-distributed tables

The Citus extension for PostgreSQL is unique in being able to form a distributed database of databases. Every node in a Citus cluster is a fully functional PostgreSQL database, and Citus adds the experience of a single homogeneous database on top. While the Citus extension for PostgreSQL doesn't provide the full functionality of PostgreSQL in a distributed way, in many cases it can take full advantage of features offered by PostgreSQL on a single machine through colocation. These features include full SQL support, transactions, and foreign keys.

In Citus, a row is stored in a shard if the hash of the value in the distribution column falls within the shard's hash range. To ensure colocation, shards with the same hash range are always placed on the same node even after rebalance operations, such that equal distribution column values are always on the same node across tables.

:::image type="content" source="./media/data-modeling/colocation-shards.png" alt-text="Illustration of shard hash ranges.":::

A distribution column that works well in practice is tenant ID in multitenant applications. For example, SaaS applications typically have many tenants, but every query they make is specific to a particular tenant. While one option is providing a database or schema for every tenant, it's often costly and impractical. There can be many operations that span across users (data loading, migrations, aggregations, analytics, schema changes, backups, etc.). These operations become harder to manage as the number of tenants grows.

### A practical example of colocation

Consider the following tables, which might be part of a multitenant web analytics SaaS:

```sql
CREATE TABLE event (
  tenant_id int,
  event_id bigint,
  page_id int,
  payload jsonb,
  primary key (tenant_id, event_id)
);

CREATE TABLE page (
  tenant_id int,
  page_id int,
  path text,
  primary key (tenant_id, page_id)
);
```

Now you want to answer queries that a customer-facing dashboard might manage, such as: "Return the number of visits in the past week for all pages starting with '/blog' in tenant six."

### Use regular PostgreSQL tables

If your data is in a single PostgreSQL node, you can easily express your query by using the rich set of relational operations offered by SQL:

```sql
SELECT page_id, count(event_id)
FROM
  page
LEFT JOIN  (
  SELECT * FROM event
  WHERE (payload->>'time')::timestamptz >= now() - interval '1 week'
) recent
USING (tenant_id, page_id)
WHERE tenant_id = 6 AND path LIKE '/blog%'
GROUP BY page_id;
```

As long as the [working set](https://en.wikipedia.org/wiki/Working_set) for this query fits in memory, this solution is appropriate for many applications since it offers maximum flexibility. However, even if you don't need to scale yet, it can be useful to consider the implications of scaling out on your data model.

### Distribute tables by ID

As the number of tenants and the data stored for each tenant grows, query times typically increase because the working set no longer fits in memory or the CPU becomes a bottleneck. In this case, you can shard the data across many nodes by using Citus. The first and most important choice you need to make when sharding is the distribution column. Let's start with a naive choice of using `event_id` for the event table and `page_id` for the `page` table:

```sql
-- naively use event_id and page_id as distribution columns

SELECT create_distributed_table('event', 'event_id');
SELECT create_distributed_table('page', 'page_id');
```

Given that the data is dispersed across different workers, you can't perform a join as you would on a single PostgreSQL node. Instead, you need to issue two queries:

Across all shards of the page table (Q1):

```sql
SELECT page_id FROM page WHERE path LIKE '/blog%' AND tenant_id = 6;
```

Across all shards of the event table (Q2):

```sql
SELECT page_id, count(*) AS count
FROM event
WHERE page_id IN (/*...page IDs from first query...*/)
  AND tenant_id = 6
  AND (payload->>'time')::date >= now() - interval '1 week'
GROUP BY page_id ORDER BY count DESC LIMIT 10;
```

Afterwards, the application needs to combine the results from the two steps.

The data required to answer the query is scattered across the shards on the different nodes and you need to query each of those shards:

:::image type="content" source="./media/data-modeling/colocation-inefficient-queries.png" alt-text="Screenshot of queries 1 and 2 hitting multiple nodes.":::

In this case, the data distribution creates substantial drawbacks:

- Overhead from querying each shard and running multiple queries
- Overhead of Q1 returning many rows to the client
- Q2 becoming large
- The need to write queries in multiple steps, combine results, requires changes in the application

A potential upside of the relevant data being dispersed is that Citus can parallelize the queries. However, this benefit only applies if the amount of work that the query does is substantially greater than the overhead of querying many shards. It's better to avoid doing such heavy lifting directly from the application, for example by preaggregating the data.

### Distribute tables by tenant

Looking at our query again, we see that all the rows that the query needs share one dimension: `tenant_id`. The dashboard only queries for a tenant's own data. That tenant data is always colocated on a single PostgreSQL node, so that node can answer our original query in a single step by performing a join on `tenant_id` and `page_id`.

In Citus, rows with the same distribution column value are guaranteed to be on the same node. Each shard in a distributed table effectively has a set of colocated shards from other distributed tables that contain the same distribution column values (data for the same tenant). Starting over, we can create our tables with `tenant_id` as the distribution column.

```sql
-- co-locate tables by using a common distribution column
SELECT create_distributed_table('event', 'tenant_id');
SELECT create_distributed_table('page', 'tenant_id', colocate_with => 'event');
```

In this case, Citus can answer the same query that you run on a single PostgreSQL node without modification (Q1):

```sql
SELECT page_id, count(event_id)
FROM
  page
LEFT JOIN  (
  SELECT * FROM event
  WHERE (payload->>'time')::timestamptz >= now() - interval '1 week'
) recent
USING (tenant_id, page_id)
WHERE tenant_id = 6 AND path LIKE '/blog%'
GROUP BY page_id;
```

Because of the tenant ID filter and join on tenant ID, Citus knows the query can be answered by using the set of colocated shards that contain the data for that particular tenant. The PostgreSQL node can answer the query in a single step, which enables full SQL support.

:::image type="content" source="./media/data-modeling/colocation-better-query.png" alt-text="Screenshot of query one accessing just one node.":::

In some cases, queries and table schemas require minor modifications to ensure that the tenant_id is always included in unique constraints and join conditions. However, this change is straightforward and avoids the extensive rewrite that would be required without colocation.

While the preceding example queries just one node because of a specific tenant_id = 6 filter, colocation also allows us to efficiently perform distributed joins on tenant_id across all nodes, even with SQL limitations.

### Colocation means better feature support

The full list of Citus features that colocation unlocks includes:

- Full SQL support for queries on a single set of colocated shards
- Multi-statement transaction support for modifications on a single set of colocated shards
- Aggregation through `INSERT..SELECT`
- Foreign keys
- Distributed outer joins
- Pushdown CTEs (requires PostgreSQL \>=12)

Data colocation is a powerful technique for providing both horizontal scale and support to relational data models. The cost of migrating or building applications by using a distributed database that enables relational operations through colocation is often substantially lower than moving to a restrictive data model (for example, NoSQL). Unlike a single-node database, it can scale out with the size of your business. For more information about migrating an existing database, see [Migrate an existing application to Citus](migrate/migration.md).

### Query performance

Citus parallelizes incoming queries by breaking them into multiple fragment queries ("tasks") that run on the worker shards in parallel. This approach lets Citus utilize the processing power of all the nodes in the cluster and the individual cores on each node for each query. Due to this parallelization, you get performance that reflects the cumulative computing power of all the cores in the cluster, leading to a dramatic decrease in query times versus PostgreSQL.

Citus uses a two-stage optimizer when planning SQL queries. The first phase converts the SQL queries into their commutative and associative form so that it can push down and run the queries on the workers in parallel. As discussed in previous sections, choosing the right distribution column and distribution method allows the distributed query planner to apply several optimizations to the queries. This choice can affect query performance by reducing network I/O.

Citus's distributed executor takes query fragments and sends them to worker PostgreSQL instances. You can tune several aspects of both the distributed planner and the executor to improve performance. When the system sends these fragments to the workers, the second phase of query optimization kicks in. The workers are simply running extended PostgreSQL servers, and they apply PostgreSQL's standard planning and execution logic to run these fragment SQL queries. Therefore, any optimization that helps PostgreSQL also helps Citus. PostgreSQL comes with conservative resource settings by default. Optimizing these configuration settings can significantly improve query times.

[Performance tuning](performance-tuning.md) discusses the relevant performance tuning steps.

## Related content

- [Determining the application type](app-type.md)
- [What is Citus?](what-is-citus.md)
- [Multitenant applications tutorial](tutorial-multi-tenant.md)
