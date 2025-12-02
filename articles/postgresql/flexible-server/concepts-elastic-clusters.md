---
title: Elastic Clusters
description: Learn about sharding and horizontal scale-out with elastic clusters on your Azure Database for PostgreSQL flexible server instance.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Elastic clusters in Azure Database for PostgreSQL

Elastic clusters on the Azure Database for PostgreSQL service are a managed offering of the open-source [Citus](https://www.citusdata.com/) extension to PostgreSQL that enables horizontal sharding of PostgreSQL.

While Citus is just an extension, it connects multiple PostgreSQL instances. When an Azure Database for PostgreSQL flexible server instance is deployed with Citus, it handles the management and configuration of multiple PostgreSQL instances as a single resource. It also automatically sets up the nodes and makes them known to the Citus extension.

Elastic clusters on the service offer two sharding models: row-based sharding and schema-based sharding. Check the open-source documentation about [sharding models](https://docs.citusdata.com/en/v12.1/get_started/concepts.html?highlight=shard#sharding-models), if you want to learn more.

## Architecture

An elastic cluster consists of one or more nodes of Azure Database for PostgreSQL flexible server instances. These instances are automatically made known to each other, and inter-connected to form a Citus cluster. The nodes are required to be of the same compute and storage tier, and can be uniformly scaled up or down to higher or lower tiers.

Elastic clusters use instances of flexible servers (called nodes) to coordinate with one another in a "shared nothing" architecture. The architecture also allows the database to scale, by adding more nodes to the cluster.

Connecting to your cluster using port 5432 lands you on the designated coordinator node. Elastic clusters also allow you to load balance connections across the cluster, using a five-tuple hash method, if you connect using port 7432. Using 7432 you can still land at the node currently designated as coordinator. For certain cluster-wide operations, like distributing tables, you might be required to connect over port 5432. We strongly recommend you to always connect on port 5432, when you plan to perform application schema upgrades and similar changes. If you [enable PgBouncer](concepts-pgbouncer.md) on elastic clusters, you can use port 8432 to load balance connections across PgBouncer instances on every node (or use port 6432 for the designated coordinator).

Unlike Cosmos DB for PostgreSQL, node addresses aren't externally exposed. If you look at Citus metadata tables like `pg_dist_node`, then you might notice all nodes having the same IP address as in the example `10.7.0.254` but different port numbers.

```sql
select nodeid, nodename, nodeport from pg_dist_node;
```

```output
 nodeid |  nodename  | nodeport
--------+------------+----------
      1 | 10.7.0.254 |     7000
      2 | 10.7.0.254 |     7001
 
(2 rows)
```

In Azure's infrastructure, these nodes live on different virtual machines even though they might seem to be different ports on the same machine.

To learn more about Citus, you can refer to the official open-source [project documentation](https://docs.citusdata.com/).

By default, tables and schemas created with Citus aren't automatically distributed among the cluster. You need to decide on a sharding model, and either decide to distribute schemas or decide to distribute your table data with row based sharding.

For each query on distributed tables, the queried node either routes it to a single node or parallelizes it across several nodes. The decision depends on whether the required data lives on a single node or on multiple. With [schema-based sharding](concepts-elastic-clusters-sharding-models.md#schema-based-sharding), the coordinator routes the queries directly to the node that hosts the schema. In both, schema-based sharding and [row-based sharding](concepts-elastic-clusters-sharding-models.md#row-based-sharding), the node decides what to do by consulting metadata tables. These tables track the location and health of nodes, and the distribution of data across nodes.

Once data is distributed using one of the sharding models, you can connect to any of the nodes to perform DML (Data Modification Language) operations (SELECT, UPDATE, INSERT, DELETE). All nodes contain the metadata required to locate data needed for the query and are able to obtain it to answer the query.

DDL (Data Definition Language) operations and cluster wide operations are currently limited to the node holding the coordinator role. Make sure you perform DDL and cluster-wide operations by connecting to port 5432, instead of using port 7432.

You can scale out an elastic cluster by adding new nodes and rebalancing the data on it. Rebalancing is an online operation and doesn't block running workloads.

## Shards

The previous section described how distributed tables are stored as shards on worker nodes. This section discusses more technical details about these shards.

The `pg_dist_shard` metadata table contains a row for each shard of each distributed table in the system. The row matches a shard identifier (`shardid`) with a range of integers in a hash space (`shardminvalue`, `shardmaxvalue`).

```sql
SELECT * from pg_dist_shard;
```

```output
logicalrelid  | shardid | shardstorage | shardminvalue | shardmaxvalue
---------------+---------+--------------+---------------+---------------
 github_events |  102026 | t            | 268435456     | 402653183
 github_events |  102027 | t            | 402653184     | 536870911
 github_events |  102028 | t            | 536870912     | 671088639
 github_events |  102029 | t            | 671088640     | 805306367
 
 (4 rows)
```

If the node wants to determine which shard holds a row of `github_events`, it hashes the value of the distribution column in the row. Then the node checks, which shard's range contains the hashed value. The ranges are defined so that the image of the hash function is their disjoint union.

### Shard placements

Suppose that shard 102027 is associated with the row in question. The row is read or written in a table called `github_events_102027` in one of the workers. With the information stored in the metadata tables, the extension determines what's that specific worker. The mapping of shard to worker is known as the shard placement.

The node rewrites queries into fragments that refer to the specific tables like `github_events_102027` and runs those fragments on the appropriate workers. Here's an example of a query run behind the scenes to find the node holding shard with identifier 102027.

```sql
SELECT
    shardid,
    node.nodename,
    node.nodeport
FROM pg_dist_placement placement
JOIN pg_dist_node node
  ON placement.groupid = node.groupid
 AND node.noderole = 'primary'::noderole
WHERE shardid = 102027;
```

```output
┌─────────┬───────────┬──────────┐
│ shardid │ nodename  │ nodeport │
├─────────┼───────────┼──────────┤
│  102027 │ localhost │     5433 │
└─────────┴───────────┴──────────┘
```

## Related content

- [Sharding models on elastic clusters in Azure Database for PostgreSQL](concepts-elastic-clusters-sharding-models.md).
- [Table types on elastic clusters in Azure Database for PostgreSQL](concepts-elastic-clusters-table-types.md).
- [Frequently asked questions about elastic clusters of Azure Database for PostgreSQL limitations](concepts-elastic-clusters-limitations.md).
